#!/usr/bin/env python3
"""
Simple Browser Use Example - Using Browser Use Cloud API
- No complex multi-agent setup
- Just Browser Use with BROWSER_USE_API_KEY
"""

import os
import asyncio
from browser_use import Agent
from dotenv import load_dotenv

async def main():
    """Run simple browser automation with Browser Use API"""
    
    # Load environment
    load_dotenv("/Users/omkarpodey/wos/browser-use-project/.env")
    
    api_key = os.getenv("BROWSER_USE_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ BROWSER_USE_API_KEY not found!\n"
            "Add to .env: BROWSER_USE_API_KEY=your-key-here"
        )
    
    print("=" * 60)
    print("🤖 Browser Use - Simple Mode")
    print("=" * 60)
    print(f"Using API Key: {api_key[:20]}...")
    
    # Task
    task = "Find the top 5 trending repositories on GitHub and tell me their names and star counts"
    print(f"\n📋 Task: {task}\n")
    
    # Create agent with Browser Use API key
    agent = Agent(
        task=task,
        api_key=api_key,
    )
    
    # Run
    print("🚀 Running agent...\n")
    result = await agent.run()
    
    print("\n" + "=" * 60)
    print("✅ Result:")
    print("=" * 60)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
