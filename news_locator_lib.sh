#!/bin/bash

# Name of the virtual environment directory
VENV_DIR="venv"

echo "--- Checking Setup ---"

# 1. Check if Virtual Environment exists
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment '$VENV_DIR' found."
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Created virtual environment."
fi

# 2. Activate the Virtual Environment
# We use source so it happens in this shell context
source "$VENV_DIR/bin/activate"

# 3. Check and Install Python Libraries
# We define an array of packages to check
PACKAGES=("newspaper3k" "spacy" "geopy" "requests" "fake-useragent" "aiohttp")

echo "--- Checking Libraries ---"

for pkg in "${PACKAGES[@]}"; do
    # 'pip show' returns exit code 0 if found, 1 if not found
    if pip show "$pkg" &> /dev/null; then
        echo "✅ Library '$pkg' is already installed."
    else
        echo "⬇️  Installing '$pkg'..."
        pip install "$pkg"
    fi
done

# 4. Check and Install spaCy Model
# We use spacy's internal info command to check if the model is linked
echo "--- Checking NLP Model ---"

if python -m spacy info en_core_web_sm &> /dev/null; then
    echo "✅ Model 'en_core_web_sm' is already downloaded."
else
    echo "⬇️  Downloading 'en_core_web_sm'..."
    python -m spacy download en_core_web_sm
fi

echo "--- Setup Complete ---"
echo "To run your scraper, use: python news_locator.py"
