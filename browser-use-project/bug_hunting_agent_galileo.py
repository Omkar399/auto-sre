#!/usr/bin/env python3
"""
🐛 Bug Hunting Agent with Galileo Observability
Combines Browser Use + Daytona + Gemini with full Galileo logging
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

import google.generativeai as genai
from google import genai as genai_client
from google.genai import types
from browser_use import Agent, Browser
from daytona import Daytona, DaytonaConfig
from galileo import galileo_context
from galileo.config import GalileoPythonConfig

# Load environment variables
load_dotenv(override=True)


class BugHuntingAgentWithGalileo:
    """
    Multi-agent bug hunting system with Galileo observability:
    1. Browser Use: Reproduce UI bugs
    2. Daytona: Test potentially buggy code
    3. Gemini: Orchestrate investigation & suggest fixes
    4. Galileo: Log & monitor all LLM interactions
    """

    def __init__(self, daytona_api_key: str, gemini_api_key: str, galileo_api_key: str):
        """Initialize all components including Galileo"""
        self.daytona_api_key = daytona_api_key
        self.gemini_api_key = gemini_api_key
        self.galileo_api_key = galileo_api_key
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.gemini_client = genai_client.Client()
        
        # Initialize Galileo
        project_name = os.getenv("GALILEO_PROJECT", "AutoSRE-BugHunting")
        log_stream_name = os.getenv("GALILEO_LOG_STREAM", "BugInvestigations")
        
        print(f"🔭 Initializing Galileo...")
        print(f"   Project: {project_name}")
        print(f"   Log Stream: {log_stream_name}")
        
        galileo_context.init(
            project=project_name,
            log_stream=log_stream_name
        )
        
        self.logger = galileo_context.get_logger_instance()
        self.logger.start_session()
        print("✅ Galileo logging enabled")
        print()
        
        # Initialize browser (local Chromium)
        self.browser = Browser(headless=False)
        
        # Initialize Daytona
        daytona_config = DaytonaConfig(api_key=daytona_api_key)
        self.daytona = Daytona(daytona_config)
        self.sandbox = None
        
        # Store investigation results
        self.investigation_log = []

    def _log_llm_interaction(self, system_prompt: str, user_prompt: str, response_text: str, 
                            model: str, usage_metadata, duration_ns: float, step_name: str):
        """Helper to log LLM interaction to Galileo"""
        try:
            self.logger.add_llm_span(
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                output=response_text,
                model=model,
                num_input_tokens=usage_metadata.prompt_token_count,
                num_output_tokens=usage_metadata.candidates_token_count,
                total_tokens=usage_metadata.total_token_count,
                duration_ns=duration_ns,
            )
            print(f"   📊 Logged to Galileo: {step_name}")
        except Exception as e:
            print(f"   ⚠️  Galileo logging error: {e}")

    async def reproduce_bug_with_browser(self, bug_description: str, ui_instructions: str, 
                                        target_url: Optional[str] = None) -> dict:
        """Tool 1: Use Browser Use to reproduce the UI bug"""
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
            # Start Galileo trace for this step
            self.logger.start_trace(name="Browser Bug Reproduction", input=task)
            
            # Run browser agent
            agent = Agent(
                task=task,
                llm=self.gemini_model,
                browser=self.browser,
            )
            result = await agent.run()
            
            # Conclude trace
            self.logger.conclude(output=str(result))
            
            print(f"✅ Bug reproduction complete:")
            print(f"{result}")
            
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
            print(f"❌ Browser reproduction error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def run_code_test_with_daytona(self, code: str, language: str = "python", 
                                   description: str = "Code test") -> dict:
        """Tool 2: Test code in Daytona sandbox"""
        print("\n" + "="*70)
        print("🏗️  TOOL 2: TESTING CODE WITH DAYTONA")
        print("="*70)
        
        try:
            # Start Galileo trace
            self.logger.start_trace(
                name=f"Daytona Code Test: {description}", 
                input=code
            )
            
            if not self.sandbox:
                print("🚀 Creating Daytona sandbox...")
                self.sandbox = self.daytona.create()
                print(f"✅ Sandbox created: {self.sandbox.id}")
            
            print(f"⚙️  Running {language} code...")
            response = self.sandbox.process.code_run(code, language)
            
            # Conclude trace
            output = f"Exit code: {response.exit_code}\nOutput: {response.result}"
            self.logger.conclude(output=output)
            
            if response.exit_code != 0:
                print(f"❌ Test failed (exit code {response.exit_code})")
                print(f"Output: {response.result}")
            else:
                print(f"✅ Test passed!")
                print(f"Output: {response.result}")
            
            log_entry = {
                "phase": "code_testing",
                "description": description,
                "exit_code": response.exit_code,
                "output": response.result,
            }
            self.investigation_log.append(log_entry)
            
            return {
                "success": response.exit_code == 0,
                "exit_code": response.exit_code,
                "output": response.result,
            }
        except Exception as e:
            print(f"❌ Daytona test error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def analyze_with_gemini(self, investigation_data: dict) -> dict:
        """Tool 3: Analyze findings and suggest fixes with Gemini + Galileo logging"""
        print("\n" + "="*70)
        print("🧠 TOOL 3: ANALYZING BUG & SUGGESTING FIXES WITH GEMINI")
        print("="*70)
        
        system_prompt = """
