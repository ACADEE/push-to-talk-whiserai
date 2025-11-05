# Quick Start Guide

Get up and running with the Whisper Dictation App in 5 minutes!

## Prerequisites

- Windows 10 or 11
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Working microphone

## Step 1: Installation

### Option A: Pre-built Executable (Recommended)

1. Download the latest release ZIP file
2. Extract to a folder (e.g., `C:\DictationApp`)
3. You should see:
   - `DictationApp.exe`
   - `api_key.txt.template`
   - `custom_dictionary.txt`
   - `settings.json`
   - `README.md`

### Option B: Run from Source

```bash
git clone <repository-url>
cd push-to-talk-whiserai
pip install -r requirements.txt
```

## Step 2: Configure API Key

1. Rename `api_key.txt.template` to `api_key.txt`
2. Open `api_key.txt` in a text editor
3. Paste your OpenAI API key
4. Save and close

**Example**:
```
sk-proj-abc123def456...
```

## Step 3: Run the App

**Executable**: Double-click `DictationApp.exe`

**Source**: Run `python dictation_app.py`

You should see the app icon in your system tray (gray circle).

## Step 4: Test Dictation

1. Open Notepad (or any text editor)
2. Click in the text area
3. **Hold down Right Ctrl** (the default hotkey)
4. Say something like: "Hello, this is a test of the dictation app"
5. **Release Right Ctrl**
6. Wait 2-3 seconds
7. Your text should appear!

## System Tray Icon Colors

- **Gray**: Ready to record
- **Red**: Currently recording
- **Orange**: Processing your speech

## Common Issues

### "No API key found"
- Make sure `api_key.txt` exists (not `.template`)
- Check that it contains your actual API key
- File should be in the same folder as the .exe

### "No transcription received"
- Check your internet connection
- Verify your API key is valid
- Check OpenAI API status: https://status.openai.com
- Make sure you have API credits

### Microphone not working
- Check Windows sound settings
- Make sure microphone is set as default recording device
- Test with Windows Voice Recorder first
- Try running the app as Administrator

### Hotkey not responding
- Try a different hotkey (edit `settings.json`)
- Close other apps that might use the same hotkey
- Run as Administrator if needed

## Next Steps

- **Customize dictionary**: Edit `custom_dictionary.txt` to add your own word mappings
- **Change hotkey**: Edit `settings.json` to use a different key
- **Read full docs**: Check out `README.md` for detailed information

## Quick Tips

1. **Speak clearly**: Better diction = better results
2. **Short bursts**: Keep recordings under 30 seconds
3. **Pause briefly**: Short pauses help with sentence recognition
4. **Good mic**: Quality microphone = better transcription
5. **Quiet space**: Less background noise = better accuracy

## Getting Help

- Check the full `README.md` for detailed troubleshooting
- Open an issue on GitHub
- Check OpenAI API documentation

Happy dictating! 🎤✨
