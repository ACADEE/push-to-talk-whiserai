# Installation Guide for Windows

This guide will help you install and build the Push-to-Talk Whisper Dictation App on Windows.

## Prerequisites

- **Windows 10 or 11**
- **Python 3.8 or higher** (Download from https://www.python.org/downloads/)
- **OpenAI API Key** (Get from https://platform.openai.com/api-keys)
- **Microphone** connected to your computer

## Important: MySQL-python Error

⚠️ **If you see an error about `MySQL-python` or `config-win.h`, this is NOT related to this project!**

This project does **NOT** require MySQL or MySQL-python. The error means:
- You might be in the wrong directory
- You might have a corrupted Python cache
- Another project's requirements are being used

### Solution:

1. **Make sure you're in the correct directory:**
   ```cmd
   cd C:\path\to\push-to-talk-whiserai
   dir
   ```
   You should see `dictation_app.py` and `requirements.txt`

2. **Verify the requirements.txt content:**
   ```cmd
   type requirements.txt
   ```
   It should contain ONLY these packages (NO MySQL-python):
   - openai
   - pystray
   - pillow
   - keyboard
   - sounddevice
   - numpy
   - pyautogui
   - wave
   - pyinstaller

3. **If the error persists, use a clean virtual environment:**
   ```cmd
   # Create a new virtual environment
   python -m venv venv_clean

   # Activate it
   venv_clean\Scripts\activate

   # Upgrade pip
   python -m pip install --upgrade pip

   # Install dependencies
   pip install -r requirements.txt
   ```

## Step-by-Step Installation

### Option 1: Run from Source (Development)

1. **Clone or download the repository:**
   ```cmd
   git clone <repository-url>
   cd push-to-talk-whiserai
   ```

2. **Create a virtual environment (recommended):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Upgrade pip:**
   ```cmd
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

   ✅ This should complete WITHOUT any MySQL-python errors!

5. **Configure your API key:**
   ```cmd
   # Copy the template
   copy api_key.txt.template api_key.txt

   # Edit api_key.txt with Notepad and paste your OpenAI API key
   notepad api_key.txt
   ```

6. **Run the application:**
   ```cmd
   python dictation_app.py
   ```

### Option 2: Build Executable (.exe)

1. **Complete steps 1-4 from Option 1 above**

2. **Build the executable:**
   ```cmd
   python build.py
   ```

3. **The executable will be created in:**
   ```
   dist\DictationApp\DictationApp.exe
   ```

4. **Configure the built application:**
   ```cmd
   cd dist\DictationApp

   # Rename the template
   ren api_key.txt.template api_key.txt

   # Edit and add your API key
   notepad api_key.txt
   ```

5. **Run the executable:**
   ```cmd
   DictationApp.exe
   ```

## Build Script Details

The `build.py` script uses PyInstaller with these features:

- **No console window** (`--windowed`): The app runs in the system tray
- **Directory mode** (not `--onefile`): Makes it easier to access config files
- **Includes config files**: api_key.txt.template, custom_dictionary.txt, settings.json
- **Creates SETUP.txt**: Instructions for end users

### Build Output Structure:
```
dist/
└── DictationApp/
    ├── DictationApp.exe          # Main executable
    ├── SETUP.txt                  # Setup instructions
    ├── README.md                  # Full documentation
    ├── api_key.txt.template       # API key template (rename to api_key.txt)
    ├── custom_dictionary.txt      # Word mappings
    ├── settings.json              # Application settings
    └── [various DLL and dependency files]
```

## Configuration

### 1. API Key (Required)

The app needs your OpenAI API key to work:

1. Get your API key: https://platform.openai.com/api-keys
2. Create/edit `api_key.txt` in the same folder as the .exe or .py file
3. Paste your key (starts with `sk-...`)
4. Save and close

### 2. Custom Dictionary (Optional)

Edit `custom_dictionary.txt` to add custom word replacements:

```
acadi -> ACADEE
jay eff kay -> JFK
my sequel -> MySQL
```

### 3. Settings (Optional)

Edit `settings.json` to customize:

```json
{
  "hotkey": "right ctrl",
  "sample_rate": 16000,
  "channels": 1,
  "audio_device": null,
  "output_language": "fr"
}
```

**Available output languages:**
- `fr` - Français (no translation)
- `en` - English
- `de` - Deutsch (German)
- `es` - Español (Spanish)
- `it` - Italiano (Italian)

## Usage

1. **Start the application**
   - Double-click `DictationApp.exe` or run `python dictation_app.py`
   - A gray circle icon appears in your system tray

2. **Select output language**
   - Right-click the tray icon
   - Choose "Output Language"
   - Select your preferred language

3. **Dictate text**
   - Open any application (Word, Notepad, browser, etc.)
   - Click where you want the text
   - **Hold** the hotkey (default: Right Ctrl)
   - Speak clearly in French
   - **Release** the hotkey
   - Text appears in your chosen language

## Troubleshooting

### "No module named 'XXX'"
- Make sure you activated the virtual environment
- Run: `pip install -r requirements.txt`

### "API key not configured"
- Check that `api_key.txt` exists in the same folder as the executable
- Verify the key is correct (starts with `sk-`)
- Make sure there are no extra spaces or line breaks

### "No audio recorded"
- Check Windows Sound Settings
- Set your microphone as the default recording device
- Test with Windows Voice Recorder first

### Hotkey not working
- Try a different hotkey in `settings.json`
- Run the app as Administrator (right-click → Run as administrator)
- Check if another app is using the same hotkey

### Build errors
- Make sure PyInstaller is installed: `pip install pyinstaller`
- Try deleting `build/` and `dist/` folders, then rebuild
- Use a clean virtual environment

### Text not appearing
- Make sure the target application has focus
- Try clicking in the text area before dictating
- Check console output for errors (run from cmd if using .exe)

## Distributing Your Built Application

After building, you can share the entire `dist\DictationApp\` folder:

1. **Zip the folder:**
   ```cmd
   # From the dist directory
   tar -a -c -f DictationApp-v1.1.0.zip DictationApp
   ```

2. **Share the zip file** with users

3. **Users should:**
   - Extract the zip
   - Follow instructions in `SETUP.txt`
   - Add their own API key
   - Run `DictationApp.exe`

## Security Notes

- **Keep your API key private!** Never share it or commit it to version control
- The `.gitignore` file prevents `api_key.txt` from being committed
- Only the template file (`api_key.txt.template`) should be in version control

## Getting Help

- Check the full `README.md` for detailed documentation
- Review error messages in the console output
- Verify all prerequisites are met
- Make sure your OpenAI account has available credits

## Cost Information

OpenAI API pricing:
- **Whisper**: $0.006 per minute of audio
- **GPT-4o-mini** (translation): ~$0.0008 per request
- **Example**: 100 minutes with translation ≈ $0.68

Monitor usage: https://platform.openai.com/usage

---

**Need more help?** Check the full README.md or open an issue on GitHub.
