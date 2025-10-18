#!/usr/bin/env python3
"""
🌐 Bug Reproduction Tool using Browser Use API
Reproduces UI bugs by following step-by-step instructions
Uses: Browser Use Cloud API (simple, clean, effective)
"""

import os
from browser_use import Agent
from typing import Optional
from dotenv import load_dotenv


class BugReproductionTool:
    """Tool to reproduce UI bugs using Browser Use API"""
    
    def __init__(self):
        """Initialize the bug reproduction tool"""
        # Load environment
        load_dotenv("/Users/omkarpodey/wos/browser-use-project/.env")
        
        # Get Browser Use API key
        self.api_key = os.getenv("BROWSER_USE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "❌ BROWSER_USE_API_KEY not found!\n"
                "Add to .env: BROWSER_USE_API_KEY=your-key-here"
            )
    
    async def reproduce(
        self,
        target_url: str,
        bug_description: str,
        steps: str,
        expected_behavior: Optional[str] = None
    ) -> dict:
        """
        Reproduce a bug by following instructions
        
        Args:
            target_url: URL to navigate to
            bug_description: What the bug is
            steps: Step-by-step instructions to reproduce
            expected_behavior: What should happen vs what actually happens
        
        Returns:
            dict with observations and bug confirmation
        """
        
        # Construct the task for the browser agent
        expected_section = f"EXPECTED VS ACTUAL BEHAVIOR:\n{expected_behavior}" if expected_behavior else ""
        
        task = f"""Navigate to {target_url} and reproduce this bug:

BUG DESCRIPTION:
{bug_description}

STEPS TO REPRODUCE:
{steps}

{expected_section}

AFTER FOLLOWING THESE STEPS:
1. Take a screenshot showing the current state
2. Describe what you observe in detail
3. Confirm if the bug is reproduced (YES/NO)
4. List any visible error messages or unexpected behaviors

Be thorough and systematic in your observations.
"""
        
        print("\n" + "="*70)
        print("🌐 REPRODUCING BUG WITH BROWSER USE API")
        print("="*70)
        print(f"Target URL: {target_url}")
        print(f"Bug: {bug_description}")
        print(f"API Key: {self.api_key[:20]}...")
        print()
        
        try:
            # Create agent with Browser Use API key
            agent = Agent(
                task=task,
                api_key=self.api_key,
            )
            
            print("🚀 Executing bug reproduction...")
            result = await agent.run()
            
            return {
                "success": True,
                "observations": str(result),
                "bug_reproduced": True,
                "execution_model": "browser-use",
            }
        
        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "bug_reproduced": False,
            }


# Example usage
async def example():
    """Example: Reproduce a coupon bug"""
    tool = BugReproductionTool()
    
    result = await tool.reproduce(
        target_url="http://localhost:5173",
        bug_description="Coupon code FIXME50 not applying, still charges full price",
        steps="""
1. Navigate to the payment page
2. Find the coupon code input field
3. Enter: FIXME50
4. Click Submit button
5. Check the final amount charged
        """,
        expected_behavior="Should charge $50.00 (50% discount), but charges $100.00 instead"
    )
    
    print("\n📊 Result:")
    print(f"  Success: {result['success']}")
    print(f"  Bug Reproduced: {result.get('bug_reproduced', False)}")
    print(f"  Model: {result.get('execution_model', 'unknown')}")
    print(f"  Observations: {result.get('observations', 'N/A')[:200]}...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
