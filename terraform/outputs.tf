output "wif_provider" {
  description = "Full WIF provider resource name – use as GCP_WIF_PROVIDER secret."
  value       = google_iam_workload_identity_pool_provider.github_oidc.name
}

output "deployer_sa_email" {
  description = "Deployer service account email – use as GCP_DEPLOYER_SA secret."
  value       = google_service_account.deployer.email
}

output "artifact_registry_url" {
  description = "Base URL for the Docker repository in Artifact Registry."
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo}"
}
