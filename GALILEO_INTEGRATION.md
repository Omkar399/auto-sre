# 🔭 Galileo Observability Integration

## Overview

Galileo has been fully integrated into the Auto-SRE project for comprehensive LLM observability, monitoring, and evaluation.

**What is Galileo?**
Galileo is an AI observability platform that helps you:
- 📊 Monitor LLM interactions in real-time
- 🔍 Debug AI agent behavior
- 📈 Track performance metrics
- 💰 Optimize costs
- 🎯 Improve accuracy

---

## ✅ Installation Complete

Galileo SDK has been installed in:
- ✅ `/browser-use-project/` 
- ✅ `/bug-hunting-agent/`

**Packages installed:**
- `galileo-sdk` v1.0.1
- `google-genai` (compatible Gemini client)
- `python-dotenv`

---

## 🔑 Configuration

### Environment Variables

The following variables have been added to `.env` files:

```bash
# Galileo Observability Platform
GALILEO_API_KEY=M7i0H4Vg-k45T5gr7VXdh4jdS81luSPI7ALhw50RxME
GALILEO_PROJECT=AutoSRE-BugHunting
GALILEO_LOG_STREAM=MainLogStream
```

**Files updated:**
- `browser-use-project/.env` ✅
- `bug-hunting-agent/.env` ✅

---

## 🚀 Quick Start

### 1. Simple Galileo Demo

Test Galileo logging with a simple example:

```bash
cd /Users/nihalnihalani/Desktop/Github/auto-sre/browser-use-project
source .venv/bin/activate
python galileo_demo.py
```

**What it does:**
- Sends a prompt to Gemini
- Logs the interaction to Galileo
- Displays links to view logs

**Expected output:**
```
🔭 Galileo Observability Demo
======================================================================

📊 Initializing Galileo...
   Project: AutoSRE-BugHunting
   Log Stream: MainLogStream
✅ Galileo session started

🧠 Initializing Gemini client...
✅ Gemini client ready

💭 Sending prompt to gemini-2.0-flash-exp...
   User: Describe Galileo

======================================================================
✨ Response from Gemini:
======================================================================

[Gemini's response about Galileo...]

======================================================================
🚀 GALILEO LOG INFORMATION:
======================================================================
🔗 Project   : https://console.getgalileo.ai/project/[project-id]
📝 Log Stream: https://console.getgalileo.ai/project/[project-id]/log-streams/[stream-id]

✅ Interaction logged successfully to Galileo!
   View your logs at the URLs above.
```

---

### 2. Bug Hunting with Galileo

Run the enhanced bug hunting agent with full observability:

```bash
cd /Users/nihalnihalani/Desktop/Github/auto-sre/browser-use-project
source .venv/bin/activate
python bug_hunting_agent_galileo.py
```

**What gets logged:**
1. 🌐 **Browser reproduction** - Agent actions and observations
2. 🏗️ **Code testing** - Daytona sandbox execution
3. 🧠 **AI analysis** - Gemini's bug investigation
4. ✅ **Fix verification** - Testing suggested solutions

**Benefits:**
- Track entire investigation workflow
- Monitor AI decision-making
- Debug agent failures
- Optimize prompts
- Measure performance

---

## 📊 Features Implemented

### 1. Automatic Trace Creation

Every major operation creates a Galileo trace:

```python
# Example: Browser bug reproduction
logger.start_trace(name="Browser Bug Reproduction", input=task)
# ... perform operation ...
logger.conclude(output=result)
```

### 2. LLM Span Logging

All Gemini interactions are logged with detailed metrics:

```python
logger.add_llm_span(
    input=[{"role": "system", "content": system_prompt},
           {"role": "user", "content": user_prompt}],
    output=response.text,
    model="gemini-2.0-flash-exp",
    num_input_tokens=usage_metadata.prompt_token_count,
    num_output_tokens=usage_metadata.candidates_token_count,
    total_tokens=usage_metadata.total_token_count,
    duration_ns=duration_ns
)
```

### 3. Hierarchical Traces

Complex workflows are organized hierarchically:

```
Bug Investigation (Main Trace)
├── Browser Bug Reproduction (Sub-trace)
├── Daytona Code Test (Sub-trace)
│   └── LLM Span: Test analysis
├── Gemini Bug Analysis (Sub-trace)
│   └── LLM Span: Root cause identification
└── Fix Verification (Sub-trace)
```

