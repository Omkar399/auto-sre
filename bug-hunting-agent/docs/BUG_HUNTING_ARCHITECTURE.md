# 🐛 Bug Hunting Agent Architecture

## Overview

A multi-agent AI system that combines three powerful tools to automatically investigate and fix bugs:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     User Submits Bug Ticket (Title, Steps, Description)    │
│                                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   Gemini Agent          │
        │   (Orchestrator)        │
        │                         │
        │  • Reads bug ticket     │
        │  • Plans investigation  │
        │  • Interprets results   │
        │  • Suggests fixes       │
        └──┬──┬──┬──┬─────────────┘
           │  │  │  │
    ┌──────┘  │  │  └──────┐
    │         │  │         │
    ▼         ▼  ▼         ▼
┌────────┐ ┌─────────┐ ┌────────┐ ┌─────────┐
│Browser │ │ Daytona │ │ Code   │ │ Report  │
│Use     │ │Sandbox  │ │Analysis│ │Gen      │
├────────┤ ├─────────┤ ├────────┤ ├─────────┤
│• Nav   │ │• Python │ │• Parse │ │• Summary│
│• Click │ │• JS     │ │• Lint  │ │• Root   │
│• Type  │ │• Bash   │ │• Test  │ │ cause   │
│• Screenshot│        │        │ │• Fix    │
└────────┘ └─────────┘ └────────┘ └────────┘
```

## Three Implementation Approaches

### Approach 1: Simple Linear Investigation
**File:** `bug_hunting_agent.py`

Follows a fixed sequence:
1. **Phase 1:** Reproduce bug with browser-use
2. **Phase 2:** Test suspect code with daytona
3. **Phase 3:** Analyze with Gemini
4. **Phase 4:** Verify fix with daytona

**Best for:** Straightforward bugs with clear reproduction steps

```python
agent = BugHuntingAgent(daytona_key, gemini_key)
report = await agent.investigate_bug(ticket)
```

---

### Approach 2: Gemini Tool-Calling (Recommended)
**File:** `bug_hunting_agent_tools.py`

Gemini dynamically decides:
- Which tools to use
- In what order
- What to test
- When to stop

**Best for:** Complex bugs requiring flexible investigation strategy

```python
agent = ToolsAgent(daytona_key, gemini_key)
result = await agent.investigate(ticket)
```

---

### Approach 3: Browser Use as Agent with Tools
**Potential:** Create a browser-use agent that has daytona & code analysis as tools

---

## Component Deep Dive

### 1. Browser Use Integration
**Purpose:** Reproduce UI bugs and gather evidence

```python
from browser_use import Agent, Browser

# Initialize with Gemini as LLM
browser = Browser(headless=False)
agent = Agent(
    task="Navigate to URL and reproduce bug by following these steps...",
    llm=gemini_model,
    browser=browser,
)
result = await agent.run()
```

**Capabilities:**
- Navigate to URLs
- Fill forms and input fields
- Click buttons and interact with elements
- Take screenshots of UI state
- Extract text and data from pages
- Handle multi-step workflows
- Report observations back to agent

**Workflow:**
```
Task Description
      ↓
Browser Agent uses Gemini to:
  1. Understand the task
  2. See current page state
  3. Take action
  4. Evaluate results
  5. Iterate until complete
      ↓
Result (text/observations)
```

---

### 2. Daytona Sandbox Integration
**Purpose:** Execute and test code safely

```python
from daytona import Daytona, DaytonaConfig

config = DaytonaConfig(api_key="your_key")
daytona = Daytona(config)
sandbox = daytona.create()

# Run Python
response = sandbox.process.code_run(code, "python")

# Run JavaScript
response = sandbox.process.code_run(code, "javascript")

# Run Bash
response = sandbox.process.code_run(code, "bash")

