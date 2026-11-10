#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${1:-ramp-portal-dev}"
REGION="${2:-us-west1}"

echo "==> [1/3] Running OpenHands Sandbox Unit Tests for gcp-mcp-zero-bloat-gateway..."
python3 -m unittest discover -s tests -p "test_*.py"

echo "==> [2/3] Initializing & Validating GCP Terraform in ./terraform..."
cd terraform
terraform init -input=false
terraform validate

echo "==> [3/3] Applying 1-Click GCP Infrastructure to project=${PROJECT_ID} region=${REGION}..."
terraform apply -auto-approve \
  -var="project_id=${PROJECT_ID}" \
  -var="region=${REGION}" \
  -var="vertex_location=global"
