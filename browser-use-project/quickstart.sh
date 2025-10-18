#!/bin/bash
# Browser Use Quickstart Script

set -e  # Exit on error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Browser Use - Local Setup"
echo "================================"
echo ""

# Check if venv exists
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run this first:"
    echo "  uv venv --python 3.13"
    echo "  uv pip install browser-use playwright"
    exit 1
fi

# Activate venv
echo "📦 Activating virtual environment..."
source "$PROJECT_DIR/.venv/bin/activate"

# Show available commands
echo ""
echo "✅ Virtual environment activated!"
echo ""
echo "Available commands:"
echo "  1. python example_simple.py          - Find GitHub stars (requires API key)"
echo "  2. python example_local_browser.py   - Use local browser (no API key needed)"
echo ""
echo "To use example 1, update your .env file with:"
echo "  BROWSER_USE_API_KEY=your-key-from-browser-use.com"
echo ""
echo "Type your command or 'exit' to quit:"
echo ""
