#!/usr/bin/env python3
"""
Browser Use Test: Open Gmail with Custom DeepSeek LLM
Uses DeepSeek v3.1 via NVIDIA API as the LLM backend
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser
from openai import OpenAI

# Load environment
load_dotenv()

class DeepSeekLLM:
    """Custom LLM wrapper for DeepSeek v3.1 to work with Browser Use"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        self.model = "deepseek-ai/deepseek-v3.1"
        self.provider = "deepseek"  # Browser Use checks this
    
    async def send_message(self, messages: list[dict]) -> str:
        """Send message to DeepSeek and get response"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    
    def __call__(self, messages: list[dict], **kwargs) -> str:
        """Make LLM callable for sync usage"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
        )
        return response.choices[0].message.content

async def test_gmail():
    """Test Gmail with custom DeepSeek LLM"""
    
    print("=" * 70)
    print("🧪 Browser Use: Gmail Test with DeepSeek v3.1")
    print("=" * 70)
    print()
    
    # Check API key
    if not os.getenv("NVIDIA_API_KEY"):
        print("❌ NVIDIA_API_KEY not found in .env")
        return
    
    print("📦 Initializing DeepSeek v3.1 LLM...")
    llm = DeepSeekLLM()
    print("✅ LLM ready")
    print()
    
    print("🌐 Creating browser (headless=False)...")
    browser = Browser(headless=False)
    print("✅ Browser ready (window should open)")
    print()
    
    task = "Go to Gmail, look at the latest email in the inbox, and tell me who it's from and what the subject is"
    
    print(f"📋 Task: {task}")
    print()
    print("⏳ Starting browser automation...")
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
    asyncio.run(test_gmail())