### 4. Rich Metadata

Every log includes:
- **Input/Output** - Full prompts and responses
- **Tokens** - Input, output, and total counts
- **Duration** - Execution time in nanoseconds
- **Model** - Which LLM was used
- **Context** - Investigation phase and purpose

---

## 📁 Files Created

### Core Integration Files

| File | Purpose | Location |
|------|---------|----------|
| `galileo_demo.py` | Simple demo | `browser-use-project/` |
| `bug_hunting_agent_galileo.py` | Full integration | `browser-use-project/` |
| `GALILEO_INTEGRATION.md` | This documentation | Root directory |

### Configuration Updates

| File | Changes | Status |
|------|---------|--------|
| `browser-use-project/.env` | Added Galileo keys | ✅ Updated |
| `bug-hunting-agent/.env` | Added Galileo keys | ✅ Updated |

---

## 🎯 Use Cases

### 1. Debug Agent Failures

When an investigation fails, view in Galileo:
- Exact prompts sent
- LLM responses received
- Where the failure occurred
- Context at failure time

### 2. Optimize Prompts

Compare different prompt versions:
- Response quality
- Token usage
- Latency
- Success rate

### 3. Monitor Costs

Track spending across:
- Different models
- Bug investigations
- Time periods
- Project phases

### 4. Improve Accuracy

Analyze patterns in:
- Successful investigations
- Failed attempts
- Edge cases
- Model behavior

---

## 📖 Code Examples

### Basic Galileo Logging

```python
from datetime import datetime
from google import genai
from google.genai import types
from galileo import galileo_context
from dotenv import load_dotenv

# Load environment
load_dotenv(override=True)

# Initialize Galileo
galileo_context.init(
    project="MyProject",
    log_stream="MyLogStream"
)

logger = galileo_context.get_logger_instance()
logger.start_session()

# Initialize Gemini
client = genai.Client()

# Start trace
logger.start_trace(name="My Operation", input="user question")

# Call LLM
start_time = datetime.now().timestamp() * 1_000_000_000
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Your prompt here"
)
duration = (datetime.now().timestamp() * 1_000_000_000) - start_time

# Log interaction
logger.add_llm_span(
    input=[{"role": "user", "content": "Your prompt"}],
    output=response.text,
    model="gemini-2.0-flash-exp",
    num_input_tokens=response.usage_metadata.prompt_token_count,
    num_output_tokens=response.usage_metadata.candidates_token_count,
    total_tokens=response.usage_metadata.total_token_count,
    duration_ns=duration
)

# Conclude
logger.conclude(output=response.text)
logger.flush()
```

### Integration with Bug Hunter

```python
from bug_hunting_agent_galileo import BugHuntingAgentWithGalileo

# Initialize with Galileo support
agent = BugHuntingAgentWithGalileo(
    daytona_api_key="...",
    gemini_api_key="...",
    galileo_api_key="..."
)

# Investigate bug (automatically logged to Galileo)
report = await agent.investigate_bug(ticket)

# View logs at printed URLs
```

---

## 🔗 Galileo Dashboard

### Accessing Your Logs

After running any script, you'll see output like:

```
🚀 GALILEO LOG INFORMATION:
🔗 Project   : https://console.getgalileo.ai/project/abc123
📝 Log Stream: https://console.getgalileo.ai/project/abc123/log-streams/def456
```

**Click these links to:**
- View all logged interactions
- Analyze token usage
- See response times
- Debug failures
- Export data

### Dashboard Features

1. **Overview**
   - Total requests
   - Token usage
   - Average latency
   - Error rate

2. **Traces**
   - Hierarchical view of operations
   - Drill down into sub-traces
   - View timing diagrams

3. **LLM Spans**
   - Full prompts and responses
   - Token breakdown
   - Model comparison

4. **Analytics**
   - Cost trends
   - Performance metrics
   - Usage patterns

---

## 🧪 Testing

### Test Galileo Integration

```bash
cd /Users/nihalnihalani/Desktop/Github/auto-sre/browser-use-project
source .venv/bin/activate
python galileo_demo.py
```

**Success indicators:**
- ✅ "Galileo session started" message
- ✅ Gemini response received
- ✅ Dashboard URLs displayed
- ✅ Logs visible in Galileo console

### Verify Environment

