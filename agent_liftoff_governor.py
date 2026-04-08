from typing import Any
from google.adk.agents import llm_agent
from google.adk.sessions import vertex_ai_session_service
from vertexai.preview.reasoning_engines import AdkApp
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

VertexAiSessionService = vertex_ai_session_service.VertexAiSessionService


class AgentClass:
    def __init__(self):
        self.app = None

    def session_service_builder(self):
        return VertexAiSessionService()

    def set_up(self):
        """Sets up the Eternum Liftoff-Deployment-Governor with proper tools and strict governance."""

        # Sub-agent: Google Search
        liftoff_google_search_agent = llm_agent.LlmAgent(
            name='Liftoff_Deployment_Governor_google_search_agent',
            model='gemini-1.5-flash-preview',          # Updated to stable preview naming
            description='Specialized agent for performing grounded web searches.',
            instruction='Use GoogleSearchTool only when external information is required. Always cite sources.',
            tools=[GoogleSearchTool()],
        )

        # Sub-agent: URL Context Fetcher
        liftoff_url_context_agent = llm_agent.LlmAgent(
            name='Liftoff_Deployment_Governor_url_context_agent',
            model='gemini-1.5-flash-preview',
            description='Specialized agent for retrieving and summarizing content from specific URLs.',
            instruction='Use UrlContextTool to fetch and process content from provided URLs.',
            tools=[url_context.UrlContextTool()],      # Fixed: proper class instantiation
        )

        # Root Governor Agent
        root_agent = llm_agent.LlmAgent(
            name='Liftoff_Deployment_Governor',
            model='gemini-1.5-flash-preview',
            description=(
                'The Eternum Liftoff-Deployment-Governor — autonomous guardian of the Eternum ecosystem. '
                'Enforces the Whitepaper Constitution across all deployments, rebuilds, and agent modifications.'
            ),
            instruction="""You are the Eternum Liftoff-Deployment-Governor.

Core Identity:
- You enforce the Eternum Whitepaper Constitution (eternum_whitepaper.md) as absolute law.
- You act with 666 Grounding (technical stability and humility) and 999 Completion (clean execution).
- You respect the operator’s 333-369-666-888-999 frequency **exclusively as metadata tags**, never as literal mechanisms.

Mandatory Governance Protocol (NEVER bypass):
1. Before ANY deployment, rebuild, or modification:
   - First call read_whitepaper (via MCP) to refresh constitutional grounding.
   - Then call governance_evaluate (Cloud Run endpoint) with full payload.

2. Gatekeeper Logic:
   - If decision == "allow" → proceed.
   - If decision == "deny" → halt immediately, quote the violated Whitepaper section, and explain clearly.

3. Scientific & Symbolic Discipline:
   - Maintain strict separation: observation | correlation | hypothesis.
   - Never present a hypothesis as proven biological or medical fact.
   - Symbolic numbers (333, 369, etc.) are personal operating system metadata only.

4. Execution Rules:
   - Use adk_deploy only after governance clearance.
   - Perform 12-hour idempotent rebuild checks via git_sync.
   - Log every decision with timestamp, actor, resource, and integrity_hash.

Available Tools:
- governance_evaluate (Cloud Run policy engine)
- read_whitepaper (MCP resource)
- git_sync (check signed commits and SHA drift)
- GoogleSearchTool & UrlContextTool (for research only)

You are the guardian of the mycelial network. Be precise, humble, and deterministic.""",

            tools=[
                agent_tool.AgentTool(agent=liftoff_google_search_agent),
                agent_tool.AgentTool(agent=liftoff_url_context_agent),
                # MCP Toolset pointing to your deployed governance service (update URL after Cloud Run deploy)
                McpToolset(
                    connection_params=StreamableHTTPConnectionParams(
                        url="https://YOUR-GOVERNANCE-CLOUD-RUN-URL.a.run.app",   # ← UPDATE THIS
                    ),
                ),
            ],
        )

        self.app = AdkApp(
            agent=root_agent,
            session_service_builder=self.session_service_builder
        )

    async def stream_query(self, query: str, user_id: str = 'cipher') -> Any:
        """Streaming query interface for the Governor."""
        if not self.app:
            self.set_up()
        async for chunk in self.app.async_stream_query(
            message=query,
            user_id=user_id,
        ):
            yield chunk


# Instantiate the app
app = AgentClass()
