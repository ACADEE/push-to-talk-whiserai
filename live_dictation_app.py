"""
Live Dictation App - Continuous Speech-to-Text with Whisper AI
Types transcribed text directly into any active application (Word, Notepad, etc.)
WITH AUDIO LEVEL METER AND START/STOP BUTTON
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import wave
import tempfile
import os
from datetime import datetime
from pathlib import Path
import sounddevice as sd
import numpy as np
import pyautogui
import pyperclip
import keyboard
from openai import OpenAI


class LiveDictationApp:
    """Main live dictation application with GUI and audio level meter"""

    def __init__(self, root):
        self.root = root
        self.root.title("Live Dictation - Whisper AI")
        self.root.geometry("580x650")
        self.root.resizable(True, True)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Get application directory
        self.app_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.api_key_file = self.app_dir / "api_key.txt"
        self.mic_config_file = self.app_dir / "microphone.txt"

        # State variables
        self.is_recording = False
        self.is_hotkey_active = False
        self.recording_thread = None
        self.api_key = None
        self.client = None
        self.audio_frames = []
        self.sample_rate = 16000
        self.stream = None
        self.selected_device = None
        self.current_audio_level = 0
        self.level_update_running = False
        self.selected_language = "fr"  # Default: French
        self.hotkey_combination = "ctrl+shift"  # Default hotkey
        self.hotkey_hook = None  # Store the hotkey hook
        self.recording_mode = "push-to-talk"  # "push-to-talk" or "live"
        self.live_recording_enabled = False  # For live mode

        # Cost tracking variables
        self.total_cost = 0.0
        self.price_per_second = 0.0001  # Default: $0.0001 per second
        self.prompt_text = ""  # Prompt for improving transcription quality

        # Setup GUI
        self.setup_gui()

        # Load saved API key
        self.load_api_key()

        # Load available audio devices
        self.load_audio_devices()

        # Start audio level monitoring
        self.start_level_monitoring()

        # Register push-to-talk hotkey
        self.register_hotkey()

    def setup_gui(self):
        """Setup the GUI components"""

        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create canvas and scrollbar
        canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)

        # Create scrollable frame
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Main container with padding (now inside scrollable frame)
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        scrollable_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Store canvas for later use
        self.canvas = canvas

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Live Dictation App",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Cost Display Section
        cost_frame = ttk.LabelFrame(main_frame, text="API Usage Cost", padding="15")
        cost_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        cost_frame.columnconfigure(0, weight=1)

        self.cost_label = ttk.Label(
            cost_frame,
            text="Total Cost: $0.0000",
            font=('Arial', 14, 'bold'),
            foreground='green'
        )
        self.cost_label.grid(row=0, column=0, pady=5)

        # Price Configuration Section
        price_frame = ttk.LabelFrame(main_frame, text="Price Configuration", padding="15")
        price_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        price_frame.columnconfigure(0, weight=1)

        ttk.Label(price_frame, text="Price per second (USD):").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.price_entry = ttk.Entry(price_frame, width=20)
        self.price_entry.insert(0, "0.0001")  # Default price
        self.price_entry.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)

        def update_price():
            try:
                new_price = float(self.price_entry.get())
                if new_price >= 0:
                    self.price_per_second = new_price
                else:
                    messagebox.showerror("Error", "Price must be a positive number")
                    self.price_entry.delete(0, tk.END)
                    self.price_entry.insert(0, str(self.price_per_second))
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, str(self.price_per_second))

        self.price_entry.bind('<Return>', lambda e: update_price())

        update_price_button = ttk.Button(
            price_frame,
            text="Update Price",
            command=update_price
        )
        update_price_button.grid(row=2, column=0, pady=5)

        ttk.Label(
            price_frame,
            text="Note: Whisper API charges $0.006 per minute = $0.0001 per second",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=3, column=0, pady=5)

        # Recording Mode Selection Section
        mode_frame = ttk.LabelFrame(main_frame, text="Recording Mode", padding="15")
        mode_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        mode_frame.columnconfigure(0, weight=1)

        ttk.Label(
            mode_frame,
            text="Choose your recording method:",
            font=('Arial', 9)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Mode selection with radio buttons
        self.mode_var = tk.StringVar(value="push-to-talk")

        push_to_talk_radio = ttk.Radiobutton(
            mode_frame,
            text="🎯 Push-to-Talk (Hold hotkey to record)",
            variable=self.mode_var,
            value="push-to-talk",
            command=self.on_mode_changed
        )
        push_to_talk_radio.grid(row=1, column=0, sticky=tk.W, pady=5)

        live_radio = ttk.Radiobutton(
            mode_frame,
            text="🔴 Live Mode (Always listening, API only when speaking)",
            variable=self.mode_var,
            value="live",
            command=self.on_mode_changed
        )
        live_radio.grid(row=2, column=0, sticky=tk.W, pady=5)

        # Start/Stop button for live mode (initially hidden)
        self.live_control_button = ttk.Button(
            mode_frame,
            text="▶ START LIVE MODE",
            command=self.toggle_live_mode
        )
        # Don't grid it yet, will show when live mode is selected

        # API Key Section
        api_frame = ttk.LabelFrame(main_frame, text="OpenAI Configuration", padding="15")
        api_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        api_frame.columnconfigure(0, weight=1)

        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.api_key_entry = ttk.Entry(api_frame, width=40, show="*")
        self.api_key_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        self.save_api_button = ttk.Button(
            api_frame,
            text="Save API Key",
            command=self.save_api_key
        )
        self.save_api_button.grid(row=2, column=0, pady=5)

        # Prompt Section (for improving transcription quality)
        prompt_frame = ttk.LabelFrame(main_frame, text="Transcription Quality Prompt (Optional)", padding="15")
        prompt_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        prompt_frame.columnconfigure(0, weight=1)

        ttk.Label(
            prompt_frame,
            text="Enter context to improve transcription quality:",
            font=('Arial', 9)
        ).grid(row=0, column=0, sticky=tk.W, pady=5)

        ttk.Label(
            prompt_frame,
            text='Example: "La conversation suivante est une dictée d\'un avocat pour la constitution d\'un dossier client."',
            font=('Arial', 8),
            foreground='gray',
            wraplength=500
        ).grid(row=1, column=0, sticky=tk.W, pady=5)

        # Create a Text widget for multi-line prompt input
        self.prompt_text_widget = tk.Text(
            prompt_frame,
            height=3,
            width=60,
            wrap=tk.WORD,
            font=('Arial', 9)
        )
        self.prompt_text_widget.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        # Scrollbar for the text widget
        prompt_scrollbar = ttk.Scrollbar(prompt_frame, orient="vertical", command=self.prompt_text_widget.yview)
        self.prompt_text_widget.configure(yscrollcommand=prompt_scrollbar.set)

        def update_prompt():
            self.prompt_text = self.prompt_text_widget.get("1.0", tk.END).strip()

        # Update prompt on any key release
        self.prompt_text_widget.bind('<KeyRelease>', lambda e: update_prompt())

        # Microphone Selection Section
        mic_frame = ttk.LabelFrame(main_frame, text="Microphone Selection", padding="15")
        mic_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        # Store the mode_frame for later use in on_mode_changed
        self.mode_frame = mode_frame
        mic_frame.columnconfigure(0, weight=1)

        ttk.Label(mic_frame, text="Select Microphone:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.mic_combo = ttk.Combobox(mic_frame, state="readonly", width=37)
        self.mic_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        self.mic_combo.bind('<<ComboboxSelected>>', self.on_mic_changed)

        refresh_button = ttk.Button(
            mic_frame,
            text="🔄 Refresh Devices",
            command=self.load_audio_devices
        )
        refresh_button.grid(row=2, column=0, pady=5)

        # Language Selection Section
        lang_frame = ttk.LabelFrame(main_frame, text="Language Selection", padding="15")
        lang_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        lang_frame.columnconfigure(0, weight=1)

        ttk.Label(lang_frame, text="Dictation Language:").grid(row=0, column=0, sticky=tk.W, pady=5)

        # Language options
        languages = [
            ("Français", "fr"),
            ("English", "en"),
            ("Deutsch", "de"),
            ("Español", "es"),
            ("Italiano", "it")
        ]

        self.language_combo = ttk.Combobox(lang_frame, state="readonly", width=37)
        self.language_combo['values'] = [lang[0] for lang in languages]
        self.language_combo.current(0)  # Default: Français
        self.language_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Store language codes
        self.language_codes = {lang[0]: lang[1] for lang in languages}

        def on_language_changed(event=None):
            selected = self.language_combo.get()
            self.selected_language = self.language_codes[selected]

        self.language_combo.bind('<<ComboboxSelected>>', on_language_changed)

        # Hotkey Configuration Section
        hotkey_frame = ttk.LabelFrame(main_frame, text="Push-to-Talk Hotkey", padding="15")
        hotkey_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        hotkey_frame.columnconfigure(0, weight=1)

        ttk.Label(hotkey_frame, text="Hold this key combination to record:").grid(row=0, column=0, sticky=tk.W, pady=5)

        # Hotkey options
        hotkey_options = [
            "ctrl+shift (Default)",
            "ctrl+alt",
            "ctrl+space",
            "shift+space",
            "alt+space",
        ]

        self.hotkey_combo = ttk.Combobox(hotkey_frame, state="readonly", width=37)
        self.hotkey_combo['values'] = hotkey_options
        self.hotkey_combo.current(0)  # Default: ctrl+shift
        self.hotkey_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        def on_hotkey_changed(event=None):
            selected = self.hotkey_combo.get()
            # Extract the actual combination (remove " (Default)")
            self.hotkey_combination = selected.split(' (')[0]
            # Re-register hotkey
            self.unregister_hotkey()
            self.register_hotkey()

        self.hotkey_combo.bind('<<ComboboxSelected>>', on_hotkey_changed)

        # Audio Level Meter Section
        level_frame = ttk.LabelFrame(main_frame, text="Microphone Level", padding="15")
        level_frame.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        level_frame.columnconfigure(0, weight=1)

        ttk.Label(level_frame, text="Check if microphone is working:").grid(row=0, column=0, sticky=tk.W, pady=5)

        # Audio level progress bar
        self.level_bar = ttk.Progressbar(
            level_frame,
            mode='determinate',
            maximum=100,
            length=400
        )
        self.level_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Level text
        self.level_label = ttk.Label(
            level_frame,
            text="🔇 No input detected",
            font=('Arial', 9)
        )
        self.level_label.grid(row=2, column=0, pady=5)

        # Recording Control Section
        control_frame = ttk.LabelFrame(main_frame, text="Push-to-Talk Status", padding="15")
        control_frame.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # Status indicator
        self.status_label = ttk.Label(
            control_frame,
            text="⚪ Ready - Hold hotkey to start",
            font=('Arial', 11, 'bold'),
            foreground="gray"
        )
        self.status_label.grid(row=0, column=0, pady=10)

        # Instruction label
        instruction_text = "Press and HOLD your hotkey, then speak.\nRelease the hotkey when done."
        instruction_label = ttk.Label(
            control_frame,
            text=instruction_text,
            font=('Arial', 9),
            foreground='blue',
            justify=tk.CENTER
        )
        instruction_label.grid(row=1, column=0, pady=5)

        # Instructions
        instructions_frame = ttk.Frame(main_frame)
        instructions_frame.grid(row=10, column=0, sticky=(tk.W, tk.E))

        instructions = (
            "Instructions:\n"
            "1. Configure the price per second (default: $0.0001)\n"
            "2. Enter your OpenAI API key and click Save\n"
            "3. (Optional) Add a prompt to improve transcription quality\n"
            "4. Select your microphone and check the level meter\n"
            "5. Select your dictation language (Français, English, etc.)\n"
            "6. Select your push-to-talk hotkey (default: Ctrl+Shift)\n"
            "7. Open Word/Notepad and click where you want text\n"
            "8. HOLD your hotkey and speak in your selected language\n"
            "9. RELEASE the hotkey when done speaking\n"
            "10. Monitor your API usage cost in real-time"
        )
        info_label = ttk.Label(
            instructions_frame,
            text=instructions,
            wraplength=500,
            foreground='gray',
            font=('Arial', 9),
            justify=tk.LEFT
        )
        info_label.grid(row=0, column=0, sticky=tk.W)

    def load_audio_devices(self):
        """Load available audio input devices"""
        try:
            devices = sd.query_devices()
            input_devices = []

            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    device_name = f"{i}: {device['name']}"
                    input_devices.append(device_name)

            if input_devices:
                self.mic_combo['values'] = input_devices

                # Try to load saved microphone
                saved_device = self.load_saved_microphone()
                device_found = False

                if saved_device is not None:
                    # Try to find the saved device
                    for idx, device_str in enumerate(input_devices):
                        if device_str.startswith(f"{saved_device}:"):
                            self.mic_combo.current(idx)
                            self.selected_device = saved_device
                            device_found = True
                            break

                if not device_found:
                    # Use first device if saved one not found
                    self.mic_combo.current(0)
                    self.selected_device = 0
            else:
                messagebox.showwarning(
                    "No Microphones",
                    "No input devices found. Please connect a microphone."
                )
                self.mic_combo['values'] = ["No devices found"]

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load audio devices: {str(e)}")

    def load_saved_microphone(self):
        """Load saved microphone selection from file"""
        try:
            if self.mic_config_file.exists():
                with open(self.mic_config_file, 'r') as f:
                    device_id = f.read().strip()
                    if device_id.isdigit():
                        return int(device_id)
        except:
            pass
        return None

    def save_microphone(self, device_id):
        """Save microphone selection to file"""
        try:
            with open(self.mic_config_file, 'w') as f:
                f.write(str(device_id))
        except:
            pass

    def on_mic_changed(self, event=None):
        """Handle microphone selection change"""
        device_selection = self.mic_combo.get()
        if device_selection and device_selection != "No devices found":
            try:
                self.selected_device = int(device_selection.split(':')[0])
                # Save the selection for future use
                self.save_microphone(self.selected_device)
                # Restart level monitoring with new device
                self.start_level_monitoring()
            except:
                pass

    def on_mode_changed(self):
        """Handle recording mode change"""
        self.recording_mode = self.mode_var.get()

        if self.recording_mode == "live":
            # Show the start/stop button for live mode
            self.live_control_button.grid(row=3, column=0, pady=10)
            # Update status
            if not self.live_recording_enabled:
                self.status_label.config(
                    text="⚪ Click START to begin live mode",
                    foreground="gray"
                )
        else:
            # Hide the live mode button
            self.live_control_button.grid_forget()
            # Update status for push-to-talk
            self.status_label.config(
                text="⚪ Ready - Hold hotkey to start",
                foreground="gray"
            )
            # Stop live recording if it was active
            if self.live_recording_enabled:
                self.toggle_live_mode()

    def toggle_live_mode(self):
        """Start or stop live recording mode"""
        if not self.live_recording_enabled:
            # Start live mode
            if not self.client:
                messagebox.showerror("Error", "Please enter and save your API key first")
                return

            self.live_recording_enabled = True
            self.live_control_button.config(text="⏹ STOP LIVE MODE")
            self.status_label.config(text="🟢 Live Mode Active - Speak anytime", foreground="green")

            # Start live recording thread
            self.start_live_recording()
        else:
            # Stop live mode
            self.live_recording_enabled = False
            self.live_control_button.config(text="▶ START LIVE MODE")
            self.status_label.config(text="⚪ Click START to begin live mode", foreground="gray")
            self.stop_recording()

    def start_live_recording(self):
        """Start live recording with VAD"""
        if not self.client:
            return

        device_selection = self.mic_combo.get()
        if not device_selection or device_selection == "No devices found":
            return

        try:
            self.selected_device = int(device_selection.split(':')[0])
        except:
            return

        self.is_recording = True
        self.audio_frames = []

        # Start recording thread for live mode
        self.recording_thread = threading.Thread(target=self.record_live_audio, daemon=True)
        self.recording_thread.start()

    def record_live_audio(self):
        """Record audio continuously in live mode, processing chunks with VAD"""
        def audio_callback(indata, frames, time, status):
            if self.is_recording and self.live_recording_enabled:
                self.audio_frames.append(indata.copy())

                # Update level bar
                try:
                    rms = np.sqrt(np.mean(indata**2))
                    level_percent = min(100, int(rms * 300))
                    self.root.after(0, lambda: self.level_bar.config(value=level_percent))

                    if level_percent > 10:
                        self.root.after(0, lambda: self.level_label.config(
                            text=f"🟢 Listening... ({level_percent}%)",
                            foreground="green"
                        ))
                except:
                    pass

        try:
            self.stream = sd.InputStream(
                device=self.selected_device,
                samplerate=self.sample_rate,
                channels=1,
                callback=audio_callback,
                dtype=np.float32
            )
            self.stream.start()

            # Process audio in 3-second chunks
            chunk_duration = 3.0
            import time

            while self.is_recording and self.live_recording_enabled:
                time.sleep(chunk_duration)

                if len(self.audio_frames) > 0:
                    # Get current chunk
                    current_frames = self.audio_frames.copy()
                    self.audio_frames = []

                    # Process this chunk in a separate thread (with VAD)
                    threading.Thread(
                        target=self.process_audio_chunk,
                        args=(current_frames,),
                        daemon=True
                    ).start()

        except Exception as e:
            pass
        finally:
            # Stream closing handled in stop_recording()
            pass

    def start_level_monitoring(self):
        """Start monitoring audio levels"""
        if not self.level_update_running:
            self.level_update_running = True
            self.update_audio_level()

    def update_audio_level(self):
        """Update audio level meter continuously"""
        if not self.level_update_running:
            return

        try:
            # Only monitor if not recording (to avoid conflicts)
            if not self.is_recording and self.selected_device is not None:
                # Record a very short sample to check level
                duration = 0.1  # 100ms
                try:
                    audio = sd.rec(
                        int(duration * self.sample_rate),
                        samplerate=self.sample_rate,
                        channels=1,
                        device=self.selected_device,
                        dtype=np.float32
                    )
                    sd.wait()

                    # Calculate RMS (Root Mean Square) level
                    rms = np.sqrt(np.mean(audio**2))

                    # Convert to percentage (0-100)
                    # Typical speech is around 0.01-0.3 RMS
                    level_percent = min(100, int(rms * 300))

                    # Update progress bar
                    self.level_bar['value'] = level_percent

                    # Update label
                    if level_percent > 30:
                        self.level_label.config(
                            text=f"🔊 Good level ({level_percent}%)",
                            foreground="green"
                        )
                    elif level_percent > 10:
                        self.level_label.config(
                            text=f"🔉 Moderate level ({level_percent}%)",
                            foreground="orange"
                        )
                    elif level_percent > 0:
                        self.level_label.config(
                            text=f"🔈 Low level ({level_percent}%)",
                            foreground="gray"
                        )
                    else:
                        self.level_label.config(
                            text="🔇 No input detected",
                            foreground="gray"
                        )
                except:
                    # Ignore errors during level monitoring
                    pass

        except Exception as e:
            pass  # Silently handle errors

        # Schedule next update (only if not recording)
        if not self.is_recording:
            self.root.after(100, self.update_audio_level)
        else:
            # Re-enable after recording stops
            self.root.after(500, self.update_audio_level)

    def load_api_key(self):
        """Load API key from file if it exists"""
        try:
            if self.api_key_file.exists():
                with open(self.api_key_file, 'r') as f:
                    saved_key = f.read().strip()
                    if saved_key:
                        # Populate the entry field
                        self.api_key_entry.delete(0, tk.END)
                        self.api_key_entry.insert(0, saved_key)

                        # Auto-initialize the client
                        self.api_key = saved_key
                        self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            pass  # Silently handle errors

    def save_api_key(self):
        """Save and validate API key"""
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            messagebox.showerror("Error", "Please enter an API key")
            return

        if not api_key.startswith('sk-'):
            result = messagebox.askyesno(
                "Warning",
                "API key should start with 'sk-'. Continue anyway?",
                icon='warning'
            )
            if not result:
                return

        try:
            self.api_key = api_key
            self.client = OpenAI(api_key=self.api_key)

            # Save to file for future use
            with open(self.api_key_file, 'w') as f:
                f.write(api_key)

            messagebox.showinfo("Success", "API key saved successfully!\n\nIt will be loaded automatically next time.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize OpenAI client: {str(e)}")

    def register_hotkey(self):
        """Register the push-to-talk hotkey"""
        try:
            # Unregister any existing hotkey first
            self.unregister_hotkey()

            # Use add_hotkey for combination press detection
            # The callback is triggered when all keys in the combination are pressed
            self.hotkey_hook = keyboard.add_hotkey(
                self.hotkey_combination,
                self.on_hotkey_press,
                suppress=False
            )

            # Set up release detection for when user releases the keys
            # This monitors all key releases
            keyboard.on_release(self.on_any_key_release)

        except Exception as e:
            pass  # Silently handle errors

    def unregister_hotkey(self):
        """Unregister the current hotkey"""
        try:
            if self.hotkey_hook is not None:
                keyboard.remove_hotkey(self.hotkey_hook)
                self.hotkey_hook = None
            # Note: we don't unhook_all() as that would remove the release listener too
        except Exception as e:
            pass  # Silently handle errors

    def on_hotkey_press(self):
        """Called when hotkey combination is pressed"""
        if not self.is_hotkey_active and not self.is_recording:
            self.is_hotkey_active = True
            self.start_recording()

    def on_any_key_release(self, event):
        """Called when any key is released - check if we should stop recording"""
        if self.is_hotkey_active and self.is_recording:
            # Check if any key in our combination was released
            # Parse the combination (e.g., "ctrl+shift" -> ["ctrl", "shift"])
            keys_in_combo = self.hotkey_combination.lower().replace(" ", "").split('+')

            # Normalize key names for comparison
            released_key = event.name.lower()

            # Map common key variations
            key_mappings = {
                'left ctrl': 'ctrl',
                'right ctrl': 'ctrl',
                'left shift': 'shift',
                'right shift': 'shift',
                'left alt': 'alt',
                'right alt': 'alt',
            }

            normalized_released_key = key_mappings.get(released_key, released_key)

            # If the released key is part of our combination, stop recording
            if normalized_released_key in keys_in_combo:
                self.is_hotkey_active = False
                self.stop_recording()

    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start push-to-talk recording"""
        # Validate API key
        if not self.client:
            return

        # Get selected device
        device_selection = self.mic_combo.get()
        if not device_selection or device_selection == "No devices found":
            return

        # Extract device index
        try:
            self.selected_device = int(device_selection.split(':')[0])
        except:
            return

        self.is_recording = True
        self.audio_frames = []

        # Update UI
        self.status_label.config(text="🔴 Recording - Speak Now!", foreground="red")

        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
        self.recording_thread.start()

    def record_audio(self):
        """Record audio while hotkey is held (push-to-talk mode)"""
        def audio_callback(indata, frames, time, status):
            if self.is_recording:
                self.audio_frames.append(indata.copy())

                # Update level bar during recording
                try:
                    rms = np.sqrt(np.mean(indata**2))
                    level_percent = min(100, int(rms * 300))
                    self.root.after(0, lambda: self.level_bar.config(value=level_percent))

                    if level_percent > 10:
                        self.root.after(0, lambda: self.level_label.config(
                            text=f"🔴 Recording... ({level_percent}%)",
                            foreground="red"
                        ))
                except:
                    pass

        try:
            # Start audio stream with selected device
            self.stream = sd.InputStream(
                device=self.selected_device,
                samplerate=self.sample_rate,
                channels=1,
                callback=audio_callback,
                dtype=np.float32
            )
            self.stream.start()

            # Just keep recording until stop_recording() is called
            # (when hotkey is released)
            import time
            while self.is_recording:
                time.sleep(0.1)  # Check every 100ms if still recording

        except Exception as e:
            # Silently handle errors
            pass
        finally:
            # Stream is now closed in stop_recording() to prevent race conditions
            pass

    def clean_filler_words(self, text):
        """Remove filler words and hesitations from text"""
        import re

        # List of filler words in multiple languages
        filler_words = [
            # French
            r'\beuh+\b', r'\beuuuh+\b', r'\beu+h+\b',
            r'\bhumm+\b', r'\bhmm+\b', r'\bhum+\b',
            r'\bbah\b', r'\bben\b', r'\bbox\b',
            r'\bbref\b', r'\bvoilà\b', r'\bquoi\b',
            r'\balors\b', r'\bdonc\b', r'\ben fait\b',
            r'\btu vois\b', r'\bvous voyez\b',

            # English
            r'\buh+\b', r'\buhh+\b', r'\buhm+\b',
            r'\bum+\b', r'\bumm+\b', r'\buhmm+\b',
            r'\ber+\b', r'\buhh+\b', r'\bahh+\b',
            r'\byou know\b', r'\blike\b', r'\bwell\b',
            r'\bso\b', r'\banyway\b', r'\bi mean\b',

            # German
            r'\bäh+\b', r'\böh+\b', r'\bahm+\b',
            r'\bähm+\b', r'\böhm+\b',

            # Spanish
            r'\beh+\b', r'\bemm+\b', r'\bpues\b',

            # Italian
            r'\beh+\b', r'\behm+\b', r'\bmah\b',
        ]

        # Apply each filter
        cleaned_text = text
        for pattern in filler_words:
            # Remove with word boundaries, case insensitive
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)

        # Clean up extra spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = cleaned_text.strip()

        # Fix punctuation spacing (remove space before punctuation)
        cleaned_text = re.sub(r'\s+([.,!?;:])', r'\1', cleaned_text)

        return cleaned_text

    def process_audio_chunk(self, frames):
        """Process and transcribe an audio chunk"""
        try:
            # Combine frames
            audio_data = np.concatenate(frames, axis=0)

            # Calculate RMS (Root Mean Square) to detect voice activity
            rms = np.sqrt(np.mean(audio_data**2))

            # Voice Activity Detection threshold
            VOICE_THRESHOLD = 0.008

            if rms < VOICE_THRESHOLD:
                # Update status to green for live mode (no API call)
                if self.recording_mode == "live" and self.live_recording_enabled:
                    self.root.after(0, lambda: self.status_label.config(
                        text="🟢 Live Mode - No speech detected (saving costs)",
                        foreground="green"
                    ))
                return  # Don't send silence to API!

            # Update status to red for live mode (API call happening)
            if self.recording_mode == "live" and self.live_recording_enabled:
                self.root.after(0, lambda: self.status_label.config(
                    text="🔴 API Call - Processing speech...",
                    foreground="red"
                ))

            # Convert to 16-bit PCM
            audio_data = (audio_data * 32767).astype(np.int16)

            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()

            with wave.open(temp_file.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())

            # Calculate audio duration for cost tracking
            audio_duration_seconds = len(audio_data) / self.sample_rate

            # Transcribe using Whisper API
            with open(temp_file.name, 'rb') as audio_file:
                # Build API call parameters
                api_params = {
                    "model": "whisper-1",
                    "file": audio_file,
                    "language": self.selected_language
                }

                # Add prompt if provided (improves transcription quality)
                if self.prompt_text:
                    api_params["prompt"] = self.prompt_text

                transcript = self.client.audio.transcriptions.create(**api_params)

            # Calculate and update cost
            cost_for_this_audio = audio_duration_seconds * self.price_per_second
            self.total_cost += cost_for_this_audio

            # Update cost display on UI thread
            self.root.after(0, lambda: self.update_cost_display())

            # Clean up temp file
            try:
                os.unlink(temp_file.name)
            except:
                pass

            # Get transcribed text
            transcribed_text = transcript.text.strip()

            # Filter out known Whisper hallucinations
            hallucinations = [
                "sous-titres réalisés para la communauté d'amara.org",
                "sous-titres réalisés par la communauté d'amara.org",
                "merci.",
                "merci",
                "thank you.",
                "thank you",
                "thanks.",
                "subtitle by",
                "subtitles by",
                ".",
                "..",
                "...",
            ]

            # Check if it's a hallucination (case-insensitive)
            text_lower = transcribed_text.lower().strip()
            is_hallucination = any(text_lower == h for h in hallucinations)

            if is_hallucination:
                # Restore live mode status after filtering hallucination
                if self.recording_mode == "live" and self.live_recording_enabled:
                    self.root.after(0, lambda: self.status_label.config(
                        text="🟢 Live Mode Active - Speak anytime",
                        foreground="green"
                    ))
                return  # Don't type hallucinations!

            # Clean filler words from transcription
            cleaned_text = self.clean_filler_words(transcribed_text)

            # Type the cleaned text if it's valid
            if cleaned_text and len(cleaned_text) > 1:
                self.type_text(cleaned_text)

            # Restore live mode status after successful typing
            if self.recording_mode == "live" and self.live_recording_enabled:
                self.root.after(0, lambda: self.status_label.config(
                    text="🟢 Live Mode Active - Speak anytime",
                    foreground="green"
                ))

        except Exception as e:
            # Log the error for debugging instead of silently failing
            error_msg = f"Error in process_audio_chunk: {str(e)}"
            # Show error in status for a moment
            self.root.after(0, lambda: self.status_label.config(
                text=f"⚠️ Error: {str(e)[:50]}",
                foreground="orange"
            ))
            # Restore normal status after 3 seconds
            import time
            def restore_status():
                time.sleep(3)
                if self.recording_mode == "live" and self.live_recording_enabled:
                    self.root.after(0, lambda: self.status_label.config(
                        text="🟢 Live Mode Active - Speak anytime",
                        foreground="green"
                    ))
                elif self.recording_mode == "push-to-talk":
                    self.root.after(0, lambda: self.status_label.config(
                        text="⚪ Ready - Hold hotkey to start",
                        foreground="gray"
                    ))
            threading.Thread(target=restore_status, daemon=True).start()

    def update_cost_display(self):
        """Update the cost display label with current total cost"""
        try:
            # Format cost to 4 decimal places
            cost_text = f"Total Cost: ${self.total_cost:.4f}"
            self.cost_label.config(text=cost_text)

            # Change color based on cost
            if self.total_cost > 1.0:
                self.cost_label.config(foreground='red')
            elif self.total_cost > 0.5:
                self.cost_label.config(foreground='orange')
            elif self.total_cost > 0.1:
                self.cost_label.config(foreground='blue')
            else:
                self.cost_label.config(foreground='green')
        except Exception as e:
            pass  # Silently handle errors

    def type_text(self, text):
        """Type transcribed text into the active window using clipboard"""
        try:
            # Add a space before the text for natural spacing
            # (unless it's the first text or starts with punctuation)
            if text and text[0] not in '.,!?;:':
                text = ' ' + text

            # Save current clipboard content
            old_clipboard = ""
            try:
                old_clipboard = pyperclip.paste()
            except Exception as clip_err:
                # If clipboard read fails, continue anyway
                pass

            # Copy text to clipboard
            import time
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    pyperclip.copy(text)
                    time.sleep(0.05)
                    break
                except Exception as copy_err:
                    if attempt == max_retries - 1:
                        raise Exception(f"Clipboard copy failed: {copy_err}")
                    time.sleep(0.1)

            # Paste using Ctrl+V with retry logic
            for attempt in range(max_retries):
                try:
                    pyautogui.hotkey('ctrl', 'v')
                    break
                except Exception as paste_err:
                    if attempt == max_retries - 1:
                        raise Exception(f"Paste failed: {paste_err}")
                    time.sleep(0.1)

            # Small delay before restoring clipboard
            time.sleep(0.1)

            # Restore old clipboard content (best effort)
            try:
                if old_clipboard:
                    pyperclip.copy(old_clipboard)
            except:
                pass  # Don't fail if clipboard restore doesn't work

        except Exception as e:
            # Show error to user instead of silently failing
            error_msg = f"⚠️ Typing failed: {str(e)[:40]}"
            self.root.after(0, lambda: self.status_label.config(
                text=error_msg,
                foreground="orange"
            ))
            # Restore status after 3 seconds
            def restore():
                import time
                time.sleep(3)
                if self.recording_mode == "live" and self.live_recording_enabled:
                    self.root.after(0, lambda: self.status_label.config(
                        text="🟢 Live Mode Active - Speak anytime",
                        foreground="green"
                    ))
                elif self.recording_mode == "push-to-talk":
                    self.root.after(0, lambda: self.status_label.config(
                        text="⚪ Ready - Hold hotkey to start",
                        foreground="gray"
                    ))
            threading.Thread(target=restore, daemon=True).start()

    def stop_recording(self):
        """Stop recording and process accumulated audio"""
        if not self.is_recording:
            return  # Already stopped

        self.is_recording = False

        # Close the stream immediately to prevent race conditions
        import time
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            except:
                pass
            time.sleep(0.1)  # Small delay to ensure stream is fully closed

        # Update UI
        self.status_label.config(text="⏳ Processing...", foreground="orange")

        # Process all accumulated audio in a separate thread
        if len(self.audio_frames) > 0:
            frames_to_process = self.audio_frames.copy()
            self.audio_frames = []

            # Process in background thread
            def process_and_update():
                self.process_audio_chunk(frames_to_process)
                # Update UI when done
                self.root.after(0, lambda: self.status_label.config(
                    text="⚪ Ready - Hold hotkey to start",
                    foreground="gray"
                ))

            threading.Thread(target=process_and_update, daemon=True).start()
        else:
            # No audio recorded, just update status
            self.status_label.config(text="⚪ Ready - Hold hotkey to start", foreground="gray")

        # Reset UI elements
        self.level_bar['value'] = 0
        self.level_label.config(text="🔇 No input detected", foreground="gray")

        # Restart level monitoring
        self.start_level_monitoring()

    def on_closing(self):
        """Handle window closing"""
        self.level_update_running = False
        if self.is_recording:
            self.stop_recording()
        # Unhook all keyboard listeners
        try:
            keyboard.unhook_all()
        except:
            pass
        self.root.destroy()


def main():
    """Main entry point"""
    # Configure pyautogui
    pyautogui.PAUSE = 0.01
    pyautogui.FAILSAFE = True  # Move mouse to corner to emergency stop

    root = tk.Tk()
    app = LiveDictationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
