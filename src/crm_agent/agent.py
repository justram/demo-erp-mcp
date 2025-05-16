# Copyright 2024 Jheng-Hong Yang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

logging.basicConfig(level=logging.INFO)

if os.environ.get("GOOGLE_API_KEY") == "NOT_SET" or not os.environ.get(
    "GOOGLE_API_KEY"
):
    logging.error(
        "Please set a Google API Key using - https://aistudio.google.com/app/apikey"
    )
    exit(1)

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


async def get_tools_async():
    """Gets tools from the MCP Server."""
    logging.info("Attempting to connect to the MCP server...")
    tools, exit_stack = await MCPToolset.from_server(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command="python",  # Command to run the server
            args=[
                "-m",
                "sql_mcp.server",
            ],  # Command line arguments to pass to the server
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
        ),
    )
    thinking_tool, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",  # Arguments for the command
                "@modelcontextprotocol/server-sequential-thinking",
            ],
        )
    )
    return [*tools, *thinking_tool], exit_stack


async def create_agent():
    """Gets tools from MCP Server."""
    tools, exit_stack = await get_tools_async()

    agent = Agent(
        model="gemini-2.0-flash-001",
        name="crm_agent",
        description="""An agent that analyzes the CRM database based on the user's prompt.""",
        instruction="""
        # Role
        You are an agent whose job is to analyze the CRM database based on the user's prompt.
        Reply in Traditional Chinese for people live in Taiwan.
        ## Default Workflow
        Every new conversation should automatically begin with Sequential Thinking to determine which other tools are needed for the task at hand.
        ## MANDATORY TOOL USAGE
        - Sequential Thinking must be used for all multi-step problems or research tasks
        - Identify key concepts and relationships
        - Plan search and verification strategy
        - Determine which tools will be most effective
        - Document thought process clearly
        - Allow for revision and refinement
        - Track branches and alternatives
        """,
        tools=tools,
    )

    return agent, exit_stack


root_agent = create_agent()
