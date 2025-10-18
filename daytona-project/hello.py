#!/usr/bin/env python3
"""
Daytona Setup Test Script
Tests the Daytona SDK with your API key
"""

import os
from dotenv import load_dotenv
from daytona import Daytona, DaytonaConfig


def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("DAYTONA_API_KEY")
    if not api_key:
        print("❌ Error: DAYTONA_API_KEY not found in environment!")
        print("   Create a .env file with: DAYTONA_API_KEY=your_key_here")
        return
    
    # Initialize Daytona with API key from environment
    config = DaytonaConfig(api_key=api_key)
    daytona = Daytona(config)
    
    print("✅ Daytona initialized successfully!")
    print(f"📍 Using API Key: {api_key[:20]}..." if len(api_key) > 20 else f"📍 Using API Key: {api_key}")
    
    try:
        # Create a sandbox
        print("\n🚀 Creating sandbox...")
        sandbox = daytona.create()
        print(f"✅ Sandbox created: {sandbox.id}")
        
        # Run a simple Python command
        print("\n⚙️  Running: print('Hello from Daytona!')")
        response = sandbox.process.code_run('print("Hello from Daytona!")')
        
        if response.exit_code != 0:
            print(f"❌ Error (exit code {response.exit_code}): {response.result}")
        else:
            print(f"✅ Output: {response.result}")
        
        # Clean up
        print("\n🧹 Cleaning up...")
        sandbox.delete()
        print("✅ Sandbox deleted successfully!")
        
        print("\n🎉 Daytona setup is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        raise


if __name__ == "__main__":
    main()
