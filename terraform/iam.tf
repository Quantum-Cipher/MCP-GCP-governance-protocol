# ---------------------------------------------------------------------------
# Deployer service account
# ---------------------------------------------------------------------------

resource "google_service_account" "deployer" {
  account_id   = var.deployer_sa_name
  display_name = "CI/CD deployer"
  description  = "Used exclusively by the GitHub Actions deploy workflow."
}

# Allow the GH Actions workflow to impersonate this SA via WIF.
resource "google_service_account_iam_member" "wif_impersonation" {
  service_account_id = google_service_account.deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member = "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${var.wif_pool_id}/attribute.repository/${var.github_org}/${var.github_repo}"
}

# ---------------------------------------------------------------------------
# Project-level IAM roles for the deployer SA
# ---------------------------------------------------------------------------

resource "google_project_iam_member" "deployer_run_developer" {
  project = var.project_id
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_project_iam_member" "deployer_ar_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.deployer.email}"
}

# Required so the deployer can set a runtime SA on the Cloud Run service
# (if a dedicated runtime SA is used in the future).
resource "google_project_iam_member" "deployer_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.deployer.email}"
}
