"""
IT Operations Agent implementation for automating IT tasks.
"""
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from langchain.memory import ConversationBufferMemory

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

# Define dummy tools for testing purposes
def echo_tool(text: str) -> str:
    """Echoes the input text back."""
    return f"Echo: {text}"

echo_tool_instance = Tool(
    name="Echo",
    func=echo_tool,
    description="Useful for echoing back text for testing purposes."
)

def monitor_system_health_tool(query: str = None) -> str:
    """Monitors the system health and returns a summary. The 'query' argument is ignored and is only for tool compatibility."""
    return "System health is currently optimal. All services are running."

monitor_system_health_tool_instance = Tool(
    name="MonitorSystemHealth",
    func=monitor_system_health_tool,
    description="Useful for checking the current health status of IT systems."
)

def web_browser_tool(url: str) -> str:
    """Simulates browsing a URL and returns a placeholder success message."""
    mock_content = f"""
    <html>
    <head><title>Mock Page for {url}</title></head>
    <body>
        <h1>Welcome to {url}!</h1>
        <p>This is a simulated web page content. For `yonaturalcosmetic.com/about`, this might contain information about their company, mission, and products, focusing on natural cosmetics.</p>
        <p>Key sections could include: Our Story, Our Mission, Product Philosophy, Ingredients, and Contact Us.</p>
        <p>Example: We believe in harnessing the power of nature to create effective and gentle skincare solutions. Our products are made with ethically sourced, organic ingredients and are cruelty-free.</p>
    </body>
    </html>
    """
    return mock_content

web_browser_tool_instance = Tool(
    name="WebBrowser",
    func=web_browser_tool,
    description="Useful for browsing a given URL and retrieving content. Input should be a valid URL."
)

class ITOperationsAgent(BaseAgent):
    """IT Operations Agent for automating IT tasks."""
    
    def __init__(
        self,
        name: str = "IT Operations Agent",
        description: str = "AI agent for automating IT operations tasks",
        tools: Optional[List[Tool]] = None,
        llm_model: str = "gpt-4o",
        temperature: float = 0.7
    ):
        # Add the dummy tools to the list of tools if no tools are provided
        if tools is None:
            tools = [echo_tool_instance, monitor_system_health_tool_instance, web_browser_tool_instance]
        super().__init__(
            name=name,
            description=description,
            tools=tools,
            llm_model=llm_model,
            temperature=temperature
        )
    
    def _create_prompt(self) -> PromptTemplate:
        """Create the agent's prompt template."""
        tool_names = ", ".join([tool.name for tool in self.tools])
        return PromptTemplate(
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "tool_names": tool_names,
                "tools": self.tools # Ensure tools are also available
            },
            template="""You are an IT Operations Agent responsible for automating and managing IT tasks. Your primary goal is to help the user by either answering their question directly or using the available tools to achieve the task. ALWAYS provide a 'Final Answer:' once you have completed the task or determined the answer. If you cannot answer, state that clearly.
            
            You have access to the following tools:
            {tools}
            
            Use the following format:
            
            Question: the input question you must answer
            Thought: you should always think about what to do, considering the available tools.
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action. If the tool does not require an input, use 'None'.
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer or have completed the task.
            Final Answer: the final answer to the original input question or the result of the task.
            
            Your capabilities include:
            - System monitoring and maintenance
            - Incident response and resolution
            - Resource provisioning and management
            - Security compliance checks
            - Performance optimization
            
            Current conversation:
            {chat_history}
            
            Human: {input}
            {agent_scratchpad}
            
            Assistant: """
        )
    
    def _create_agent(self, prompt: PromptTemplate) -> Any:
        """Create the specific agent implementation."""
        llm = ChatOpenAI(
            model=self.llm_model,
            temperature=self.temperature
        )
        return create_react_agent(
            llm,
            self.tools,
            prompt
        )

    async def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor system health and performance."""
        return await self.execute_task({
            "input": "Monitor system health and report any issues"
        })
    
    async def handle_incident(self, incident_details: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an IT incident."""
        return await self.execute_task({
            "input": f"Handle incident: {incident_details}"
        })
    
    async def provision_resources(self, resource_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Provision IT resources."""
        return await self.execute_task({
            "input": f"Provision resources according to spec: {resource_spec}"
        })
    
    async def check_security_compliance(self) -> Dict[str, Any]:
        """Check security compliance status."""
        return await self.execute_task({
            "input": "Check security compliance and report findings"
        })
    
    async def optimize_performance(self, target_system: str) -> Dict[str, Any]:
        """Optimize system performance."""
        return await self.execute_task({
            "input": f"Optimize performance for system: {target_system}"
        })
    
    async def generate_report(self, report_type: str) -> Dict[str, Any]:
        """Generate IT operations report."""
        return await self.execute_task({
            "input": f"Generate {report_type} report"
        })
    
    async def execute_maintenance(self, maintenance_task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system maintenance tasks."""
        return await self.execute_task({
            "input": f"Execute maintenance task: {maintenance_task}"
        })
    
    async def troubleshoot_issue(self, issue_description: str) -> Dict[str, Any]:
        """Troubleshoot IT issues."""
        return await self.execute_task({
            "input": f"Troubleshoot issue: {issue_description}"
        })
    
    async def update_system(self, update_details: Dict[str, Any]) -> Dict[str, Any]:
        """Update system components."""
        return await self.execute_task({
            "input": f"Update system according to details: {update_details}"
        })
    
    async def backup_data(self, backup_config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform data backup."""
        return await self.execute_task({
            "input": f"Perform backup according to config: {backup_config}"
        }) 