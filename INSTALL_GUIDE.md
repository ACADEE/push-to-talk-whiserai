# 📥 Installation Guide - Spelling Practice App

Complete step-by-step guide for installing and running the Spelling Practice App.

---

## 🎯 Choose Your Method

**Method 1**: [Run from Source](#method-1-run-from-source) (Easiest, works immediately)
**Method 2**: [Build Windows .exe](#method-2-build-windows-exe) (For sharing/distribution)

---

## Method 1: Run from Source

This method runs the Python script directly. Best for testing and personal use.

### Step 1: Install Python

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click the big yellow "Download Python 3.x.x" button
   - Version 3.8 or newer required

2. **Install Python**
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Python Installation**
   - Open Command Prompt (Windows key + R, type `cmd`, press Enter)
   - Type: `python --version`
   - You should see: `Python 3.x.x`
   - If error, restart your computer and try again

### Step 2: Download the Project

**Option A: Using Git (if installed)**
```bash
git clone https://github.com/ACADEE/push-to-talk-whiserai.git
cd push-to-talk-whiserai
```

**Option B: Manual Download**
1. Go to: https://github.com/ACADEE/push-to-talk-whiserai
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder (e.g., `C:\SpellingApp\`)
5. Remember this folder location!

### Step 3: Open Command Prompt in Project Folder

**Windows Explorer Method:**
1. Open File Explorer
2. Navigate to the project folder (where you extracted/cloned)
3. Click in the address bar (where it shows the path)
4. Type `cmd` and press Enter
5. Command Prompt opens in this folder

**Manual Method:**
1. Press Windows key + R
2. Type `cmd` and press Enter
3. Type: `cd C:\path\to\your\folder`
4. Press Enter

### Step 4: Install Required Libraries

In the Command Prompt, type this command:

```bash
pip install -r requirements.txt
```

Press Enter and wait. You'll see:
```
Collecting openai...
Collecting sounddevice...
Collecting numpy...
... (more lines)
Successfully installed openai-1.x.x sounddevice-0.x.x ...
```

**If you see "pip is not recognized":**
Try: `python -m pip install -r requirements.txt`

### Step 5: Get Your OpenAI API Key

1. **Create OpenAI Account**
   - Go to: https://platform.openai.com/signup
   - Sign up with email or Google/Microsoft account
   - Verify your email

2. **Add Payment Method**
   - Go to: https://platform.openai.com/account/billing
   - Click "Add payment method"
   - Add credit card (you'll be charged only for usage)
   - Minimum: $5 (will last for many practice sessions)

3. **Create API Key**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Give it a name (e.g., "Spelling Practice")
   - Click "Create secret key"
   - **COPY THE KEY** (starts with `sk-...`)
   - ⚠️ Save it somewhere safe - you can't see it again!

### Step 6: Run the App

In Command Prompt (in project folder):

```bash
python spelling_practice_app.py
```

Press Enter. A window should appear!

### Step 7: First Use

1. **Enter API Key**
   - Paste your API key (sk-...) in the top field
   - Click "Save API Key"
   - You should see "API key saved successfully!"

2. **Set Target Word**
   - Type a word to practice (e.g., "accommodation")
   - Click in the "Word to Practice" field

3. **Start Recording**
   - Click "🎤 Start Recording"
   - Status changes to "● Recording" (red)
   - Speak the word clearly into your microphone
   - Wait 3 seconds for transcription to appear
   - Keep speaking to see live updates

4. **See Results**
   - Green ✓ = Correct! You said the target word
   - Red ✗ = Incorrect or different word heard
   - History shows all your attempts

5. **Stop Recording**
   - Click "⏹ Stop Recording"
   - Practice more words or close the app

---

## Method 2: Build Windows .exe

This creates a standalone executable that works without Python installed.

### Requirements

- Windows 10 or 11
- Python 3.8+ installed (see Method 1, Step 1)
- 500 MB free disk space

### Step 1-3: Same as Method 1

Follow Steps 1-3 from Method 1 above to:
- Install Python
- Download the project
- Open Command Prompt in project folder

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs everything needed, including PyInstaller.

### Step 5: Run Build Script

In Command Prompt:

```bash
python build_spelling_app.py
```

You'll see:
```
============================================================
Building Spelling Practice App Executable
============================================================
✓ PyInstaller version: 6.x.x
...
✓ Build completed successfully!
============================================================
```

This takes 1-3 minutes.

### Step 6: Find Your Executable

After build completes:

```
📁 push-to-talk-whiserai/
  📁 dist/
    📄 SpellingPracticeApp.exe  ← Here it is!
```

File location: `dist\SpellingPracticeApp.exe`

### Step 7: Test the .exe

1. Navigate to `dist` folder in File Explorer
2. Double-click `SpellingPracticeApp.exe`
3. App window should open
4. Follow Step 7 from Method 1 (First Use)

### Step 8: Distribute (Optional)

To share with others:

1. Copy `SpellingPracticeApp.exe` to a USB drive or cloud storage
2. Recipients just double-click the .exe
3. They need:
   - Windows 10/11
   - Their own OpenAI API key
   - A microphone
   - Internet connection

**No Python installation needed for recipients!**

---

## 🔧 Troubleshooting

### "Python is not recognized"

**Problem**: Windows can't find Python

**Solution**:
1. Uninstall Python
2. Reinstall and CHECK "Add Python to PATH"
3. Restart computer
4. Try again

### "pip is not recognized"

**Problem**: pip not in PATH

**Solution**:
```bash
python -m pip install -r requirements.txt
```

### "No module named 'tkinter'"

**Problem**: tkinter not included with Python

**Solution**:
1. Reinstall Python
2. During installation, click "Customize Installation"
3. Make sure "tcl/tk and IDLE" is checked
4. Complete installation

### "ModuleNotFoundError: No module named..."

**Problem**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt --force-reinstall
```

### "Access is denied" errors

**Problem**: Permission issues

**Solution**:
1. Right-click Command Prompt
2. Choose "Run as administrator"
3. Navigate to project folder
4. Run commands again

### Microphone not working

**Problem**: App can't access microphone

**Solution**:
1. **Windows Settings** → **Privacy** → **Microphone**
2. Enable "Let apps access your microphone"
3. Test microphone with Windows Voice Recorder first
4. Make sure microphone is default recording device

### No transcription appearing

**Problem**: API issues

**Solutions**:
- Check internet connection
- Verify API key is correct (starts with `sk-`)
- Check OpenAI account has credits: https://platform.openai.com/account/usage
- Look for error messages in transcription window

### Windows Defender blocks .exe

**Problem**: Antivirus flags the executable

**Solution**:
- This is common with PyInstaller
- Click "More info" → "Run anyway"
- Or add to Windows Defender exclusions:
  1. **Windows Settings** → **Virus & threat protection**
  2. **Manage settings** → **Add or remove exclusions**
  3. Add the `dist` folder

### "Failed to execute script"

**Problem**: Missing dependencies in built .exe

**Solution**:
1. Delete `build` and `dist` folders
2. Run: `pip install -r requirements.txt --force-reinstall`
3. Run: `python build_spelling_app.py` again

---

## 📝 Quick Command Reference

### Run from source:
```bash
python spelling_practice_app.py
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Build executable:
```bash
python build_spelling_app.py
```

### Check Python version:
```bash
python --version
```

### Upgrade pip:
```bash
python -m pip install --upgrade pip
```

### Clean build (start fresh):
```bash
rmdir /S /Q build dist
python build_spelling_app.py
```

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Python is installed and in PATH
- [ ] Project files are downloaded
- [ ] Dependencies are installed (`pip install -r requirements.txt` succeeded)
- [ ] App runs without errors
- [ ] Window appears with all buttons and fields
- [ ] API key can be saved
- [ ] Recording button works
- [ ] Microphone is detected
- [ ] Transcription appears after speaking
- [ ] Colors work (green for correct, red for incorrect)

---

## 💡 Tips for Success

1. **Use a good microphone**: Built-in laptop mics work, but headset mics are better
2. **Quiet environment**: Background noise affects accuracy
3. **Speak clearly**: Pronounce each syllable
4. **Wait for updates**: Transcription updates every ~3 seconds
5. **Check your balance**: Monitor API usage at https://platform.openai.com/account/usage

---

## 🎓 First Time Using OpenAI API?

### Costs
- Whisper API: $0.006 per minute
- 10 minutes of practice = $0.06
- Typical session = $0.02-0.10

### Free Trial
- New accounts may get free credits
- Check: https://platform.openai.com/account/usage

### Setting Limits
1. Go to: https://platform.openai.com/account/billing/limits
2. Set a monthly budget (e.g., $5)
3. You'll get notified if you approach the limit

---

## 🆘 Still Need Help?

### Check Console for Errors

Run the app from Command Prompt to see error messages:
```bash
python spelling_practice_app.py
```

Any errors will appear in the console window.

### Common Error Messages

**"Invalid API key"**
- API key is wrong or expired
- Regenerate at https://platform.openai.com/api-keys

**"You exceeded your current quota"**
- Add credits to your OpenAI account
- Go to https://platform.openai.com/account/billing

**"Connection error"**
- Check your internet connection
- Check firewall isn't blocking Python

**"Audio device not found"**
- Plug in microphone
- Set as default in Windows Sound settings

---

## 📚 Additional Resources

- **OpenAI API Documentation**: https://platform.openai.com/docs
- **Python Download**: https://www.python.org/downloads/
- **Project Repository**: https://github.com/ACADEE/push-to-talk-whiserai
- **Whisper API Pricing**: https://openai.com/pricing

---

## 🎉 You're All Set!

Your app is now ready to use. Enjoy practicing spelling with AI-powered live transcription!

For detailed feature documentation, see [README_SPELLING_APP.md](README_SPELLING_APP.md).
