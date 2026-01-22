"""
Push-to-Talk Whisper AI Dictation App
A Windows desktop application for voice-to-text dictation using OpenAI's Whisper API
"""

import os
import sys
import threading
import wave
import tempfile
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple

import sounddevice as sd
import numpy as np
import pystray
from PIL import Image, ImageDraw
import keyboard
import pyautogui
from openai import OpenAI


class ConfigManager:
    """Handles loading and managing configuration files"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.api_key_file = base_dir / "api_key.txt"
        self.dictionary_file = base_dir / "custom_dictionary.txt"
        self.settings_file = base_dir / "settings.json"
        self.translation_prompt_file = base_dir / "translation_prompt.txt"

    def load_api_key(self) -> Optional[str]:
        """Load OpenAI API key from file"""
        try:
            if self.api_key_file.exists():
                with open(self.api_key_file, 'r') as f:
                    key = f.read().strip()
                    if key:
                        return key
            return None
        except Exception as e:
            print(f"Error loading API key: {e}")
            return None

    def load_custom_dictionary(self) -> Dict[str, str]:
        """Load custom dictionary mappings from file"""
        dictionary = {}
        try:
            if self.dictionary_file.exists():
                with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and '->' in line:
                            # Split on -> and clean up whitespace
                            parts = line.split('->')
                            if len(parts) == 2:
                                phonetic = parts[0].strip().lower()
                                correct = parts[1].strip()
                                dictionary[phonetic] = correct
            return dictionary
        except Exception as e:
            print(f"Error loading custom dictionary: {e}")
            return {}

    def load_settings(self) -> Dict:
        """Load application settings"""
        default_settings = {
            "hotkey": "right ctrl",
            "sample_rate": 16000,
            "channels": 1,
            "audio_device": None,
            "input_language": "fr",  # Language spoken (for Whisper transcription)
            "output_language": "fr"  # Language for text output (with translation if different)
        }

        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults
                    default_settings.update(settings)
        except Exception as e:
            print(f"Error loading settings: {e}")

        return default_settings

    def save_settings(self, settings: Dict):
        """Save application settings"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_translation_prompt(self) -> str:
        """Load custom translation prompt from file"""
        default_prompt = "You are a professional translator. Translate the following text from {source_language} to {target_language} accurately and naturally. Only provide the translation, nothing else."

        try:
            if self.translation_prompt_file.exists():
                with open(self.translation_prompt_file, 'r', encoding='utf-8') as f:
                    prompt = f.read().strip()
                    if prompt:
                        return prompt
        except Exception as e:
            print(f"Error loading translation prompt: {e}")

        return default_prompt


class AudioRecorder:
    """Handles audio recording from microphone"""

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.frames = []

    def start_recording(self):
        """Start recording audio"""
        self.recording = True
        self.frames = []

        def callback(indata, frames, time, status):
            if status:
                print(f"Audio callback status: {status}")
            if self.recording:
                self.frames.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback,
            dtype=np.float32
        )
        self.stream.start()

    def stop_recording(self) -> Optional[str]:
        """Stop recording and save to temporary file"""
        self.recording = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()

        if not self.frames:
            return None

        # Combine all frames
        audio_data = np.concatenate(self.frames, axis=0)

        # Convert to 16-bit PCM
        audio_data = (audio_data * 32767).astype(np.int16)

        # Save to temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()

        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

        return temp_file.name


