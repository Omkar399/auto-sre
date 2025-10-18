# 🚀 Quick Start: Bug Hunting Agent

## 5-Minute Setup

### 1. Install Gemini API Package
```bash
cd /Users/omkarpodey/wos/browser-use-project
uv pip install google-generativeai
```

### 2. Get API Keys
- **Gemini API Key:** https://aistudio.google.com/app/apikeys
- **Daytona API Key:** Already have it (dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8)

### 3. Set Environment Variables
```bash
export GEMINI_API_KEY="your-gemini-key-here"
export DAYTONA_API_KEY="dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8"
```

Or add to `.env`:
```
GEMINI_API_KEY=your-key
DAYTONA_API_KEY=dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8
```

---

## Which Version to Use?

### Option A: Simple & Linear (Start Here!) 📌
**File:** `bug_hunting_agent.py`

Best for getting started. Follows predictable phases.

```bash
python bug_hunting_agent.py
```

**Workflow:**
```
1. Reproduce bug (Browser Use)
2. Test code (Daytona)
3. Analyze & suggest fix (Gemini)
4. Verify fix works (Daytona)
```

**Example:** 
- ✅ Simple bug with clear steps
- ✅ You have suspect code
- ✅ Want predictable process

---

### Option B: Smart & Flexible (Recommended!) ⭐
**File:** `bug_hunting_agent_tools.py`

Gemini decides what to do next based on findings.

```bash
python bug_hunting_agent_tools.py
```

**Workflow:**
```
Gemini reads ticket
    ↓
Decides which tool to use (Browser/Daytona/Analysis)
    ↓
Executes tool
    ↓
Evaluates results
    ↓
Decides next step
    ↓
Repeats until investigation complete
```

**Example:**
- ✅ Complex bug with unclear cause
- ✅ Need flexible investigation
- ✅ Prefer AI to decide strategy

---

## Custom Usage

### Use in Your Own Script

```python
import asyncio
import os
from bug_hunting_agent import BugHuntingAgent

async def main():
    # Get API keys
    daytona_key = os.getenv("DAYTONA_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    # Create agent
    agent = BugHuntingAgent(daytona_key, gemini_key)
    
    try:
        # Define your bug ticket
        ticket = {
            "title": "Login button doesn't work",
            "description": "Users cannot log in using the login button",
            "steps_to_reproduce": """
                1. Go to http://localhost:3000/login
                2. Enter email: test@example.com
                3. Enter password: password123
                4. Click Login button
                5. Nothing happens
            """,
            "target_url": "http://localhost:3000",
            "suspect_code": """
            async function handleLogin(email, password) {
                const user = await validateCredentials(email, password);
                // Missing: redirect to dashboard
                return user;
            }
            """
        }
        
        # Investigate the bug
        report = await agent.investigate_bug(ticket)
        
        # Print results
        print("\n✅ Investigation Complete!")
        print(f"Root Cause: {report['phases']['3_analysis']['analysis']['root_cause']}")
        print(f"Suggested Fix: {report['phases']['3_analysis']['analysis']['suggested_fix']}")
        
    finally:
        agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Run It
```bash
python your_script.py
```

---

## Common Ticket Formats

### Backend Bug
```python
ticket = {
    "title": "API endpoint returns 500 error",
    "description": "GET /api/users returns 500 instead of user list",
    "steps_to_reproduce": "curl http://localhost:3000/api/users",
    "target_url": "http://localhost:3000",
    "suspect_code": """
def get_users():
    users = db.query(User)  # Missing .all()
    return users
    """
}
```

### Frontend Bug
```python
ticket = {
    "title": "Modal doesn't close",
    "description": "Close button on modal doesn't work",
    "steps_to_reproduce": """
1. Click 'Open Dialog'
2. See modal appears
3. Click X button
4. Modal stays open
    """,
    "target_url": "http://localhost:3000",
    "suspect_code": """
function closeModal() {
    // Missing: setOpen(false)
    resetForm();
}
    """
}
```

### Integration Bug
```python
ticket = {
    "title": "Payment processing fails",
    "description": "Payment goes through but order not created",
    "steps_to_reproduce": """
1. Add item to cart
2. Checkout
3. Enter payment info
4. Process payment
5. Payment succeeds but no order
    """,
    "target_url": "http://localhost:3000",
    "suspect_code": """
async function processPayment(paymentData) {
    const result = await stripe.processPayment(paymentData);
    // Missing: createOrder(result)
    return result;
}
    """
}
```

---

## Expected Output

### Linear Agent Output
```
==============================================================================
🐛 BUG HUNTING INVESTIGATION STARTED
==============================================================================

📋 Ticket: Login button doesn't work
   Description: Users cannot log in using the login button

▶️  PHASE 1: REPRODUCING BUG...

🌐 TOOL 1: REPRODUCING BUG WITH BROWSER USE
==============================================================================
✅ Bug reproduction complete:
Bug confirmed: Login button not responding, page doesn't navigate after click

▶️  PHASE 2: TESTING SUSPECT CODE...

🏗️  TOOL 2: TESTING CODE WITH DAYTONA
==============================================================================
✅ Test passed!
Output: 
User retrieved successfully but no navigation