sandbox.delete()  # Cleanup
```

**Capabilities:**
- Isolated execution environment
- Multiple language support (Python, JS, Bash)
- Exit code and output capture
- File system operations
- Git operations
- No need to worry about breaking your system

**Use Cases:**
1. **Reproduce the bug in code:**
   ```python
   code = """
   # Simulate the bug scenario
   def submit_form(data):
       # Missing validation
       return True
   
   result = submit_form({})  # Should fail but doesn't
   print(f"Bug: {result}")
   """
   ```

2. **Test potential fixes:**
   ```python
   code = """
   def submit_form(data):
       if not data:  # FIX ADDED
           return False
       return True
   
   assert submit_form({}) == False, "Fix doesn't work"
   print("✅ Fix verified")
   """
   ```

3. **Run test suites:**
   ```python
   code = """
   import subprocess
   result = subprocess.run(['npm', 'test'], capture_output=True)
   print(result.stdout.decode())
   """
   ```

---

### 3. Gemini Agent Orchestration
**Purpose:** Intelligent decision-making and analysis

#### Method A: Direct API Calls
```python
import google.generativeai as genai

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.0-flash')

response = model.generate_content(prompt)
```

#### Method B: Tool Calling (Recommended)
```python
# Define tools Gemini can call
tools = [
    {
        "name": "reproduce_ui_bug",
        "description": "...",
        "input_schema": {...}
    },
    {
        "name": "run_code_test",
        "description": "...",
        "input_schema": {...}
    }
]

model = genai.GenerativeModel('gemini-2.0-flash', tools=tools)

# Gemini will now suggest calling these tools
response = model.generate_content(prompt)

# Check for tool calls and execute them
tool_calls = [p for p in response.content.parts if p.function_call]
for call in tool_calls:
    result = execute_tool(call.name, call.args)
    # Send result back to Gemini
```

**Flow:**
```
Ticket → Gemini reads ticket → Decides which tool to call first
             ↓
        Browser Use reproduces bug → Results back to Gemini
             ↓
        Gemini analyzes, calls Daytona → Code test results
             ↓
        Gemini analyzes all evidence → Suggests fix
             ↓
        Daytona tests fix → Success/Failure
             ↓
        Final report generated
