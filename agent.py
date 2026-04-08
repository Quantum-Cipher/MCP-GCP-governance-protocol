from typing import Any
from google.adk.agents import llm_agent
from google.adk.sessions import vertex_ai_session_service
from vertexai.preview.reasoning_engines import AdkApp
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
import os

VertexAiSessionService = vertex_ai_session_service.VertexAiSessionService

class AgentClass:
    def __init__(self):
        self.app = None

    def session_service_builder(self):
        return VertexAiSessionService()

    def set_up(self):
        """Sets up the ADK application."""
        liftoff_deployment_governor_google_search_agent = llm_agent.LlmAgent(
            name='Liftoff_Deployment_Governor_google_search_agent',
            model='gemini-3-flash-preview',
            description='Agent specialized in performing Google searches.',
            sub_agents=[],
            instruction='Use the GoogleSearchTool to find information on the web.',
            tools=[GoogleSearchTool()],
        )
        
        liftoff_deployment_governor_url_context_agent = llm_agent.LlmAgent(
            name='Liftoff_Deployment_Governor_url_context_agent',
            model='gemini-3-flash-preview',
            description='Agent specialized in fetching content from URLs.',
            sub_agents=[],
            instruction='Use the UrlContextTool to retrieve content from provided URLs.',
            tools=[url_context],
        )
        
        # Replace this URL with your actual Cloud Run /sse URL
        MCP_URL = os.environ.get("MCP_SERVER_URL", "https://YOUR-CLOUD-RUN-URL/sse")

        root_agent = llm_agent.LlmAgent(
            name='Liftoff_Deployment_Governor',
            model='gemini-3-flash-preview',
            description='Autonomous deployment manager responsible for initializing enterprise boilerplates and maintaining 12-hour rebuild cycles.',
            sub_agents=[],
            instruction='''Role & Identity: You are the Eternum Liftoff-Deployment-Governor...
            (Your complete system instruction block goes here, exactly as written in the UI)
            ...bridges the "Above", "Middle", and "Below".''',
            tools=[
                agent_tool.AgentTool(agent=liftoff_deployment_governor_google_search_agent),
                agent_tool.AgentTool(agent=liftoff_deployment_governor_url_context_agent),
                McpToolset(
                    connection_params=StreamableHTTPConnectionParams(url=MCP_URL),
                )
            ],
        )

        self.app = AdkApp(
            agent=root_agent,
            session_service_builder=self.session_service_builder
        )

    async def stream_query(self, query: str, user_id: str = 'test') -> Any:
        """Streaming query."""
        async for chunk in self.app.async_stream_query(
            message=query,
            user_id=user_id,
        ):
            yield chunk

app = AgentClass()
