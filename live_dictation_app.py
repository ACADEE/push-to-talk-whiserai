"""
Live Dictation App - Continuous Speech-to-Text with Whisper AI
Types transcribed text directly into any active application (Word, Notepad, etc.)
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
    """Main live dictation application with GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Live Dictation - Whisper AI")
        self.root.geometry("500x400")
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

        # Setup GUI
        self.setup_gui()

        # Load available audio devices
        self.load_audio_devices()

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

        refresh_button = ttk.Button(
            mic_frame,
            text="🔄 Refresh Devices",
            command=self.load_audio_devices
        )
        refresh_button.grid(row=2, column=0, pady=5)

        # Recording Control Section
        control_frame = ttk.LabelFrame(main_frame, text="Dictation Control", padding="15")
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # Status indicator
        self.status_label = ttk.Label(
            control_frame,
            text="⚪ Microphone Disabled",
            font=('Arial', 12, 'bold'),
            foreground="gray"
        )
        self.status_label.grid(row=0, column=0, pady=10)

        # Toggle button
        self.toggle_button = ttk.Button(
            control_frame,
            text="🎤 Enable Microphone",
            command=self.toggle_recording,
            width=30
        )
        self.toggle_button.grid(row=1, column=0, pady=5)

        # Instructions
        instructions_frame = ttk.Frame(main_frame)
        instructions_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))

        instructions = (
            "Instructions:\n"
            "1. Enter your OpenAI API key and click Save\n"
            "2. Select your microphone from the list\n"
            "3. Click 'Enable Microphone' to start\n"
            "4. Open Word/Notepad and click where you want text\n"
            "5. Speak naturally - text appears every ~3 seconds\n"
            "6. Click 'Disable Microphone' when done"
        )
        info_label = ttk.Label(
            instructions_frame,
            text=instructions,
            wraplength=450,
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
        self.toggle_button.config(text="🔴 Disable Microphone")
        self.status_label.config(text="🔴 Recording - Speak Now!", foreground="red")
        self.mic_combo.config(state="disabled")
        self.save_api_button.config(state="disabled")

        # Show instruction
        messagebox.showinfo(
            "Dictation Started",
            "Microphone is now active!\n\n"
            "Click on your Word/Notepad document and start speaking.\n"
            "Text will appear automatically every ~3 seconds.\n\n"
            "Click 'Disable Microphone' when done."
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

                    # Process this chunk
                    self.process_audio_chunk(current_frames)

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
                print(f"Transcribed: {transcribed_text}")

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
        self.toggle_button.config(text="🎤 Enable Microphone")
        self.status_label.config(text="⚪ Microphone Disabled", foreground="gray")
        self.mic_combo.config(state="readonly")
        self.save_api_button.config(state="normal")

    def on_closing(self):
        """Handle window closing"""
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
