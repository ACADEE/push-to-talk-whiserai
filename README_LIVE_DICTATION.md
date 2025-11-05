# Live Dictation App - Continuous Speech-to-Text

A Windows GUI application that provides **continuous live dictation** directly into Word, Notepad, or any text application using OpenAI's Whisper AI.

## ✨ Key Features

- **Live Transcription**: Continuous speech-to-text that types as you speak
- **Universal Compatibility**: Works with Word, Notepad, browsers, any text field
- **Microphone Selection**: Choose from multiple microphones/audio devices
- **Enable/Disable Toggle**: Simple on/off control for dictation
- **Real-time Typing**: Transcribed text appears automatically every ~3 seconds
- **Simple GUI**: Clean, minimal interface
- **OpenAI Whisper AI**: Industry-leading speech recognition accuracy

## 🎯 How It Works

1. Enable microphone in the app
2. Click on your Word/Notepad document where you want text
3. Speak naturally into your microphone
4. Text appears automatically in your document every ~3 seconds
5. Keep speaking - it's continuous!
6. Disable microphone when done

## 📋 Requirements

- **Windows 10 or 11**
- **Python 3.8+** (for running from source)
- **OpenAI API Key** with Whisper API access
- **Microphone** (headset recommended)
- **Internet connection** for API calls

## 🚀 Quick Start

### Option 1: Run from Source (Easiest)

1. **Install Python dependencies**:
   ```bash
   pip install openai sounddevice numpy pyautogui
   ```

2. **Run the application**:
   ```bash
   python live_dictation_app.py
   ```

3. **First time setup**:
   - Enter your OpenAI API key
   - Click "Save API Key"
   - Select your microphone from the dropdown
   - Click "Enable Microphone"

4. **Start dictating**:
   - Open Word or Notepad
   - Click where you want text to appear
   - Start speaking!

### Option 2: Build Windows .exe

On Windows:

```bash
python build_live_dictation.py
```

Your executable will be at: `dist/LiveDictationApp.exe`

## 🎤 Microphone Selection

The app automatically detects all available microphones:

- **Built-in microphone**: Usually labeled "Microphone Array" or "Internal Mic"
- **USB microphone**: Shows USB device name
- **Headset**: Shows headset model name
- **Virtual audio devices**: Any virtual input devices

**To refresh the list**: Click "🔄 Refresh Devices"

**Recommended**: Use a headset or external USB microphone for best results.

## 📝 Using with Different Applications

### Microsoft Word
1. Open Word document
2. Click where you want text
3. Enable microphone in app
4. Start speaking - text appears automatically!

### Notepad
1. Open Notepad
2. Click in the text area
3. Enable microphone
4. Speak naturally

### Google Docs / Browser
1. Open your browser and document
2. Click in the text field
3. Enable microphone
4. Start dictating

### Any Text Application
Works with any application that accepts keyboard input!

## ⚙️ Configuration

### API Key Setup

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy key (starts with `sk-...`)
5. Paste into app and click "Save API Key"

### Transcription Settings

Built into the code (you can modify):
- **Chunk duration**: 3 seconds (line ~292 in code)
- **Sample rate**: 16kHz (optimal for Whisper)
- **Language**: English (can be changed)
- **Typing speed**: 0.01s between characters

## 💰 API Costs

OpenAI Whisper API pricing:
- **$0.006 per minute** of audio
- Example: 30 minutes of dictation = $0.18
- Very affordable for regular use!

Monitor usage: https://platform.openai.com/usage

## 🎬 Usage Tips

### For Best Results

1. **Speak naturally**: Don't slow down or over-enunciate
2. **Use a headset**: Better audio quality = better accuracy
3. **Quiet environment**: Minimize background noise
4. **Pause briefly**: Between sentences for better punctuation
5. **Stay focused**: Keep cursor in the text field

### Voice Commands (Natural Speech)

The app transcribes what you say, so:
- Say "period" → types "period" (not ".")
- Say "new line" → types "new line" (not creates new line)
- Punctuation is automatic based on speech patterns

For punctuation, speak naturally and Whisper will add it automatically.

## 🔧 Troubleshooting

### Microphone not detected
- **Check Windows Sound Settings**: Make sure microphone is enabled
- **Try USB port**: If using USB mic, try different port
- **Click Refresh**: Use "🔄 Refresh Devices" button

### No text appearing
- **Check cursor position**: Make sure cursor is in a text field
- **Check API key**: Verify key is correct
- **Check internet**: Whisper API requires connection
- **Check console**: Run from command line to see errors

### Text appears in wrong place
- **Click in text field first**: Before enabling microphone
- **Keep window focused**: Don't switch windows while speaking
- **Disable microphone**: Before switching applications

