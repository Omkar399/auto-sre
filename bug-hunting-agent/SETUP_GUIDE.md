# 🐛 Bug Hunting Agent - Setup & Usage Guide

## 📋 Overview

The Bug Hunting Agent is a three-tool system that automatically:
1. **🌐 Reproduces UI bugs** using Browser Use (from browser-use-project)
2. **🧪 Tests suspect code** using Daytona sandbox
3. **🧠 Analyzes findings** using Google Gemini

## 🏗️ Architecture

```
bug-hunting-agent/
├── bug_hunting_agent.py          ← Main orchestrator
├── test_patch_agent.py           ← Test against patch agent
└── (imports from browser-use-project)

browser-use-project/
├── bug_reproduction_tool.py      ← Browser automation tool ✅
├── example_simple.py
└── example_local_browser.py
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/omkarpodey/wos/bug-hunting-agent
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 2. Set Environment Variables

```bash
export DAYTONA_API_KEY="dtn_..."          # Your Daytona API key
export GEMINI_API_KEY="your-gemini-key"   # Get from https://aistudio.google.com/app/apikeys
export ANTHROPIC_API_KEY="your-claude-key" # For browser automation
```

### 3. Run the Test

```bash
python test_patch_agent.py
```

## 🔧 How It Works

### Phase 1: Browser Reproduction ✅
- Uses `BugReproductionTool` from `browser-use-project/bug_reproduction_tool.py`
- Navigates to target URL
- Follows step-by-step instructions
- Uses Anthropic Claude for browser control
- Returns observations and screenshot

### Phase 2: Code Testing
- Creates Daytona sandbox
- Tests suspect code logic
- Captures output and errors

### Phase 3: Gemini Analysis
- Analyzes all investigation results
- Identifies root cause
- Suggests code fix
- Provides test case
- Rates severity

## 📝 Example: Coupon Bug

**Input:**
```python
ticket = {
    "title": "Coupon Code FIXME50 Not Applied",
    "description": "Frontend shows $50 discount, but charges $100",
    "steps_to_reproduce": """
        1. Navigate to http://localhost:5173/
        2. Enter coupon code: FIXME50
        3. Click Submit
        4. Observe: charges full $100 instead of $50
    """,
    "target_url": "http://localhost:5173",
    "suspect_code": """
        app.post('/pay', async (req, res) => {
          const discountedAmount = isValidCoupon ? amount * 0.5 : amount;
          const chargeAmount = amount; // BUG: should be discountedAmount
          await paymentGateway.charge({ amount: chargeAmount });
        });
    """
}
```

**Output:**
```
Root Cause: Backend ignores discounted amount
Severity: Critical
Suggested Fix: Change `chargeAmount = amount` to `chargeAmount = discountedAmount`
```

## 🛠️ Key Files

| File | Purpose |
|------|---------|
| `bug_hunting_agent.py` | Main orchestrator class |
| `test_patch_agent.py` | Test runner with coupon bug example |
| `../browser-use-project/bug_reproduction_tool.py` | Browser automation (external) |

## ✨ Features

✅ **Fully Autonomous** - No human intervention needed
✅ **Multi-Tool** - Browser, Daytona, Gemini
✅ **Complete Analysis** - Root cause, fix, tests, severity
✅ **Fast** - ~5-10 minutes per bug
✅ **Cost Effective** - ~$0.15 per investigation

## 🔗 Dependencies

- **browser-use** - Browser automation
- **daytona** - Code execution sandbox
- **google-generativeai** - Gemini AI analysis
- **anthropic** - Claude for browser control

## 📊 Investigation Phases

```
🐛 BUG HUNTING INVESTIGATION STARTED

▶️  PHASE 1: REPRODUCING BUG...
    🌐 REPRODUCING BUG WITH BROWSER USE
    → Navigates to URL
    → Follows steps
    → Takes screenshot
    → Returns observations

▶️  PHASE 2: TESTING SUSPECT CODE...
    🏗️  TOOL 2: TESTING CODE WITH DAYTONA
    → Creates sandbox
    → Analyzes code logic
    → Runs tests

▶️  PHASE 3: ANALYZING & SUGGESTING FIXES...
    🧠 TOOL 3: ANALYZING BUG & SUGGESTING FIXES WITH GEMINI
    → Identifies root cause
    → Suggests code fix
    → Provides test case
    → Rates severity

======================================================================
✅ INVESTIGATION COMPLETE
======================================================================
```

## 🎯 Usage Patterns

### Run Full Investigation
```python
import asyncio
from bug_hunting_agent import BugHuntingAgent

async def main():
    agent = BugHuntingAgent(daytona_key, gemini_key)
    report = await agent.investigate_bug(ticket)
    print(report)

asyncio.run(main())
```

### Just Reproduce Bug
```python
from browser_use_project.bug_reproduction_tool import BugReproductionTool

tool = BugReproductionTool()
result = await tool.reproduce(
    target_url="...",
    bug_description="...",
    steps="..."
)
```

## 📞 Support

- Issues? Check your API keys are set
- Browser issues? Ensure Chrome/Chromium is installed
- Need help? Run individual phases separately

---

**Ready to hunt bugs?** 🐛🔍

Run: `python test_patch_agent.py`
