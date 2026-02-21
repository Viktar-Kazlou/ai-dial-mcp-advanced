import asyncio
import json
import os

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.dial_client import DialClient
from agent.models.message import Message, Role


async def main():
    api_key = os.getenv("DIAL_API_KEY")
    if not api_key:
        raise ValueError("DIAL_API_KEY is required")

    tools: list[dict] = []
    tool_name_client_map: dict[str, MCPClient | CustomMCPClient] = {}

    ums_client = await MCPClient.create("http://localhost:8005/mcp")
    ums_tools = await ums_client.get_tools()
    tools.extend(ums_tools)
    for tool in ums_tools:
        tool_name_client_map[tool["function"]["name"]] = ums_client

    fetch_client = await CustomMCPClient.create("https://remote.mcpservers.org/fetch/mcp")
    fetch_tools = await fetch_client.get_tools()
    tools.extend(fetch_tools)
    for tool in fetch_tools:
        tool_name_client_map[tool["function"]["name"]] = fetch_client

    print(f"Loaded tools: {json.dumps([tool['function']['name'] for tool in tools], indent=2)}")

    dial_client = DialClient(
        api_key=api_key,
        endpoint="https://ai-proxy.lab.epam.com",
        tools=tools,
        tool_name_client_map=tool_name_client_map,
    )

    messages = [
        Message(
            role=Role.SYSTEM,
            content="You are a helpful assistant. Use available tools to manage users and fetch web data when needed."
        )
    ]

    while True:
        user_input = input("\n👤: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Chat ended.")
            break
        if not user_input:
            continue

        messages.append(Message(role=Role.USER, content=user_input))
        ai_message = await dial_client.get_completion(messages)
        messages.append(ai_message)

if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him