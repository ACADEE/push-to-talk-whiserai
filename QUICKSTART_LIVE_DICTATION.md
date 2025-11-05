# ⚡ Quick Start - Live Dictation App

**Start dictating to Word/Notepad in 5 minutes!**

---

## 🚀 Super Fast Setup

### 1️⃣ Install Python (if not installed)

1. Download: **https://www.python.org/downloads/**
2. Run installer
3. ✅ **CHECK "Add Python to PATH"**
4. Click "Install Now"

### 2️⃣ Install Dependencies

Open Command Prompt or PowerShell:

```bash
pip install openai sounddevice numpy pyautogui
```

Wait ~1 minute for installation.

### 3️⃣ Get OpenAI API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign up/login
3. Add payment method ($5 minimum)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)

### 4️⃣ Run the App

In your project folder:

```bash
python live_dictation_app.py
```

A window appears! 🎉

### 5️⃣ Configure the App

1. **Paste API key** in the field
2. Click "**Save API Key**"
3. **Select your microphone** from dropdown
4. Click "**Enable Microphone**"

### 6️⃣ Start Dictating!

1. **Open Word** or Notepad
2. **Click** where you want text
3. **Start speaking** naturally
4. **Text appears** every ~3 seconds!
5. **Keep speaking** - it's continuous!

---

## 🎤 What You'll See

```
┌──────────────────────────────────────┐
│      Live Dictation App              │
├──────────────────────────────────────┤
│ OpenAI Configuration                 │
│ API Key: [sk-****]  [Save API Key]  │
│                                      │
│ Microphone Selection                 │
│ Select: [0: Microphone (USB)]       │
│         [🔄 Refresh Devices]        │
│                                      │
│ Dictation Control                    │
│    🔴 Recording - Speak Now!        │
│   [🔴 Disable Microphone]           │
│                                      │
│ Instructions:                        │
│ 1. Enter API key and click Save     │
│ 2. Select your microphone           │
│ 3. Click 'Enable Microphone'        │
│ 4. Open Word/Notepad               │
│ 5. Speak naturally                  │
└──────────────────────────────────────┘
```

---

## 💡 How to Use

### Basic Usage

1. **Enable microphone** in app
2. **Click in Word/Notepad** where you want text
3. **Speak**: "This is a test of the dictation app"
4. **Wait 3 seconds**
5. **Text appears**: "This is a test of the dictation app"
6. **Keep speaking** for continuous dictation!

### When You're Done

- Click "**Disable Microphone**"
- Your text stays in the document
- Close the app or dictate more later

---

## 🔧 Common Issues

### No microphone in list?
→ Click "🔄 Refresh Devices"
→ Check microphone is plugged in
→ Check Windows microphone permissions

### Text not appearing?
→ Make sure you clicked in Word/Notepad first
→ Check API key is saved
→ Check internet connection

### Wrong microphone selected?
→ Open dropdown and select the correct one
→ Built-in mic usually says "Internal" or "Array"
→ USB mics show their name

### Poor accuracy?
→ Use a headset or external microphone
→ Speak in a quiet environment
→ Speak naturally and clearly

---

## 💰 How Much Does It Cost?

- **$0.006 per minute** of audio
- 30 minutes of dictation = **$0.18** (18 cents!)
- Very affordable for regular use

Monitor usage: https://platform.openai.com/usage

---

## 🎯 Tips for Best Results

1. **Use a headset** - Much better than built-in mic
2. **Speak naturally** - Don't slow down or shout
3. **Quiet room** - Less background noise = better accuracy
4. **Keep window focused** - Don't switch apps while dictating
5. **Pause between thoughts** - Helps with punctuation

---

## 📝 Works With

✅ Microsoft Word
✅ Notepad
✅ Google Docs
✅ Email (Gmail, Outlook, etc.)
✅ Code editors (VS Code, etc.)
✅ Any application that accepts text input!

---

## 🏗️ Want a Windows .exe?

Build a standalone executable:

```bash
python build_live_dictation.py
```

Find it at: `dist/LiveDictationApp.exe`

Share with anyone - no Python needed!

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python with "Add to PATH" |
| "pip not found" | Use `python -m pip install ...` |
| No microphones | Check Windows Privacy → Microphone |
| API error | Check key is correct, has credits |
| Text in wrong place | Click in text field first |

---

## 📚 More Help

- **Detailed guide**: See [README_LIVE_DICTATION.md](README_LIVE_DICTATION.md)
- **Installation help**: See [INSTALL_GUIDE.md](INSTALL_GUIDE.md)
- **API setup**: https://platform.openai.com/docs

---

## ✨ Example Session

```
You: *Click in Word document*
You: *Enable microphone*
You: "This is my first test of live dictation."
App: *3 seconds later*
Word: "This is my first test of live dictation."
You: "It works great and is very accurate."
App: *3 seconds later*
Word: "This is my first test of live dictation. It works great and is very accurate."
```

---

## 🎉 You're Ready!

Start dictating hands-free to any application!

**For more features, see the full documentation.**

---

**Happy dictating!** 🎤✨
