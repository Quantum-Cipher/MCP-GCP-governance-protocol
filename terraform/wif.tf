# ---------------------------------------------------------------------------
# Workload Identity Federation
# ---------------------------------------------------------------------------
# Enables GitHub Actions to exchange a short-lived OIDC token for a
# Google access token – no long-lived service account keys required.

resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = var.wif_pool_id
  display_name              = "GitHub Actions pool"
  description               = "Pool for GitHub OIDC tokens from Actions workflows."
}

resource "google_iam_workload_identity_pool_provider" "github_oidc" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = var.wif_provider_id
  display_name                       = "GitHub OIDC provider"
  description                        = "Maps GitHub Actions OIDC tokens to Google credentials."

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }

  # Scope token exchange to this specific repository only.
  attribute_condition = "attribute.repository == \"${var.github_org}/${var.github_repo}\""
}
