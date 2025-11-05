# Building Spelling Practice App on Windows

Quick guide for building the Windows .exe executable.

## Prerequisites

1. **Windows 10 or 11**
2. **Python 3.8 or higher** installed
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

## Step-by-Step Build Instructions

### 1. Download the Project

```bash
# If you have git:
git clone <repository-url>
cd push-to-talk-whiserai

# Or download and extract the ZIP file
```

### 2. Install Dependencies

Open Command Prompt or PowerShell in the project folder:

```bash
pip install -r requirements.txt
```

This installs:
- openai
- sounddevice
- numpy
- tkinter (usually built-in)
- Pillow
- pyinstaller

### 3. Run the Build Script

```bash
python build_spelling_app.py
```

The build process will:
- Check for PyInstaller (install if needed)
- Compile the Python app into a single .exe
- Create the `dist/` folder with your executable
- Take 1-3 minutes depending on your system

### 4. Locate Your Executable

After successful build:

```
📁 push-to-talk-whiserai/
  📁 dist/
    📄 SpellingPracticeApp.exe  ← Your executable!
  📁 build/                       ← Can be deleted
  📄 SpellingPracticeApp.spec    ← Can be deleted
```

### 5. Test the Executable

1. Navigate to `dist/` folder
2. Double-click `SpellingPracticeApp.exe`
3. The app should open with a GUI window
4. Enter your OpenAI API key
5. Try recording!

## Distribution

### Sharing the App

You can share just the .exe file:
- **File**: `SpellingPracticeApp.exe`
- **Size**: ~7-10 MB
- **Requirements**: Windows 10/11, microphone
- **No Python needed**: Fully standalone

### What Users Need

Recipients only need:
1. Windows 10 or 11
2. A microphone
3. An OpenAI API key (they provide their own)
4. Internet connection

## Troubleshooting Build Issues

### "Python is not recognized"
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH in Environment Variables

### "pip is not recognized"
- Python installation may be incomplete
- Try: `python -m pip install -r requirements.txt`

### Build fails with "module not found"
- Run: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt --force-reinstall`

### Antivirus blocks the .exe
- Common with PyInstaller executables
- Add to antivirus exceptions
- Or whitelist the entire `dist/` folder

### "Access denied" errors
- Run Command Prompt as Administrator
- Right-click → "Run as administrator"
- Then run build script again

### Missing Visual C++ error
- Download Visual C++ Redistributable
- Link: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install and retry build

## Build Options

You can customize the build by editing `build_spelling_app.py`:

### Single File (default)
```python
"--onefile",  # Creates one .exe file
```

### Folder Distribution
Remove `--onefile` to create a folder with separate files:
- Faster startup
- Larger distribution size

### Console Window (for debugging)
Remove `--windowed` to show console:
```python
# Remove this line:
"--windowed",
```

### Add Icon
Replace `"NONE"` with your icon file:
```python
"--icon", "myicon.ico",
```

## Testing Before Distribution

1. **Test on clean system** (no Python installed)
2. **Check Windows Defender** doesn't block it
3. **Verify API key input** works correctly
4. **Test microphone recording** functionality
5. **Check file size** is reasonable (~10 MB)

## Advanced: Silent Build

For automated builds, you can run silently:

```bash
python build_spelling_app.py > build.log 2>&1
```

## File Sizes

Typical executable sizes:
- **Onefile mode**: 7-10 MB
- **Onedir mode**: 15-25 MB total (many files)

## Distribution Checklist

Before sharing your .exe:

- [ ] Tested on Windows 10
- [ ] Tested on Windows 11
- [ ] Tested without Python installed
- [ ] Added to antivirus exceptions
- [ ] Verified API key input works
- [ ] Verified recording works
- [ ] Verified transcription works
- [ ] Included README or instructions
- [ ] Specified OpenAI API requirement

## Quick Build Command Reference

```bash
# Full build process (one command)
pip install -r requirements.txt && python build_spelling_app.py

# Clean build (removes old files first)
rmdir /S /Q build dist && python build_spelling_app.py

# Build with console for debugging
# (edit build_spelling_app.py and remove --windowed first)
python build_spelling_app.py
```

## What Gets Bundled

The .exe includes:
- Python interpreter
- All Python libraries (openai, tkinter, numpy, etc.)
- Your application code
- Required DLLs

The .exe does NOT include:
- OpenAI API key (user must provide)
- Internet connection (user must have)
- Microphone drivers (uses Windows defaults)

## Next Steps

After building:
1. Test thoroughly on target Windows versions
2. Create a user guide (README_SPELLING_APP.md provided)
3. Consider code signing (optional, reduces Windows warnings)
4. Host on GitHub Releases for easy distribution

## Questions?

- Check PyInstaller docs: https://pyinstaller.org/
- Review error logs in console output
- Test on a clean Windows VM first
