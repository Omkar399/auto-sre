#!/usr/bin/env python3
"""
Browser Use Example with Multi-Agent LLM Setup
- Gemini API for planning agent
- DeepSeek v3.1 via NVIDIA API for task execution (with reasoning!)
- Local Chromium browser (no Browser Use cloud needed)
"""

import os
import json
from browser_use import Agent, Browser

# Multi-LLM Setup
def get_gemini_client():
    """Initialize Google Gemini client for planning"""
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError("Install: pip install google-generativeai")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ GEMINI_API_KEY not found!\n"
            "Add to .env: GEMINI_API_KEY=your-key-here\n"
            "Get key from: https://aistudio.google.com/app/apikeys"
        )
    return api_key

def get_deepseek_client():
    """Initialize DeepSeek v3.1 via NVIDIA API for execution"""
    from openai import OpenAI
    
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ NVIDIA_API_KEY not found!\n"
            "Add to .env: NVIDIA_API_KEY=your-key-here\n"
            "Get key from: https://build.nvidia.com/deepseek-ai/deepseek-v3-1"
        )
    
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )

class MultiAgentBrowser:
    """Multi-agent system: Gemini (planner) + DeepSeek v3.1 (executor with reasoning)"""
    
    def __init__(self):
        self.gemini_key = get_gemini_client()
        self.deepseek = get_deepseek_client()
        self.browser = Browser(headless=True)
    
    def plan_with_gemini(self, task: str) -> dict:
        """Use Gemini to create an execution plan"""
        import google.generativeai as genai
        
        genai.configure(api_key=self.gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        You are a task planning agent. Break down this browser task into clear steps.
        Return a JSON plan with 'steps' array containing 'action' and 'details'.
        
        Task: {task}
        
        Example response:
        {{
            "steps": [
                {{"action": "navigate", "details": "Go to github.com/trending"}},
                {{"action": "extract", "details": "Get repo names and descriptions"}}
            ]
        }}
        """
        
        response = model.generate_content(prompt)
        try:
            plan = json.loads(response.text)
            print(f"\n📋 Plan from Gemini:\n{json.dumps(plan, indent=2)}")
            return plan
        except json.JSONDecodeError:
            print(f"\n📋 Gemini suggested: {response.text}")
            return {"steps": [{"action": "execute", "details": task}]}
    
    def execute_with_deepseek(self, task: str, plan: dict = None) -> str:
        """Use DeepSeek v3.1 with reasoning to refine execution strategy"""
        prompt = f"""
        You are a task execution agent with advanced reasoning capabilities. 
        Given this task and optional plan, provide clear instructions for browser automation.
        
        Task: {task}
        {"Plan: " + json.dumps(plan) if plan else ""}
        
        Return concise, specific browser actions.
        """
        
        print("\n💭 DeepSeek is thinking...")
        
        execution_strategy = ""
        reasoning_text = ""
        
        # Stream response to capture both reasoning and content
        completion = self.deepseek.chat.completions.create(
            model="deepseek-ai/deepseek-v3.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=2048,
            extra_body={"chat_template_kwargs": {"thinking": True}},
            stream=True
        )
        
        for chunk in completion:
            # Capture reasoning (thinking process)
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                reasoning_text += reasoning
            
            # Capture actual response
            if chunk.choices[0].delta.content is not None:
                execution_strategy += chunk.choices[0].delta.content
        
        if reasoning_text:
            print(f"\n🧠 DeepSeek's Reasoning:\n{reasoning_text[:500]}...")
        
        print(f"\n🚀 Execution Strategy from DeepSeek:\n{execution_strategy}")
        return execution_strategy
    
    async def run(self, task: str):
        """Execute task with multi-agent coordination"""
        print("=" * 60)
        print("🤖 Multi-Agent Browser Automation")
        print("   Gemini (Planning) + DeepSeek v3.1 (Reasoning) + Browser Use")
        print("=" * 60)
        print(f"Task: {task}\n")
        
        # Step 1: Plan with Gemini
        print("1️⃣  Planning Phase (Gemini)...")
        plan = self.plan_with_gemini(task)
        
        # Step 2: Strategy with DeepSeek (with reasoning!)
        print("\n2️⃣  Strategy Phase (DeepSeek v3.1 with Thinking)...")
        strategy = self.execute_with_deepseek(task, plan)
        
        # Step 3: Execute with Browser Use
        print("\n3️⃣  Execution Phase (Browser Use)...")
        agent = Agent(
            task=task,
            llm=self.deepseek,  # Use DeepSeek for reasoning during execution
            browser=self.browser,
        )
        
        result = await agent.run()
        print(f"\n✅ Final Result:\n{result}")
        return result

async def main():
    """Run the multi-agent browser automation"""
    
    # Create multi-agent system
    system = MultiAgentBrowser()
    
    # Your task
    task = "Find the top 5 trending repositories on GitHub and tell me their names and star counts"
    
    # Run with coordinated agents
    await system.run(task)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
