"""
Build script for creating Windows executable
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """Build the Windows executable"""

    print("=" * 60)
    print("Building Whisper Dictation App")
    print("=" * 60)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define build parameters
    app_name = "DictationApp"
    main_script = "dictation_app.py"

    # Build command
    build_command = [
        "pyinstaller",
        "--name", app_name,
        "--windowed",  # No console window
        # Using --onedir (default) instead of --onefile to easily access config files
        "--add-data", "api_key.txt.template;.",  # Include template file
        "--add-data", "custom_dictionary.txt;.",  # Include dictionary file
        "--add-data", "settings.json;.",  # Include settings file
        "--add-data", "translation_prompt.txt;.",  # Include translation prompt
        # Hidden imports for packages PyInstaller might miss
        "--hidden-import", "sounddevice",
        "--hidden-import", "_sounddevice",
        "--hidden-import", "numpy",
        "--hidden-import", "numpy.core._multiarray_umath",
        "--hidden-import", "openai",
        "--hidden-import", "pystray._win32",
        "--hidden-import", "PIL._tkinter_finder",
        "--collect-all", "sounddevice",  # Collect all sounddevice files including binaries
        "--icon=NONE", # No icon (can add later)
        "--clean",     # Clean PyInstaller cache
        main_script
    ]

    print("\nBuilding executable...")
    print(f"Command: {' '.join(build_command)}")
    print()

    # Run PyInstaller
    result = subprocess.run(build_command)

    if result.returncode != 0:
        print("\nBuild failed!")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Build successful!")
    print("=" * 60)

    # The dist folder structure with --onedir:
    # dist/DictationApp/ contains the .exe and all dependencies
    dist_dir = Path("dist")
    app_dir = dist_dir / app_name

    if not app_dir.exists():
        print(f"\nError: Build directory {app_dir} not found!")
        sys.exit(1)

    print(f"\nApplication built in: {app_dir.absolute()}")

    # Copy additional configuration files to the app directory
    files_to_copy = [
        "api_key.txt.template",
        "custom_dictionary.txt",
        "settings.json",
        "translation_prompt.txt",
        "README.md"
    ]

    print("\nCopying additional configuration files to app directory...")
    for file in files_to_copy:
        src = Path(file)
        dest = app_dir / file
        if src.exists() and not dest.exists():
            shutil.copy(src, dest)
            print(f"  - {file}")

    # Create setup instructions
    setup_instructions = """
SETUP INSTRUCTIONS
==================

FIRST TIME SETUP:
1. Rename 'api_key.txt.template' to 'api_key.txt'
2. Edit 'api_key.txt' and add your OpenAI API key
   Get your key from: https://platform.openai.com/api-keys
3. Customize 'custom_dictionary.txt' with your own word mappings (optional)
4. Adjust 'settings.json' if needed (optional)
5. Edit 'translation_prompt.txt' for custom translation behavior (optional)

RUNNING THE APPLICATION:
- Double-click 'DictationApp.exe'
- The app will appear in your system tray (look for a gray circle icon)
- Right-click the tray icon to:
  * Select input language (speech language)
  * Select output language (text language with translation)
  * Reload dictionary, API key, or prompts
  * Exit the application

USING THE DICTATION:
1. Open any application where you want to type
2. Place your cursor where you want the text
3. Hold down the hotkey (default: Right Ctrl)
4. Speak clearly into your microphone
5. Release the hotkey when done
6. Wait for the transcribed text to appear

For detailed instructions, see README.md
"""

    with open(app_dir / "SETUP.txt", "w") as f:
        f.write(setup_instructions)

    print("\n" + "=" * 60)
    print("Application package created!")
    print("=" * 60)
    print(f"\nLocation: {app_dir.absolute()}")
    print("\nMain files:")
    print(f"  - DictationApp.exe (main executable)")
    print(f"  - SETUP.txt (setup instructions)")
    print(f"  - README.md (full documentation)")
    print(f"  - api_key.txt.template (rename and add your API key)")
    print(f"  - custom_dictionary.txt (word replacement mappings)")
    print(f"  - settings.json (application settings)")
    print(f"  - translation_prompt.txt (custom translation prompt)")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("=" * 60)
    print("1. Navigate to the folder above")
    print("2. Follow instructions in SETUP.txt")
    print("3. Run DictationApp.exe")
    print("\nBuild complete!")


if __name__ == "__main__":
    main()
