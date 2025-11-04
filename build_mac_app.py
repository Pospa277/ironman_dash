"""
Build script for creating standalone Mac application
Creates Ironman Dashboard.app that can be double-clicked to run
"""
import os
import sys
import subprocess
import shutil

def create_mac_app():
    """Create standalone Mac application"""

    print("🍎 Building Ironman Dashboard for macOS...")
    print("=" * 60)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

    # Create build directory
    build_dir = "build_mac"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    print("\n📦 Packaging application...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=Ironman Dashboard",
        "--windowed",
        "--onedir",
        "--icon=app_icon.icns" if os.path.exists("app_icon.icns") else "",
        "--add-data=web/templates:web/templates",
        "--add-data=web/static:web/static",
        "--hidden-import=flask",
        "--hidden-import=werkzeug",
        "--hidden-import=jinja2",
        "--clean",
        "web/app.py"
    ]

    # Remove empty icon arg if no icon exists
    cmd = [arg for arg in cmd if arg]

    try:
        subprocess.check_call(cmd)
        print("\n✅ Build successful!")
        print(f"\n📁 Application created in: dist/Ironman Dashboard.app")
        print("\n🚀 To run: Double-click 'Ironman Dashboard.app' in Finder")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False

def create_simple_launcher():
    """Create simple launcher script for Mac"""

    print("\n🔧 Creating simple launcher...")

    launcher_script = """#!/bin/bash

# Ironman Dashboard Launcher for Mac
# Double-click this file to start the dashboard

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is not installed. Please install Python 3 from python.org or using Homebrew (brew install python3)" buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing Flask..."
    python3 -m pip install flask --user
fi

# Start the application
echo "Starting Ironman Dashboard..."
echo "Opening browser at http://localhost:5000"
echo "Press Ctrl+C to stop the server"

# Open browser after 2 seconds
(sleep 2 && open http://localhost:5000) &

# Run the Flask app
cd "$DIR/web"
python3 app.py
"""

    with open("Start_Ironman_Dashboard.command", "w") as f:
        f.write(launcher_script)

    # Make it executable
    os.chmod("Start_Ironman_Dashboard.command", 0o755)

    print("✅ Launcher created: Start_Ironman_Dashboard.command")
    print("   Just double-click this file to start!")

def create_dmg_installer():
    """Create DMG installer (requires create-dmg tool)"""

    print("\n📀 Creating DMG installer...")

    if not os.path.exists("dist/Ironman Dashboard.app"):
        print("❌ App bundle not found. Build the app first.")
        return False

    # Check if create-dmg is available
    if shutil.which("create-dmg"):
        cmd = [
            "create-dmg",
            "--volname", "Ironman Dashboard",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--app-drop-link", "425", "120",
            "Ironman_Dashboard.dmg",
            "dist/Ironman Dashboard.app"
        ]

        try:
            subprocess.check_call(cmd)
            print("✅ DMG created: Ironman_Dashboard.dmg")
            return True
        except subprocess.CalledProcessError:
            print("❌ DMG creation failed")
            return False
    else:
        print("ℹ️  create-dmg not found. Install with: brew install create-dmg")
        print("   Skipping DMG creation...")
        return False

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║     Ironman Dashboard - Mac App Builder                 ║
╚══════════════════════════════════════════════════════════╝
""")

    print("Choose build option:")
    print("1. Create simple launcher (recommended, easy)")
    print("2. Build standalone .app bundle (advanced)")
    print("3. Build both")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1" or choice == "3":
        create_simple_launcher()

    if choice == "2" or choice == "3":
        if create_mac_app():
            print("\n🎉 Standalone app created!")

            # Ask about DMG
            dmg_choice = input("\nCreate DMG installer? (y/n): ").strip().lower()
            if dmg_choice == "y":
                create_dmg_installer()

    print("\n" + "=" * 60)
    print("✅ Build complete!")
    print("=" * 60)
