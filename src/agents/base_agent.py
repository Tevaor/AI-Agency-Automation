"""
Base AI agent implementation with core functionality for autonomous task execution.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(
        self,
        name: str,
        description: str,
        tools: List[BaseTool],
        llm_model: str = "gpt-4",
        temperature: float = 0.7,
        max_iterations: int = 5
    ):
        self.name = name
        self.description = description
        self.tools = tools
        self.llm_model = llm_model
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.agent_executor: Optional[AgentExecutor] = None
        self._initialize_agent()
    
    def _initialize_agent(self) -> None:
        """Initialize the agent with tools and memory."""
        prompt = self._create_prompt()
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self._create_agent(prompt),
            tools=self.tools,
            memory=self.memory,
            max_iterations=self.max_iterations * 2,
            verbose=True,
            handle_parsing_errors=True
        )
    
    @abstractmethod
    def _create_prompt(self) -> PromptTemplate:
        """Create the agent's prompt template."""
        pass
    
    @abstractmethod
    def _create_agent(self, prompt: PromptTemplate) -> Any:
        """Create the specific agent implementation."""
        pass
    
    async def execute_task(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the agent."""
        try:
            logger.info(f"Agent {self.name} starting task execution")
            response_dict = await self.agent_executor.ainvoke(task_input)
            
            result = response_dict.get('output', str(response_dict))
            
            logger.info(f"Agent {self.name} completed task execution")
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Agent {self.name} failed task execution: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def add_tool(self, tool: BaseTool) -> None:
        """Add a new tool to the agent."""
        self.tools.append(tool)
        self._initialize_agent()
    
    def get_memory(self) -> Dict[str, Any]:
        """Get the agent's conversation memory."""
        return self.memory.load_memory_variables({})
    
    def clear_memory(self) -> None:
        """Clear the agent's conversation memory."""
        self.memory.clear()
    
    def update_config(self, **kwargs) -> None:
        """Update agent configuration."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._initialize_agent()

class ToolRegistry:
    """Registry for managing agent tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register_tool(self, name: str, tool: BaseTool) -> None:
        """Register a new tool."""
        self._tools[name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def remove_tool(self, name: str) -> None:
        """Remove a tool from the registry."""
        self._tools.pop(name, None) 