variable "project_id" {
  description = "GCP project ID that hosts all resources."
  type        = string
  default     = "logfox-api-daemon"
}

variable "project_number" {
  description = "Numeric GCP project number (required for WIF principal bindings)."
  type        = string
}

variable "region" {
  description = "GCP region for Artifact Registry and Cloud Run."
  type        = string
  default     = "us-central1"
}

variable "github_org" {
  description = "GitHub organization or username that owns the repository."
  type        = string
  default     = "Quantum-Cipher"
}

variable "github_repo" {
  description = "GitHub repository name (without the org prefix)."
  type        = string
  default     = "MCP-GCP-governance-protocol"
}

variable "wif_pool_id" {
  description = "ID for the Workload Identity Pool."
  type        = string
  default     = "github-actions-pool"
}

variable "wif_provider_id" {
  description = "ID for the Workload Identity Provider inside the pool."
  type        = string
  default     = "github-oidc"
}

variable "deployer_sa_name" {
  description = "Name (account ID) of the deployer service account."
  type        = string
  default     = "deployer"
}

variable "artifact_registry_repo" {
  description = "Artifact Registry Docker repository name."
  type        = string
  default     = "governance"
}
