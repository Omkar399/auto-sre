#!/usr/bin/env python3
"""
Browser Use Test: Open Gmail with Claude
Uses Claude API which Browser Use natively supports
"""

import asyncio
import os
from browser_use import Agent, Browser
from anthropic import Anthropic

async def test_gmail_claude():
    """Test Gmail with Claude"""
    
    print("=" * 70)
    print("🧪 Browser Use: Gmail Test with Claude")
    print("=" * 70)
    print()
    
    # Get API key - try from env or use default
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not in .env")
        print("   Please add your Claude API key to .env:")
        print("   ANTHROPIC_API_KEY=sk-ant-...")
        print()
        print("   Get key at: https://console.anthropic.com")
        return
    
    print("📦 Initializing Claude LLM...")
    llm = Anthropic(api_key=api_key)
    print("✅ Claude ready")
    print()
    
    print("🌐 Creating browser (headless=False - window should appear)...")
    browser = Browser(headless=False)
    print("✅ Browser ready")
    print()
    
    task = "Open Gmail, look at the latest email in the inbox, and tell me who it's from and what the subject is"
    
    print(f"📋 Task: {task}")
    print()
    print("⏳ Starting browser automation...")
    print("   (Chromium window should open shortly)")
    print()
    
    try:
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
        )
        
        result = await agent.run()
        
        print()
        print("=" * 70)
        print("✅ RESULT:")
        print("=" * 70)
        print(result)
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gmail_claude())

