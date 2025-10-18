#!/usr/bin/env python3
"""Quick test for NVIDIA DeepSeek API key"""

import os
from openai import OpenAI

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    print("❌ NVIDIA_API_KEY not found in environment!")
    exit(1)

print(f"✅ Found NVIDIA_API_KEY: {api_key[:20]}...")

try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    print("\n🔄 Testing DeepSeek v3.1 API...")
    
    response = client.chat.completions.create(
        model="deepseek-ai/deepseek-v3.1",
        messages=[{"role": "user", "content": "Say 'Hello from DeepSeek!' and nothing else."}],
        temperature=0.2,
        max_tokens=100,
    )
    
    print(f"\n✅ API Response successful!")
    print(f"Model: {response.model}")
    print(f"Message: {response.choices[0].message.content}")
    print(f"\n🎉 NVIDIA DeepSeek key is working!")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"Details: {str(e)}")
    exit(1)
