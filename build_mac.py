"""
Build script for creating macOS application bundle (.app)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """Build the macOS .app bundle"""

    print("=" * 60)
    print("Building Whisper Dictation App for macOS")
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

    # Build command for macOS
    build_command = [
        "pyinstaller",
        "--name", app_name,
        "--windowed",  # No terminal window (creates .app bundle)
        "--onedir",    # Directory mode for easier config file access
        "--add-data", "api_key.txt.template:.",  # Include template file
        "--add-data", "custom_dictionary.txt:.",  # Include dictionary file
        "--add-data", "settings.json:.",  # Include settings file
        "--add-data", "translation_prompt.txt:.",  # Include translation prompt
        "--icon=NONE", # No icon (can add later with .icns file)
        "--clean",     # Clean PyInstaller cache
        "--osx-bundle-identifier", "com.acadee.dictationapp",  # macOS bundle identifier
        main_script
    ]

    print("\nBuilding macOS application...")
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

    # The dist folder structure for macOS
    dist_dir = Path("dist")
    app_bundle = dist_dir / f"{app_name}.app"

    if not app_bundle.exists():
        print(f"\nError: Build bundle {app_bundle} not found!")
        sys.exit(1)

    # macOS .app structure:
    # DictationApp.app/
    #   Contents/
    #     MacOS/
    #       DictationApp (executable)
    #       [dependencies]
    #     Resources/
    #       [config files should go here]

    resources_dir = app_bundle / "Contents" / "Resources"

    print(f"\nApplication bundle created: {app_bundle.absolute()}")

    # Copy additional configuration files to Resources directory
    files_to_copy = [
        "api_key.txt.template",
        "custom_dictionary.txt",
        "settings.json",
        "translation_prompt.txt",
        "README.md"
    ]

    print("\nCopying configuration files to Resources...")
    for file in files_to_copy:
        src = Path(file)
        dest = resources_dir / file
        if src.exists() and not dest.exists():
            shutil.copy(src, dest)
            print(f"  - {file}")

    # Create setup instructions for macOS
    setup_instructions = """
SETUP INSTRUCTIONS FOR macOS
============================

FIRST TIME SETUP:
1. Navigate to the Resources folder:
   - Right-click DictationApp.app → Show Package Contents
   - Navigate to Contents/Resources/

2. Rename 'api_key.txt.template' to 'api_key.txt'

3. Edit 'api_key.txt' and add your OpenAI API key
   - Use TextEdit or your preferred text editor
   - Get your key from: https://platform.openai.com/api-keys

4. Customize 'custom_dictionary.txt' with your own word mappings (optional)

5. Adjust 'settings.json' if needed (optional)

6. Edit 'translation_prompt.txt' for custom translation behavior (optional)

RUNNING THE APPLICATION:
- Double-click 'DictationApp.app' to launch
- The app will appear in your menu bar (look for a gray circle icon)
- Right-click the menu bar icon to:
  * Select input language (speech language)
  * Select output language (text language)
  * Reload dictionary, API key, or prompts
  * Exit the application

USING THE DICTATION:
1. Open any application where you want to type
2. Place your cursor where you want the text
3. Hold down the hotkey (default: Right Ctrl)
4. Speak clearly into your microphone
5. Release the hotkey when done
6. Wait for the transcribed text to appear

PERMISSIONS:
- macOS may ask for microphone access - you must grant this
- macOS may ask for accessibility access for keyboard input - grant this too
- Go to System Preferences → Security & Privacy to manage permissions

For detailed instructions, see README.md
"""

    with open(resources_dir / "SETUP.txt", "w") as f:
        f.write(setup_instructions)

    print("\n" + "=" * 60)
    print("macOS Application Bundle Created!")
    print("=" * 60)
    print(f"\nLocation: {app_bundle.absolute()}")
    print("\nMain files:")
    print(f"  - DictationApp.app (macOS application bundle)")
    print(f"  - Contents/Resources/SETUP.txt (setup instructions)")
    print(f"  - Contents/Resources/api_key.txt.template (rename and add your API key)")
    print(f"  - Contents/Resources/custom_dictionary.txt (word mappings)")
    print(f"  - Contents/Resources/settings.json (application settings)")
    print(f"  - Contents/Resources/translation_prompt.txt (custom translation prompt)")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("=" * 60)
    print("1. Right-click DictationApp.app → Show Package Contents")
    print("2. Navigate to Contents/Resources/")
    print("3. Follow instructions in SETUP.txt")
    print("4. Double-click DictationApp.app to run")

    print("\n" + "=" * 60)
    print("Distribution:")
    print("=" * 60)
    print("To distribute:")
    print("1. Zip the entire DictationApp.app bundle:")
    print(f"   cd {dist_dir}")
    print(f"   zip -r DictationApp-macOS.zip {app_name}.app")
    print("2. Share the .zip file with users")
    print("3. Users extract and drag DictationApp.app to Applications folder")

    print("\nBuild complete!")


if __name__ == "__main__":
    main()
