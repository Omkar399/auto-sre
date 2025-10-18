#!/usr/bin/env python3
"""
Simple Browser Use Test: Open Gmail
Just open Gmail and see if the browser opens
"""

import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

async def test_gmail_simple():
    """Simple test - just open Gmail"""
    
    print("=" * 70)
    print("🧪 Simple Browser Use Test: Open Gmail")
    print("=" * 70)
    print()
    
    print("🌐 Creating browser (headless=False - should show window)...")
    browser = Browser(headless=False)
    print("✅ Browser created")
    print()
    
    print("🚀 Starting task...")
    print("   Task: Open Gmail and read the latest email")
    print()
    
    agent = Agent(
        task="Open Gmail, look at the latest email in the inbox, and tell me the sender and subject",
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    print("⏳ Running agent (this may take a moment)...")
    result = await agent.run()
    
    print()
    print("=" * 70)
    print("✅ RESULT:")
    print("=" * 70)
    print(result)
    print()

if __name__ == "__main__":
    asyncio.run(test_gmail_simple())
