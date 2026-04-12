terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Remote state – update the bucket name before first `terraform init`.
  # The bucket must already exist and have versioning enabled.
  backend "gcs" {
    bucket = "logfox-api-daemon-tfstate"
    prefix = "mcp-gcp-governance-protocol"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
