"""Generates 1-Click GCP Terraform Modules, Cloud Build configs, and Cloud Run deploy scripts."""

import json
import stat
from pathlib import Path
from typing import Any, Dict


def write_terraform_suite_for_post(post: Dict[str, Any], repo_dir: Path) -> Dict[str, Any]:
    """Write complete Terraform configuration, Dockerfile, cloudbuild.yaml, and 1-click deploy script."""
    tf_dir = repo_dir / "terraform"
    scripts_dir = repo_dir / "scripts"
    tf_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    service_name = post.get("repo_name", post["repo_slug"])[:48]
    slug = post["repo_slug"]

    versions_tf = """terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.40"
    }
  }
}
"""

    variables_tf = f"""variable "project_id" {{
  description = "Target Google Cloud Project ID for 1-Click Agentic Deployment"
  type        = string
  default     = "nitina-ggarwal-sandbox-647724"
}}

variable "region" {{
  description = "Primary Google Cloud region for Cloud Run and Artifact Registry"
  type        = string
  default     = "us-west1"
}}

variable "vertex_location" {{
  description = "Vertex AI endpoint location (Rule 55 mandates 'global' for Gemini 4 Argon & 3.8 Flash)"
  type        = string
  default     = "global"
}}

variable "service_name" {{
  description = "Cloud Run v2 service name"
  type        = string
  default     = "{service_name}"
}}

variable "container_image" {{
  description = "Container image URI deployed to Cloud Run"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}}
"""

    main_tf = f"""provider "google" {{
  project = var.project_id
  region  = var.region
}}

locals {{
  required_apis = [
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "firestore.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudtrace.googleapis.com",
  ]
  common_labels = {{
    managed_by      = "terraform"
    agent_harness   = "openhands-google-adk"
    post_id         = "{post['id'].lower()}"
    security_posture = "zero-hallucination"
  }}
}}

resource "google_project_service" "enabled_apis" {{
  for_each           = toset(local.required_apis)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}}

resource "google_service_account" "agent_runtime_sa" {{
  account_id   = substr(replace("{service_name}-sa", "_", "-"), 0, 28)
  display_name = "Least-Privilege ADK Runtime SA ({post['id']})"
  description  = "Service Account for {post['post_title'][:80]}"
  depends_on   = [google_project_service.enabled_apis]
}}

resource "google_project_iam_member" "vertex_ai_user" {{
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${{google_service_account.agent_runtime_sa.email}}"
}}

resource "google_project_iam_member" "datastore_user" {{
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${{google_service_account.agent_runtime_sa.email}}"
}}

resource "google_project_iam_member" "trace_agent" {{
  project = var.project_id
  role    = "roles/cloudtrace.agent"
  member  = "serviceAccount:${{google_service_account.agent_runtime_sa.email}}"
}}

resource "google_artifact_registry_repository" "agent_repo" {{
  location      = var.region
  repository_id = "{service_name}-repo"
  description   = "Container repository for {slug}"
  format        = "DOCKER"
  labels        = local.common_labels
  depends_on    = [google_project_service.enabled_apis]
}}

resource "google_cloud_run_v2_service" "agent_service" {{
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"
  labels   = local.common_labels

  template {{
    service_account = google_service_account.agent_runtime_sa.email
    scaling {{
      min_instance_count = 0
      max_instance_count = 5
    }}
    containers {{
      image = var.container_image
      ports {{
        container_port = 8080
      }}
      env {{
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }}
      env {{
        name  = "VERTEX_AI_LOCATION"
        value = var.vertex_location
      }}
      env {{
        name  = "FRONTIER_MODEL"
        value = "gemini-4-argon"
      }}
      env {{
        name  = "FLASH_MODEL"
        value = "gemini-3.8-flash"
      }}
      env {{
        name  = "THINKING_LEVEL"
        value = "HIGH"
      }}
      env {{
        name  = "MAX_OUTPUT_TOKENS"
        value = "32768"
      }}
      env {{
        name  = "SOURCE_ACTIVITY_URN"
        value = "{post['activity_urn']}"
      }}
    }}
  }}

  depends_on = [
    google_project_service.enabled_apis,
    google_project_iam_member.vertex_ai_user,
  ]
}}
"""

    outputs_tf = """output "cloud_run_service_url" {
  description = "Deployed Cloud Run v2 Agent Endpoint URI"
  value       = google_cloud_run_v2_service.agent_service.uri
}

output "service_account_email" {
  description = "Least-privilege Agent Runtime Service Account"
  value       = google_service_account.agent_runtime_sa.email
}

output "artifact_registry_repo" {
  description = "Artifact Registry Docker Repository ID"
  value       = google_artifact_registry_repository.agent_repo.name
}
"""

    tfvars_example = f"""project_id      = "nitina-ggarwal-sandbox-647724"
region          = "us-west1"
vertex_location = "global"
service_name    = "{service_name}"
"""

    (tf_dir / "versions.tf").write_text(versions_tf, encoding="utf-8")
    (tf_dir / "variables.tf").write_text(variables_tf, encoding="utf-8")
    (tf_dir / "main.tf").write_text(main_tf, encoding="utf-8")
    (tf_dir / "outputs.tf").write_text(outputs_tf, encoding="utf-8")
    (tf_dir / "terraform.tfvars.example").write_text(tfvars_example, encoding="utf-8")

    # Dockerfile & cloudbuild.yaml & app_cloudshell.json
    dockerfile = """FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PORT=8080
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 -m unittest discover -s tests -p "test_*.py"
EXPOSE 8080
CMD ["python3", "app.py"]
"""
    (repo_dir / "Dockerfile").write_text(dockerfile, encoding="utf-8")

    cloudbuild_yaml = f"""steps:
  - name: 'python:3.11-slim'
    entrypoint: 'python3'
    args: ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-west1-docker.pkg.dev/$PROJECT_ID/{service_name}-repo/{service_name}:latest', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-west1-docker.pkg.dev/$PROJECT_ID/{service_name}-repo/{service_name}:latest']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - '{service_name}'
      - '--image=us-west1-docker.pkg.dev/$PROJECT_ID/{service_name}-repo/{service_name}:latest'
      - '--region=us-west1'
      - '--platform=managed'
      - '--set-env-vars=VERTEX_AI_LOCATION=global,FRONTIER_MODEL=gemini-4-argon,FLASH_MODEL=gemini-3.8-flash,THINKING_LEVEL=HIGH'
options:
  logging: CLOUD_LOGGING_ONLY
"""
    (repo_dir / "cloudbuild.yaml").write_text(cloudbuild_yaml, encoding="utf-8")

    deploy_sh = f"""#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${{1:-nitina-ggarwal-sandbox-647724}}"
REGION="${{2:-us-west1}}"

echo "==> [1/3] Running OpenHands Sandbox Unit Tests for {slug}..."
python3 -m unittest discover -s tests -p "test_*.py"

echo "==> [2/3] Initializing & Validating GCP Terraform in ./terraform..."
cd terraform
terraform init -input=false
terraform validate

echo "==> [3/3] Applying 1-Click GCP Infrastructure to project=${{PROJECT_ID}} region=${{REGION}}..."
terraform apply -auto-approve \\
  -var="project_id=${{PROJECT_ID}}" \\
  -var="region=${{REGION}}" \\
  -var="vertex_location=global"
"""
    deploy_script_path = scripts_dir / "deploy_gcp_one_click.sh"
    deploy_script_path.write_text(deploy_sh, encoding="utf-8")
    deploy_script_path.chmod(deploy_script_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    cloudshell_json = {
        "name": service_name,
        "env": {
            "VERTEX_AI_LOCATION": {"description": "Vertex AI Global Endpoint", "value": "global"},
            "FRONTIER_MODEL": {"description": "Primary Frontier Reasoning Model", "value": "gemini-4-argon"},
            "FLASH_MODEL": {"description": "High-Throughput Agent Loop Model", "value": "gemini-3.8-flash"},
            "THINKING_LEVEL": {"description": "Discrete Thinking Level (HIGH|MEDIUM|LOW)", "value": "HIGH"},
        },
        "options": {"allow-unauthenticated": False, "memory": "1Gi", "cpu": "1"},
    }
    (repo_dir / "app_cloudshell.json").write_text(json.dumps(cloudshell_json, indent=2), encoding="utf-8")

    return {
        "terraform_files": [
            str(tf_dir / "versions.tf"),
            str(tf_dir / "variables.tf"),
            str(tf_dir / "main.tf"),
            str(tf_dir / "outputs.tf"),
            str(tf_dir / "terraform.tfvars.example"),
        ],
        "deploy_script": str(deploy_script_path),
    }
