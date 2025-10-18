#!/usr/bin/env python3
"""
Browser Use Test: Open Gmail and Read Latest Email
Tests the multi-agent setup with real-world use case
- Gemini: Plans how to navigate Gmail
- DeepSeek v3.1: Executes with advanced reasoning
- Browser Use: Controls Chromium to read email
"""

import os
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, Browser
from openai import OpenAI
import google.generativeai as genai

# Load environment variables
load_dotenv()

def get_gemini_client():
    """Initialize Google Gemini client"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY not found in .env")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

def get_deepseek_client():
    """Initialize DeepSeek v3.1 via NVIDIA"""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("❌ NVIDIA_API_KEY not found in .env")
    
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )

async def test_gmail():
    """Test: Open Gmail and read latest email"""
    
    print("=" * 70)
    print("🧪 Testing Browser Use: Gmail Email Reader")
    print("=" * 70)
    print()
    
    # Initialize clients
    print("📦 Initializing AI models...")
    gemini = get_gemini_client()
    deepseek = get_deepseek_client()
    print("  ✅ Gemini ready")
    print("  ✅ DeepSeek v3.1 ready")
    print()
    
    # Create browser
    print("🌐 Initializing browser...")
    browser = Browser(headless=False)  # Show browser window so you can see it
    print("  ✅ Chromium ready")
    print()
    
    # Task
    task = "Open Gmail, look at the latest email in the inbox, and tell me the sender, subject, and a brief summary of the email content"
    
    print(f"📋 Task: {task}")
    print()
    
    # Step 1: Plan with Gemini
    print("1️⃣  Planning Phase (Gemini)...")
    print("-" * 70)
    prompt = f"""
    You are a task planning agent for browser automation.
    Break down this Gmail task into clear steps:
    
    Task: {task}
    
    Return a brief numbered list of steps to accomplish this.
    """
    
    response = gemini.generate_content(prompt)
    plan = response.text
    print(plan)
    print()
    
    # Step 2: Strategy with DeepSeek
    print("2️⃣  Strategy Phase (DeepSeek v3.1 with Extended Thinking)...")
    print("-" * 70)
    print("💭 DeepSeek is analyzing strategy...\n")
    
    strategy_prompt = f"""
    You are a task execution strategist. Given this Gmail task and plan,
    provide specific, detailed instructions for browser automation.
    
    Task: {task}
    
    Plan:
    {plan}
    
    Think through the steps carefully, then provide clear instructions.
    """
    
    reasoning_text = ""
    strategy_text = ""
    
    completion = deepseek.chat.completions.create(
        model="deepseek-ai/deepseek-v3.1",
        messages=[{"role": "user", "content": strategy_prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=2048,
        extra_body={"chat_template_kwargs": {"thinking": True}},
        stream=True
    )
    
    for chunk in completion:
        reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
        if reasoning:
            reasoning_text += reasoning
        
        if chunk.choices[0].delta.content is not None:
            strategy_text += chunk.choices[0].delta.content
    
    if reasoning_text:
        print(f"🧠 Extended Thinking Output:\n{reasoning_text[:300]}...\n")
    
    print(f"🚀 Strategy:\n{strategy_text}\n")
    
    # Step 3: Execute with Browser Use
    print("3️⃣  Execution Phase (Browser Use + DeepSeek)...")
    print("-" * 70)
    print("🔄 Executing task in browser...\n")
    
    agent = Agent(
        task=task,
        llm=deepseek,
        browser=browser,
    )
    
    result = await agent.run()
    
    print()
    print("=" * 70)
    print("✅ RESULT:")
    print("=" * 70)
    print(result)
    print()
    
    return result

if __name__ == "__main__":
    asyncio.run(test_gmail())
