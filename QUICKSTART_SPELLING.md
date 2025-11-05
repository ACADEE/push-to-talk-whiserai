# ⚡ Quick Start - Spelling Practice App

**Get up and running in 5 minutes!**

---

## 🚀 Super Simple Installation

### 1️⃣ Install Python

1. Go to: **https://www.python.org/downloads/**
2. Download Python (3.8 or newer)
3. Run installer
4. ✅ **CHECK** "Add Python to PATH"
5. Click "Install Now"

### 2️⃣ Download This Project

**Easy way:**
1. Download ZIP from GitHub
2. Right-click → Extract All
3. Remember the folder location

**Or use git:**
```bash
git clone https://github.com/ACADEE/push-to-talk-whiserai.git
```

### 3️⃣ Open Command Prompt Here

1. Open the extracted folder in File Explorer
2. Click in the address bar (top)
3. Type: `cmd`
4. Press Enter

### 4️⃣ Install Dependencies

Type this command:
```bash
pip install -r requirements.txt
```

Wait 1-2 minutes for installation.

### 5️⃣ Get OpenAI API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign up/login
3. Add payment method (starts at $5)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)

### 6️⃣ Run the App

Type this command:
```bash
python spelling_practice_app.py
```

A window opens! 🎉

### 7️⃣ Use the App

1. **Paste your API key** in the top field
2. Click "**Save API Key**"
3. Type a **word to practice** (e.g., "beautiful")
4. Click "**🎤 Start Recording**"
5. **Speak the word** into your microphone
6. Watch the **live transcription** appear!
7. See **green ✓** if correct, **red ✗** if wrong

---

## 🎯 That's It!

You're now using AI-powered spelling practice with live transcription.

---

## 🔴 Problems?

### "Python is not recognized"
- Reinstall Python
- Check "Add to PATH" during installation
- Restart computer

### "pip is not recognized"
- Try: `python -m pip install -r requirements.txt`

### No sound/microphone?
- Check Windows microphone permissions
- Settings → Privacy → Microphone → Allow apps

### No transcription?
- Check internet connection
- Verify API key is correct
- Check OpenAI account has credits

---

## 💰 How Much Does It Cost?

- **$0.006 per minute** of audio
- 10 minutes = **$0.06** (6 cents)
- A typical session = **$0.02 - $0.10**

Very affordable! 🎉

---

## 📖 Need More Help?

See detailed guide: [INSTALL_GUIDE.md](INSTALL_GUIDE.md)

---

## 🎬 What You'll See

```
┌─────────────────────────────────────────┐
│   Spelling Practice App                 │
├─────────────────────────────────────────┤
│ OpenAI API Key: [sk-****] [Save]       │
│ Word to Practice: [beautiful]           │
│                                         │
│ [🎤 Start Recording]  [Clear]  ● Idle   │
│                                         │
│ Live Transcription:                     │
│ ┌─────────────────────────────────────┐ │
│ │ [10:30:15] ✓ beautiful              │ │
│ │ [10:30:45] ✗ beautifull             │ │
│ │ [10:31:20] ✓ beautiful              │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Practice History:                       │
│ ┌─────────────────────────────────────┐ │
│ │ Target: 'beautiful' | Heard: '...'  │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## ✨ Features

✅ Real-time transcription (3-second updates)
✅ Color-coded feedback (green/red)
✅ Practice history tracking
✅ Secure API key input
✅ Works with any word

---

## 🏗️ Want a Standalone .exe?

On Windows, run:
```bash
python build_spelling_app.py
```

Find your .exe in: `dist/SpellingPracticeApp.exe`

Share it with anyone! They won't need Python installed.

---

**Happy practicing! 🎤✨**
