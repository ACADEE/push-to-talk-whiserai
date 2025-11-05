# Push-to-Talk Whisper AI Dictation App

A Windows desktop application that enables voice-to-text dictation directly into any active application using OpenAI's Whisper AI for speech recognition.

## Features

- **Push-to-Talk Recording**: Hold a configurable hotkey to record audio, release to transcribe
- **Universal Compatibility**: Works with any Windows application (Word, Notepad, browsers, etc.)
- **Custom Dictionary**: Define custom phonetic mappings for specialized terms, acronyms, and brand names
- **System Tray Integration**: Minimal UI that runs in the background
- **Real-time Feedback**: Visual indicators for recording and processing states
- **OpenAI Whisper API**: Industry-leading speech recognition accuracy

## Requirements

- Windows 10 or Windows 11
- Python 3.8 or higher (for running from source)
- OpenAI API key with access to Whisper API
- Microphone connected to your computer

## Installation

### Option 1: Run from Source (Development)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd push-to-talk-whiserai
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**:
   - Copy `api_key.txt.template` to `api_key.txt`
   - Edit `api_key.txt` and paste your OpenAI API key
   - Get your API key from: https://platform.openai.com/api-keys

4. **Run the application**:
   ```bash
   python dictation_app.py
   ```

### Option 2: Use Pre-built Executable (Production)

1. Download the latest release from the releases page
2. Extract the ZIP file to a folder of your choice
3. Configure your API key (see Configuration section below)
4. Run `dictation_app.exe`

## Configuration

### API Key Setup

Create a file named `api_key.txt` in the same directory as the application:

```
sk-your-openai-api-key-here
```

**Important**: Never share your API key or commit it to version control!

### Custom Dictionary

Edit `custom_dictionary.txt` to add custom word mappings. Format:

```
phonetic_phrase -> CORRECT_SPELLING
```

**Examples**:
```
acadi -> ACADEE
jay eff kay -> JFK
triple a -> AAA
my sequel -> MySQL
```

**Rules**:
- One mapping per line
- Matching is case-insensitive
- Replacement preserves the case you specify
- Longer phrases are matched first (to handle overlapping patterns)
- Use `->` to separate phonetic from correct spelling

### Settings Configuration

Edit `settings.json` to customize application behavior:

```json
{
  "hotkey": "right ctrl",
  "sample_rate": 16000,
  "channels": 1,
  "audio_device": null
}
```

**Available hotkeys**:
- `right ctrl` or `left ctrl`
- `right shift` or `left shift`
- `right alt` or `left alt`
- Function keys: `f1`, `f2`, etc.
- Or any key name supported by the `keyboard` library

## Usage

1. **Start the application**:
   - Run `dictation_app.exe` (or `python dictation_app.py`)
   - The app icon will appear in your system tray

2. **System tray states**:
   - **Gray**: Idle, ready to record
   - **Red**: Recording audio
   - **Orange**: Processing/transcribing

3. **Dictate text**:
   - Open any application where you want to type (Word, Notepad, etc.)
   - Place your cursor where you want the text to appear
   - **Hold down the hotkey** (default: Right Ctrl)
   - Speak clearly into your microphone
   - **Release the hotkey** when done speaking
   - Wait for the transcribed text to appear

4. **System tray menu** (right-click the tray icon):
   - **Reload Dictionary**: Reload custom dictionary without restarting
   - **Reload API Key**: Reload API key without restarting
   - **Settings**: Open settings (coming soon)
   - **About**: Show application information
   - **Exit**: Close the application

## Building Executable

To build a standalone Windows executable:

```bash
python build.py
```

This will create:
- `dist/dictation_app.exe` - Standalone executable
- `dist/DictationApp/` - Folder with all dependencies

You can distribute the entire `dist/DictationApp/` folder or just the executable if you use the `--onefile` option.

## Troubleshooting

### Application won't start
- **Check Python version**: Must be 3.8 or higher
- **Install dependencies**: Run `pip install -r requirements.txt`
- **Administrator rights**: Some hotkeys may require running as administrator

### No transcription happening
- **Verify API key**: Ensure `api_key.txt` contains a valid OpenAI API key
- **Check API credits**: Verify your OpenAI account has available credits
- **Network connection**: Whisper API requires internet connectivity
- **Check console**: Run from command line to see error messages

### Microphone not working
- **Default device**: Ensure your microphone is set as the default recording device in Windows
- **Permissions**: Grant microphone permissions to the application
- **Test recording**: Use Windows Voice Recorder to verify microphone works

### Hotkey not responding
- **Conflicting hotkeys**: Choose a different hotkey if another app uses it
- **Administrator rights**: Some apps require admin rights to receive hotkeys
- **Keyboard library**: Try running as administrator

### Text insertion issues
- **Focus**: Ensure the target application has focus before releasing hotkey
- **Special characters**: Some applications may handle special characters differently
- **Delay**: You may need to adjust `pyautogui.PAUSE` in the code

### Custom dictionary not working
- **Format**: Verify format is `phonetic -> CORRECT` with `->`
- **Reload**: Use "Reload Dictionary" from system tray menu
- **Case sensitivity**: Matching is case-insensitive, check your patterns
- **Encoding**: Ensure file is saved as UTF-8

## Performance Tips

1. **Speak clearly**: Better articulation = better transcription
2. **Pause briefly**: Short pauses help Whisper identify sentence boundaries
3. **Short recordings**: Keep recordings under 30 seconds for faster processing
4. **Good microphone**: Quality microphone significantly improves accuracy
5. **Quiet environment**: Background noise can affect transcription quality

## API Costs

OpenAI Whisper API pricing (as of 2024):
- $0.006 per minute of audio
- Example: 100 minutes of dictation = $0.60

Monitor your usage at: https://platform.openai.com/usage

## Privacy & Security

- **Local processing**: Audio is only sent to OpenAI's Whisper API
- **No storage**: Audio files are temporary and deleted after transcription
- **API key security**: Keep your `api_key.txt` secure and never share it
- **Network only**: The app requires internet only for API calls

## Known Limitations

- **Windows only**: This application is designed specifically for Windows
- **Internet required**: Requires internet connection for Whisper API
- **Hotkey conflicts**: May conflict with other applications using the same hotkey
- **API latency**: Transcription speed depends on internet connection and API response time
- **Language support**: Currently configured for English (can be modified in code)

## Project Structure

```
push-to-talk-whiserai/
├── dictation_app.py          # Main application
├── requirements.txt           # Python dependencies
├── settings.json             # Application settings
├── custom_dictionary.txt     # Custom word mappings
├── api_key.txt              # Your OpenAI API key (not in git)
├── api_key.txt.template     # Template for API key file
├── build.py                 # Build script for creating .exe
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development

### Running in Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python dictation_app.py
```

### Code Structure

- **ConfigManager**: Handles loading configuration files
- **AudioRecorder**: Manages microphone recording
- **WhisperTranscriber**: Interfaces with OpenAI Whisper API
- **DictionaryReplacer**: Applies custom dictionary replacements
- **DictationApp**: Main application orchestration and UI

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[Specify your license here]

## Credits

- OpenAI Whisper API for speech recognition
- Built with Python and various open-source libraries

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Changelog

### Version 1.0.0 (Initial Release)
- Push-to-talk recording with configurable hotkey
- OpenAI Whisper API integration
- Custom dictionary support
- System tray integration
- Works with all Windows applications
- Configuration file support
