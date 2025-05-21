# File: app/agent.py

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.cost_tools import list_idle_resources, suggest_optimizations
import os

class CostOptimizerAgent:
    def __init__(self, openai_key=None):
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=self.openai_key)
        self.agent = None
        self.last_context = None  # to avoid redundant runs

        self.tools = [
            Tool(
                name="ListIdleResources",
                func=lambda x: list_idle_resources(*x.split(",")),
                description="List idle resources like VMs, disks, IPs, etc."
            ),
            Tool(
                name="SuggestOptimizations",
                func=lambda x: suggest_optimizations(*x.split(",")),
                description="Suggest cost optimization with priorities and optionally execute actions."
            )
        ]

    def initialize(self):
        if not self.agent:
            self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    def run(self, cloud_provider: str, project_id: str, mode: str) -> str:
        context = f"{cloud_provider},{project_id},{mode}"
        if self.last_context == context:
            return "ℹ️ Agent already ran with this context. Please change inputs to rerun."
        
        self.last_context = context
        self.initialize()
        return self.agent.run(f"Analyze cost optimization for context: {context}")