You are an expert software debugging assistant. Your task is to analyze bug 
investigation data and provide actionable fixes. Always be specific and provide 
working code examples.
"""
        
        user_prompt = f"""
        Analyze this bug investigation:
        
        Bug Title: {investigation_data.get('ticket_title', 'Unknown')}
        Description: {investigation_data.get('bug_description', '')}
        
        Investigation Findings:
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
            # Start Galileo trace
            self.logger.start_trace(name="Gemini Bug Analysis", input=user_prompt)
            
            # Time the request
            start_time_ns = datetime.now().timestamp() * 1_000_000_000
            
            # Send request to Gemini
            response = self.gemini_client.models.generate_content(
                model="gemini-2.0-flash-exp",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                ),
                contents=user_prompt
            )
            
            duration_ns = (datetime.now().timestamp() * 1_000_000_000) - start_time_ns
            
            # Log to Galileo
            self._log_llm_interaction(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_text=response.text,
                model="gemini-2.0-flash-exp",
                usage_metadata=response.usage_metadata,
                duration_ns=duration_ns,
                step_name="Bug Analysis"
            )
            
            # Conclude trace
            self.logger.conclude(output=response.text)
            
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
        """Main workflow: Investigate a bug ticket end-to-end with Galileo logging"""
        print("\n" + "🐛"*35)
        print("🐛 BUG HUNTING INVESTIGATION STARTED (WITH GALILEO)")
        print("🐛"*35)
        
        title = ticket.get("title", "Unknown Bug")
        description = ticket.get("description", "")
        steps = ticket.get("steps_to_reproduce", "")
        target_url = ticket.get("target_url", "http://localhost:3000")
        suspect_code = ticket.get("suspect_code", "")
        
        print(f"\n📋 Ticket: {title}")
        print(f"   Description: {description}")
        
        # Start main investigation trace
        self.logger.start_trace(
            name=f"Bug Investigation: {title}", 
            input=json.dumps(ticket, indent=2)
        )
        
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
            test_code = f"""
# Bug reproduction test
{suspect_code}

# Try to trigger the bug
try:
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
        
        # Conclude main trace
        self.logger.conclude(output=json.dumps(report, indent=2))
        self.logger.flush()
        
        # Show Galileo links
        config = GalileoPythonConfig.get()
        project_url = f"{config.console_url}project/{self.logger.project_id}"
        log_stream_url = f"{project_url}/log-streams/{self.logger.log_stream_id}"
        
        print("\n" + "="*70)
        print("🔭 GALILEO OBSERVABILITY LINKS:")
        print("="*70)
        print(f"🔗 Project   : {project_url}")
        print(f"📝 Log Stream: {log_stream_url}")
        print()
        print("✅ Full investigation logged to Galileo!")
        
        return report

    def cleanup(self):
        """Clean up resources"""
        if self.sandbox:
            print("\n🧹 Cleaning up Daytona sandbox...")
            self.sandbox.delete()
            print("✅ Sandbox deleted")


async def main():
    """Example: Run the bug hunting agent with Galileo"""
    
    # Load API keys from environment
    daytona_api_key = os.getenv("DAYTONA_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    galileo_api_key = os.getenv("GALILEO_API_KEY")
    
    if not daytona_api_key or not gemini_api_key or not galileo_api_key:
        print("❌ Missing API keys!")
        print("Required: DAYTONA_API_KEY, GEMINI_API_KEY, GALILEO_API_KEY")
        return
    
    # Initialize agent with Galileo
    agent = BugHuntingAgentWithGalileo(daytona_api_key, gemini_api_key, galileo_api_key)
    
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

