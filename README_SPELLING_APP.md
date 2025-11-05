# Spelling Practice App - Live Whisper AI Transcription

A simple Windows GUI application for practicing spelling with real-time voice recognition using OpenAI's Whisper API.

## Features

- **Simple GUI Interface**: Easy-to-use window with input fields
- **Live Transcription**: Real-time speech-to-text as you speak
- **Spelling Practice**: Set a target word and get instant feedback
- **Visual Feedback**: Green checkmark for correct, red X for incorrect
- **Practice History**: Track all your attempts with timestamps
- **OpenAI Whisper AI**: Industry-leading speech recognition

## Screenshots

The app includes:
- API Key input field (secure password field)
- Target word input
- Start/Stop recording button
- Live transcription display with color-coded results
- Practice history log
- Real-time status indicator

## Requirements

- **Windows 10 or 11** (for .exe)
- **Python 3.8+** (for running from source)
- **OpenAI API Key** with Whisper API access
- **Microphone** connected to your computer
- **Internet connection** for API calls

## Installation & Usage

### Option 1: Run from Source (Any Platform)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python spelling_practice_app.py
   ```

3. **Use the app**:
   - Enter your OpenAI API key in the top field
   - Click "Save API Key"
   - Enter a word to practice (e.g., "accommodate")
   - Click "Start Recording" and speak the word
   - The app will transcribe in real-time (updates every 3 seconds)
   - Green text = correct match
   - Red text = incorrect/no match

### Option 2: Build Windows .exe

**On a Windows Machine**:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script**:
   ```bash
   python build_spelling_app.py
   ```

3. **Find your executable**:
   - Location: `dist/SpellingPracticeApp.exe`
   - Size: ~7-10 MB (single file)
   - Portable: No installation needed!

4. **Distribute**:
   - Copy `SpellingPracticeApp.exe` anywhere
   - Run it on any Windows PC (no Python needed)
   - First-time users will need to enter their API key

## How It Works

1. **Recording**: The app records audio in 3-second chunks while "Recording" is active
2. **Transcription**: Each chunk is sent to OpenAI's Whisper API
3. **Display**: Transcribed text appears in real-time with timestamps
4. **Matching**: The app checks if the target word appears in the transcription
5. **Feedback**: Visual indicators show success (green ✓) or failure (red ✗)
6. **History**: All attempts are logged with timestamps

## API Key Setup

### Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy your key (starts with `sk-...`)
5. Paste it into the app's API Key field
6. Click "Save API Key"

### API Key Security

- Keys are stored in memory only (not saved to disk)
- The password field hides your key with asterisks
- Never share your API key with anyone
- If compromised, regenerate it on OpenAI's website

## API Costs

OpenAI Whisper API pricing:
- **$0.006 per minute** of audio
- Example: 10 minutes of practice = $0.06
- Typical spelling practice session: $0.02-0.10

Monitor usage at: https://platform.openai.com/usage

## Tips for Best Results

1. **Speak Clearly**: Enunciate each word carefully
2. **Good Microphone**: Use a quality microphone or headset
3. **Quiet Environment**: Minimize background noise
4. **Wait for Updates**: Transcription updates every ~3 seconds
5. **Short Phrases**: Keep recordings under 30 seconds for best performance

## Troubleshooting

### No transcription appearing
- Check your internet connection
- Verify API key is correct (starts with `sk-...`)
- Check OpenAI account has available credits
- Look at console output for error messages

### Microphone not working
- Check Windows microphone permissions
- Set correct microphone as default in Windows Sound settings
- Test with Windows Voice Recorder first
- Try running the app as administrator

### API Key errors
- Verify key starts with `sk-`
- Check for extra spaces when copying
- Regenerate key on OpenAI platform if needed
- Ensure OpenAI account is active with credits

### Build errors on Windows
- Install latest Python (3.8+)
- Run as Administrator if needed
- Install Visual C++ Redistributable if prompted
- Check PyInstaller is installed: `pip install pyinstaller`

## Project Files

```
push-to-talk-whiserai/
├── spelling_practice_app.py      # Main GUI application
├── build_spelling_app.py          # Build script for .exe
├── requirements.txt               # Python dependencies
├── README_SPELLING_APP.md         # This file
└── dist/                          # Built executables (after build)
    └── SpellingPracticeApp.exe
```

## Technical Details

- **GUI Framework**: tkinter (built into Python)
- **Audio Recording**: sounddevice + numpy
- **Speech Recognition**: OpenAI Whisper API
- **Build Tool**: PyInstaller
- **Chunk Size**: 3 seconds (configurable in code)
- **Sample Rate**: 16kHz mono audio

## Customization

You can modify `spelling_practice_app.py`:

- **Chunk duration**: Change `chunk_duration = 3.0` (line ~320)
- **Sample rate**: Change `self.sample_rate = 16000` (line ~29)
- **Colors**: Modify tag configurations (lines ~150-155)
- **Window size**: Change `root.geometry("700x600")` (line ~20)
- **Language**: Add `language` parameter to API call (defaults to English)

## Differences from Main Dictation App

This spelling practice app is simpler and different from `dictation_app.py`:

| Feature | Spelling App | Dictation App |
|---------|--------------|---------------|
| Interface | GUI Window | System Tray |
| Mode | Live/Continuous | Push-to-Talk |
| Purpose | Spelling Practice | General Dictation |
| Display | On-screen feedback | Types into apps |
| Comparison | Checks target word | No validation |
| History | Built-in log | None |

## License

[Specify your license here]

## Support

For issues or questions:
- Check the troubleshooting section above
- Review error messages in the console
- Verify OpenAI API status at status.openai.com

## Version History

### Version 1.0.0 (Initial Release)
- Live transcription with 3-second updates
- GUI interface with input fields
- Real-time spelling validation
- Practice history tracking
- Color-coded feedback (green/red)
- Windows .exe compilation support
- Secure API key input

## Credits

- **OpenAI Whisper API** for speech recognition
- **Python tkinter** for GUI
- **sounddevice** for audio recording
- **PyInstaller** for executable compilation
