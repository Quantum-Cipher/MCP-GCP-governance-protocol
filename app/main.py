#!/usr/bin/env python3
import os
import logging
from flask import Flask, jsonify, request
from core.policy_engine import evaluate_governance_request

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)

app = Flask(__name__)

@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok", "service": "eternum-mcp-gcp-governance"}), 200

@app.get("/readyz")
def readyz():
    return jsonify({"status": "ready", "service": "eternum-mcp-gcp-governance"}), 200

@app.post("/governance/evaluate")
def governance_evaluate():
    payload = request.get_json(silent=True) or {}
    result = evaluate_governance_request(payload)
    status_code = 200 if result.get("decision") != "deny" else 403
    return jsonify(result), status_code

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
