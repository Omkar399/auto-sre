# Bug Hunting Agent Architecture

## 🎯 How It Works

The Bug Hunting Agent is a **3-Tool Coordinated System**:

```
┌─────────────────────────────────────────────────────────┐
│ TOOL 1: Browser Use API - Reproduce Bug in UI          │
│ ✓ Navigates to target URL                              │
│ ✓ Follows reproduction steps                            │
│ ✓ Takes screenshots of bug behavior                     │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ TOOL 2: Daytona Sandbox - Test Code Execution          │
│ ✓ Runs test code provided by Gemini                    │
│ ✓ Confirms bug via code analysis                        │
│ ✓ Verifies Gemini's fix works                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ TOOL 3: Gemini - Interactive Analysis Loop             │
│ ✓ Step 1: Writes TEST CODE (Python) to demonstrate bug │
│ ✓ Step 2: Analyzes sandbox output                      │
│ ✓ Step 3: Writes FIX CODE (Python) to resolve bug      │
│ ✓ Step 4: Verifies fix works in sandbox               │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Interactive Loop: Gemini ↔ Sandbox

### Phase 1: Reproduce Bug
```
Browser Use: Navigate to http://localhost:5173
           ↓
           Interact with UI (click, fill forms, etc)
           ↓
           Screenshots show: Bug exists! ✓
```

### Phase 2: Test Suspect Code
```
Gemini writes: "Here's test code that demonstrates the bug"
           ↓
Sandbox runs: Python code analyzing the suspect code logic
           ↓
Output: "✗ BUG CONFIRMED: Variable 'amount' is used instead of 'discountedAmount'"
```

### Phase 3: Analyze & Suggest Fix
```
Gemini analyzes: "The test output shows X is happening"
           ↓
Gemini writes: "Here's the fix that resolves it"
           ↓
Sandbox runs: Python code with the fixed logic
           ↓
Output: "✓ FIX VERIFIED: Discount now applied correctly"
```

## 📝 Code Translation

**Why Python for Sandbox?**

The Daytona sandbox has issues running JavaScript/other languages directly. So we use this approach:

1. **Suspect Code** is in JavaScript (or any language):
   ```javascript
   const chargeAmount = amount;  // BUG: ignores discount
   ```

2. **Gemini Converts** to Python logic:
   ```python
   charge_amount = amount  # BUG: ignores discount
   ```

3. **Sandbox Runs** Python test code to demonstrate the bug

4. **Gemini Provides** Python fix:
   ```python
   charge_amount = discounted_amount  # FIXED
   ```

## 🛠 Key Components

### `bug_hunting_agent.py`
- **`reproduce_bug_with_browser()`** - Tool 1: Browser automation
- **`run_code_test_with_daytona()`** - Tool 2: Code execution
- **`analyze_with_gemini()`** - Tool 3: Interactive analysis + sandbox loop
- **`_detect_code_language()`** - Detects suspect code language

### `sandbox_tool.py`
- **`SandboxTool` class** - Wraps Daytona API
- **`create_sandbox()`** - Creates isolated execution environment
- **`run_code()`** - Executes code in sandbox
- **`cleanup()`** - Closes sandbox

### `bug_reproduction_tool.py`
- **`BugReproductionTool` class** - Browser Use API wrapper
- **`reproduce()`** - Navigates and reproduces UI bugs

## 📊 Example Flow

```
User reports: "Coupon FIXME50 doesn't apply - still charges $100"
                         ↓
Browser Use: Navigates, applies coupon, confirms UI shows $50
                         ↓
Gemini: "The bug is in the backend. Let me write a test..."
                         ↓
Sandbox: Runs test, finds "chargeAmount = amount" bug
                         ↓
Gemini: "The fix is to use discountedAmount instead"
                         ↓
Sandbox: Runs fix, confirms "charge_amount = discounted_amount" works ✓
                         ↓
REPORT: Root cause identified + Fix verified!
```

## ✅ What Gets Verified

1. **Bug Reproduction** - Browser Use confirms UI behavior
2. **Bug Analysis** - Sandbox confirms code contains bug pattern
3. **Fix Correctness** - Sandbox confirms fix works

---

**Next Steps:** Run `test_patch_agent.py` to see it in action!
