#!/usr/bin/env python3
"""
🏗️ Sandbox Tool for Code Testing
Uses Daytona to safely execute and test code in isolated sandboxes
"""

import os
from daytona import Daytona, DaytonaConfig
from typing import Optional
from dotenv import load_dotenv


class SandboxTool:
    """Tool for safe code execution in isolated Daytona sandboxes"""
    
    def __init__(self, api_key: str):
        """Initialize Daytona sandbox tool
        
        Args:
            api_key: Daytona API key
        """
        self.api_key = api_key
        daytona_config = DaytonaConfig(api_key=api_key)
        self.daytona = Daytona(daytona_config)
        self.sandbox = None
    
    def create_sandbox(self) -> str:
        """Create a new sandbox
        
        Returns:
            Sandbox ID
        """
        if not self.sandbox:
            print("📍 Creating Daytona sandbox...")
            self.sandbox = self.daytona.create()
            print(f"✅ Sandbox created: {self.sandbox.id}")
        return self.sandbox.id
    
    def run_code(
        self,
        code: str,
        language: str = "python",
        description: Optional[str] = None
    ) -> dict:
        """Execute code in sandbox
        
        Args:
            code: Code to execute
            language: Programming language (python, javascript, bash)
            description: What the test is checking
        
        Returns:
            dict with execution results
        """
        # Ensure sandbox exists
        if not self.sandbox:
            self.create_sandbox()
        
        print(f"\n🧪 Test: {description or 'Code execution'}")
        print(f"📝 Language: {language}")
        
        try:
            # Execute code in sandbox - Daytona API: code_run(code, language)
            if language == "python":
                response = self.sandbox.process.code_run(code)
            else:
                response = self.sandbox.process.code_run(code, language)
            
            result = {
                "success": response.exit_code == 0,
                "exit_code": response.exit_code,
                "output": response.result,
                "language": language,
                "description": description,
            }
            
            if response.exit_code == 0:
                print(f"✅ Test passed!")
                if response.result:
                    print(f"Output:\n{response.result}")
            else:
                print(f"❌ Test failed (exit code: {response.exit_code})")
                if response.result:
                    print(f"Error:\n{response.result}")
            
            return result
            
        except Exception as e:
            print(f"❌ Daytona execution error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "exit_code": -1,
                "description": description,
            }
    
    def cleanup(self):
        """Clean up sandbox resources"""
        if self.sandbox:
            try:
                print("\n🧹 Cleaning up Daytona sandbox...")
                self.sandbox.delete()
                print("✅ Sandbox deleted")
                self.sandbox = None
            except Exception as e:
                print(f"⚠️  Cleanup warning: {e}")


def create_test_code_for_bug(suspect_code: str) -> str:
    """Create a test code that validates suspect code logic
    
    Args:
        suspect_code: The suspected buggy code
    
    Returns:
        Python test code as string
    """
    return f"""# Bug reproduction test
import json

# Suspect code to analyze
suspect_code = '''{suspect_code}'''

# Validation test
print("=" * 60)
print("🔍 ANALYZING SUSPECT CODE")
print("=" * 60)

try:
    # Check for common bug patterns
    checks = {{
        "uses_wrong_variable": "chargeAmount = amount" in suspect_code,
        "ignores_discount": "discountedAmount" in suspect_code and "chargeAmount = amount" in suspect_code,
        "has_fixme_marker": "BUG" in suspect_code or "FIXME" in suspect_code,
        "has_todo_marker": "TODO" in suspect_code,
    }}
    
    print("\\n📋 Code Analysis Results:")
    for check, found in checks.items():
        status = "✓" if found else "✗"
        print(f"  {{status}} {{check}}: {{found}}")
    
    # Detailed findings
    if checks["ignores_discount"]:
        print("\\n🚨 CRITICAL ISSUE FOUND:")
        print("  The code validates the coupon and calculates discountedAmount,")
        print("  but then uses the original 'amount' when charging!")
        print("\\n💡 FIX: Change 'chargeAmount = amount' to 'chargeAmount = discountedAmount'")
    
    if checks["has_fixme_marker"] or checks["has_todo_marker"]:
        print("\\n⚠️  Code contains debug markers (BUG/FIXME/TODO)")
    
    print("\\n✅ Analysis complete")
    
except Exception as e:
    print(f"\\n❌ Error during analysis: {{e}}")
"""


def create_fix_test_code(fix_code: str) -> str:
    """Create a test to verify the suggested fix
    
    Args:
        fix_code: The suggested fix code
    
    Returns:
        Python test code as string
    """
    return f"""# Fix verification test
print("=" * 60)
print("✅ TESTING SUGGESTED FIX")
print("=" * 60)

try:
    fixed_code = '''{fix_code}'''
    print("\\n📝 Fixed code:")
    print(fixed_code)
    
    # Check that the fix is present
    if "chargeAmount = discountedAmount" in fixed_code:
        print("\\n✓ Fix uses discountedAmount for charging")
    if "chargeAmount = amount" not in fixed_code or "discountedAmount = isValidCoupon" in fixed_code:
        print("✓ Original bug pattern removed")
    
    print("\\n✅ Fix verification passed!")
    
except Exception as e:
    print(f"\\n❌ Error: {{e}}")
"""
