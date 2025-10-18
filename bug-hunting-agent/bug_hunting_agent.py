#!/usr/bin/env python3
"""
🐛 Bug Hunting Agent with Browser Use + Daytona + Gemini
Combines UI automation, code testing, and AI reasoning to hunt and fix bugs.
"""

import os
import json
import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add browser-use-project to path to import the tool
sys.path.insert(0, str(Path(__file__).parent.parent / "browser-use-project"))
from bug_reproduction_tool import BugReproductionTool

# Import sandbox tool
from sandbox_tool import SandboxTool, create_test_code_for_bug, create_fix_test_code

import google.generativeai as genai
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
        
        # Initialize browser reproduction tool
        self.browser_tool = BugReproductionTool()
        
        # Initialize sandbox tool
        self.sandbox_tool = SandboxTool(api_key=daytona_api_key)
        
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
        
        if not target_url:
            target_url = "http://localhost:3000"
        
        try:
            # Use the dedicated bug reproduction tool
            result = await self.browser_tool.reproduce(
                target_url=target_url,
                bug_description=bug_description,
                steps=ui_instructions,
            )
            
            # Log result
            log_entry = {
                "phase": "browser_reproduction",
                "status": "completed",
                "result": result.get("observations", ""),
            }
            self.investigation_log.append(log_entry)
            
            return result
            
        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "bug_confirmed": False,
            }

    def run_code_test_with_daytona(
        self,
        code: str,
        language: str = "python",
        description: Optional[str] = None,
        show_header: bool = False,
        header_text: Optional[str] = None
    ) -> dict:
        """
        Tool 2: Execute code in Daytona sandbox to identify the bug
        
        Args:
            code: Code to execute
            language: python, javascript, or bash
            description: What the test is checking
            show_header: Whether to show the tool header
            header_text: Custom header text if different from default
        
        Returns:
            dict with execution results and any errors
        """
        if show_header:
            header = header_text or "🏗️  TOOL 2: TESTING CODE WITH DAYTONA"
            print("\n" + "="*70)
            print(header)
            print("="*70)
        
        # Use sandbox tool to run code
        result = self.sandbox_tool.run_code(
            code=code,
            language=language,
            description=description,
        )
        
        # Log the result
        log_entry = {
            "phase": "code_testing",
            "test": description,
            "exit_code": result.get("exit_code"),
            "success": result.get("success"),
        }
        self.investigation_log.append(log_entry)
        
        return result

    async def analyze_with_gemini(self, context: dict) -> dict:
        """
        Tool 3: Interactive analysis loop - Gemini writes code, sandbox executes it
        
        Loop:
        1. Gemini writes TEST CODE to reproduce/demonstrate the bug
        2. Sandbox executes it
        3. Gemini analyzes output and writes FIX CODE
        4. Sandbox executes the fix to verify it works
        
        Args:
            context: Dict containing bug details and reproduction results
        
        Returns:
            dict with analysis, test results, and fix verification
        """
        print("\n" + "="*70)
        print("🧠 TOOL 3: GEMINI ANALYSIS WITH SANDBOX VERIFICATION")
        print("="*70)
        
        prompt = f"""
You are a senior software engineer debugging an application. Your task is to:

1. ANALYZE the bug from this context:
{json.dumps(context, indent=2)}

2. WRITE TEST CODE (Python) that demonstrates the bug's behavior
   - Include print statements showing the bug clearly
   - Show expected vs actual behavior
   - Return this as a code block that can be executed

3. After I tell you the test results, WRITE FIX CODE
   - Show the corrected version
   - Include verification that the fix works
   - Return this as a code block

IMPORTANT: I will execute your code in a sandbox and show you the results.
First, provide ONLY the TEST CODE that demonstrates the bug.
Use this JSON format:

{{
    "phase": "test_code",
    "description": "Brief description of what the test does",
    "code": "Your Python code here",
    "root_cause_hypothesis": "What you think is causing the bug"
}}
"""
        
        print("\n📝 Step 1: Gemini writes test code to demonstrate bug...")
        
        try:
            response = self.gemini_model.generate_content(prompt)
            
            # Parse Gemini's response
            try:
                test_phase = json.loads(response.text)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    test_phase = json.loads(json_match.group())
                else:
                    return {
                        "success": False,
                        "error": "Could not parse Gemini response",
                        "raw_response": response.text,
                    }
            
            print(f"\n🧪 Running test code in sandbox...")
            print(f"   Hypothesis: {test_phase.get('root_cause_hypothesis', 'N/A')}")
            
            # EXECUTE: Run test code in sandbox (no header - we're inside Tool 3)
            test_result = self.run_code_test_with_daytona(
                code=test_phase.get("code", "print('test')"),
                language="python",
                description=test_phase.get("description", "Gemini test code"),
                show_header=False,
            )
            
            print(f"\n✅ Test executed. Output:")
            print(f"   {test_result['output']}")
            
            # NOW: Ask Gemini to write fix code based on results
            print(f"\n💡 Step 2: Gemini analyzes results and writes fix code...")
            
            fix_prompt = f"""
Great! The test confirmed the bug. Here's what we found:

TEST RESULTS:
{test_result['output']}

Now, please write the CORRECTED CODE that fixes this bug.
Include verification code that proves the fix works.

Return ONLY valid JSON in this format:
{{
    "phase": "fix_code",
    "root_cause": "Explanation of what was wrong",
    "why_it_occurs": "Technical reason for the bug",
    "fix_explanation": "How your fix resolves it",
    "code": "Your fixed Python code here",
    "severity": "Critical/High/Medium/Low"
}}
"""
            
            fix_response = self.gemini_model.generate_content(fix_prompt)
            
            # Parse fix response
            try:
                fix_phase = json.loads(fix_response.text)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', fix_response.text, re.DOTALL)
                if json_match:
                    fix_phase = json.loads(json_match.group())
                else:
                    return {
                        "success": False,
                        "error": "Could not parse fix response",
                        "test_phase": test_phase,
                        "test_result": test_result,
                    }
            
            print(f"\n🔧 Root Cause: {fix_phase.get('root_cause', 'N/A')}")
            print(f"   Fix: {fix_phase.get('fix_explanation', 'N/A')}")
            
            # EXECUTE: Run fix code in sandbox (no header - we're inside Tool 3)
            print(f"\n✅ Running fix code in sandbox...")
            fix_result = self.run_code_test_with_daytona(
                code=fix_phase.get("code", "print('fixed')"),
                language="python",
                description="Testing Gemini's fix",
                show_header=False,
            )
            
            print(f"\n✅ Fix executed. Output:")
            print(f"   {fix_result['output']}")
            
            # Compile results
            return {
                "success": True,
                "test_phase": test_phase,
                "test_result": test_result,
                "fix_phase": fix_phase,
                "fix_result": fix_result,
                "analysis": {
                    "root_cause": fix_phase.get("root_cause", "N/A"),
                    "why_it_occurs": fix_phase.get("why_it_occurs", "N/A"),
                    "fix_explanation": fix_phase.get("fix_explanation", "N/A"),
                    "severity": fix_phase.get("severity", "Unknown"),
                    "suggested_fix": fix_phase.get("code", "N/A"),
                }
            }
            
        except Exception as e:
            print(f"❌ Gemini analysis error: {e}")
            import traceback
            traceback.print_exc()
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
            test_code = create_test_code_for_bug(suspect_code)
            test_result = self.run_code_test_with_daytona(
                code=test_code,
                language="python",
                description="Testing suspected buggy code",
                show_header=True,
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
            fix_code = create_fix_test_code(analysis["analysis"]["suggested_fix"])
            fix_test = self.run_code_test_with_daytona(
                code=fix_code,
                language="python",
                description="Testing suggested fix",
                show_header=True,
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
        if self.sandbox_tool:
            self.sandbox_tool.cleanup()
        
        if self.browser_tool:
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
