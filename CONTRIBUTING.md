# Contributing to Push-to-Talk Whisper Dictation App

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Windows 10/11 for testing (or Windows VM)
- OpenAI API key for testing

### Development Setup

1. **Fork the repository**

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/push-to-talk-whiserai.git
   cd push-to-talk-whiserai
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**:
   ```bash
   cp api_key.txt.template api_key.txt
   # Edit api_key.txt with your API key
   ```

5. **Run the application**:
   ```bash
   python dictation_app.py
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

**Good bug reports include**:
- Clear, descriptive title
- Exact steps to reproduce
- Expected vs actual behavior
- System information (Windows version, Python version)
- Screenshots if applicable
- Error messages or logs

**Template**:
```markdown
**Description**
A clear description of the bug.

**To Reproduce**
1. Step one
2. Step two
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: Windows 10/11
- Python Version: 3.x
- App Version: 1.0.0

**Additional Context**
Any other relevant information.
```

### Suggesting Features

Feature suggestions are welcome! Please:
- Check if the feature is already planned (see CHANGELOG.md)
- Explain the use case and benefits
- Provide examples of how it would work

### Pull Requests

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, commented code
   - Follow the existing code style
   - Update documentation as needed

3. **Test your changes**:
   - Test on Windows
   - Verify all existing features still work
   - Test edge cases

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Provide a clear description
   - Reference any related issues
   - Include screenshots if UI changes

## Code Style

### Python Style Guide

Follow PEP 8 guidelines:
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names
- Add docstrings to classes and functions

**Example**:
```python
def transcribe_audio(audio_file_path: str) -> Optional[str]:
    """
    Transcribe audio file using Whisper API.

    Args:
        audio_file_path: Path to the audio file

    Returns:
        Transcribed text or None if failed
    """
    # Implementation
    pass
```

### Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Add inline comments for complex logic
- Include docstrings for all public functions

## Project Structure

```
push-to-talk-whiserai/
├── dictation_app.py          # Main application file
│   ├── ConfigManager          # Configuration handling
│   ├── AudioRecorder          # Audio recording
│   ├── WhisperTranscriber    # API integration
│   ├── DictionaryReplacer    # Text replacement
│   └── DictationApp          # Main orchestration
├── build.py                   # Build script
├── requirements.txt           # Dependencies
├── settings.json             # User settings
├── custom_dictionary.txt     # User dictionary
└── README.md                 # Documentation
```

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] App starts without errors
- [ ] System tray icon appears
- [ ] Recording starts on hotkey press
- [ ] Recording stops on hotkey release
- [ ] Transcription completes successfully
- [ ] Text inserts into active application
- [ ] Custom dictionary replacements work
- [ ] Configuration reload functions work
- [ ] Error handling works (invalid API key, no internet, etc.)
- [ ] App exits cleanly

### Test Cases to Consider

1. **Audio Recording**:
   - Very short recordings (< 1 second)
   - Long recordings (> 30 seconds)
   - No audio input
   - Multiple rapid recordings

2. **API Integration**:
   - Invalid API key
   - Network disconnection
   - API rate limits
   - Large audio files

3. **Dictionary**:
   - Case sensitivity
   - Multi-word phrases
   - Overlapping patterns
   - Empty dictionary
   - Malformed entries

4. **Hotkeys**:
   - Different hotkey combinations
   - Hotkey conflicts
   - Rapid press/release
   - Holding for extended time

## Areas for Contribution

### High Priority

- [ ] Settings UI implementation
- [ ] Audio device selection UI
- [ ] Transcription preview feature
- [ ] Automated tests
- [ ] Error handling improvements

### Medium Priority

- [ ] Multi-language support
- [ ] Audio feedback (beeps)
- [ ] Undo last dictation
- [ ] Usage logging/statistics
- [ ] Performance optimizations

### Low Priority

- [ ] Custom icon design
- [ ] Installer creation
- [ ] Auto-update functionality
- [ ] Plugin system
- [ ] Cloud dictionary sync

### Documentation

- [ ] Video tutorials
- [ ] FAQ section
- [ ] Advanced configuration guide
- [ ] Developer API documentation
- [ ] Localization/translation

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment.

### Our Standards

**Positive behavior**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior**:
- Trolling, insulting, or derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
