#!/usr/bin/env python3
"""
Gmail Reader with Direct Playwright + Your Own APIs
- Gemini: Planning and analysis
- DeepSeek v3.1: Execution reasoning
- Playwright: Direct browser control
NO Browser Use wrapper - pure control!
"""

import asyncio
import json
import os
from playwright.async_api import async_playwright
from openai import OpenAI
import google.generativeai as genai

# Load your own APIs
GEMINI_KEY = "AIzaSyAl_k3SccXBoeS1MuxeZHw961Skk1R51lQ"
NVIDIA_KEY = "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"

def init_gemini():
    """Initialize Gemini for planning"""
    genai.configure(api_key=GEMINI_KEY)
    return genai.GenerativeModel('gemini-2.0-flash')

def init_deepseek():
    """Initialize DeepSeek v3.1 via NVIDIA"""
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_KEY
    )

async def gmail_reader():
    """Read Gmail using Playwright + your APIs"""
    
    print("=" * 70)
    print("📧 Gmail Reader - Direct Control")
    print("=" * 70)
    print()
    
    # Initialize your APIs
    print("🧠 Initializing Gemini...")
    gemini = init_gemini()
    print("✅ Gemini ready")
    
    print("🚀 Initializing DeepSeek v3.1...")
    deepseek = init_deepseek()
    print("✅ DeepSeek ready")
    print()
    
    # Use Playwright directly
    print("🌐 Opening browser with Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser!
        page = await browser.new_page()
        print("✅ Browser opened (visible window)")
        print()
        
        # Step 1: Get plan from Gemini
        print("1️⃣  Getting plan from Gemini...")
        print("-" * 70)
        gemini_prompt = """
        Plan these steps to read the latest Gmail email:
        1. Navigate to gmail.com
        2. Wait for page to load
        3. Check if logged in
        4. Find the latest email
        5. Read sender, subject, and preview
        
        Give me step-by-step instructions.
        """
        
        plan_response = gemini.generate_content(gemini_prompt)
        plan = plan_response.text
        print(plan)
        print()
        
        # Step 2: Get strategy from DeepSeek
        print("2️⃣  Getting strategy from DeepSeek...")
        print("-" * 70)
        print("💭 DeepSeek analyzing...\n")
        
        deepseek_prompt = f"""
        Given this plan for Gmail automation:
        {plan}
        
        Provide specific CSS selectors or xpaths for:
        - Email list container
        - First email subject
        - First email sender
        - First email preview text
        
        Also suggest wait times and strategies.
        """
        
        deepseek_response = deepseek.chat.completions.create(
            model="deepseek-ai/deepseek-v3.1",
            messages=[{"role": "user", "content": deepseek_prompt}],
            temperature=0.2,
            max_tokens=1024,
        )
        
        strategy = deepseek_response.choices[0].message.content
        print(f"🚀 Strategy:\n{strategy}\n")
        
        # Step 3: Execute with Playwright
        print("3️⃣  Executing with Playwright...")
        print("-" * 70)
        print("⏳ Opening Gmail...")
        
        try:
            # Navigate to Gmail
            await page.goto("https://mail.google.com", wait_until="networkidle")
            print("✅ Loaded Gmail")
            
            # Wait a moment for page to settle
            await page.wait_for_timeout(2000)
            
            # Take screenshot to see what we have
            print("📸 Taking screenshot...")
            await page.screenshot(path="gmail_screenshot.png")
            print("✅ Screenshot saved: gmail_screenshot.png")
            
            # Try to get email data
            print("\n📧 Looking for emails...")
            
            # Try multiple selectors for first email
            email_selectors = [
                '[data-thread-id]',
                '[role="main"] [data-draggable-id]',
                'div[data-thread-id]',
                '[data-message-id]',
            ]
            
            email_found = False
            for selector in email_selectors:
                try:
                    emails = await page.locator(selector).all()
                    if emails:
                        print(f"✅ Found {len(emails)} emails using selector: {selector}")
                        email_found = True
                        
                        # Get first email details
                        first_email = emails[0]
                        text = await first_email.text_content()
                        print(f"\n📧 First Email Content:\n{text[:500]}")
                        break
                except:
                    continue
            
            if not email_found:
                print("📝 No emails found with standard selectors")
                print("   (You may need to log in to Gmail)")
                print(f"\n   Page title: {await page.title()}")
                print(f"   Current URL: {page.url}")
            
            print("\n" + "=" * 70)
            print("✅ Gmail page open in browser (keep it open to inspect)")
            print("=" * 70)
            print("\n💡 Next: Manually inspect the page or enhance selectors")
            
            # Keep browser open for manual inspection
            print("\n(Browser will stay open for 30 seconds, then close)")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await browser.close()
            print("\n🔚 Browser closed")

if __name__ == "__main__":
    asyncio.run(gmail_reader())