```

---

## Ticket Format

```python
ticket = {
    "title": "Submit button not working on form",
    
    "description": """
    When users fill out the contact form and click submit, 
    nothing happens. No error message, just silent failure.
    """,
    
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
    """
}
```

---

## How to Use

### Setup
```bash
cd /Users/omkarpodey/wos/browser-use-project

# Install dependencies
uv pip install google-generativeai

# Set environment variables
export GEMINI_API_KEY="your-gemini-key"
export DAYTONA_API_KEY="your-daytona-key"
```

### Simple Example (Linear)
```bash
python bug_hunting_agent.py
```

### Advanced Example (Tool-Calling)
```bash
python bug_hunting_agent_tools.py
```

### Integration Example
```python
import asyncio
from bug_hunting_agent import BugHuntingAgent

async def main():
    agent = BugHuntingAgent(daytona_key, gemini_key)
    
    ticket = {
        "title": "Your bug here",
        "description": "...",
        "steps_to_reproduce": "...",
        "target_url": "http://localhost:3000",
        "suspect_code": "..."
    }
    
    report = await agent.investigate_bug(ticket)
    print(report)
    
    agent.cleanup()

asyncio.run(main())
```

---

## Investigation Phases

### Phase 1: Bug Reproduction
**Tool:** Browser Use  
**Goal:** Confirm the bug exists  
**Output:** Screenshots, observations, error messages

```
Browser navigates to URL
    ↓
Follows reproduction steps
    ↓
Takes screenshots at each step
    ↓
Describes what it sees vs expected
    ↓
Confirms if bug reproduced
```

### Phase 2: Code Testing
**Tool:** Daytona  
**Goal:** Understand the bug at code level  
**Output:** Test results, error traces, code behavior

```
Create minimal test case
    ↓
Run in sandbox
    ↓
Capture output and errors
    ↓
Analyze code paths
    ↓
Identify problematic logic
```

### Phase 3: Analysis & Fix
**Tool:** Gemini  
**Goal:** Synthesize evidence and suggest fix  
**Output:** Root cause, fix code, explanation

```
Review all evidence
    ↓
Identify root cause
    ↓
Generate fix
    ↓
Explain why it works
    ↓
Create test case
```

### Phase 4: Verification
**Tool:** Daytona  
**Goal:** Verify fix works  
**Output:** Test results proving fix

```
Apply fix
    ↓
Run test suite
    ↓
Confirm bug gone
    ↓
Check no regressions
```

---

## Investigation Log

Agent tracks all steps in `investigation_log`:

```python
investigation_log = [
    {
        "phase": "browser_reproduction",
        "status": "completed",
        "result": "Bug confirmed: Submit button not responding"
    },
    {
        "phase": "code_testing",
        "test": "Testing submit_form function",
        "exit_code": 0,
    },
    {
        "phase": "code_testing",
        "test": "Testing with fix applied",
        "exit_code": 0,
    },
    # ... more entries
]
```

---

## Tips & Best Practices

### For Browser Use
- ✅ Provide clear, detailed reproduction steps
- ✅ Include expected vs actual behavior
- ✅ Use target_url to point to your local app
- ✅ Set headless=False to see browser during debugging

### For Daytona
- ✅ Keep code snippets minimal and focused
- ✅ Include assertions to verify behavior
- ✅ Capture both stdout and stderr
- ✅ Test edge cases, not just happy path

### For Gemini
- ✅ Provide context from both tools
- ✅ Use tool calling for complex decisions
- ✅ Let it decide investigation strategy
- ✅ Include investigation log in prompts

### General
- ✅ Combine multiple tools for better results
- ✅ Let agent iterate based on findings
- ✅ Log everything for debugging
- ✅ Clean up resources (sandbox, browser)

---

## Extension Ideas

### 1. Auto-Fix PR Generation
```python
# Generate a PR with the fix
def generate_pr(fix_code, ticket):
    # Create branch, commit, push
    # Open PR on GitHub
```

### 2. Multi-Browser Testing
```python
# Test on Chrome, Firefox, Safari
for browser_type in ['chromium', 'firefox', 'webkit']:
    # Run reproduction on each
```

### 3. Performance Testing
```python
# Add performance metrics to investigation
def measure_performance(code):
    # Run with timing
    # Report slowdowns
```

### 4. Regression Detection
```python
# Run test suite before and after
# Detect if fix breaks anything else
```

### 5. Interactive Investigation
```python
# Let human developer inspect sandbox
# Pause at breakpoints
# Inspect variables
```

---

## Troubleshooting

### "Chrome/Chromium not found"
```bash
uvx playwright install chromium --with-deps
```

### "Daytona connection error"
- Check API key is set correctly
- Verify network connectivity
- Check Daytona service status

### "Gemini API error"
- Verify API key is valid
- Check quota hasn't been exceeded
- Ensure model name is correct

### "Browser agent getting stuck"
- Add max_iterations limit
- Check if website is responsive
- Try with headless=True

---

## Architecture Comparison

| Feature | Linear | Tool-Calling | Browser-Agent |
|---------|--------|--------------|---------------|
| **Flexibility** | Low | High | Medium |
| **Complexity** | Simple | Medium | High |
| **Decision Making** | Hardcoded | Gemini | Agent |
| **Best For** | Simple bugs | Complex bugs | Integration |
| **Iterations** | Fixed phases | Dynamic | Variable |

---

## Next Steps

1. **Try Linear Agent:** Run `bug_hunting_agent.py`
2. **Try Tool-Calling:** Run `bug_hunting_agent_tools.py`
3. **Customize:** Modify prompts for your domain
4. **Integrate:** Use in your bug tracking system
5. **Deploy:** Run as a service on your CI/CD

Happy bug hunting! 🐛🔍
