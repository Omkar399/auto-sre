#!/usr/bin/env python3
"""
🐛 Bug Hunting Agent with Browser Use + Daytona + Gemini
Combines UI automation, code testing, and AI reasoning to hunt and fix bugs.
"""

import os
import json
import asyncio
import base64
from pathlib import Path
from typing import Optional
import google.generativeai as genai
from browser_use import Agent, Browser
from daytona import Daytona, DaytonaConfig


class BugHuntingAgent:
    """
    Multi-agent system for bug hunting:
    1. Browser Use: Reproduce UI bugs
    2. Daytona: Test potentially buggy code
    3. Gemini: Orchestrate investigation & suggest fixes
    """

    def __init__(self, daytona_api_key: str, gemini_api_key: str):
        """Initialize all components"""
        self.daytona_api_key = daytona_api_key
        self.gemini_api_key = gemini_api_key
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-flash-lite-latest')
        
        # Initialize browser (local Chromium)
        self.browser = Browser(headless=False)  # Set to True for headless
        
        # Initialize Daytona
        daytona_config = DaytonaConfig(api_key=daytona_api_key)
        self.daytona = Daytona(daytona_config)
        self.sandbox = None
        
        # Store investigation results
        self.investigation_log = []
        self.screenshots = []

    async def reproduce_bug_with_browser(self, bug_description: str, ui_instructions: str, target_url: Optional[str] = None) -> dict:
        """
        Tool 1: Use Browser Use to reproduce the UI bug
        
        Args:
            bug_description: What the bug is
            ui_instructions: Step-by-step instructions from ticket
            target_url: Local app URL (e.g., http://localhost:3000)
        
        Returns:
            dict with screenshot, observations, and bug confirmation
        """
        print("\n" + "="*70)
        print("🌐 TOOL 1: REPRODUCING BUG WITH BROWSER USE")
        print("="*70)
        
        task = f"""
        Reproduce the following bug by following these exact instructions:
        
        Bug Description: {bug_description}
        
        Instructions from ticket:
        {ui_instructions}
        
        {"Target URL: " + target_url if target_url else ""}
        
        After completing the steps:
        1. Take a screenshot showing the bug
        2. Describe what you see
        3. Confirm if the bug is reproduced
        4. List any error messages visible
        """
        
        try:
            # Run browser agent
            agent = Agent(
                task=task,
                llm=self.gemini_model,
                browser=self.browser,
            )
            result = await agent.run()
            
            # Log result
            log_entry = {
                "phase": "browser_reproduction",
                "status": "completed",
                "result": str(result),
            }
            self.investigation_log.append(log_entry)
            
            return {
                "success": True,
                "reproduction_result": str(result),
                "bug_confirmed": True,
            }
        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "bug_confirmed": False,
            }

    def run_code_test_with_daytona(self, code: str, language: str = "python", description: str = "") -> dict:
        """
        Tool 2: Execute code in Daytona sandbox to identify the bug
        
        Args:
            code: Code to execute
            language: python, javascript, or bash
            description: What the test is checking
        
        Returns:
            dict with execution results and any errors
        """
        print("\n" + "="*70)
        print("🏗️  TOOL 2: TESTING CODE WITH DAYTONA")
        print("="*70)
        
        if not self.sandbox:
            print("📍 Creating Daytona sandbox...")
            self.sandbox = self.daytona.create()
            print(f"✅ Sandbox created: {self.sandbox.id}")
        
        print(f"🧪 Test: {description or 'Code execution'}")
        print(f"📝 Language: {language}")
        
        try:
            response = self.sandbox.process.code_run(code, language)
            
            result = {
                "success": response.exit_code == 0,
                "exit_code": response.exit_code,
                "output": response.result,
                "language": language,
                "description": description,
            }
            
            # Log
            log_entry = {
                "phase": "code_testing",
                "test": description,
                "exit_code": response.exit_code,
            }
            self.investigation_log.append(log_entry)
            
            if response.exit_code == 0:
                print(f"✅ Test passed!")
                print(f"Output:\n{response.result}")
            else:
                print(f"❌ Test failed!")
                print(f"Error:\n{response.result}")
            
            return result
        except Exception as e:
            print(f"❌ Daytona execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "exit_code": -1,
            }

    async def analyze_with_gemini(self, context: dict) -> dict:
        """
        Tool 3: Use Gemini to analyze the investigation and suggest fixes
        
        Args:
            context: Dict containing bug_description, reproduction_results, test_results, code_snippet
        
        Returns:
            dict with analysis and suggested fixes
        """
        print("\n" + "="*70)
        print("🧠 TOOL 3: ANALYZING BUG & SUGGESTING FIXES WITH GEMINI")
        print("="*70)
        
        prompt = f"""
        You are a senior software engineer debugging an application bug.
        
        INVESTIGATION CONTEXT:
        {json.dumps(context, indent=2)}
        
        INVESTIGATION LOG:
        {json.dumps(self.investigation_log, indent=2)}
        
        Based on this investigation:
        1. Identify the root cause of the bug
        2. Explain why this bug occurs
        3. Provide the exact code fix
        4. Write a test case to verify the fix
        5. Rate the severity (Critical/High/Medium/Low)
        
        Format your response as JSON with these keys:
        - root_cause: String explaining the root cause
        - why_it_occurs: Technical explanation
        - severity: Critical/High/Medium/Low
        - suggested_fix: Code snippet with the fix
        - fix_explanation: Why this fixes it
        - test_case: Python code to verify the fix
        - additional_notes: Any other important points
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            
            # Try to parse as JSON, fallback to text
            try:
                analysis = json.loads(response.text)
            except json.JSONDecodeError:
                analysis = {"raw_analysis": response.text}
            
            print("📊 Analysis Results:")
            print(json.dumps(analysis, indent=2))
            
            return {
                "success": True,
                "analysis": analysis,
            }
        except Exception as e:
            print(f"❌ Gemini analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def investigate_bug(self, ticket: dict) -> dict:
        """
        Main workflow: Investigate a bug ticket end-to-end
        
        Args:
            ticket: Dict with keys:
                - title: Bug title
                - description: What's broken
                - steps_to_reproduce: How to reproduce
                - target_url: URL of local app
                - suspect_code: Code snippet suspected to be buggy (optional)
        
        Returns:
            Complete investigation report
        """
        print("\n" + "🐛"*35)
        print("🐛 BUG HUNTING INVESTIGATION STARTED")
        print("🐛"*35)
        
        title = ticket.get("title", "Unknown Bug")
        description = ticket.get("description", "")
        steps = ticket.get("steps_to_reproduce", "")
        target_url = ticket.get("target_url", "http://localhost:3000")
        suspect_code = ticket.get("suspect_code", "")
        
        print(f"\n📋 Ticket: {title}")
        print(f"   Description: {description}")
        
        # PHASE 1: Reproduce with browser
        print("\n▶️  PHASE 1: REPRODUCING BUG...")
        browser_result = await self.reproduce_bug_with_browser(
            bug_description=description,
            ui_instructions=steps,
            target_url=target_url,
        )
        
        # PHASE 2: Test the suspected code
        print("\n▶️  PHASE 2: TESTING SUSPECT CODE...")
        test_results = []
        
        if suspect_code:
            # Create a test that demonstrates the bug
            test_code = f"""
