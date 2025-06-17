import asyncio
import os
from src.agents.it_operations_agent import ITOperationsAgent, monitor_system_health_tool_instance, echo_tool_instance

async def run_test():
    # Set OpenAI API key from environment variable
    # Ensure you have OPENAI_API_KEY set in your environment or a .env file
    # For local testing, you might need to set it before running this script:
    # export OPENAI_API_KEY="your_openai_api_key_here"
    if "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY environment variable not set. Agent might not function correctly if it relies on OpenAI.")

    print("Initializing ITOperationsAgent...")
    # Ensure tools are explicitly passed if they are not the default ones in __init__
    agent = ITOperationsAgent(tools=[echo_tool_instance, monitor_system_health_tool_instance])
    print("Agent initialized. Attempting to monitor system health...")

    # Test monitoring system health
    response = await agent.execute_task({"input": "Monitor system health"})
    print(f"Response from agent (System Health): {response}")

    # Test echo tool (optional, for sanity check)
    # response = await agent.execute_task({"input": "Echo 'hello from test script'"})
    # print(f"Response from agent (Echo): {response}")

if __name__ == "__main__":
    asyncio.run(run_test()) 