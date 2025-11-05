"""
Spelling Practice App with Live Whisper AI Transcription
A simple Windows GUI app for practicing spelling with real-time voice recognition
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import wave
import tempfile
import os
from datetime import datetime
import sounddevice as sd
import numpy as np
from openai import OpenAI


class SpellingPracticeApp:
    """Main spelling practice application with GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Spelling Practice - Live Whisper AI")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

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

        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components"""

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Spelling Practice App",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # API Key Section
        api_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        api_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)

        ttk.Label(api_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(api_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        self.save_api_button = ttk.Button(
            api_frame,
            text="Save API Key",
            command=self.save_api_key
        )
        self.save_api_button.grid(row=0, column=2, padx=(5, 0), pady=5)

        # Target Word Section
        word_frame = ttk.LabelFrame(main_frame, text="Target Word", padding="10")
        word_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        word_frame.columnconfigure(1, weight=1)

        ttk.Label(word_frame, text="Word to Practice:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.target_word_entry = ttk.Entry(word_frame, width=30, font=('Arial', 12))
        self.target_word_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        # Recording Control Section
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        self.record_button = ttk.Button(
            control_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            width=25
        )
        self.record_button.grid(row=0, column=0, padx=5)

        self.clear_button = ttk.Button(
            control_frame,
            text="Clear Transcription",
            command=self.clear_transcription,
            width=20
        )
        self.clear_button.grid(row=0, column=1, padx=5)

        # Status indicator
        self.status_label = ttk.Label(
            control_frame,
            text="● Idle",
            foreground="gray",
            font=('Arial', 10, 'bold')
        )
        self.status_label.grid(row=0, column=2, padx=10)

        # Live Transcription Display
        transcription_frame = ttk.LabelFrame(
            main_frame,
            text="Live Transcription",
            padding="10"
        )
        transcription_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        transcription_frame.columnconfigure(0, weight=1)
        transcription_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        self.transcription_display = scrolledtext.ScrolledText(
            transcription_frame,
            width=60,
            height=10,
            font=('Arial', 12),
            wrap=tk.WORD,
            state='disabled'
        )
        self.transcription_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure text tags for colored output
        self.transcription_display.tag_configure('correct', foreground='green', font=('Arial', 12, 'bold'))
        self.transcription_display.tag_configure('incorrect', foreground='red', font=('Arial', 12, 'bold'))
        self.transcription_display.tag_configure('info', foreground='blue', font=('Arial', 10, 'italic'))
        self.transcription_display.tag_configure('timestamp', foreground='gray', font=('Arial', 9))

        # History Section
        history_frame = ttk.LabelFrame(main_frame, text="Practice History", padding="10")
        history_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        history_frame.columnconfigure(0, weight=1)

        self.history_display = scrolledtext.ScrolledText(
            history_frame,
            width=60,
            height=5,
            font=('Arial', 9),
            wrap=tk.WORD,
            state='disabled'
        )
        self.history_display.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Instructions
        instructions = (
            "Instructions: Enter your OpenAI API key, set a target word, "
            "then click 'Start Recording' and speak the word. "
            "The app will transcribe in real-time and show if you spelled it correctly!"
        )
        info_label = ttk.Label(
            main_frame,
            text=instructions,
            wraplength=650,
            foreground='gray',
            font=('Arial', 9)
        )
        info_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))

    def save_api_key(self):
        """Save and validate API key"""
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            messagebox.showerror("Error", "Please enter an API key")
            return

        if not api_key.startswith('sk-'):
            messagebox.showwarning(
                "Warning",
                "API key should start with 'sk-'. Please verify your key."
            )
            return

        try:
            self.api_key = api_key
            self.client = OpenAI(api_key=self.api_key)
            messagebox.showinfo("Success", "API key saved successfully!")
            self.log_message("API key configured successfully", 'info')
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
        if not self.client:
            messagebox.showerror("Error", "Please save your API key first!")
            return

        target_word = self.target_word_entry.get().strip()
        if not target_word:
            messagebox.showerror("Error", "Please enter a target word!")
            return

        self.is_recording = True
        self.audio_frames = []

        # Update UI
        self.record_button.config(text="⏹ Stop Recording")
        self.status_label.config(text="● Recording", foreground="red")
        self.log_message(f"Started recording. Target word: '{target_word}'", 'info')

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
            # Start audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=audio_callback,
                dtype=np.float32
            )
            self.stream.start()

            # Process audio in 3-second chunks for "live" transcription
            chunk_duration = 3.0  # seconds
            chunk_size = int(self.sample_rate * chunk_duration)

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
            self.log_message(f"Recording error: {str(e)}", 'incorrect')
            print(f"Recording error: {e}")
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

            # Transcribe
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

            # Display transcription
            transcribed_text = transcript.text.strip()
            if transcribed_text:
                self.display_transcription(transcribed_text)

        except Exception as e:
            self.log_message(f"Transcription error: {str(e)}", 'incorrect')
            print(f"Transcription error: {e}")

    def display_transcription(self, text):
        """Display transcribed text and check against target word"""
        target_word = self.target_word_entry.get().strip()

        # Get timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Enable editing
        self.transcription_display.config(state='normal')

        # Add timestamp
        self.transcription_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')

        # Check if transcription matches target word
        if target_word.lower() in text.lower():
            # Success!
            self.transcription_display.insert(tk.END, f"✓ {text}\n", 'correct')
            self.add_to_history(target_word, text, True)
            self.log_message(f"Match found! Heard: '{text}'", 'correct')
        else:
            # Doesn't match
            self.transcription_display.insert(tk.END, f"✗ {text}\n", 'incorrect')
            self.add_to_history(target_word, text, False)

        # Scroll to bottom
        self.transcription_display.see(tk.END)

        # Disable editing
        self.transcription_display.config(state='disabled')

    def add_to_history(self, target, heard, is_correct):
        """Add result to practice history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = "✓" if is_correct else "✗"

        self.history_display.config(state='normal')
        self.history_display.insert(
            tk.END,
            f"[{timestamp}] Target: '{target}' | Heard: '{heard}' {result}\n"
        )
        self.history_display.see(tk.END)
        self.history_display.config(state='disabled')

    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False

        # Update UI
        self.record_button.config(text="🎤 Start Recording")
        self.status_label.config(text="● Idle", foreground="gray")
        self.log_message("Recording stopped", 'info')

    def clear_transcription(self):
        """Clear the transcription display"""
        self.transcription_display.config(state='normal')
        self.transcription_display.delete('1.0', tk.END)
        self.transcription_display.config(state='disabled')
        self.log_message("Transcription cleared", 'info')

    def log_message(self, message, tag='info'):
        """Log a message to the transcription display"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.transcription_display.config(state='normal')
        self.transcription_display.insert(
            tk.END,
            f"[{timestamp}] {message}\n",
            tag
        )
        self.transcription_display.see(tk.END)
        self.transcription_display.config(state='disabled')

    def on_closing(self):
        """Handle window closing"""
        if self.is_recording:
            self.stop_recording()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SpellingPracticeApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
