output "cloud_run_service_url" {
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