# Bug reproduction test
{suspect_code}

# Try to trigger the bug
try:
    # Call the function that should trigger the bug
    result = 1  # Placeholder - user provides actual test
    print(f"Result: {{result}}")
except Exception as e:
    print(f"Error triggered: {{e}}")
"""
            test_result = self.run_code_test_with_daytona(
                code=test_code,
                language="python",
                description="Testing suspected buggy code",
            )
            test_results.append(test_result)
        
        # PHASE 3: Analyze and suggest fix
        print("\n▶️  PHASE 3: ANALYZING & SUGGESTING FIXES...")
        analysis = await self.analyze_with_gemini({
            "ticket_title": title,
            "bug_description": description,
            "reproduction_result": browser_result,
            "test_results": test_results,
            "suspect_code": suspect_code,
        })
        
        # PHASE 4: Test the suggested fix
        if analysis.get("success") and "suggested_fix" in analysis.get("analysis", {}):
            print("\n▶️  PHASE 4: TESTING SUGGESTED FIX...")
            fix_code = analysis["analysis"]["suggested_fix"]
            fix_test = self.run_code_test_with_daytona(
                code=fix_code,
                language="python",
                description="Testing suggested fix",
            )
            test_results.append(fix_test)
        
        # Generate final report
        report = {
            "ticket_title": title,
            "investigation_status": "completed",
            "phases": {
                "1_reproduction": browser_result,
                "2_testing": test_results,
                "3_analysis": analysis,
            },
            "investigation_log": self.investigation_log,
        }
        
        return report

    def cleanup(self):
        """Clean up resources"""
        if self.sandbox:
            print("\n🧹 Cleaning up Daytona sandbox...")
            self.sandbox.delete()
            print("✅ Sandbox deleted")
        
        if self.browser:
            print("🧹 Closing browser...")
            # Browser cleanup happens automatically


async def main():
    """Example: Run the bug hunting agent"""
    
    # Load API keys from environment
    daytona_api_key = os.getenv("DAYTONA_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not daytona_api_key or not gemini_api_key:
        print("❌ Missing API keys!")
        print("Set DAYTONA_API_KEY and GEMINI_API_KEY environment variables")
        return
    
    # Initialize agent
    agent = BugHuntingAgent(daytona_api_key, gemini_api_key)
    
    try:
        # Example ticket
        ticket = {
            "title": "Submit button not working on form",
            "description": "When users fill out the contact form and click submit, nothing happens. No error message, just silent failure.",
            "steps_to_reproduce": """
                1. Navigate to http://localhost:3000/contact
                2. Fill in Name field with 'Test User'
                3. Fill in Email field with 'test@example.com'
                4. Fill in Message field with 'This is a test'
                5. Click Submit button
                6. Observe that nothing happens
            """,
            "target_url": "http://localhost:3000",
            "suspect_code": """
def submit_form(data):
    if not validate_data(data):
        return False
    # Missing: actual submission logic
    return True
            """,
        }
        
        # Run investigation
        report = await agent.investigate_bug(ticket)
        
        # Print report
        print("\n" + "="*70)
        print("📊 INVESTIGATION REPORT")
        print("="*70)
        print(json.dumps(report, indent=2))
        
    finally:
        agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
