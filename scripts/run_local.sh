#!/bin/bash
set -euo pipefail

cd ~/Projects/MCP-GCP-governance-protocol
source ~/Projects/MCP-GCP-governance-protocol/.venv/bin/activate
PYTHONPATH="$PWD" python -m app.main
