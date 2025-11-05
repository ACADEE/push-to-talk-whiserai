# Changelog

All notable changes to the Push-to-Talk Whisper Dictation App will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-05

### Added
- Initial release of Push-to-Talk Whisper Dictation App
- Push-to-talk recording with configurable hotkey (default: Right Ctrl)
- OpenAI Whisper API integration for speech-to-text transcription
- Custom dictionary support for phonetic word replacements
- System tray integration with status indicators (idle/recording/processing)
- Universal text insertion works with any Windows application
- Configuration files support:
  - `api_key.txt` for OpenAI API key
  - `custom_dictionary.txt` for custom word mappings
  - `settings.json` for application settings
- Real-time visual feedback via system tray icon colors
- System tray menu with options to reload configuration
- Automatic audio recording and transcription workflow
- Cross-application dictation support (Word, Notepad, browsers, etc.)
- Graceful error handling with user notifications
- Comprehensive documentation (README.md, QUICKSTART.md)
- Build script for creating Windows executable
- Sample configuration templates

### Features in Detail
- **Audio Recording**: High-quality 16kHz mono audio capture
- **Custom Dictionary**: Case-insensitive matching with configurable replacements
- **Hotkey Support**: Configurable hotkey for push-to-talk activation
- **Low Latency**: Optimized for fast transcription and text insertion
- **Background Operation**: Minimal UI, runs in system tray
- **No Data Storage**: Audio files are temporary and deleted after use

### Technical
- Python-based application
- Uses OpenAI Whisper-1 model
- Supports Windows 10 and Windows 11
- Can be built into standalone executable with PyInstaller

### Documentation
- Complete installation guide
- Quick start guide for new users
- Troubleshooting section
- API cost information
- Privacy and security notes

## [Unreleased]

### Planned Features
- Settings dialog UI for easier configuration
- Audio feedback (beep on recording start/stop)
- Transcription preview before insertion
- Multiple dictionary file support
- Undo last dictation command
- Multi-language support
- Keyboard shortcut customization UI
- Audio device selection UI
- Usage statistics and logging
- Auto-update functionality

### Known Issues
- Settings menu item opens notification (UI not yet implemented)
- Requires administrator privileges for hotkeys in some applications
- May have conflicts with other apps using the same hotkey
- Limited to English language in current version

## [Future Versions]

### Roadmap
- Version 1.1: Settings UI implementation
- Version 1.2: Multi-language support
- Version 1.3: Advanced dictionary features
- Version 2.0: Offline mode with local Whisper model

---

For detailed changes in each version, see the [releases page](https://github.com/yourusername/push-to-talk-whiserai/releases).
