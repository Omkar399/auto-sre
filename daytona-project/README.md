# 🚀 Daytona Setup with UV

This project demonstrates a fully configured Daytona development environment using `uv` as the Python package manager.

## ✅ Setup Status

- ✅ Daytona SDK installed (v0.111.0)
- ✅ Python virtual environment created and managed by `uv`
- ✅ API key configured and tested
- ✅ Sandbox creation and code execution working

## 📦 Project Structure

```
daytona-project/
├── .venv/                 # Virtual environment (managed by uv)
├── hello.py              # Test script demonstrating Daytona usage
├── pyproject.toml        # uv project configuration
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+ (already installed)
- `uv` package manager (already installed: v0.7.12)

### Project is Ready to Use

The project is already fully set up. The following was done:

1. **Initialized project** with `uv init daytona-project`
2. **Added Daytona SDK** with `uv add daytona`
3. **Created test script** to verify connectivity
4. **Tested successfully** with your API key

## 🎯 Quick Start

### Run the Test Script

```bash
cd /Users/omkarpodey/wos/daytona-project
uv run hello.py
```

### Create Your Own Sandbox

```bash
uv run
```

Then in the Python REPL:

```python
from daytona import Daytona, DaytonaConfig

config = DaytonaConfig(api_key="dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8")
daytona = Daytona(config)

# Create a sandbox
sandbox = daytona.create()
print(f"Sandbox ID: {sandbox.id}")

# Run code
response = sandbox.process.code_run('print("Hello from Daytona!")')
print(response.result)

# Clean up
sandbox.delete()
```

## 📚 Dependencies

- **daytona** (0.111.0) - Main Daytona SDK
- **daytona-api-client** - API client for Daytona
- **daytona-api-client-async** - Async API client
- **pydantic** - Data validation and settings management
- **httpx** - HTTP client library
- **python-dotenv** - Environment variable management

See `uv.lock` for the complete dependency tree.

## 🔑 API Key

Your API key is configured in `hello.py`:

```
dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8
```

For production, consider using environment variables:

```bash
export DAYTONA_API_KEY="dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8"
```

Then update your scripts to use:
```python
import os
api_key = os.getenv("DAYTONA_API_KEY")
config = DaytonaConfig(api_key=api_key)
```

## 📖 Resources

- [Daytona Documentation](https://www.daytona.io/docs/en/)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [Daytona SDK Repo](https://github.com/daytonaio/daytona)

## 🛠️ Common Commands

```bash
# Run the test script
uv run hello.py

# Enter Python interactive shell
uv run

# Update dependencies
uv sync

# Add a new package
uv add <package_name>

# Remove a package
uv remove <package_name>

# View installed packages
uv pip list
```

## ✨ What You Can Do With Daytona

Daytona allows you to:

- 🔒 Execute code securely in isolated sandbox environments
- 🌐 Run code on remote machines
- ⚙️ Manage development environments programmatically
- 📦 Build AI-powered development tools
- 🚀 Create CI/CD pipelines
- 💾 Work with file systems and git operations

## 📝 Next Steps

1. Explore the Daytona documentation
2. Build custom scripts for your use case
3. Integrate with your applications
4. Consider using environment variables for sensitive data

Happy coding! 🎉