### Microphone permission denied
- **Windows Settings** → **Privacy** → **Microphone**
- Enable "Let apps access your microphone"
- Allow Python to access microphone

### Poor transcription quality
- **Better microphone**: Use headset or external mic
- **Reduce noise**: Minimize background sounds
- **Check levels**: Windows Sound Settings → Recording → adjust level
- **Speak clearly**: Natural but clear pronunciation

### "API key not configured"
- Enter API key in the field
- Click "Save API Key" button
- Look for success message

### Text types too fast/slow
- Modify `pyautogui.PAUSE` value in code (line ~10)
- Default: 0.01 seconds between characters
- Increase for slower typing, decrease for faster

## 🔒 Privacy & Security

- **API key stored in memory only**: Not saved to disk
- **Audio is temporary**: Deleted immediately after transcription
- **No logging**: Your speech is not recorded or stored
- **Internet only for API**: Only sends audio to OpenAI's Whisper API

## 📊 Performance

- **Latency**: ~3-5 seconds from speech to text
- **Memory usage**: ~100-200 MB while running
- **CPU usage**: Minimal when not recording
- **Network**: ~100 KB per 3 seconds of audio

## ⌨️ Keyboard Shortcuts

- **Move mouse to top-left corner**: Emergency stop (PyAutoGUI failsafe)
- No other keyboard shortcuts (to avoid conflicts)

## 🏗️ Building the Executable

### On Windows

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run build script:
   ```bash
   python build_live_dictation.py
   ```

3. Find executable:
   ```
   dist/LiveDictationApp.exe
   ```

4. Distribute:
   - Single file, ~7-10 MB
   - No Python needed on target machine
   - Just double-click to run

## 📁 Project Structure

```
live_dictation_app.py      # Main application
build_live_dictation.py    # Build script
README_LIVE_DICTATION.md   # This file
```

## 🔄 Differences from Other Apps

| Feature | Live Dictation | Push-to-Talk Dictation | Spelling Practice |
|---------|----------------|------------------------|-------------------|
| Mode | Continuous | Hold hotkey | Practice mode |
| UI | GUI window | System tray | GUI window |
| Typing | Auto-types | Auto-types | Display only |
| Mic Selection | ✅ Yes | ❌ No | ❌ No |
| Target | General use | General use | Learning |

## 🐛 Known Limitations

- **3-second chunks**: Updates every ~3 seconds (not truly "instant")
- **Focus required**: Cursor must be in text field
- **Punctuation**: Automatic, can't force specific punctuation
- **No editing**: Can't undo or edit previous transcriptions
- **Windows only**: Designed for Windows OS

## 🎓 Examples

### Writing an Email

1. Open Gmail or Outlook
2. Click in email body
3. Enable microphone
4. Speak: "Hi John, I wanted to follow up on our meeting yesterday..."
5. Text appears in the email!

### Taking Notes

1. Open OneNote or Notepad
2. Enable microphone
3. Speak your thoughts
4. Text appears as you speak
5. Continue for as long as needed

### Documenting Code

1. Open your code editor
2. Click in a comment block
3. Enable microphone
4. Describe what the code does
5. Comments appear automatically!

## 💡 Pro Tips

1. **Use with custom dictionary**: Combine with the dictation app's custom dictionary feature for specialized terms
2. **Practice makes perfect**: Speech recognition improves with use
3. **Natural speech**: Don't over-think it, just talk normally
4. **Background app**: Keep the app window open but minimized
5. **Quick toggle**: Click "Disable Microphone" when you need to pause

## 🆘 Getting Help

### Error Messages

**"Please save your API key first!"**
- Enter API key and click "Save API Key"

**"Please select a microphone!"**
- Choose a microphone from the dropdown

**"Failed to record audio"**
- Check microphone is plugged in
- Check Windows microphone permissions
- Try selecting a different microphone

**"Transcription error"**
- Check internet connection
- Verify API key has credits
- Check OpenAI API status

### Support Resources

- OpenAI API Status: https://status.openai.com/
- OpenAI Documentation: https://platform.openai.com/docs
- Check API usage: https://platform.openai.com/usage

## 📜 Version History

### Version 1.0.0 (Initial Release)
- Continuous live dictation
- Microphone selection with dropdown
- Enable/disable toggle control
- Auto-typing into any application
- Real-time transcription (3-second chunks)
- Clean GUI interface
- Windows .exe compilation support

## 📄 License

[Specify your license here]

## 🙏 Credits

- **OpenAI Whisper API** for speech recognition
- **Python tkinter** for GUI
- **sounddevice** for audio recording
- **pyautogui** for keyboard simulation
- **PyInstaller** for executable compilation

---

**Enjoy hands-free dictation!** 🎤✨
