#!/usr/bin/env python3
"""
Test the fixed Sandbox Tool
Verifies it works with the correct Daytona API
"""

import os
import asyncio
from dotenv import load_dotenv
from sandbox_tool import SandboxTool, create_test_code_for_bug

async def main():
    """Test the sandbox tool"""
    
    # Load environment
    load_dotenv()
    
    api_key = os.getenv("DAYTONA_API_KEY")
    if not api_key:
        print("❌ DAYTONA_API_KEY not set")
        print("   Set it: export DAYTONA_API_KEY='dtn_...'")
        return
    
    print("🧪 Testing Sandbox Tool")
    print("=" * 70)
    print(f"API Key: {api_key[:20]}...")
    print()
    
    # Initialize sandbox tool
    sandbox = SandboxTool(api_key=api_key)
    
    try:
        # Test 1: Simple Python code
        print("\n📝 Test 1: Simple Python Code")
        print("-" * 70)
        result1 = sandbox.run_code(
            code='print("Hello from sandbox!")\nprint(2 + 2)',
            description="Simple math and print test"
        )
        print(f"Success: {result1['success']}")
        
        # Test 2: Bug analysis code
        print("\n📝 Test 2: Bug Analysis Code")
        print("-" * 70)
        suspect_code = """
app.post('/pay', async (req, res) => {
  const { amount, coupon } = req.body;
  const isValidCoupon = coupon === 'FIXME50';
  const discountedAmount = isValidCoupon ? amount * 0.5 : amount;
  const chargeAmount = amount;  // BUG: ignores discount!
  await paymentGateway.charge({amount: chargeAmount});
});
        """
        
        test_code = create_test_code_for_bug(suspect_code)
        result2 = sandbox.run_code(
            code=test_code,
            description="Bug analysis test"
        )
        print(f"Success: {result2['success']}")
        
        # Test 3: JavaScript code
        print("\n📝 Test 3: JavaScript Code")
        print("-" * 70)
        result3 = sandbox.run_code(
            code='console.log("Hello from JS!"); console.log(2 + 2);',
            language="javascript",
            description="Simple JavaScript test"
        )
        print(f"Success: {result3['success']}")
        
    finally:
        # Clean up
        sandbox.cleanup()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
