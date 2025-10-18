#!/usr/bin/env python3
"""
Advanced Daytona Examples
Demonstrates various Daytona sandbox capabilities
"""

import os
from dotenv import load_dotenv
from daytona import Daytona, DaytonaConfig


def python_example(sandbox):
    """Execute Python code in sandbox"""
    print("\n" + "="*60)
    print("🐍 Python Example")
    print("="*60)
    
    code = """
import json
import datetime

data = {
    'timestamp': str(datetime.datetime.now()),
    'message': 'Hello from Daytona sandbox!',
    'numbers': list(range(1, 6))
}

print(json.dumps(data, indent=2))
"""
    
    response = sandbox.process.code_run(code)
    print("Output:")
    print(response.result)


def javascript_example(sandbox):
    """Execute JavaScript code in sandbox"""
    print("\n" + "="*60)
    print("🟨 JavaScript Example")
    print("="*60)
    
    code = """
const data = {
    timestamp: new Date().toISOString(),
    message: 'Hello from Daytona sandbox!',
    numbers: Array.from({length: 5}, (_, i) => i + 1)
};

console.log(JSON.stringify(data, null, 2));
"""
    
    response = sandbox.process.code_run(code, 'javascript')
    print("Output:")
    print(response.result)


def bash_example(sandbox):
    """Execute bash commands in sandbox"""
    print("\n" + "="*60)
    print("🔨 Bash Example")
    print("="*60)
    
    code = """
echo "System Information:"
echo "==================="
uname -a
echo ""
echo "Current Directory:"
pwd
echo ""
echo "Available Python Version:"
python3 --version
"""
    
    response = sandbox.process.code_run(code, 'bash')
    print("Output:")
    print(response.result)


def data_processing_example(sandbox):
    """Demonstrate data processing capabilities"""
    print("\n" + "="*60)
    print("📊 Data Processing Example")
    print("="*60)
    
    code = """
import json

# Simulate API response processing
api_response = {
    "users": [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35},
    ]
}

# Process data
adult_users = [u for u in api_response["users"] if u["age"] >= 25]
avg_age = sum(u["age"] for u in adult_users) / len(adult_users)

result = {
    "total_users": len(api_response["users"]),
    "adult_count": len(adult_users),
    "average_age": round(avg_age, 2),
    "names": [u["name"] for u in adult_users]
}

print(json.dumps(result, indent=2))
"""
    
    response = sandbox.process.code_run(code)
    print("Output:")
    print(response.result)


def main():
    """Run all examples"""
    print("🚀 Daytona Advanced Examples")
    print("="*60)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("DAYTONA_API_KEY")
    if not api_key:
        print("❌ Error: DAYTONA_API_KEY not found in environment!")
        print("   Create a .env file with: DAYTONA_API_KEY=your_key_here")
        return
    
    # Initialize Daytona
    config = DaytonaConfig(api_key=api_key)
    daytona = Daytona(config)
    
    print("✅ Daytona initialized")
    print("📍 Creating sandbox...")
    
    try:
        # Create a sandbox
        sandbox = daytona.create()
        print(f"✅ Sandbox created: {sandbox.id}\n")
        
        # Run examples
        python_example(sandbox)
        javascript_example(sandbox)
        bash_example(sandbox)
        data_processing_example(sandbox)
        
        # Clean up
        print("\n" + "="*60)
        print("🧹 Cleaning up...")
        sandbox.delete()
        print("✅ Sandbox deleted successfully!")
        print("🎉 All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
