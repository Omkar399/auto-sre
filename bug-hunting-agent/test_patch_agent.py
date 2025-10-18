#!/usr/bin/env python3
"""
Test the Bug Hunting Agent against the running Patch Agent app
"""

import asyncio
import os
from bug_hunting_agent import BugHuntingAgent

async def main():
    """Test investigating the Patch Agent bug"""
    
    # Get API keys
    daytona_key = os.getenv("DAYTONA_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not daytona_key:
        print("❌ DAYTONA_API_KEY not set")
        print("   Set it: export DAYTONA_API_KEY='dtn_...'")
        return
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not set")
        print("   Get one: https://aistudio.google.com/app/apikeys")
        print("   Set it: export GEMINI_API_KEY='your-key'")
        return
    
    print("🐛 Bug Hunting Agent - Investigating Patch Agent App")
    print("=" * 70)
    print()
    
    # Create agent
    agent = BugHuntingAgent(daytona_key, gemini_key)
    
    # Define the bug ticket
    ticket = {
        "title": "Coupon Code FIXME50 Not Applied - Charges Full Price Instead of Discount",
        "description": """
User enters coupon code 'FIXME50' on the payment page. 
The frontend UI shows the discounted price ($50.00), but when submit is clicked,
the payment gateway still charges the full amount ($100.00).
This is a critical payment bug causing financial loss.
        """,
        "steps_to_reproduce": """
1. Navigate to http://localhost:5173/
2. Look for payment/checkout form
3. Find the coupon code input field
4. Enter coupon code: FIXME50
5. Click Submit button
6. Observe: Frontend displays $50.00 (50% discount applied)
7. BUT payment processes and charges $100.00 instead of $50.00
        """,
        "target_url": "http://localhost:5173",
        "suspect_code": """
// Backend receives coupon but ignores it when charging
app.post('/pay', async (req, res) => {
  const { amount, coupon } = req.body;
  
  // Coupon validation happens here
  const isValidCoupon = coupon === 'FIXME50';
  const discountedAmount = isValidCoupon ? amount * 0.5 : amount;
  
  // BUG: Still sends original amount to payment gateway
  // Should send discountedAmount instead
  const chargeAmount = amount; // <-- BUG: ignores discount!
  
  await paymentGateway.charge({
    amount: chargeAmount,
    currency: 'USD'
  });
});
        """
    }
    
    print("📋 BUG TICKET:")
    print(f"   Title: {ticket['title']}")
    print(f"   Target: {ticket['target_url']}")
    print()
    
    # Run investigation
    try:
        result = await agent.investigate_bug(ticket)
        
        print()
        print("=" * 70)
        print("✅ INVESTIGATION COMPLETE")
        print("=" * 70)
        print()
        
        # Print phases
        if "phases" in result:
            print("📊 INVESTIGATION PHASES:")
            print(f"   1️⃣  Reproduction: {result['phases'].get('1_reproduction', {}).get('success', False)}")
            print(f"   2️⃣  Testing: {len(result['phases'].get('2_testing', []))} tests run")
            if result['phases'].get('3_analysis', {}).get('success'):
                analysis = result['phases']['3_analysis'].get('analysis', {})
                print(f"   3️⃣  Analysis: {analysis.get('severity', 'Unknown')} severity")
                print()
                print("📝 ROOT CAUSE:")
                print(f"   {analysis.get('root_cause', 'N/A')}")
                print()
                print("🔧 SUGGESTED FIX:")
                print(f"   {analysis.get('suggested_fix', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error during investigation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
