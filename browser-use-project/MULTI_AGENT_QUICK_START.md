# 🚀 Multi-Agent Browser Use - Quick Start

## What You Just Got

✅ **example_local_browser.py** - Multi-Agent Browser Automation  
✅ **Gemini** - Planning & Task Breakdown  
✅ **DeepSeek** - Execution & Reasoning  
✅ **Local Chromium** - Browser Control (No Browser Use API key needed!)

---

## ⚡ In 5 Minutes

### Step 1: Get Gemini API Key (Free! 🎁)

```bash
# Go here and click "Create API Key"
https://aistudio.google.com/app/apikeys
```

Update `.env`:
```
GEMINI_API_KEY=your-key-here
```

### Step 2: Get DeepSeek API Key

```bash
# Sign up and create API key
https://platform.deepseek.com
```

Update `.env`:
```
DEEPSEEK_API_KEY=your-key-here
```

### Step 3: Run It!

```bash
cd /Users/omkarpodey/wos/browser-use-project
source .venv/bin/activate
python example_local_browser.py
```

---

## 🎯 What Happens

1. **Gemini plans** the task (breaks it down)
2. **DeepSeek strategizes** (optimizes approach)
3. **Browser Use executes** using DeepSeek's reasoning
4. **Result** is returned to you

All using **your own API keys**. No Browser Use dependency! ✅

---

## 💡 Try This First

Edit `example_local_browser.py` and change the task:

```python
task = "Check the Bitcoin price on Coinbase"
```

Or:
```python
task = "Find the 3 most starred Python projects on GitHub"
```

---

## 📊 Costs

- **Gemini**: Free tier (60 requests/minute)
- **DeepSeek**: ~$0.14 per million tokens (super cheap!)
- **Browser Use Cloud**: Not needed

**Total**: Essentially free to very cheap! 💰

---

## 📁 Files

```
browser-use-project/
├── example_local_browser.py      ← Edit this!
├── MULTI_AGENT_SETUP.md          ← Full documentation
├── .env                          ← Add your API keys
└── ... (other setup files)
```

---

## ❓ Need Help?

### Issue: "GEMINI_API_KEY not found"
→ Update `.env` with your Gemini key

### Issue: "DEEPSEEK_API_KEY not found"
→ Update `.env` with your DeepSeek key

### Issue: "JSON decode error"
→ Normal! Falls back to simple execution

See **MULTI_AGENT_SETUP.md** for more troubleshooting.

---

## 🎓 What Each Agent Does

| Agent | Role | Task |
|-------|------|------|
| **Gemini** | 🧠 Planner | Breaks down complex tasks into steps |
| **DeepSeek** | 🚀 Executor | Reasons through execution, refines strategy |
| **Browser Use** | 🌐 Driver | Controls Chromium, navigates, extracts |

---

## ✨ Key Features

✅ No Browser Use API key needed  
✅ Use your own cost-effective APIs  
✅ Multi-agent coordination  
✅ Flexible model swapping  
✅ Fast & efficient  

---

## 🔥 Next Steps

1. Get your API keys (5 min)
2. Update `.env` file (1 min)
3. Run: `python example_local_browser.py` (2 min)
4. Edit task and experiment! (∞ fun)

**That's it!** 🎉

---

For detailed setup, see **MULTI_AGENT_SETUP.md**
