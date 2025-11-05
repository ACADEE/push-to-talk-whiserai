"""
Build script to create standalone .exe for Live Dictation App
Run this on Windows to create a distributable executable
"""
import PyInstaller.__main__
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(script_dir, 'live_dictation_app.py')

# PyInstaller arguments
PyInstaller.__main__.run([
    app_path,
    '--name=SpeechToText',
    '--onefile',  # Single .exe file
    '--windowed',  # No console window
    '--icon=NONE',  # Add your icon here if you have one
    # Include hidden imports that might be missed
    '--hidden-import=sounddevice',
    '--hidden-import=numpy',
    '--hidden-import=pyautogui',
    '--hidden-import=pyperclip',
    '--hidden-import=keyboard',
    '--hidden-import=openai',
    # Clean build
    '--clean',
    # Additional options
    '--noconfirm',  # Replace output directory without asking
])

print("\n" + "="*60)
print("Build complete!")
print("Your .exe file is in the 'dist' folder:")
print("  → dist/SpeechToText.exe")
print("="*60)
print("\nTo distribute:")
print("1. Copy dist/SpeechToText.exe to any Windows computer")
print("2. The .exe is standalone - no Python installation needed")
print("3. User just double-clicks to run")
print("\nNote: api_key.txt and microphone.txt will be created")
print("      in the same folder as the .exe when first used")
