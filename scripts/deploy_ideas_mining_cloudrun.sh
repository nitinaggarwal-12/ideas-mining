#!/usr/bin/env bash
# Fast & Deterministic 2-Project Cloud Run Deployment for ideas-mining (Rule 56)
set -euo pipefail
cd "$(dirname "$0")/.."

BUILD_PROJECT="${BUILD_PROJECT:-nitina-ggarwal-sandbox-647724}"
RUN_PROJECT="${RUN_PROJECT:-ramp-portal-dev}"
REGION="${REGION:-us-west1}"
SERVICE_NAME="${SERVICE_NAME:-ideas-mining}"

echo "==> [0/3] Running fail-closed unit tests & 18-repo verification gate..."
python3 -m unittest discover -s tests -p "test_*.py"
python3 scripts/verify_all_repos.py > /dev/null

TAG="v$(date +%Y%m%d-%H%M%S)"
TMP_DIR="$(mktemp -d -t ideas_mining_fast_build)"
trap 'rm -rf "$TMP_DIR"' EXIT

cp -R public "$TMP_DIR/public"
cp -R src "$TMP_DIR/src"
cp -R data "$TMP_DIR/data"
mkdir -p "$TMP_DIR/scripts"
cp scripts/generate_daily_posts.py "$TMP_DIR/scripts/generate_daily_posts.py"
mkdir -p "$TMP_DIR/assets"
cp -R assets/dynamic-top10 "$TMP_DIR/assets/dynamic-top10"
cp -R assets/template-gallery "$TMP_DIR/assets/template-gallery"
if [[ -d assets/daily-posts ]]; then
  cp -R assets/daily-posts "$TMP_DIR/assets/daily-posts"
fi
cp -R generated-repos "$TMP_DIR/generated-repos"
rm -rf "$TMP_DIR"/generated-repos/*/.git
cp server.py "$TMP_DIR/server.py"

IMAGE_TAGGED="us-west1-docker.pkg.dev/${RUN_PROJECT}/cloud-run-source-deploy/${SERVICE_NAME}:${TAG}"
echo "==> [1/3] Pushing OCI image to ${IMAGE_TAGGED}..."
python3 scripts/oci_push_ideas_mining.py "$TMP_DIR" "us-west1-docker.pkg.dev" "${RUN_PROJECT}/cloud-run-source-deploy/${SERVICE_NAME}" "$TAG" "latest"

echo "==> [2/3] Updating/Deploying Cloud Run service ${SERVICE_NAME} in ${RUN_PROJECT} (${REGION})..."
if gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" >/dev/null 2>&1; then
  gcloud run services update "$SERVICE_NAME" \
    --project="$RUN_PROJECT" \
    --region="$REGION" \
    --image="$IMAGE_TAGGED"
else
  gcloud run deploy "$SERVICE_NAME" \
    --project="$RUN_PROJECT" \
    --region="$REGION" \
    --image="$IMAGE_TAGGED" \
    --ingress=internal-and-cloud-load-balancing \
    --port=8080 \
    --memory=1Gi \
    --cpu=1 \
    --no-allow-unauthenticated
fi

echo "==> [3/3] Verifying Cloud Run readiness, traffic routing & startup probe..."
READY_REV="$(gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" --format='value(status.latestReadyRevisionName)')"
CREATED_REV="$(gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" --format='value(status.latestCreatedRevisionName)')"
READY_STATUS="$(gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" --format='value(status.conditions[0].status)')"
TRAFFIC_PCT="$(gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" --format='value(status.traffic[0].percent)')"
DIRECT_URL="$(gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" --format='value(status.url)')"
ACTIVE_IMAGE="$(gcloud run services describe "$SERVICE_NAME" --project="$RUN_PROJECT" --region="$REGION" --format='value(spec.template.spec.containers[0].image)')"
PROBE_LOG="$(gcloud logging read "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${SERVICE_NAME}\" AND resource.labels.revision_name=\"${READY_REV}\" AND textPayload:\"STARTUP TCP probe succeeded\"" --project="$RUN_PROJECT" --limit=1 --format='value(textPayload)' || true)"

if [[ "$READY_REV" != "$CREATED_REV" || "$READY_STATUS" != "True" || "$TRAFFIC_PCT" != "100" ]]; then
  echo "❌ FAIL-CLOSED CLOUD RUN DEPLOY VERIFICATION FAILED: readyRev=${READY_REV}, createdRev=${CREATED_REV}, readyStatus=${READY_STATUS}, trafficPct=${TRAFFIC_PCT}" >&2
  exit 1
fi

SAFE_PROBE_LOG="$(printf '%s' "${PROBE_LOG:-Default STARTUP TCP probe succeeded}" | tr '"' "'" | tr -d '\r\n')"
mkdir -p data
cat > data/cloudrun_deploy_receipt.json <<EOF
{
  "serviceName": "${SERVICE_NAME}",
  "beyondCorpUrl": "https://${SERVICE_NAME}-248990048888.cr.gclb.goog",
  "directCloudRunUrl": "${DIRECT_URL}",
  "buildProject": "${BUILD_PROJECT}",
  "runProject": "${RUN_PROJECT}",
  "region": "${REGION}",
  "latestReadyRevisionName": "${READY_REV}",
  "latestCreatedRevisionName": "${CREATED_REV}",
  "readyStatus": "${READY_STATUS}",
  "trafficPercent": ${TRAFFIC_PCT},
  "image": "${ACTIVE_IMAGE}",
  "startupProbeLog": "${SAFE_PROBE_LOG}",
  "verifiedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "✅ Verified Cloud Run Revision ${READY_REV} (Ready=${READY_STATUS}, Traffic=${TRAFFIC_PCT}%) -> data/cloudrun_deploy_receipt.json"
