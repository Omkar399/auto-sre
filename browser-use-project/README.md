# 🤖 Browser Use - Local Setup

This is a local setup of **Browser Use**, an AI browser automation library that makes websites accessible to AI agents.

**No cloning needed!** We install the package directly from PyPI using `uv`.

## 🚀 Quick Start

### Prerequisites

✅ You already have:
- **Python 3.13.5** installed
- **uv** installed (0.7.12)
- **Chromium** downloaded

### Setup (Already Done!)

```bash
# 1. Created virtual environment
uv venv --python 3.13

# 2. Installed browser-use package
uv pip install browser-use

# 3. Downloaded Chromium
uvx playwright install chromium --with-deps
```

## 📋 Configuration

### Option 1: Use Browser Use Cloud (Recommended for Testing)

Get a free API key with $10 credits:
1. Visit https://browser-use.com
2. Sign up for free credits
3. Copy your API key
4. Update `.env`:
   ```bash
   BROWSER_USE_API_KEY=your-api-key-here
   ```

### Option 2: Use Local Browser (No API Key Needed)

Just run the examples - they'll use your local Chromium automatically!

## 🎯 Running Examples

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Run Simple Example

```bash
python example_simple.py
```

This finds the number of stars on the browser-use GitHub repository.

### Run Local Browser Example

```bash
python example_local_browser.py
```

This uses your local Chromium (no cloud needed).

## 📚 File Structure

```
browser-use-project/
├── .env                      # API configuration (update with your key)
├── .venv/                    # Virtual environment
├── example_simple.py         # Basic example (requires API key)
├── example_local_browser.py  # Local browser example (no API key needed)
└── README.md                 # This file
```

## 💡 How to Use Browser Use

### Basic Pattern

```python
from browser_use import Agent, ChatBrowserUse

agent = Agent(
    task="Your task here",
    llm=ChatBrowserUse(),
)
result = await agent.run()
```

### With Local Browser

```python
from browser_use import Agent, Browser, ChatBrowserUse

browser = Browser(headless=True)  # Local Chromium
agent = Agent(
    task="Your task here",
    llm=ChatBrowserUse(),
    browser=browser,
)
result = await agent.run()
```

## 📖 Task Ideas to Try

- "Search for 'Python machine learning' and summarize the top 3 results"
- "Go to weather.com and tell me tomorrow's forecast for New York"
- "Find the cheapest iPhone 15 on Amazon"
- "Create a GitHub issue with title 'Test' and description 'Test issue'"
- "Fill out this form with sample data: [form URL]"

## 🔧 Installed Packages

Key packages installed:
- `browser-use==0.8.1` - The main library
- `playwright==4.x` - Browser automation
- `anthropic==0.71.0` - Claude API (for ChatBrowserUse)
- Plus 80+ dependencies

## 📚 Resources

- **Official Docs**: https://docs.browser-use.com
- **GitHub**: https://github.com/browser-use/browser-use
- **Examples**: https://github.com/browser-use/browser-use/tree/main/examples
- **Discord**: Join the community on their website

## 🚨 Troubleshooting

### "ChatBrowserUse() requires API key"

Add your API key to `.env`:
```bash
BROWSER_USE_API_KEY=sk-...
```

Or use local browser instead (see examples).

### "Chromium not found"

Re-install:
```bash
source .venv/bin/activate
uvx playwright install chromium --with-deps
```

### "Port 8000 already in use"

The package may run a local server. You can specify a different port.

## ✨ Next Steps

1. **Get API key** from https://browser-use.com (optional, for cloud features)
2. **Update .env** with your key
3. **Run example**: `python example_simple.py`
4. **Create your own task** - modify the examples!

---

**Made with ❤️ using Browser Use** - https://browser-use.com
