#!/bin/bash

# Get the directory where this script is located
# (This ensures it works even if you call it from a different folder)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Path to the virtual environment
VENV_PATH="$DIR/venv"

# Check if venv exists
if [ -d "$VENV_PATH" ]; then
    # Activate the environment
    source "$VENV_PATH/bin/activate"
    
    # Run the Python script
    echo "🚀 Running News Locator..."
    python "$DIR/news_locator.py"
else
    echo "❌ Error: Virtual environment not found at $VENV_PATH"
    echo "   Run ./news_locator_lib.sh first!"
    exit 1
fi
