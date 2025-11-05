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
        "--onefile",   # Single executable
        "--icon=NONE", # No icon (can add later)
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

    # Create distribution folder
    dist_dir = Path("dist")
    release_dir = dist_dir / "release"

    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    # Copy executable
    exe_file = dist_dir / f"{app_name}.exe"
    if exe_file.exists():
        shutil.copy(exe_file, release_dir / f"{app_name}.exe")
        print(f"\nExecutable: {release_dir / f'{app_name}.exe'}")

    # Copy configuration templates
    files_to_copy = [
        "api_key.txt.template",
        "custom_dictionary.txt",
        "settings.json",
        "README.md"
    ]

    print("\nCopying configuration files...")
    for file in files_to_copy:
        src = Path(file)
        if src.exists():
            shutil.copy(src, release_dir / file)
            print(f"  - {file}")

    # Create setup instructions
    setup_instructions = """
SETUP INSTRUCTIONS
==================

1. Rename 'api_key.txt.template' to 'api_key.txt'
2. Edit 'api_key.txt' and add your OpenAI API key
3. Customize 'custom_dictionary.txt' with your own word mappings
4. Run 'DictationApp.exe'

For detailed instructions, see README.md
"""

    with open(release_dir / "SETUP.txt", "w") as f:
        f.write(setup_instructions)

    print("\n" + "=" * 60)
    print("Release package created!")
    print("=" * 60)
    print(f"\nLocation: {release_dir.absolute()}")
    print("\nContents:")
    for file in release_dir.iterdir():
        print(f"  - {file.name}")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("=" * 60)
    print("1. Navigate to the release folder")
    print("2. Follow instructions in SETUP.txt")
    print("3. Run DictationApp.exe")
    print("\nBuild complete!")


if __name__ == "__main__":
    main()
