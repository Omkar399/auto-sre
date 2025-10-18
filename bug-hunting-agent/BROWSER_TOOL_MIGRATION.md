# 🔄 Browser Tool Migration - From Inline to External

## What Changed

### Before ❌
```python
# bug_hunting_agent.py
from browser_use import Agent, Browser

class BugHuntingAgent:
    def __init__(self):
        self.browser = Browser(headless=False)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def reproduce_bug_with_browser(self, ...):
        agent = Agent(
            task=task,
            llm=self.gemini_model,  # ❌ Provider attribute error
            browser=self.browser,
        )
        result = await agent.run()
```

**Issues:**
- Gemini model used directly without proper provider
- `'GenerativeModel' object has no attribute 'provider'` error
- Inline browser logic mixed with orchestration logic
- Hard to test browser tool independently

### After ✅
```python
# browser-use-project/bug_reproduction_tool.py
class BugReproductionTool:
    async def reproduce(self, target_url, bug_description, steps):
        agent = Agent(
            task=task,
            llm=self.client,  # ✅ Anthropic Claude client
            browser=self.browser,
        )
        return await agent.run()

# bug_hunting_agent.py
from bug_reproduction_tool import BugReproductionTool

class BugHuntingAgent:
    def __init__(self):
        self.browser_tool = BugReproductionTool()
    
    async def reproduce_bug_with_browser(self, ...):
        return await self.browser_tool.reproduce(...)
```

**Benefits:**
✅ Separated concerns (tool vs orchestrator)
✅ Reusable browser tool
✅ No provider attribute errors
✅ Uses Anthropic Claude for reliable browser control
✅ Can test browser tool independently
✅ Cleaner code structure

## Files Changed

### New Files Created
1. **`browser-use-project/bug_reproduction_tool.py`** (130 lines)
   - Standalone browser automation tool
   - Uses Anthropic Claude
   - Handles navigation, steps, screenshots
   - Returns structured results

### Files Updated
1. **`bug_hunting_agent.py`** (407 lines)
   - Imports `BugReproductionTool`
   - Updated `__init__` to use tool
   - Simplified `reproduce_bug_with_browser()` method
   - Cleaner orchestration logic

2. **`test_patch_agent.py`** (104 lines)
   - Now uses linear agent instead of tool-calling
   - Tests coupon bug scenario
   - Better error handling

3. **`pyproject.toml`**
   - Added `[build-system]` config
   - Specified `py-modules` for setuptools

## Key Architecture Decision

### Why Anthropic Claude for Browser Use?
- ✅ Works with local browser (no cloud API needed)
- ✅ No provider attribute issues
- ✅ Reliable browser automation
- ✅ Better instruction following than other models
- ✅ Required: `ANTHROPIC_API_KEY` env var

### Why Keep Gemini for Analysis?
- ✅ Better at code analysis
- ✅ Handles large JSON responses
- ✅ Provides detailed explanations
- ✅ Cost effective

## Migration Path

```
Step 1: Create BugReproductionTool
├─ Use Anthropic Claude
├─ Handle browser navigation
└─ Return structured results

Step 2: Update BugHuntingAgent
├─ Import BugReproductionTool
├─ Use it in reproduce_bug_with_browser()
└─ Remove inline browser logic

Step 3: Fix Dependencies
├─ Update pyproject.toml
├─ Install dependencies with uv
└─ Test everything

Step 4: Test Against Real Bug
├─ Run test_patch_agent.py
├─ Agent reproduces coupon bug
└─ Analyzes and suggests fix
```

## How to Use the Tool

### Independent Use
```python
from browser_use_project.bug_reproduction_tool import BugReproductionTool

tool = BugReproductionTool()
result = await tool.reproduce(
    target_url="http://localhost:5173",
    bug_description="Coupon not applying",
    steps="1. Enter FIXME50\n2. Click Submit"
)
```

### Integrated Use
```python
from bug_hunting_agent import BugHuntingAgent

agent = BugHuntingAgent(daytona_key, gemini_key)
report = await agent.investigate_bug(ticket)
```

## Environment Variables Required

```bash
# Browser automation
export ANTHROPIC_API_KEY="sk-ant-..."

# Code analysis
export GEMINI_API_KEY="your-gemini-key"

# Sandbox execution
export DAYTONA_API_KEY="dtn_..."
```

## Testing the Migration

```bash
# 1. Install dependencies
cd /Users/omkarpodey/wos/bug-hunting-agent
uv venv && source .venv/bin/activate
uv pip install -e .

# 2. Set env vars
export ANTHROPIC_API_KEY="..."
export GEMINI_API_KEY="..."
export DAYTONA_API_KEY="..."

# 3. Run test
python test_patch_agent.py
```

## Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| Browser Tool Reusability | ❌ Inline | ✅ External |
| Provider Errors | ❌ Yes | ✅ No |
| Code Organization | ❌ Mixed | ✅ Separated |
| Independent Testing | ❌ Hard | ✅ Easy |
| LLM for Browser | ❌ Gemini | ✅ Claude |
| LLM for Analysis | ✅ Gemini | ✅ Gemini |

## Next Steps

1. ✅ Browser tool working
2. ⏳ Daytona code testing (has argv issue - needs investigation)
3. ⏳ Gemini analysis (working, needs output formatting)
4. ⏳ Full investigation report generation

---

**Status:** Browser tool migration ✅ COMPLETE