▶️  PHASE 3: ANALYZING & SUGGESTING FIXES...

🧠 TOOL 3: ANALYZING BUG & SUGGESTING FIXES WITH GEMINI
==============================================================================
📊 Analysis Results:
{
  "root_cause": "handleLogin function doesn't redirect after auth",
  "why_it_occurs": "Missing redirect call after validateCredentials",
  "severity": "High",
  "suggested_fix": "await router.push('/dashboard');",
  "fix_explanation": "Add navigation after successful login",
  ...
}

==============================================================================
📊 INVESTIGATION REPORT
==============================================================================
{...full report...}
```

### Tool-Calling Agent Output
```
======================================================================
🐛 BUG HUNTING WITH GEMINI TOOL CALLING
======================================================================

▶️  Iteration 1/10
📞 Gemini calling 1 tool(s)...

   → Executing: reproduce_ui_bug
     Input: {
       "target_url": "http://localhost:3000/login",
       "steps": "1. Enter credentials 2. Click login",
       ...
     }
     Result: ✅ Bug reproduction complete: Login button not responding...

▶️  Iteration 2/10
📞 Gemini calling 1 tool(s)...

   → Executing: run_code_test
     Input: {
       "code": "...",
       "language": "python",
       "description": "Testing handleLogin function"
     }
     Result: ✅ Test passed!...

▶️  Iteration 3/10
📞 Gemini calling 1 tool(s)...

   → Executing: suggest_fix
   ...

✅ Investigation complete - Gemini finished analysis

======================================================================
📋 FINAL RESULT
======================================================================
{...analysis...}
```

---

## Tips for Best Results

### 1. Detailed Reproduction Steps
✅ **Good:**
```
1. Navigate to http://localhost:3000/checkout
2. Add item to cart
3. Click 'Proceed to Checkout'
4. Select shipping address
5. Enter payment info
6. Click 'Complete Order'
7. Observe error message appears
```

❌ **Bad:**
```
Order isn't created
```

### 2. Clear Suspect Code
✅ **Good:**
```python
async def create_order(cart_items):
    # Calculate total
    total = sum(item.price for item in cart_items)
    # Missing: save to database
    return {"total": total}
```

❌ **Bad:**
```
Something's wrong in the backend
```

### 3. Accessible Target URL
✅ Local app running on http://localhost:3000  
❌ Production website (too risky!)

---

## Troubleshooting

### "Module not found: google.generativeai"
```bash
uv pip install google-generativeai
```

### "GEMINI_API_KEY not set"
```bash
export GEMINI_API_KEY="your-key-from-aistudio.google.com"
```

### "Browser stuck/not responding"
- Try `headless=False` in code to see what's happening
- Add explicit wait times
- Check if website is loading properly

### "Daytona connection error"
- Verify API key is correct
- Check internet connection
- Daytona status might be down

### "Timeout during investigation"
- Reduce complexity of ticket
- Break into smaller bugs
- Use Option A (Linear) instead of Option B

---

## What Happens Behind the Scenes

```python
# 1. Browser Use Runs
browser_agent = Agent(
    task="Reproduce bug by following these steps...",
    llm=gemini_model,  # Uses Gemini as LLM!
    browser=browser,   # Your local Chromium
)
result = await browser_agent.run()
# → Gets observations, screenshots

# 2. Daytona Executes Code
sandbox = daytona.create()
response = sandbox.process.code_run(code, "python")
# → Runs code in isolated environment
# → Returns output and exit code

# 3. Gemini Analyzes Everything
response = gemini_model.generate_content(
    f"Bug description: {ticket['description']}\n"
    f"Observations: {browser_result}\n"
    f"Test output: {test_result}\n"
    f"Suggest root cause and fix"
)
# → Returns analysis and suggested fix
```

---

## Integration with Your Tools

### Use with GitHub Issues
```python
# Parse issue data
import requests

issue_data = requests.get(
    "https://api.github.com/repos/user/repo/issues/123"
).json()

ticket = {
    "title": issue_data["title"],
    "description": issue_data["body"],
    "steps_to_reproduce": extract_steps(issue_data["body"]),
    "target_url": "http://localhost:3000",
}

result = await agent.investigate_bug(ticket)

# Post result as comment
requests.post(
    f"https://api.github.com/repos/user/repo/issues/123/comments",
    json={"body": f"🐛 Investigation:\n{result['analysis']}"}
)
```

### Use with Slack
```python
from slack_sdk import WebClient

slack = WebClient(token="xoxb-...")

# Get bug from Slack message
message_ts = request.json["event"]["ts"]

# Investigate
result = await agent.investigate_bug(ticket)

# Post results back
slack.chat_postMessage(
    channel="C123456",
    thread_ts=message_ts,
    text=f"✅ Investigation complete!\n{result['analysis']}"
)
```

---

## Next Steps

1. ✅ Set up API keys
2. ✅ Run `python bug_hunting_agent.py`
3. ✅ Customize ticket for your bug
4. ✅ Review generated analysis
5. ✅ Apply suggested fix to your code
6. ✅ Integrate into your workflow

---

Happy bug hunting! 🐛🔍✨
