# Troubleshooting Guide

Comprehensive guide to solving common issues with the Push-to-Talk Whisper Dictation App.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [API Key Problems](#api-key-problems)
3. [Microphone Issues](#microphone-issues)
4. [Hotkey Problems](#hotkey-problems)
5. [Transcription Issues](#transcription-issues)
6. [Text Insertion Problems](#text-insertion-problems)
7. [Dictionary Not Working](#dictionary-not-working)
8. [Performance Issues](#performance-issues)
9. [Error Messages](#error-messages)

---

## Installation Issues

### "Python not found" or "python is not recognized"

**Solution**:
1. Install Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your command prompt/terminal

### Dependencies won't install

**Problem**: `pip install -r requirements.txt` fails

**Solutions**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install dependencies one by one to identify problematic package
pip install openai
pip install pystray
pip install pillow
# ... etc

# If sounddevice fails, you may need Visual C++ Redistributables
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### "Module not found" when running

**Solution**:
```bash
# Make sure you're in the correct directory
cd push-to-talk-whiserai

# Verify virtual environment is activated (if using one)
# Install all requirements again
pip install -r requirements.txt
```

---

## API Key Problems

### "No API key found"

**Checklist**:
- [ ] File is named `api_key.txt` (not `.template`)
- [ ] File is in the same directory as `dictation_app.py` or `.exe`
- [ ] File contains only the API key, no extra text
- [ ] No spaces before or after the key
- [ ] File is saved (not just open in editor)

**Test**:
```bash
# Check if file exists
dir api_key.txt  # Windows
ls api_key.txt   # Linux/Mac

# View contents (careful with sensitive data!)
type api_key.txt  # Windows
cat api_key.txt   # Linux/Mac
```

### "Invalid API key" error

**Solutions**:
1. **Verify the key**:
   - Log in to https://platform.openai.com/api-keys
   - Check if the key is still active
   - Verify you copied the entire key

2. **Create new key**:
   - If key is revoked, create a new one
   - Update `api_key.txt` with the new key
   - Use "Reload API Key" from system tray menu

3. **Check format**:
   ```
   ✓ Correct: sk-proj-abc123...
   ✗ Wrong: "sk-proj-abc123..." (has quotes)
   ✗ Wrong: API_KEY=sk-proj-abc123... (has prefix)
   ```

### "Insufficient credits" or rate limit errors

**Solutions**:
- Check usage: https://platform.openai.com/usage
- Add credits to your account
- Wait if you hit rate limits (usually 3 requests/minute for free tier)
- Upgrade to paid plan for higher limits

---

## Microphone Issues

### App doesn't record any audio

**Solutions**:

1. **Check default device**:
   - Right-click speaker icon in Windows taskbar
   - Select "Sounds" → "Recording" tab
   - Set your microphone as "Default Device"
   - Test by speaking and watching the level meter

2. **Test microphone**:
   - Open Windows Voice Recorder
   - Record a short clip
   - If Voice Recorder doesn't work, it's a system issue

3. **Check permissions**:
   - Windows Settings → Privacy → Microphone
   - Ensure "Allow apps to access your microphone" is ON
   - Allow Python or the app specifically

4. **Try different device**:
   - Edit `settings.json`:
     ```json
     {
       "audio_device": 0,  # Try 0, 1, 2, etc.
       ...
     }
     ```

5. **List available devices** (for developers):
   ```python
   import sounddevice as sd
   print(sd.query_devices())
   ```

### Audio quality is poor

**Solutions**:
- Use a better quality microphone
- Reduce background noise
- Increase sample rate in `settings.json`:
  ```json
  {
    "sample_rate": 44100,
    ...
  }
  ```
- Position microphone closer to mouth
- Use pop filter or windscreen

### Microphone stops working after a while

**Solutions**:
- Update audio drivers
- Check for Windows updates
- Restart the application
- Restart Windows audio service:
  ```
  services.msc → Windows Audio → Restart
  ```

---

## Hotkey Problems

### Hotkey doesn't trigger recording

**Solutions**:

1. **Try running as Administrator**:
   - Right-click `DictationApp.exe`
   - Select "Run as administrator"
   - Some apps require admin privileges to receive hotkeys

2. **Check for conflicts**:
   - Close other apps that might use the same hotkey
   - Try a different hotkey in `settings.json`:
     ```json
     {
       "hotkey": "f9",
       ...
     }
     ```

3. **Available hotkey options**:
   - `f1`, `f2`, ... `f12`
   - `right ctrl`, `left ctrl`
   - `right shift`, `left shift`
   - `right alt`, `left alt`
   - `caps lock`
   - Mouse buttons: `mouse side button 1`, etc.

4. **Test hotkey detection**:
   - Run app from command line to see debug output
   - Watch for "Hotkey registered" message

### Hotkey triggers but nothing happens

**Solutions**:
- Check API key is configured
- Check internet connection
- Look for error messages in console (run from command line)
- Verify microphone is working (see Microphone Issues)

### Can't release hotkey / stuck recording

**Solutions**:
- Press and release the hotkey again
- Click on the system tray icon
- Exit and restart the app
- Restart Windows if necessary

---

## Transcription Issues

### "No transcription received"

**Possible causes and solutions**:

1. **Too short recording**:
   - Record at least 1-2 seconds
   - Speak during recording

2. **No audio captured**:
   - Check microphone (see Microphone Issues)
   - Verify levels in Windows Sound settings

3. **API timeout**:
   - Check internet connection
   - Check OpenAI API status: https://status.openai.com
   - Try again after a few seconds

4. **File format issue**:
   - App should handle this automatically
   - Check temp directory has space: `%TEMP%`

### Transcription is inaccurate

**Solutions**:

1. **Improve audio quality**:
   - Speak clearly and at moderate pace
   - Reduce background noise
   - Use better microphone
   - Position mic 4-6 inches from mouth

2. **Adjust speaking style**:
   - Speak in complete phrases
   - Pause briefly between sentences
   - Articulate words clearly
   - Don't mumble or speak too fast

3. **Use custom dictionary**:
   - Add commonly misheard words to `custom_dictionary.txt`
   - Example:
     ```
     acadi -> ACADEE
     data base -> database
     ```

### Wrong language detected

**Solution**:
- App is configured for English
- To change, edit `dictation_app.py` line ~135:
  ```python
  transcript = self.client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file,
      language="es"  # Change to: es, fr, de, etc.
  )
  ```

---

## Text Insertion Problems

### Text doesn't appear in target application

**Solutions**:

1. **Ensure app has focus**:
   - Click in the text field before dictating
   - Cursor should be blinking

2. **Try different application**:
   - Test in Notepad first
   - Some apps may block programmatic input

3. **Increase delay**:
   - Edit `dictation_app.py` line ~286:
     ```python
     pyautogui.PAUSE = 0.1  # Increase from 0.01
     ```

4. **Run as Administrator**:
   - Some protected apps require admin privileges

### Text appears in wrong location

**Solutions**:
- Don't move mouse or change focus after pressing hotkey
- Position cursor before starting dictation
- Add delay before text insertion (edit code)

### Special characters don't work

**Solutions**:
- Use custom dictionary to replace words with special chars
- Some characters may not work in all apps
- Consider using clipboard instead:
  ```python
  import pyperclip
  pyperclip.copy(text)
  pyautogui.hotkey('ctrl', 'v')
  ```

---

## Dictionary Not Working

### Replacements not applied

**Checklist**:
- [ ] File is named `custom_dictionary.txt` exactly
- [ ] File is in the same directory as the app
- [ ] Format is correct: `phonetic -> REPLACEMENT`
- [ ] Used "Reload Dictionary" from system tray menu

**Test**:
```
# In custom_dictionary.txt:
test word -> REPLACED

# Say: "This is a test word"
# Should appear as: "This is a REPLACED"
```

### Case not working as expected

**Understanding**:
- Matching is case-insensitive: `test`, `TEST`, `Test` all match `test -> REPLACED`
- Replacement uses the exact case you specify: `test -> ABC` always gives `ABC`

**Examples**:
```
# Dictionary entry:
jay eff kay -> JFK

# Transcription: "I saw jay eff kay"
# Result: "I saw JFK" ✓

# Transcription: "I saw JAY EFF KAY"
# Result: "I saw JFK" ✓
```

### Multi-word phrases not matching

**Solutions**:
- Ensure exact spacing matches what Whisper produces
- Test what Whisper actually transcribes:
  1. Dictate without dictionary entry
  2. See what appears
  3. Use that exact text as the phonetic pattern

**Example**:
```
# What you say: "triple A"
# What Whisper hears: "triple a" or "AAA" (varies)
# Dictionary entry should match Whisper's output:
triple a -> AAA
```

---

## Performance Issues

### Slow transcription

**Causes and solutions**:

1. **Slow internet**:
   - Check connection speed
   - Move closer to router
   - Use wired connection

2. **Large audio files**:
   - Keep recordings under 30 seconds
   - Higher quality = larger file = slower upload

3. **API response time**:
   - Varies based on OpenAI server load
   - Usually 2-5 seconds
   - Nothing you can do except wait

### High CPU/memory usage

**Solutions**:
- Close other applications
- Check for memory leaks (restart app periodically)
- Update to latest version
- Check Windows Task Manager for other resource hogs

### System tray icon not updating

**Solutions**:
- Wait a few seconds (may be delayed)
- Hover mouse over icon
- Restart the app
- Windows explorer may need restart:
  ```
  Task Manager → Windows Explorer → Restart
  ```

---

## Error Messages

### "Failed to process audio"

**Possible causes**:
- Network error
- API error
- Audio file corruption
- Insufficient permissions

**Solutions**:
- Check internet connection
- Verify API key
- Check API credits
- Try recording again
- Restart the app

### "Error inserting text"

**Possible causes**:
- No window has focus
- Target app blocks keyboard input
- Permissions issue

**Solutions**:
- Click in target application first
- Run as Administrator
- Try different application (test with Notepad)

### "Error loading API key"

**Solutions**:
- Check file permissions
- Verify file exists
- Check file isn't locked by another program
- Try copying file contents to new file

---

## Getting More Help

### Enable Debug Output

Run from command line to see detailed output:
```bash
python dictation_app.py
```

Watch for:
- Startup messages
- "Hotkey registered" message
- "Starting recording" message
- "Transcribing audio" message
- Any error messages

### Check Log Files

Create a log file for persistent debugging:
```python
# Add to top of dictation_app.py:
import logging
logging.basicConfig(
    filename='dictation_app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### System Information

When asking for help, provide:
- Windows version: `winver`
- Python version: `python --version`
- App version
- Error messages
- Steps to reproduce

### Where to Get Help

- GitHub Issues: [Create an issue](https://github.com/yourusername/push-to-talk-whiserai/issues)
- Check existing issues for similar problems
- OpenAI API Status: https://status.openai.com
- OpenAI Community: https://community.openai.com

---

## Still Having Issues?

If none of these solutions work:

1. **Reinstall**:
   - Delete the app directory
   - Download fresh copy
   - Reinstall dependencies
   - Reconfigure

2. **Check system requirements**:
   - Windows 10/11
   - Python 3.8+
   - Working internet
   - Valid API key

3. **Report a bug**:
   - Open GitHub issue
   - Include all relevant information
   - Attach logs if possible
   - Describe exact steps to reproduce

We're here to help! 🎯
