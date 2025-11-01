#!/bin/bash

# Ironman Dashboard startup script

echo "Starting Ironman Training Dashboard..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Run Flask app
echo "Starting Flask server..."
cd web
python app.py
