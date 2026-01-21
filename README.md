# Push-to-Talk Whisper AI Dictation App

A Windows desktop application that enables voice-to-text dictation directly into any active application using OpenAI's Whisper AI for speech recognition.

## Features

- **Push-to-Talk Recording**: Hold a configurable hotkey to record audio, release to transcribe
- **Multi-Language Translation**: Speak in French and get output in French, English, German, Spanish, or Italian
- **Universal Compatibility**: Works with any Windows application (Word, Notepad, browsers, etc.)
- **Custom Dictionary**: Define custom phonetic mappings for specialized terms, acronyms, and brand names
- **System Tray Integration**: Minimal UI that runs in the background with language selection menu
- **Real-time Feedback**: Visual indicators for recording and processing states
- **OpenAI Whisper API**: Industry-leading speech recognition accuracy
- **Smart Translation**: Powered by GPT-4o-mini for natural, context-aware translations

## Requirements

- Windows 10 or Windows 11
- Python 3.8 or higher (for running from source)
- OpenAI API key with access to Whisper API
- Microphone connected to your computer

## Installation

> **Windows Users:** For detailed Windows installation instructions and troubleshooting (especially if you encounter MySQL-python errors), see [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md)

### Option 1: Run from Source (Development)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd push-to-talk-whiserai
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**:
   - Copy `api_key.txt.template` to `api_key.txt`
   - Edit `api_key.txt` and paste your OpenAI API key
   - Get your API key from: https://platform.openai.com/api-keys

5. **Run the application**:
   ```bash
   python dictation_app.py
   ```

### Option 2: Use Pre-built Executable (Production)

1. Download the latest release from the releases page
2. Extract the ZIP file to a folder of your choice
3. Follow instructions in `SETUP.txt`
4. Configure your API key
5. Run `DictationApp.exe`

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
  "audio_device": null,
  "output_language": "fr"
}
```

**Available settings**:
- **hotkey**: The key to press for recording
  - `right ctrl` or `left ctrl`
  - `right shift` or `left shift`
  - `right alt` or `left alt`
  - Function keys: `f1`, `f2`, etc.
  - Or any key name supported by the `keyboard` library
- **output_language**: Language for the transcribed text (default: `fr`)
  - `fr` - Français (no translation)
  - `en` - English
  - `de` - Deutsch (German)
  - `es` - Español (Spanish)
  - `it` - Italiano (Italian)

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
   - **Output Language**: Select your desired output language
     - Français (FR) - Speak and output in French (no translation)
     - English (EN) - Speak in French, output in English
     - Deutsch (DE) - Speak in French, output in German
     - Español (ES) - Speak in French, output in Spanish
     - Italiano (IT) - Speak in French, output in Italian
   - **Reload Dictionary**: Reload custom dictionary without restarting
   - **Reload API Key**: Reload API key without restarting
   - **About**: Show application information and current language
   - **Exit**: Close the application

## Building Executable

To build a standalone Windows executable:

1. **Install dependencies** (including PyInstaller):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script**:
   ```bash
   python build.py
   ```

3. **Find your built application**:
   ```
   dist/DictationApp/
   ├── DictationApp.exe          # Main executable
   ├── SETUP.txt                  # Setup instructions
   ├── README.md                  # Documentation
   ├── api_key.txt.template       # Rename and add your API key
   ├── custom_dictionary.txt      # Word mappings
   ├── settings.json              # Settings
   └── [dependency files]         # Required DLLs
   ```

4. **Distribute the entire `dist/DictationApp/` folder**
   - Zip the folder for easy sharing
   - Users extract and follow `SETUP.txt`
   - They add their own API key
   - Run `DictationApp.exe`

**Note:** The build uses `--onedir` mode (not `--onefile`) to ensure config files are easily accessible and editable by users.

## Troubleshooting

> **Windows Users:** For comprehensive troubleshooting, see [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md)

### Application won't start
- **Check Python version**: Must be 3.8 or higher
- **Install dependencies**: Run `pip install -r requirements.txt`
- **Virtual environment**: Use a clean virtual environment to avoid conflicts
- **Administrator rights**: Some hotkeys may require running as administrator

### MySQL-python or config-win.h Error
⚠️ **This is NOT a dependency of this project!**

If you see errors about `MySQL-python` or `config-win.h`:
1. Verify you're in the correct directory (should contain `dictation_app.py`)
2. Check your `requirements.txt` - it should NOT contain `MySQL-python`
3. Create a fresh virtual environment:
   ```bash
   python -m venv venv_clean
   venv_clean\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
4. See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed solutions

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

OpenAI API pricing (as of 2024):
- **Whisper API**: $0.006 per minute of audio
- **GPT-4o-mini** (for translation): ~$0.00015 per request (input) + ~$0.0006 per response (output)
- Example costs:
  - 100 minutes of French dictation (no translation): ~$0.60
  - 100 minutes with translation to English: ~$0.60 + ~$0.08 = ~$0.68

Monitor your usage at: https://platform.openai.com/usage

## Privacy & Security

- **Local processing**: Audio is only sent to OpenAI's Whisper API
- **No storage**: Audio files are temporary and deleted after transcription
- **API key security**: Keep your `api_key.txt` secure and never share it
- **Network only**: The app requires internet only for API calls

## Known Limitations

- **Windows only**: This application is designed specifically for Windows
- **Internet required**: Requires internet connection for Whisper API and translation
- **Hotkey conflicts**: May conflict with other applications using the same hotkey
- **API latency**: Transcription and translation speed depends on internet connection and API response time
- **Input language**: Currently configured for French audio input (Whisper transcription)
- **Translation quality**: Translation quality depends on context and may vary

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
- **WhisperTranscriber**: Interfaces with OpenAI Whisper API for speech-to-text
- **Translator**: Handles translation using OpenAI GPT-4o-mini API
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

### Version 1.1.1 (Build & Installation Update)
- Improved build.py script for better .exe generation
  - Changed to --onedir mode for easier config file access
  - Added --add-data flags to include config files
  - Enhanced SETUP.txt with detailed instructions
  - Better build output and file organization
- Added comprehensive INSTALL_WINDOWS.md guide
  - Detailed troubleshooting for MySQL-python error
  - Step-by-step installation instructions
  - Virtual environment setup guide
  - Build and distribution instructions
- Updated README.md with build and installation improvements
- Config files (api_key.txt, custom_dictionary.txt, settings.json) are now easily accessible in built .exe

### Version 1.1.0 (Translation Update)
- Added multi-language translation support (French to EN/DE/ES/IT)
- Output language selection via system tray menu
- GPT-4o-mini integration for natural translations
- Updated settings.json with output_language parameter
- Enhanced system tray menu with language options
- Real-time language switching without restart

### Version 1.0.0 (Initial Release)
- Push-to-talk recording with configurable hotkey
- OpenAI Whisper API integration
- Custom dictionary support
- System tray integration
- Works with all Windows applications
- Configuration file support
