provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  required_apis = [
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "firestore.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudtrace.googleapis.com",
  ]
  common_labels = {
    managed_by      = "terraform"
    agent_harness   = "openhands-google-adk"
    post_id         = "mint-01"
    security_posture = "zero-hallucination"
  }
}

resource "google_project_service" "enabled_apis" {
  for_each           = toset(local.required_apis)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_service_account" "agent_runtime_sa" {
  account_id   = substr(replace("gcp-mcp-zero-bloat-gateway-sa", "_", "-"), 0, 28)
  display_name = "Least-Privilege ADK Runtime SA (MINT-01)"
  description  = "Service Account for Zero-Bloat MCP Gateway: Dynamic Top-K Tool Search + RFC 8693 OAuth 2.1 On-Behalf"
  depends_on   = [google_project_service.enabled_apis]
}

resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_project_iam_member" "datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_project_iam_member" "trace_agent" {
  project = var.project_id
  role    = "roles/cloudtrace.agent"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_artifact_registry_repository" "agent_repo" {
  location      = var.region
  repository_id = "gcp-mcp-zero-bloat-gateway-repo"
  description   = "Container repository for gcp-mcp-zero-bloat-gateway"
  format        = "DOCKER"
  labels        = local.common_labels
  depends_on    = [google_project_service.enabled_apis]
}

resource "google_cloud_run_v2_service" "agent_service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"
  labels   = local.common_labels

  template {
    service_account = google_service_account.agent_runtime_sa.email
    scaling {
      min_instance_count = 0
      max_instance_count = 5
    }
    containers {
      image = var.container_image
      ports {
        container_port = 8080
      }
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "VERTEX_AI_LOCATION"
        value = var.vertex_location
      }
      env {
        name  = "FRONTIER_MODEL"
        value = "gemini-4-argon"
      }
      env {
        name  = "FLASH_MODEL"
        value = "gemini-3.8-flash"
      }
      env {
        name  = "THINKING_LEVEL"
        value = "HIGH"
      }
      env {
        name  = "MAX_OUTPUT_TOKENS"
        value = "32768"
      }
      env {
        name  = "SOURCE_ACTIVITY_URN"
        value = "urn:ietf:rfc:8693:mcp-zero-bloat-gateway-2026"
      }
    }
  }

  depends_on = [
    google_project_service.enabled_apis,
    google_project_iam_member.vertex_ai_user,
  ]
}