class WhisperTranscriber:
    """Handles transcription using OpenAI Whisper API"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, audio_file_path: str, language: str = "fr") -> Optional[str]:
        """Transcribe audio file using Whisper API"""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            return transcript.text
        except Exception as e:
            print(f"Transcription error: {e}")
            return None


class Translator:
    """Handles text translation using OpenAI GPT API"""

    # Language code mapping
    LANGUAGES = {
        "fr": "French",
        "en": "English",
        "de": "German",
        "es": "Spanish",
        "it": "Italian"
    }

    def __init__(self, api_key: str, custom_prompt: str = None):
        self.client = OpenAI(api_key=api_key)
        self.custom_prompt = custom_prompt

    def translate(self, text: str, source_lang: str = "fr", target_lang: str = "en") -> Optional[str]:
        """Translate text from source language to target language"""
        # If source and target are the same, no translation needed
        if source_lang == target_lang:
            return text

        try:
            source_name = self.LANGUAGES.get(source_lang, source_lang)
            target_name = self.LANGUAGES.get(target_lang, target_lang)

            # Use custom prompt if available, otherwise use default
            if self.custom_prompt:
                system_prompt = self.custom_prompt.format(
                    source_language=source_name,
                    target_language=target_name
                )
            else:
                system_prompt = f"You are a professional translator. Translate from {source_name} to {target_name} accurately and naturally."

            user_prompt = f"Translate the following text from {source_name} to {target_name}. Only provide the translation, nothing else:\n\n{text}"

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using mini model for cost efficiency
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            translated_text = response.choices[0].message.content.strip()
            return translated_text

        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails


class DictionaryReplacer:
    """Handles custom dictionary replacements"""

    def __init__(self, dictionary: Dict[str, str]):
        self.dictionary = dictionary

    def apply_replacements(self, text: str) -> str:
        """Apply custom dictionary replacements to text"""
        if not self.dictionary or not text:
            return text

        # Work with lowercase for matching but preserve original case structure
        result = text

        # Sort by length (longest first) to handle multi-word phrases
        sorted_patterns = sorted(self.dictionary.items(),
                                key=lambda x: len(x[0]),
                                reverse=True)

        for phonetic, correct in sorted_patterns:
            # Case-insensitive search and replace
            # Use word boundaries to avoid partial matches
            import re
            pattern = re.compile(re.escape(phonetic), re.IGNORECASE)
            result = pattern.sub(correct, result)

        return result


class DictationApp:
    """Main application class"""

    def __init__(self):
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.config_manager = ConfigManager(self.base_dir)

        # Load configuration
        self.api_key = None
        self.custom_dictionary = {}
        self.settings = {}
        self.translation_prompt = None
        self.reload_configuration()

        # Initialize components
        self.audio_recorder = None
        self.transcriber = None
        self.translator = None
        self.dictionary_replacer = None
        self.initialize_components()

        # State management
        self.is_recording = False
        self.is_processing = False
        self.hotkey_pressed = False

        # System tray
        self.icon = None

    def reload_configuration(self):
        """Reload all configuration files"""
        self.api_key = self.config_manager.load_api_key()
        self.custom_dictionary = self.config_manager.load_custom_dictionary()
        self.settings = self.config_manager.load_settings()
        self.translation_prompt = self.config_manager.load_translation_prompt()

        print(f"Loaded {len(self.custom_dictionary)} dictionary entries")
        print(f"Hotkey: {self.settings.get('hotkey', 'right ctrl')}")
        print(f"Input language: {self.settings.get('input_language', 'fr')} → Output language: {self.settings.get('output_language', 'fr')}")

    def initialize_components(self):
        """Initialize application components"""
        if self.api_key:
            self.transcriber = WhisperTranscriber(self.api_key)
            self.translator = Translator(self.api_key, custom_prompt=self.translation_prompt)
        else:
            print("WARNING: No API key found. Transcription will not work.")

        self.dictionary_replacer = DictionaryReplacer(self.custom_dictionary)
        self.audio_recorder = AudioRecorder(
            sample_rate=self.settings.get('sample_rate', 16000),
            channels=self.settings.get('channels', 1)
        )

    def create_icon_image(self, state: str = "idle") -> Image.Image:
        """Create system tray icon based on state with improved visibility"""
        size = (64, 64)
        image = Image.new('RGBA', size, color=(0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        if state == "idle":
            # Gray microphone icon
            draw.ellipse([16, 16, 48, 48], fill=(100, 100, 100), outline=(60, 60, 60), width=2)
            # Small mic detail
            draw.ellipse([28, 24, 36, 40], fill=(200, 200, 200))

        elif state == "recording":
            # Bright red pulsing circle - VERY VISIBLE
            draw.ellipse([4, 4, 60, 60], fill=(255, 0, 0), outline=(180, 0, 0), width=3)
            # White recording dot in center
            draw.ellipse([24, 24, 40, 40], fill=(255, 255, 255))
            # Add small text "REC"
            try:
                # Simple visual indicator without font
                draw.rectangle([20, 48, 44, 56], fill=(255, 255, 255))
            except:
                pass

        elif state == "processing":
            # Orange processing indicator
            draw.ellipse([12, 12, 52, 52], fill=(255, 165, 0), outline=(200, 120, 0), width=2)
            # Rotating effect with arcs
            draw.arc([16, 16, 48, 48], 0, 270, fill=(255, 215, 0), width=4)

        return image

    def update_icon_state(self, state: str):
        """Update system tray icon to reflect current state"""
        if self.icon:
            self.icon.icon = self.create_icon_image(state)

    def on_hotkey_press(self, event):
        """Handle hotkey press event"""
        if not self.hotkey_pressed and not self.is_processing:
            self.hotkey_pressed = True
            self.start_recording()

    def on_hotkey_release(self, event):
        """Handle hotkey release event"""
        if self.hotkey_pressed:
            self.hotkey_pressed = False
            self.stop_recording()

    def start_recording(self):
        """Start audio recording"""
        if self.is_recording or self.is_processing:
            return

        print("Starting recording...")
        self.is_recording = True
        self.update_icon_state("recording")
        self.audio_recorder.start_recording()

    def stop_recording(self):
        """Stop recording and process audio"""
        if not self.is_recording:
            return

        print("Stopping recording...")
        self.is_recording = False
        self.update_icon_state("processing")

        # Process in background thread to avoid blocking
        thread = threading.Thread(target=self.process_audio)
        thread.daemon = True
        thread.start()

    def process_audio(self):
        """Process recorded audio and insert transcribed text"""
        self.is_processing = True

        try:
            # Stop recording and get audio file
            audio_file = self.audio_recorder.stop_recording()

            if not audio_file:
                print("No audio recorded")
                return

            # Check if transcriber is available
            if not self.transcriber:
                self.show_notification("Error", "API key not configured")
                return

            # Transcribe audio using configured input language
            input_language = self.settings.get('input_language', 'fr')
            print(f"Transcribing audio (language: {input_language})...")
            text = self.transcriber.transcribe(audio_file, language=input_language)

            # Clean up temp file
            try:
                os.unlink(audio_file)
            except:
                pass

            if not text:
                print("No transcription received")
                return

            print(f"Original transcription: {text}")

            # Apply custom dictionary replacements
            corrected_text = self.dictionary_replacer.apply_replacements(text)
            print(f"After dictionary: {corrected_text}")

            # Translate to output language if needed
            input_language = self.settings.get('input_language', 'fr')
            output_language = self.settings.get('output_language', 'fr')
            if output_language != input_language and self.translator:
                print(f"Translating from {input_language} to {output_language}...")
                translated_text = self.translator.translate(corrected_text, source_lang=input_language, target_lang=output_language)
                print(f"After translation: {translated_text}")
                final_text = translated_text
            else:
                final_text = corrected_text

            # Insert text into active application
            self.insert_text(final_text)

        except Exception as e:
            print(f"Error processing audio: {e}")
            self.show_notification("Error", f"Failed to process: {str(e)}")

        finally:
            self.is_processing = False
            self.update_icon_state("idle")

    def insert_text(self, text: str):
        """Insert text into the active application"""
        try:
            # Small delay to ensure focus is correct
            pyautogui.PAUSE = 0.01

            # Type the text
            pyautogui.write(text, interval=0.01)

        except Exception as e:
            print(f"Error inserting text: {e}")

    def show_notification(self, title: str, message: str):
        """Show system notification"""
        if self.icon:
            self.icon.notify(title=title, message=message)

    def setup_hotkey(self):
        """Setup keyboard hotkey listener"""
        hotkey = self.settings.get('hotkey', 'right ctrl')

        try:
            # Register hotkey
            keyboard.on_press_key(hotkey, self.on_hotkey_press)
            keyboard.on_release_key(hotkey, self.on_hotkey_release)
            print(f"Hotkey registered: {hotkey}")
        except Exception as e:
            print(f"Error setting up hotkey: {e}")

    def create_menu(self):
        """Create system tray menu"""
        # Get current languages for checkmarks
        current_input_lang = self.settings.get('input_language', 'fr')
        current_output_lang = self.settings.get('output_language', 'fr')

        # Create input language submenu
        input_language_menu = pystray.Menu(
            pystray.MenuItem(
                "Français (FR)" + (" ✓" if current_input_lang == "fr" else ""),
                lambda: self.set_input_language("fr")
            ),
            pystray.MenuItem(
                "English (EN)" + (" ✓" if current_input_lang == "en" else ""),
                lambda: self.set_input_language("en")
            ),
            pystray.MenuItem(
                "Deutsch (DE)" + (" ✓" if current_input_lang == "de" else ""),
                lambda: self.set_input_language("de")
            ),
            pystray.MenuItem(
                "Español (ES)" + (" ✓" if current_input_lang == "es" else ""),
                lambda: self.set_input_language("es")
            ),
            pystray.MenuItem(
                "Italiano (IT)" + (" ✓" if current_input_lang == "it" else ""),
                lambda: self.set_input_language("it")
            )
        )

        # Create output language submenu
        output_language_menu = pystray.Menu(
            pystray.MenuItem(
                "Français (FR)" + (" ✓" if current_output_lang == "fr" else ""),
                lambda: self.set_output_language("fr")
            ),
            pystray.MenuItem(
                "English (EN)" + (" ✓" if current_output_lang == "en" else ""),
                lambda: self.set_output_language("en")
            ),
            pystray.MenuItem(
                "Deutsch (DE)" + (" ✓" if current_output_lang == "de" else ""),
                lambda: self.set_output_language("de")
            ),
            pystray.MenuItem(
                "Español (ES)" + (" ✓" if current_output_lang == "es" else ""),
                lambda: self.set_output_language("es")
            ),
            pystray.MenuItem(
                "Italiano (IT)" + (" ✓" if current_output_lang == "it" else ""),
                lambda: self.set_output_language("it")
            )
        )

        return pystray.Menu(
            pystray.MenuItem("Input Language (Speech)", input_language_menu),
            pystray.MenuItem("Output Language (Text)", output_language_menu),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Reload Dictionary", self.menu_reload_dictionary),
            pystray.MenuItem("Reload API Key", self.menu_reload_api_key),
            pystray.MenuItem("About", self.menu_about),
            pystray.MenuItem("Exit", self.menu_exit)
        )

    def menu_reload_dictionary(self):
        """Reload custom dictionary"""
        self.custom_dictionary = self.config_manager.load_custom_dictionary()
        self.dictionary_replacer = DictionaryReplacer(self.custom_dictionary)
        self.show_notification("Dictionary Reloaded",
                             f"Loaded {len(self.custom_dictionary)} entries")

    def menu_reload_api_key(self):
        """Reload API key and translation prompt"""
        self.api_key = self.config_manager.load_api_key()
        self.translation_prompt = self.config_manager.load_translation_prompt()
        if self.api_key:
            self.transcriber = WhisperTranscriber(self.api_key)
            self.translator = Translator(self.api_key, custom_prompt=self.translation_prompt)
            self.show_notification("Configuration Reloaded", "API key and prompts loaded successfully")
        else:
            self.show_notification("Error", "Failed to load API key")

    def set_input_language(self, language_code: str):
        """Set the input language (speech) and save to settings"""
        self.settings['input_language'] = language_code
        self.config_manager.save_settings(self.settings)

        language_names = {
            "fr": "Français",
            "en": "English",
            "de": "Deutsch",
            "es": "Español",
            "it": "Italiano"
        }

        language_name = language_names.get(language_code, language_code)
        self.show_notification(
            "Input Language Changed",
            f"Speech language set to {language_name}"
        )

        # Recreate menu to update checkmarks
        if self.icon:
            self.icon.menu = self.create_menu()

    def set_output_language(self, language_code: str):
        """Set the output language (text) and save to settings"""
        self.settings['output_language'] = language_code
        self.config_manager.save_settings(self.settings)

        language_names = {
            "fr": "Français",
            "en": "English",
            "de": "Deutsch",
            "es": "Español",
            "it": "Italiano"
        }

        language_name = language_names.get(language_code, language_code)
        self.show_notification(
            "Output Language Changed",
            f"Text output language set to {language_name}"
        )

        # Recreate menu to update checkmarks
        if self.icon:
            self.icon.menu = self.create_menu()

    def menu_about(self):
        """Show about information"""
        input_lang = self.settings.get('input_language', 'fr')
        output_lang = self.settings.get('output_language', 'fr')
        lang_names = {"fr": "FR", "en": "EN", "de": "DE", "es": "ES", "it": "IT"}
        self.show_notification(
            "Push-to-Talk Whisper Dictation",
            f"Voice-to-text with translation\nInput: {lang_names.get(input_lang, input_lang)} → Output: {lang_names.get(output_lang, output_lang)}"
        )

    def menu_exit(self):
        """Exit application"""
        self.icon.stop()

    def run(self):
        """Run the application"""
        # Validate configuration
        if not self.api_key:
            print("ERROR: API key not found in api_key.txt")
            print("Please create api_key.txt with your OpenAI API key")

        # Setup hotkey
        self.setup_hotkey()

        # Create system tray icon
        self.icon = pystray.Icon(
            "dictation_app",
            self.create_icon_image("idle"),
            "Whisper Dictation App",
            self.create_menu()
        )

        print("Application started. Press hotkey to start dictation.")

        # Run system tray (this blocks)
        self.icon.run()


def main():
    """Main entry point"""
    app = DictationApp()
    app.run()


if __name__ == "__main__":
    main()
