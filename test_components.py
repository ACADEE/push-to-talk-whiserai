"""
Component Testing Script
Test individual components of the dictation app
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dictation_app import (
    ConfigManager,
    DictionaryReplacer
)


def test_config_manager():
    """Test configuration loading"""
    print("\n" + "="*60)
    print("Testing ConfigManager")
    print("="*60)

    base_dir = Path(__file__).parent
    config = ConfigManager(base_dir)

    # Test API key loading
    print("\n1. Testing API Key Loading...")
    api_key = config.load_api_key()
    if api_key:
        print(f"   ✓ API key loaded: {api_key[:10]}...")
    else:
        print("   ✗ No API key found (expected if not configured)")

    # Test dictionary loading
    print("\n2. Testing Dictionary Loading...")
    dictionary = config.load_custom_dictionary()
    print(f"   Loaded {len(dictionary)} entries")
    if dictionary:
        print("   Sample entries:")
        for i, (key, value) in enumerate(list(dictionary.items())[:5]):
            print(f"     - '{key}' -> '{value}'")

    # Test settings loading
    print("\n3. Testing Settings Loading...")
    settings = config.load_settings()
    print(f"   Hotkey: {settings.get('hotkey')}")
    print(f"   Sample Rate: {settings.get('sample_rate')}")
    print(f"   Channels: {settings.get('channels')}")

    return config, dictionary


def test_dictionary_replacer(dictionary):
    """Test dictionary replacement logic"""
    print("\n" + "="*60)
    print("Testing DictionaryReplacer")
    print("="*60)

    replacer = DictionaryReplacer(dictionary)

    test_cases = [
        ("This is acadi speaking", "acadi -> ACADEE"),
        ("I work at acady", "acady -> ACADEE"),
        ("Triple A batteries", "triple a -> AAA"),
        ("Jay eff kay airport", "jay eff kay -> JFK"),
        ("I use my sequel database", "my sequel -> MySQL"),
        ("Regular text without replacements", "No replacements"),
    ]

    print("\nTesting replacements:")
    for i, (input_text, description) in enumerate(test_cases, 1):
        output = replacer.apply_replacements(input_text)
        print(f"\n{i}. {description}")
        print(f"   Input:  '{input_text}'")
        print(f"   Output: '{output}'")
        if input_text != output:
            print("   ✓ Replacement applied")
        else:
            print("   - No replacement")


def test_audio_devices():
    """List available audio devices"""
    print("\n" + "="*60)
    print("Testing Audio Devices")
    print("="*60)

    try:
        import sounddevice as sd
        print("\nAvailable audio devices:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"\n{i}. {device['name']}")
                print(f"   Channels: {device['max_input_channels']}")
                print(f"   Sample Rate: {device['default_samplerate']}")

        print(f"\nDefault input device: {sd.query_devices(kind='input')['name']}")

    except Exception as e:
        print(f"Error querying audio devices: {e}")


def test_keyboard_hotkeys():
    """Test keyboard hotkey detection"""
    print("\n" + "="*60)
    print("Testing Keyboard Hotkeys")
    print("="*60)

    try:
        import keyboard

        print("\nPress 'Right Ctrl' to test hotkey detection...")
        print("Press 'Escape' to exit test")

        def on_key(e):
            print(f"Key event: {e.name} - {e.event_type}")

        keyboard.on_press_key('right ctrl', lambda e: on_key(e))
        keyboard.wait('esc')

        print("Hotkey test completed")

    except Exception as e:
        print(f"Error testing hotkeys: {e}")


def run_all_tests():
    """Run all component tests"""
    print("\n" + "="*60)
    print("PUSH-TO-TALK WHISPER DICTATION APP")
    print("Component Test Suite")
    print("="*60)

    try:
        # Test configuration
        config, dictionary = test_config_manager()

        # Test dictionary replacer
        if dictionary:
            test_dictionary_replacer(dictionary)
        else:
            print("\nSkipping dictionary tests (no dictionary loaded)")

        # Test audio devices
        test_audio_devices()

        # Prompt for hotkey test
        print("\n" + "="*60)
        print("\nWould you like to test hotkey detection? (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            test_keyboard_hotkeys()

        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nError during tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
