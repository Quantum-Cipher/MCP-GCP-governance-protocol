# MCP GCP Governance Protocol

A hardened governance control service for GCP-oriented deployment workflows.

## Purpose
This service evaluates deployment actions against policy before liftoff, rebuild, rollback, or validation operations proceed.

## v2 Scope
- policy-based allow / deny decisions
- signed commit enforcement
- environment gating
- change-window checks
- provenance requirement flag
- structured JSON decision logs
- health and readiness endpoints
- Cloud Run containerization
- starter schema set for future MCP-style tool integration

## Local bootstrap
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app/main.py
```

## CI/CD – GitHub Actions deploy workflow

The `.github/workflows/deploy.yml` workflow builds a Docker image, pushes it to Artifact Registry, and deploys to Cloud Run on every push to `main` (or on manual dispatch).

Authentication uses **Workload Identity Federation (WIF)** — no long-lived service account keys are stored in GitHub.

### Required GitHub Actions secrets

| Secret name | Value |
|---|---|
| `GCP_WIF_PROVIDER` | Full WIF provider resource name, e.g. `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID` |
| `GCP_DEPLOYER_SA` | Deployer service account email, e.g. `deployer@logfox-api-daemon.iam.gserviceaccount.com` |

Add these at **GitHub → Settings → Secrets and variables → Actions → Repository secrets**.

### GCP prerequisites

The following must exist in GCP project `logfox-api-daemon` before the workflow can succeed:

1. **Workload Identity Pool** — a pool configured for GitHub OIDC.
2. **Workload Identity Provider** in that pool with the attribute mapping:
   ```
   attribute.repository = assertion.repository
   ```
   and the condition:
   ```
   assertion.repository == "Quantum-Cipher/MCP-GCP-governance-protocol"
   ```
3. **Deployer service account** with the following IAM roles:
   - `roles/run.developer` — deploy Cloud Run services
   - `roles/artifactregistry.writer` — push images
   - `roles/iam.serviceAccountUser` — act as the runtime service account (if different)
4. **Workload Identity User binding** on the deployer SA:
   ```
   principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/attribute.repository/Quantum-Cipher/MCP-GCP-governance-protocol
   ```
   granted the role `roles/iam.workloadIdentityUser`.
5. **Artifact Registry repository** named `governance` in region `us-central1`.
6. **Cloud Run API** and **Artifact Registry API** enabled in the project.

### Smoke-test checklist after setup

- [ ] Both secrets (`GCP_WIF_PROVIDER`, `GCP_DEPLOYER_SA`) are present in GitHub repo secrets
- [ ] Trigger the workflow manually via **Actions → Deploy to Cloud Run → Run workflow**
- [ ] `Authenticate to Google Cloud` step passes (OIDC token exchanged successfully)
- [ ] `Set up gcloud CLI` step passes
- [ ] `Build and push Docker image` step passes (image visible in Artifact Registry)
- [ ] `Deploy to Cloud Run` step passes
- [ ] Service URL printed; `/healthz` returns `{"status": "ok"}`
