# agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain.tools import Tool
from llm.gemini_llm import GeminiLLM, GeminiConfig
from config.api_keys import APIKeyManager


class BaseAgent(ABC):
    """Base class for all specialized agents in the multi-agent system"""
    
    def __init__(self, agent_name: str, description: str, tools: List[Tool] = None):
        """Initialize base agent
        
        Args:
            agent_name: Name of the agent
            description: Description of the agent's purpose
            tools: List of tools available to this agent
        """
        self.agent_name = agent_name
        self.description = description
        self.tools = tools or []
        self.llm = self._create_llm()
    
    def _create_llm(self) -> GeminiLLM:
        """Create LLM instance for the agent"""
        api_manager = APIKeyManager()
        api_key = api_manager.get_api_key("gemini")
        
        if not api_key:
            raise ValueError("Gemini API key not found. Please configure API keys first.")
        
        config = GeminiConfig(
            model_name="gemini-2.0-flash",
            temperature=0.3,
            max_output_tokens=2048
        )
        
        return GeminiLLM(api_key=api_key, config=config)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return updated state"""
        pass
    
    def get_tool_names(self) -> List[str]:
        """Return list of tool names available to this agent"""
        return [tool.name for tool in self.tools]
    
    def execute_tool(self, tool_name: str, tool_input: Any) -> Any:
        """Execute a specific tool"""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.func(tool_input)
        raise ValueError(f"Tool '{tool_name}' not found in agent {self.agent_name}")
    
    def __str__(self) -> str:
        return f"{self.agent_name}: {self.description}"