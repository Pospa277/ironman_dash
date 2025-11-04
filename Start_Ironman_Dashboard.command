#!/bin/bash

# Ironman Dashboard Launcher for Mac
# Double-click this file to start the dashboard

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Ironman Dashboard - Starting...                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo ""
    echo "Please install Python 3:"
    echo "  Option 1: Download from https://www.python.org/downloads/"
    echo "  Option 2: Install via Homebrew: brew install python3"
    echo ""
    osascript -e 'display dialog "Python 3 is required. Please install from python.org or use Homebrew." buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null 2>&1; then
    echo "📦 Flask not found. Installing..."
    python3 -m pip install --user flask
    if [ $? -eq 0 ]; then
        echo "✓ Flask installed"
    else
        echo "❌ Failed to install Flask"
        echo "   Try manually: pip3 install flask"
        exit 1
    fi
else
    echo "✓ Flask found"
fi

# Check if port 5000 is available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5000 is already in use (possibly AirPlay Receiver)"
    echo "   You can disable AirPlay Receiver in System Preferences > Sharing"
    echo "   Or the app will try to use port 8080 instead..."

    # Modify app.py temporarily to use port 8080
    PORT=8080
else
    PORT=5000
fi

echo ""
echo "🚀 Starting Ironman Dashboard..."
echo "   Dashboard will open at: http://localhost:$PORT"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Open browser after 3 seconds
(sleep 3 && open "http://localhost:$PORT") &

# Change to web directory and run the app
cd "$DIR/web"

if [ $PORT -eq 8080 ]; then
    # Run on alternative port
    python3 -c "
import sys
sys.path.insert(0, '$DIR')
from web.app import app
print('Starting on port 8080...')
app.run(debug=False, host='0.0.0.0', port=8080)
"
else
    # Run on default port
    python3 app.py
fi
