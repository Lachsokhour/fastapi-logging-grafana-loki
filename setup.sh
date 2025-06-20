#!/bin/bash

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "✅ Virtual environment created."
fi

# Activate
source .venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
  echo "📦 Dependencies installed from requirements.txt"
else
  echo "⚠️ No requirements.txt found"
fi