```bash
# Check if Galileo is installed
python -c "import galileo; print('✅ Galileo installed')"

# Check API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ GALILEO_API_KEY set' if os.getenv('GALILEO_API_KEY') else '❌ Missing key')"
```

---

## 📊 Metrics Tracked

### Automatically Logged

| Metric | Description | Unit |
|--------|-------------|------|
| Input Tokens | Prompt size | tokens |
| Output Tokens | Response size | tokens |
| Total Tokens | Combined | tokens |
| Duration | Execution time | nanoseconds |
| Model | LLM used | string |
| Success | Operation result | boolean |

### Custom Metadata

You can add custom fields:

```python
logger.start_trace(
    name="Custom Operation",
    input="...",
    metadata={
        "bug_severity": "high",
        "ticket_id": "BUG-123",
        "assigned_to": "agent"
    }
)
```

---

## 🎓 Best Practices

### 1. Meaningful Trace Names

❌ Bad: `logger.start_trace(name="trace1", ...)`  
✅ Good: `logger.start_trace(name="Bug Investigation: Login Failure", ...)`

### 2. Complete Context

Include relevant information in traces:

```python
logger.start_trace(
    name=f"Investigating {ticket['title']}",
    input=json.dumps({
        "ticket_id": ticket["id"],
        "severity": ticket["severity"],
        "steps": ticket["steps_to_reproduce"]
    })
)
```

### 3. Error Handling

Always flush logs even on errors:

```python
try:
    # Your code
    logger.conclude(output=result)
finally:
    logger.flush()
```

### 4. Session Management

Start session once per run:

```python
logger.start_session()  # At startup
# ... multiple operations ...
logger.flush()  # At cleanup
```

---

## 🔧 Configuration Options

### Environment Variables

```bash
# Required
GALILEO_API_KEY=your-api-key

# Optional (can also set in code)
GALILEO_PROJECT=MyProject
GALILEO_LOG_STREAM=MyLogStream
GALILEO_CONSOLE_URL=https://console.getgalileo.ai
```

### Programmatic Config

```python
# Custom project/stream
galileo_context.init(
    project="CustomProject",
    log_stream="CustomStream"
)

# Access config
from galileo.config import GalileoPythonConfig
config = GalileoPythonConfig.get()
print(config.console_url)
print(config.api_key)
```

---

## 📈 Performance Impact

Galileo logging is **asynchronous and lightweight**:

- **Overhead:** < 1ms per log entry
- **Network:** Batched uploads
- **Memory:** Minimal buffering
- **CPU:** Negligible impact

**Recommendation:** Keep logging enabled in production for full observability.

---

## 🚨 Troubleshooting

### Issue: "API key not found"

```bash
# Check .env file
cat /Users/nihalnihalani/Desktop/Github/auto-sre/browser-use-project/.env | grep GALILEO

# Verify loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GALILEO_API_KEY'))"
```

### Issue: "Module not found: galileo"

```bash
cd browser-use-project
source .venv/bin/activate
uv pip install galileo-sdk
```

### Issue: Logs not appearing in dashboard

1. Check internet connection
2. Verify API key is valid
3. Ensure `logger.flush()` is called
4. Check console for errors
5. Wait 30 seconds for processing

---

## 🎉 Summary

### What Was Added

✅ **Galileo SDK** installed in 2 projects  
✅ **API keys** configured in .env files  
✅ **Demo script** for testing (`galileo_demo.py`)  
✅ **Enhanced agent** with full logging (`bug_hunting_agent_galileo.py`)  
✅ **Documentation** (this file)

### What You Can Do

1. **Monitor** - Track all LLM interactions
2. **Debug** - See exact prompts and responses
3. **Optimize** - Improve prompts and reduce costs
4. **Analyze** - Understand agent behavior
5. **Report** - Share insights with team

### Next Steps

1. Run `python galileo_demo.py` to test
2. Check dashboard at printed URLs
3. Run `python bug_hunting_agent_galileo.py` for full demo
4. Customize for your use cases
5. Monitor and optimize!

---

## 🔗 Resources

- **Galileo Console:** https://console.getgalileo.ai
- **Documentation:** https://docs.getgalileo.ai
- **Python SDK:** https://pypi.org/project/galileo-sdk/
- **Support:** support@getgalileo.ai

---

**Galileo observability is now fully integrated! 🔭✨**

Run `python galileo_demo.py` to see it in action!

---

*Last updated: October 18, 2025*
*Galileo SDK version: 1.0.1*

