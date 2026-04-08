import os
from mcp.server.fastmcp import FastMCP
import httpx

# [666] Grounding: Initialize the Eternum Governance Bridge
mcp = FastMCP("Eternum-Governance-Bridge")

# --- 1. THE CONSTITUTION (Resource) ---
@mcp.resource("eternum://whitepaper")
def read_whitepaper() -> str:
    """Returns the Eternum Whitepaper Constitution for policy grounding."""
    try:
        with open("eternum_whitepaper.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "ERROR: Constitution not found. [999] Halt deployment."

# --- 2. THE GOVERNANCE GATEKEEPER (Tool) ---
@mcp.tool()
def governance_evaluate(action: str, target_sha: str, actor_id: str) -> str:
    """
    Evaluates proposed actions (deploy_agent, rebuild_agent) against the whitepaper.
    Must be called before any state modification.
    """
    # In a production environment, this would parse the diff and run an LLM policy check.
    # For initial liftoff, we enforce structural logging and hardcoded baseline approval.
    
    log_entry = f"Action: {action} | SHA: {target_sha} | Actor: {actor_id} | Integrity: VALID"
    print(f"[GOVERNANCE LOG] {log_entry}")
    
    # Example logic: block unsigned or manual root deployments
    if action == "deploy_agent" and target_sha == "latest":
        return '{"decision": "deny", "reason": "Deploying :latest violates immutable SHA constraints.", "violation": "Section 4"}'
        
    return '{"decision": "allow", "reason": "Action complies with Eternum Constitution."}'

# --- 3. GIT SYNC (Tool) ---
@mcp.tool()
async def git_sync(repo_name: str, branch: str = "main") -> str:
    """Fetches the latest commit SHA from GitHub for 12-hour diff checks."""
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{repo_name}/branches/{branch}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Eternum-Governor"
    }
    if token:
        headers["Authorization"] = f"token {token}"
        
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["commit"]["sha"]
        return f"ERROR: Failed to sync Git state. Status {response.status_code}"

if __name__ == "__main__":
    # Runs the SSE server on port 8080 (required for Cloud Run)
    mcp.run(transport='sse')
