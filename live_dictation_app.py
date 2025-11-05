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
import sounddevice as sd
import numpy as np
import pyautogui
from openai import OpenAI


class LiveDictationApp:
    """Main live dictation application with GUI and audio level meter"""

    def __init__(self, root):
        self.root = root
        self.root.title("Live Dictation - Whisper AI")
        self.root.geometry("550x500")
        self.root.resizable(False, False)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # State variables
        self.is_recording = False
        self.recording_thread = None
        self.api_key = None
        self.client = None
        self.audio_frames = []
        self.sample_rate = 16000
        self.stream = None
        self.selected_device = None
        self.current_audio_level = 0
        self.level_update_running = False

        # Setup GUI
        self.setup_gui()

        # Load available audio devices
        self.load_audio_devices()

        # Start audio level monitoring
        self.start_level_monitoring()

    def setup_gui(self):
        """Setup the GUI components"""

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Live Dictation App",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # API Key Section
        api_frame = ttk.LabelFrame(main_frame, text="OpenAI Configuration", padding="15")
        api_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
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

        # Microphone Selection Section
        mic_frame = ttk.LabelFrame(main_frame, text="Microphone Selection", padding="15")
        mic_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
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

        # Audio Level Meter Section
        level_frame = ttk.LabelFrame(main_frame, text="Microphone Level", padding="15")
        level_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
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
        control_frame = ttk.LabelFrame(main_frame, text="Dictation Control", padding="15")
        control_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # Status indicator
        self.status_label = ttk.Label(
            control_frame,
            text="⚪ Stopped",
            font=('Arial', 12, 'bold'),
            foreground="gray"
        )
        self.status_label.grid(row=0, column=0, pady=10)

        # Start/Stop button
        self.start_stop_button = ttk.Button(
            control_frame,
            text="▶ START DICTATION",
            command=self.toggle_recording,
            width=30
        )
        self.start_stop_button.grid(row=1, column=0, pady=5)

        # Instructions
        instructions_frame = ttk.Frame(main_frame)
        instructions_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))

        instructions = (
            "Instructions:\n"
            "1. Enter your OpenAI API key and click Save\n"
            "2. Select your microphone and check the level meter\n"
            "3. Click 'START DICTATION' button\n"
            "4. Open Word/Notepad and click where you want text\n"
            "5. Speak naturally - text appears live every ~3 seconds\n"
            "6. Click 'STOP DICTATION' when done"
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
                self.mic_combo.current(0)  # Select first device by default

                # Extract device index from selection
                self.selected_device = 0
            else:
                messagebox.showwarning(
                    "No Microphones",
                    "No input devices found. Please connect a microphone."
                )
                self.mic_combo['values'] = ["No devices found"]

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load audio devices: {str(e)}")

    def on_mic_changed(self, event=None):
        """Handle microphone selection change"""
        device_selection = self.mic_combo.get()
        if device_selection and device_selection != "No devices found":
            try:
                self.selected_device = int(device_selection.split(':')[0])
                # Restart level monitoring with new device
                self.start_level_monitoring()
            except:
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
            print(f"Level monitoring error: {e}")

        # Schedule next update (only if not recording)
        if not self.is_recording:
            self.root.after(100, self.update_audio_level)
        else:
            # Re-enable after recording stops
            self.root.after(500, self.update_audio_level)

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
            messagebox.showinfo("Success", "API key saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize OpenAI client: {str(e)}")

    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start continuous recording and transcription"""
        # Validate API key
        if not self.client:
            messagebox.showerror("Error", "Please save your API key first!")
            return

        # Get selected device
        device_selection = self.mic_combo.get()
        if not device_selection or device_selection == "No devices found":
            messagebox.showerror("Error", "Please select a microphone!")
            return

        # Extract device index
        try:
            self.selected_device = int(device_selection.split(':')[0])
        except:
            messagebox.showerror("Error", "Invalid microphone selection!")
            return

        self.is_recording = True
        self.audio_frames = []

        # Update UI
        self.start_stop_button.config(text="⏹ STOP DICTATION")
        self.status_label.config(text="🔴 Recording - Speak Now!", foreground="red")
        self.mic_combo.config(state="disabled")
        self.save_api_button.config(state="disabled")
        self.level_bar['value'] = 0

        # Show instruction
        messagebox.showinfo(
            "Dictation Started",
            "Microphone is now RECORDING!\n\n"
            "📝 Click on your Word/Notepad document and start speaking.\n"
            "✅ Text will appear automatically every ~3 seconds.\n"
            "⏹ Click 'STOP DICTATION' when done."
        )

        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
        self.recording_thread.start()

    def record_audio(self):
        """Record audio in chunks and transcribe continuously"""
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
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

            # Process audio in 3-second chunks for live transcription
            chunk_duration = 3.0  # seconds

            while self.is_recording:
                # Wait for enough audio frames
                import time
                time.sleep(chunk_duration)

                if len(self.audio_frames) > 0 and self.is_recording:
                    # Get current chunk
                    current_frames = self.audio_frames.copy()
                    self.audio_frames = []  # Clear for next chunk

                    # Process this chunk in a separate thread to avoid blocking
                    threading.Thread(
                        target=self.process_audio_chunk,
                        args=(current_frames,),
                        daemon=True
                    ).start()

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Recording Error",
                f"Failed to record audio: {str(e)}"
            ))
            self.root.after(0, self.stop_recording)
        finally:
            if self.stream:
                self.stream.stop()
                self.stream.close()

    def process_audio_chunk(self, frames):
        """Process and transcribe an audio chunk"""
        try:
            # Combine frames
            audio_data = np.concatenate(frames, axis=0)

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

            # Transcribe using Whisper API
            with open(temp_file.name, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )

            # Clean up temp file
            try:
                os.unlink(temp_file.name)
            except:
                pass

            # Type the transcribed text
            transcribed_text = transcript.text.strip()
            if transcribed_text:
                self.type_text(transcribed_text)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Transcribed: {transcribed_text}")

        except Exception as e:
            print(f"Transcription error: {e}")
            # Continue recording even if one chunk fails

    def type_text(self, text):
        """Type transcribed text into the active window"""
        try:
            # Add a space before the text for natural spacing
            # (unless it's the first text or starts with punctuation)
            if text and text[0] not in '.,!?;:':
                text = ' ' + text

            # Type the text with a small delay between characters
            pyautogui.write(text, interval=0.01)

        except Exception as e:
            print(f"Error typing text: {e}")

    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False

        # Update UI
        self.start_stop_button.config(text="▶ START DICTATION")
        self.status_label.config(text="⚪ Stopped", foreground="gray")
        self.mic_combo.config(state="readonly")
        self.save_api_button.config(state="normal")
        self.level_bar['value'] = 0
        self.level_label.config(text="🔇 No input detected", foreground="gray")

        # Restart level monitoring
        self.start_level_monitoring()

    def on_closing(self):
        """Handle window closing"""
        self.level_update_running = False
        if self.is_recording:
            self.stop_recording()
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
