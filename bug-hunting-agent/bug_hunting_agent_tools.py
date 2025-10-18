#!/usr/bin/env python3
"""
🐛 Advanced Bug Hunting Agent with Gemini Tool Use
Uses Gemini's native tool-calling to orchestrate browser-use and daytona execution.
"""

import os
import json
import asyncio
from typing import Any
import google.generativeai as genai
from browser_use import Agent, Browser
from daytona import Daytona, DaytonaConfig


class ToolsAgent:
    """Bug hunting agent using Gemini's tool calling feature"""

    def __init__(self, daytona_api_key: str, gemini_api_key: str):
        """Initialize with APIs"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash',
            tools=self._define_tools()
        )
        
        # Initialize components
        self.browser = Browser(headless=False)
        daytona_config = DaytonaConfig(api_key=daytona_api_key)
        self.daytona = Daytona(daytona_config)
        self.sandbox = None
        
        self.investigation_log = []

    def _define_tools(self):
        """Define the tools Gemini can call"""
        from google.generativeai.types import content_types
        
        return [
            {
                "name": "reproduce_ui_bug",
                "description": "Reproduce a UI bug by navigating and performing actions in the browser. Returns observations about the bug.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_url": {
                            "type": "string",
                            "description": "URL to navigate to"
                        },
                        "steps": {
                            "type": "string",
                            "description": "Step-by-step instructions to reproduce the bug"
                        },
                        "expected_behavior": {
                            "type": "string",
                            "description": "What should happen vs what actually happens"
                        }
                    },
                    "required": ["target_url", "steps"]
                }
            },
            {
                "name": "run_code_test",
                "description": "Execute code in an isolated Daytona sandbox to test or debug code. Supports Python, JavaScript, and Bash.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The code to execute"
                        },
                        "language": {
                            "type": "string",
                            "enum": ["python", "javascript", "bash"],
                            "description": "Programming language"
                        },
                        "description": {
                            "type": "string",
                            "description": "What this test is checking"
                        }
                    },
                    "required": ["code", "language"]
                }
            },
            {
                "name": "suggest_fix",
                "description": "Analyze collected evidence and suggest a bug fix with test case",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "bug_analysis": {
                            "type": "string",
                            "description": "Your analysis of the bug based on evidence"
                        },
                        "evidence": {
                            "type": "string",
                            "description": "Summary of evidence collected so far"
                        }
                    },
                    "required": ["bug_analysis"]
                }
            },
            {
                "name": "generate_report",
                "description": "Generate the final investigation report with findings and recommendations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "findings": {
                            "type": "string",
                            "description": "Key findings from investigation"
                        },
                        "root_cause": {
                            "type": "string",
                            "description": "Root cause of the bug"
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["Critical", "High", "Medium", "Low"],
                            "description": "Bug severity"
                        }
                    },
                    "required": ["findings", "root_cause"]
                }
            }
        ]

    async def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute requested tool and return results"""
        
        if tool_name == "reproduce_ui_bug":
            return await self._tool_reproduce_bug(
                tool_input.get("target_url"),
                tool_input.get("steps"),
                tool_input.get("expected_behavior", "")
            )
        
        elif tool_name == "run_code_test":
            return self._tool_run_test(
                tool_input.get("code"),
                tool_input.get("language", "python"),
                tool_input.get("description", "")
            )
        
        elif tool_name == "suggest_fix":
            return self._tool_suggest_fix(
                tool_input.get("bug_analysis"),
                tool_input.get("evidence", "")
            )
        
        elif tool_name == "generate_report":
            return self._tool_generate_report(
                tool_input.get("findings"),
                tool_input.get("root_cause"),
                tool_input.get("severity", "Medium")
            )
        
        else:
            return f"Unknown tool: {tool_name}"

    async def _tool_reproduce_bug(self, target_url: str, steps: str, expected: str) -> str:
        """Tool 1: Browser Use to reproduce bug"""
        print("\n🌐 [TOOL] Reproducing UI Bug with Browser Use...")
        
        task = f"""
Navigate to {target_url} and perform these steps:
{steps}

Expected behavior: {expected}

After completing:
1. Take a screenshot
2. Describe what you observe
3. Confirm if bug is reproduced
        """
        
        try:
            agent = Agent(
                task=task,
                llm=self.model,
                browser=self.browser,
            )
            result = await agent.run()
            
            log_result = {
                "tool": "reproduce_ui_bug",
                "status": "completed",
                "result": str(result),
            }
            self.investigation_log.append(log_result)
            
            return f"✅ Bug reproduction complete:\n{result}"
        except Exception as e:
            return f"❌ Browser error: {str(e)}"

    def _tool_run_test(self, code: str, language: str, description: str) -> str:
        """Tool 2: Daytona code execution"""
        print(f"\n🏗️  [TOOL] Running {language} code in Daytona sandbox...")
        
        if not self.sandbox:
            self.sandbox = self.daytona.create()
            print(f"✅ Sandbox created: {self.sandbox.id}")
        
        try:
            response = self.sandbox.process.code_run(code, language)
            
            log_result = {
                "tool": "run_code_test",
                "language": language,
                "description": description,
                "exit_code": response.exit_code,
            }
            self.investigation_log.append(log_result)
            
            if response.exit_code == 0:
                return f"✅ Test passed:\n{response.result}"
            else:
                return f"❌ Test failed (exit code {response.exit_code}):\n{response.result}"
        except Exception as e:
            return f"❌ Execution error: {str(e)}"

    def _tool_suggest_fix(self, bug_analysis: str, evidence: str) -> str:
        """Tool 3: Suggest fix based on analysis"""
        print("\n🧠 [TOOL] Suggesting fix based on analysis...")
        
        # Use a synchronous call for suggestions
        prompt = f"""
Based on this bug analysis:
{bug_analysis}

Evidence collected:
{evidence}

Investigation log:
{json.dumps(self.investigation_log[-5:], indent=2)}

Provide:
1. Root cause
2. Exact code fix (as Python/JS code snippet)
3. Why this fixes it
4. Test case to verify

Format as JSON.
        """
        
        response = self.model.generate_content(prompt)
        
        try:
            fix_data = json.loads(response.text)
            return f"✅ Fix suggested:\n{json.dumps(fix_data, indent=2)}"
        except:
            return f"✅ Fix suggested:\n{response.text}"

    def _tool_generate_report(self, findings: str, root_cause: str, severity: str = "Medium") -> str:
        """Tool 4: Generate final report"""
        print("\n📊 [TOOL] Generating final investigation report...")
        
        report = {
            "status": "Investigation Complete",
            "findings": findings,
            "root_cause": root_cause,
            "severity": severity,
            "investigation_phases": len(self.investigation_log),
            "log_summary": self.investigation_log,
        }
        
        return f"✅ Report generated:\n{json.dumps(report, indent=2)}"

    async def investigate(self, ticket: dict) -> dict:
        """
        Main investigation loop - Gemini decides which tools to call
        """
        print("\n" + "="*70)
        print("🐛 BUG HUNTING WITH GEMINI TOOL CALLING")
        print("="*70)
        
        # Initial prompt for Gemini
        initial_message = f"""
You are a senior QA engineer investigating a bug report using specialized tools.

BUG TICKET:
Title: {ticket.get('title', 'Unknown')}
Description: {ticket.get('description', '')}
Steps to Reproduce: {ticket.get('steps_to_reproduce', '')}
Target URL: {ticket.get('target_url', 'http://localhost:3000')}
Suspect Code: {ticket.get('suspect_code', 'Not provided')}

Your investigation process:
1. Use 'reproduce_ui_bug' tool to confirm the bug exists
2. Use 'run_code_test' tool to test the suspect code
3. Use 'suggest_fix' tool to propose a solution
4. Use 'generate_report' tool to create final report

Start by reproducing the bug, then decide what to test next based on findings.
Be thorough and systematic.
        """
        
        # Conversation for multi-turn agent interaction
        messages = [{"role": "user", "content": initial_message}]
        
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            print(f"\n▶️  Iteration {iteration + 1}/{max_iterations}")
            
            # Get response from Gemini
            response = await asyncio.to_thread(
                self.model.generate_content,
                messages
            )
            
            # Check if Gemini wants to call tools
            if not response.candidates[0].content.parts:
                print("No response generated")
                break
            
            # Process tool calls if any
            tool_calls = [
                part for part in response.candidates[0].content.parts
                if part.function_call
            ]
            
            if not tool_calls:
                # No more tool calls, investigation complete
                print("\n✅ Investigation complete - Gemini finished analysis")
                
                # Extract final response
                final_response = response.text
                return {
                    "status": "completed",
                    "final_analysis": final_response,
                    "investigation_log": self.investigation_log,
                }
            
            # Execute tool calls
            print(f"📞 Gemini calling {len(tool_calls)} tool(s)...")
            
            for tool_call in tool_calls:
                tool_name = tool_call.function_call.name
                tool_input = dict(tool_call.function_call.args)
                
                print(f"\n   → Executing: {tool_name}")
                print(f"     Input: {json.dumps(tool_input, indent=6)}")
                
                # Execute tool
                tool_result = await self._execute_tool(tool_name, tool_input)
                print(f"     Result: {tool_result[:200]}...")
                
                # Add tool result to conversation
                messages.append({"role": "model", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": f"Tool '{tool_name}' returned:\n{tool_result}"
                })
            
            iteration += 1
        
        return {
            "status": "max_iterations_reached",
            "investigation_log": self.investigation_log,
        }

    def cleanup(self):
        """Clean up resources"""
        if self.sandbox:
            self.sandbox.delete()
            print("✅ Sandbox cleaned up")


async def main():
    """Example usage"""
    
    daytona_api_key = os.getenv("DAYTONA_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not daytona_api_key or not gemini_api_key:
        print("❌ Missing API keys!")
        return
    
    agent = ToolsAgent(daytona_api_key, gemini_api_key)
    
    try:
        ticket = {
            "title": "Form submission fails silently",
            "description": "Contact form doesn't submit when clicking the submit button",
            "steps_to_reproduce": """
1. Go to /contact
2. Fill Name field
3. Fill Email field
4. Fill Message field
5. Click Submit
6. Nothing happens
            """,
            "target_url": "http://localhost:3000",
            "suspect_code": """
function submitForm() {
    if (!validateForm()) return;
    // Missing fetch call!
}
            """
        }
        
        result = await agent.investigate(ticket)
        
        print("\n" + "="*70)
        print("📋 FINAL RESULT")
        print("="*70)
        print(json.dumps(result, indent=2))
        
    finally:
        agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
