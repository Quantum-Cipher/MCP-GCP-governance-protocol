#!/usr/bin/env python3
from datetime import datetime, timezone

REQUIRED_METADATA_KEYS = ["signed_commit", "change_window"]
ALLOWED_ACTIONS = {"deploy_agent", "rollback_agent", "rebuild_agent", "validate_deployment"}
ALLOWED_ENVIRONMENTS = {"dev", "staging", "prod"}

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def evaluate_governance_request(payload: dict) -> dict:
    action = payload.get("action")
    environment = payload.get("environment")
    actor = payload.get("actor", "unknown")
    resource = payload.get("resource", "unspecified")
    metadata = payload.get("metadata", {})

    reasons = []

    if action not in ALLOWED_ACTIONS:
        reasons.append(f"unsupported action: {action}")
    if environment not in ALLOWED_ENVIRONMENTS:
        reasons.append(f"unsupported environment: {environment}")
    for key in REQUIRED_METADATA_KEYS:
        if key not in metadata:
            reasons.append(f"missing metadata key: {key}")
    if metadata.get("signed_commit") is not True:
        reasons.append("signed_commit must be true")
    if environment == "prod" and metadata.get("change_window") != "approved":
        reasons.append("prod deployments require approved change_window")

    decision = "allow" if not reasons else "deny"

    return {
        "decision": decision,
        "timestamp": utc_now(),
        "actor": actor,
        "resource": resource,
        "action": action,
        "environment": environment,
        "reasons": reasons,
        "eternum_note": "Governance aligned with whitepaper constitution + mycelium oracle data"
    }
