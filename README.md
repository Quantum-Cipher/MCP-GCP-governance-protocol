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
