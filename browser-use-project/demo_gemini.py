#!/usr/bin/env python3
"""
Simple Browser Use Demo with Gemini
Uses Gemini AI to control a local Chromium browser
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser
import google.generativeai as genai

# Load environment variables
load_dotenv()

async def main():
    """Run a simple browser automation task with Gemini"""
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file!")
        return
    
    print("="*60)
    print("🤖 Browser Automation with Gemini AI")
    print("="*60)
    
    # Configure and initialize Gemini
    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Create browser instance
    browser = Browser(
        headless=False,  # Set to True to hide browser window
    )
    
    # Define the task
    task = "Go to GitHub trending page and find the top 3 trending repositories. Tell me their names."
    
    print(f"\n🎯 Task: {task}\n")
    print("🚀 Starting browser agent...\n")
    
    # Create and run the agent
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
    )
    
    try:
        result = await agent.run()
        
        print("\n" + "="*60)
        print("✅ Task Completed!")
        print("="*60)
        print(f"\nResult:\n{result}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n🎉 Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())

