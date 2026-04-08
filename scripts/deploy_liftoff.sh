#!/bin/bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-logfox-api-daemon}"
REGION="${REGION:-us-central1}"
REPOSITORY="${REPOSITORY:-governance}"
IMAGE="${IMAGE:-mcp-gcp-governance-protocol}"
SERVICE="${SERVICE:-mcp-gcp-governance-protocol}"
RUNTIME_SA="${RUNTIME_SA:-}"

cd ~/Projects/MCP-GCP-governance-protocol

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

gcloud config set project "${PROJECT_ID}"

gcloud services enable \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  aiplatform.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  cloudtrace.googleapis.com \
  cloudresourcemanager.googleapis.com

gcloud artifacts repositories describe "${REPOSITORY}" \
  --location="${REGION}" >/dev/null 2>&1 || \
gcloud artifacts repositories create "${REPOSITORY}" \
  --repository-format=docker \
  --location="${REGION}" \
  --description="MCP governance images"

gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION="${REGION}",_REPOSITORY="${REPOSITORY}",_IMAGE="${IMAGE}"

DEPLOY_ARGS=(
  run deploy "${SERVICE}"
  --image "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}:latest"
  --region "${REGION}"
  --platform managed
  --allow-unauthenticated
  --set-env-vars "APP_ENV=production,PROJECT_ID=${PROJECT_ID},REGION=${REGION},SERVICE_NAME=${SERVICE}"
)

if [ -n "${RUNTIME_SA}" ]; then
  DEPLOY_ARGS+=(--service-account "${RUNTIME_SA}")
fi

gcloud "${DEPLOY_ARGS[@]}"

gcloud run services describe "${SERVICE}" \
  --region "${REGION}" \
  --format="value(status.url)"
