# 🤖 Multi-Agent Browser Automation Setup

This setup uses:
- **Gemini** (Google) - Planning & Analysis Agent
- **DeepSeek** - Execution & Reasoning Agent  
- **Browser Use** - Local Chromium Automation

**No Browser Use API key needed!** ✅

---

## 🚀 Quick Start

### 1. Get Your API Keys

**Gemini (Free!):**
1. Go to https://aistudio.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the key
4. Add to `.env`:
   ```
   GEMINI_API_KEY=your-key-here
   ```

**DeepSeek:**
1. Go to https://platform.deepseek.com
2. Sign up/Login
3. Create API key in settings
4. Add to `.env`:
   ```
   DEEPSEEK_API_KEY=your-key-here
   ```

### 2. Run the Example

```bash
cd /Users/omkarpodey/wos/browser-use-project
source .venv/bin/activate
python example_local_browser.py
```

---

## 📋 How It Works

### Execution Flow

```
┌─────────────────────────────────────────┐
│ Your Task                               │
│ "Find top GitHub repos"                 │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────▼────────┐
         │ Gemini (Planner) │
         │ Breaks down task │
         │ Creates plan     │
         └─────────┬────────┘
                   │
         ┌─────────▼──────────┐
         │ DeepSeek (Strategy)│
         │ Refines execution  │
         │ Optimizes approach │
         └─────────┬──────────┘
                   │
         ┌─────────▼───────────────┐
         │ Browser Use (Executor)  │
         │ Uses DeepSeek as LLM    │
         │ Controls Chromium       │
         │ Gets results            │
         └─────────┬───────────────┘
                   │
         ┌─────────▼────────┐
         │ Final Result     │
         │ Return to user   │
         └──────────────────┘
```

### Phase 1: Planning (Gemini)
- Breaks down complex task into steps
- Creates structured execution plan
- Identifies key information to extract

### Phase 2: Strategy (DeepSeek)
- Receives plan from Gemini
- Optimizes execution strategy
- Provides specific browser actions
- Used for final reasoning during execution

### Phase 3: Execution (Browser Use + DeepSeek)
- Browser Use controls Chromium
- DeepSeek provides intelligent reasoning
- Navigation, extraction, analysis
- Returns structured results

---

## 💡 Example Tasks

Try editing the task in `example_local_browser.py`:

```python
task = "Your task here"
```

Examples:

```python
# Search and summarize
task = "Search for 'machine learning' and summarize top 3 results"

# Price comparison
task = "Find the cheapest laptop under $1000 on Amazon"

# Data extraction
task = "Extract all contact emails from techcrunch.com homepage"

# Form filling
task = "Sign up for the newsletter on example.com"

# Analysis
task = "Compare prices of iPhone 15 across 3 retailers"
```

---

## 🔧 Advanced Usage

### Use Gemini Only (No DeepSeek)
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

agent = Agent(
    task="Your task",
    llm=model,
    browser=browser,
)
```

### Use DeepSeek Only (No Gemini)
```python
from openai import OpenAI

deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

agent = Agent(
    task="Your task",
    llm=deepseek,
    browser=browser,
)
```

### Custom Multi-Agent Orchestration

```python
from example_local_browser import MultiAgentBrowser

system = MultiAgentBrowser()
result = await system.run("Your complex task here")
```

---

## 📊 Cost Comparison

| Setup | Gemini | DeepSeek | Total |
|-------|--------|----------|-------|
| Gemini + DeepSeek | Free tier* | ~$0.14/1M tokens | Low |
| Gemini Only | Free tier* | - | Free |
| DeepSeek Only | - | ~$0.14/1M tokens | Very Low |
| Browser Use Cloud | Not needed | Not needed | Paid |

*Gemini has generous free tier (60 requests/minute)

---

## 🚨 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# 1. Get key from https://aistudio.google.com/app/apikeys
# 2. Update .env file
# 3. Make sure .env is in project root
```

### "DEEPSEEK_API_KEY not found"
```bash
# 1. Get key from https://platform.deepseek.com
# 2. Update .env file
# 3. Verify key format (should start with sk-...)
```

### "Rate limit exceeded"
- **Gemini**: 60 requests/minute free tier
- **DeepSeek**: Check your plan limits at https://platform.deepseek.com

### "JSON decode error in Gemini response"
- Gemini sometimes returns non-JSON
- Fallback to simple execution works automatically

---

## 🎯 Why This Multi-Agent Approach?

✅ **Better Planning**: Gemini is excellent at breaking down tasks
✅ **Cost Efficient**: DeepSeek is very affordable (~$0.14 per million tokens)
✅ **Specialized Roles**: Each model excels at different tasks
✅ **No Browser Use Dependency**: Your own API keys, full control
✅ **Flexible**: Easy to swap models

---

## 📚 API Limits

### Gemini Free Tier
- 60 requests per minute
- 1,500 requests per day
- Great for planning/analysis

### DeepSeek
- Depends on your plan
- Very competitive pricing
- Check https://platform.deepseek.com/account/api_keys

---

## 🔄 Switching to Different Models

### Use Claude instead of DeepSeek:
```python
from anthropic import Anthropic

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
agent = Agent(
    task="Your task",
    llm=anthropic,
    browser=browser,
)
```

### Use GPT-4 for execution:
```python
from openai import OpenAI

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
agent = Agent(
    task="Your task",
    llm=openai,
    browser=browser,
)
```

---

## ✨ Next Steps

1. ✅ Get Gemini API key (free)
2. ✅ Get DeepSeek API key (affordable)
3. ✅ Update `.env` file
4. ✅ Run: `python example_local_browser.py`
5. ✅ Edit task and experiment!

---

**Enjoy multi-agent browser automation!** 🚀
