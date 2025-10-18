#!/usr/bin/env python3
"""
Test script to verify all components are set up correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from all project directories
load_dotenv("/Users/nihalnihalani/Desktop/Github/auto-sre/browser-use-project/.env")
load_dotenv("/Users/nihalnihalani/Desktop/Github/auto-sre/bug-hunting-agent/.env")
load_dotenv("/Users/nihalnihalani/Desktop/Github/auto-sre/daytona-project/.env")

def test_env_vars():
    """Test if all required environment variables are set"""
    print("=" * 70)
    print("🔍 Testing Environment Variables")
    print("=" * 70)
    print()
    
    required_vars = {
        "GEMINI_API_KEY": "Gemini AI (Google)",
        "NVIDIA_API_KEY": "NVIDIA DeepSeek v3.1",
        "DAYTONA_API_KEY": "Daytona Sandbox",
        "GALILEO_API_KEY": "Galileo Observability",
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked = f"{value[:20]}..." if len(value) > 20 else value
            print(f"✅ {var}")
            print(f"   {description}: {masked}")
        else:
            print(f"❌ {var}")
            print(f"   {description}: NOT SET")
            all_set = False
        print()
    
    return all_set

def test_imports():
    """Test if all required packages are importable"""
    print("=" * 70)
    print("📦 Testing Package Imports")
    print("=" * 70)
    print()
    
    packages = [
        ("google.generativeai", "Google Gemini AI"),
        ("daytona", "Daytona SDK"),
        ("browser_use", "Browser Use"),
        ("anthropic", "Anthropic Claude"),
        ("openai", "OpenAI/NVIDIA API"),
        ("galileo", "Galileo Observability"),
    ]
    
    all_imported = True
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            print(f"   {description}: Imported successfully")
        except ImportError as e:
            print(f"❌ {package}")
            print(f"   {description}: Failed to import")
            print(f"   Error: {e}")
            all_imported = False
        print()
    
    return all_imported

def test_daytona_connection():
    """Test Daytona API connection"""
    print("=" * 70)
    print("🏗️  Testing Daytona Connection")
    print("=" * 70)
    print()
    
    try:
        from daytona import Daytona, DaytonaConfig
        
        api_key = os.getenv("DAYTONA_API_KEY")
        if not api_key:
            print("❌ DAYTONA_API_KEY not set")
            return False
        
        config = DaytonaConfig(api_key=api_key)
        daytona = Daytona(config)
        
        print("✅ Daytona initialized successfully")
        print(f"   API Key: {api_key[:20]}...")
        print()
        
        # Try to create and delete a sandbox
        print("🚀 Creating test sandbox...")
        sandbox = daytona.create()
        print(f"✅ Sandbox created: {sandbox.id}")
        print()
        
        # Run a simple command
        print("⚙️  Running test command: print('Hello!')")
        response = sandbox.process.code_run('print("Hello from Daytona!")')
        print(f"✅ Output: {response.result}")
        print(f"   Exit code: {response.exit_code}")
        print()
        
        # Clean up
        print("🧹 Cleaning up sandbox...")
        sandbox.delete()
        print("✅ Sandbox deleted successfully")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Daytona test failed: {e}")
        return False

def test_gemini_connection():
    """Test Gemini API connection"""
    print("=" * 70)
    print("🧠 Testing Gemini AI Connection")
    print("=" * 70)
    print()
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not set")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        print("✅ Gemini initialized successfully")
        print(f"   API Key: {api_key[:20]}...")
        print()
        
        # Test a simple generation
        print("💭 Testing generation with prompt: 'Say hello in 5 words'")
        response = model.generate_content("Say hello in 5 words")
        print(f"✅ Response: {response.text}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False

def test_galileo_connection():
    """Test Galileo SDK"""
    print("=" * 70)
    print("🔭 Testing Galileo Observability")
    print("=" * 70)
    print()
    
    try:
        from galileo import galileo_context
        from galileo.config import GalileoPythonConfig
        
        api_key = os.getenv("GALILEO_API_KEY")
        if not api_key:
            print("❌ GALILEO_API_KEY not set")
            return False
        
        print("✅ Galileo SDK imported successfully")
        print(f"   API Key: {api_key[:20]}...")
        print()
        
        # Note: We don't initialize a session in the test to avoid
        # creating unnecessary log entries
        print("✅ Galileo is ready for use")
        print("   Run galileo_demo.py to test full functionality")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Galileo test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🎯" * 35)
    print("🎯 AUTO-SRE PROJECT SETUP TEST")
    print("🎯" * 35)
    print()
    
    results = {}
    
    # Test 1: Environment Variables
    results['env_vars'] = test_env_vars()
    
    # Test 2: Package Imports
    results['imports'] = test_imports()
    
    # Test 3: Daytona Connection
    results['daytona'] = test_daytona_connection()
    
    # Test 4: Gemini Connection
    results['gemini'] = test_gemini_connection()
    
    # Test 5: Galileo SDK
    results['galileo'] = test_galileo_connection()
    
    # Summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print()
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.upper():20s} {status}")
    
    all_passed = all(results.values())
    
    print()
    print("=" * 70)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your setup is ready to use!")
        print("=" * 70)
        print()
        print("🚀 Next steps:")
        print("   1. Test Galileo observability:")
        print("      cd browser-use-project && python galileo_demo.py")
        print()
        print("   2. Run the bug hunting agent:")
        print("      cd browser-use-project && python bug_hunting_agent.py")
        print()
        print("   3. Or try the Daytona sandbox:")
        print("      cd daytona-project && python hello.py")
        print()
        return 0
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())

