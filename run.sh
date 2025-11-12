#!/bin/bash
# Launcher script for Financial Planning Assistant

echo "🚀 Starting Financial Planning Assistant..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✓ Python: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Check for configuration
if [ ! -f "config.json" ]; then
    echo ""
    echo "⚠️  No config.json found!"
    echo "   Copy config.json.template to config.json and add your Azure credentials."
    echo "   Or set environment variables for Azure services."
    echo ""
fi

# Launch application
echo ""
echo "✓ Launching application..."
python3 main_app.py
