"""
Optimized build script - creates smaller, faster .exe
"""
import PyInstaller.__main__
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(script_dir, 'live_dictation_app.py')

PyInstaller.__main__.run([
    app_path,
    '--name=SpeechToText',
    '--onedir',  # Multiple files but faster startup
    '--windowed',
    '--hidden-import=sounddevice',
    '--hidden-import=numpy',
    '--hidden-import=pyautogui',
    '--hidden-import=pyperclip',
    '--hidden-import=keyboard',
    '--hidden-import=openai',
    # Optimization
    '--exclude-module=matplotlib',  # Exclude unnecessary modules
    '--exclude-module=scipy',
    '--exclude-module=pandas',
    '--clean',
    '--noconfirm',
])

print("\n" + "="*60)
print("Optimized build complete!")
print("Your app is in the 'dist/SpeechToText' folder")
print("  → Distribute the entire 'dist/SpeechToText' folder")
print("  → User runs: SpeechToText/SpeechToText.exe")
print("="*60)
