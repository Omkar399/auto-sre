#!/usr/bin/env python3
"""
Simple Browser Use Example
Finds the number of stars on the browser-use GitHub repository
"""

from browser_use import Agent, ChatBrowserUse

async def main():
    """Run the browser agent"""
    agent = Agent(
        task="Find the number of stars of the browser-use repo on GitHub",
        llm=ChatBrowserUse(),
    )
    result = await agent.run()
    print(f"\n✅ Agent Result: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
