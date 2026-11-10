variable "project_id" {
  description = "Target Google Cloud Project ID for 1-Click Agentic Deployment"
  type        = string
  default     = "ramp-portal-dev"
}

variable "region" {
  description = "Primary Google Cloud region for Cloud Run and Artifact Registry"
  type        = string
  default     = "us-west1"
}

variable "vertex_location" {
  description = "Vertex AI endpoint location (Rule 55 mandates 'global' for Gemini 4 Argon & 3.8 Flash)"
  type        = string
  default     = "global"
}

variable "service_name" {
  description = "Cloud Run v2 service name"
  type        = string
  default     = "gcp-mcp-zero-bloat-gateway"
}

variable "container_image" {
  description = "Container image URI deployed to Cloud Run"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}
