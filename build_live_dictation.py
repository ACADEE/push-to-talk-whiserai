"""
Build script for Live Dictation App
Compiles the application into a standalone Windows executable
"""

import subprocess
import sys
import os
from pathlib import Path


def build_executable():
    """Build the live dictation app executable using PyInstaller"""

    print("=" * 60)
    print("Building Live Dictation App Executable")
    print("=" * 60)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

    # Application details
    app_name = "LiveDictationApp"
    script_name = "live_dictation_app.py"

    # Build options
    build_options = [
        "pyinstaller",
        "--name", app_name,
        "--onefile",  # Single executable file
        "--windowed",  # No console window (GUI only)
        "--icon", "NONE",  # No icon for now
        "--clean",  # Clean PyInstaller cache
        "--noconfirm",  # Replace output directory without asking
    ]

    # Add hidden imports that PyInstaller might miss
    hidden_imports = [
        "openai",
        "sounddevice",
        "numpy",
        "tkinter",
        "pyautogui",
        "wave",
    ]

    for module in hidden_imports:
        build_options.extend(["--hidden-import", module])

    # Add the script to build
    build_options.append(script_name)

    print("\nBuild configuration:")
    print(f"  - Script: {script_name}")
    print(f"  - Output name: {app_name}")
    print(f"  - Mode: Single file executable")
    print(f"  - Window mode: GUI (no console)")
    print(f"  - Hidden imports: {', '.join(hidden_imports)}")

    print("\n" + "-" * 60)
    print("Starting build process...")
    print("-" * 60 + "\n")

    try:
        # Run PyInstaller
        result = subprocess.run(
            build_options,
            check=True,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        print("\n" + "=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)

        # Check output location
        exe_path = Path("dist") / f"{app_name}.exe"
        if exe_path.exists():
            print(f"\n✓ Executable created: {exe_path.absolute()}")
            print(f"  Size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        else:
            print(f"\n⚠ Warning: Expected executable not found at {exe_path}")

        print("\nBuild artifacts:")
        print(f"  - Executable: dist/{app_name}.exe")
        print(f"  - Build files: build/ (can be deleted)")
        print(f"  - Spec file: {app_name}.spec (can be deleted)")

        print("\nUsage:")
        print(f"  1. Navigate to the dist/ folder")
        print(f"  2. Run {app_name}.exe")
        print(f"  3. Enter your OpenAI API key")
        print(f"  4. Select your microphone")
        print(f"  5. Click 'Enable Microphone'")
        print(f"  6. Open Word/Notepad and start speaking!")

        return True

    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"\nError: {e}")
        if e.output:
            print(f"\nOutput:\n{e.output}")
        if e.stderr:
            print(f"\nError output:\n{e.stderr}")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


def main():
    """Main entry point"""
    print("\nLive Dictation App - Build Script")
    print("=" * 60 + "\n")

    # Check if script exists
    if not Path("live_dictation_app.py").exists():
        print("✗ Error: live_dictation_app.py not found!")
        print("  Make sure you're running this script from the project directory.")
        sys.exit(1)

    # Build
    success = build_executable()

    if success:
        print("\n" + "=" * 60)
        print("Build process completed successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("Build process failed. Please check the errors above.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
