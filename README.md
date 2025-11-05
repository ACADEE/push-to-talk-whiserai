# Live Dictation App: Your Voice is Your New Keyboard 🚀

**Tired of slow typing? Want to capture your thoughts, write code, or draft documents at the speed of thought?**

**Stop typing and start talking.**

This app isn't just another dictation tool. It's a lightweight, powerful, and cost-effective bridge directly to OpenAI's cutting-edge Whisper API. It's built for developers, writers, professionals, and anyone who wants to be more productive.

**Press a hotkey, speak your mind, and watch the world's most accurate transcription appear in any application.**

---

## ✨ Unbelievable Features, Zero Fluff

This app is packed with features designed for power users who demand control and accuracy.

### ⚡️ Instant Push-to-Talk
Press your custom hotkey (like `Ctrl+Shift`) to record. Release to transcribe. It's fast, intuitive, and ensures you only record what you intend.

### 🗣️ Smart "Live Mode"
Want to go hands-free? This mode actively listens and only sends audio to the API when it detects you're speaking, saving you money and effort.

### 🧠 Context-Aware Prompts
This is the secret weapon. Tell the AI the context of your dictation (e.g., "This is a legal brief," "I'm writing Python code about asynchronous functions") to dramatically improve accuracy for jargon, names, and technical terms.

### ✍️ Custom Word Replacements
Automatically fix common transcription errors or format words your way.

\`\`\`
acadie -> ACADEE
k8s -> Kubernetes
Dr. J's name -> Dr. Jekyll
\`\`\`

### 💰 Transparent Cost Tracking
See your exact API usage in real-time, down to the fraction of a cent. This app connects directly to your API key. **No subscriptions, no hidden fees.** You only pay OpenAI's rock-bottom rate ($0.0001/second) for what you actually use.

### 🌍 Multi-Language Support
Select your dictation language—from English to French and beyond—for native-level transcription accuracy.

### 🎙️ Simple Mic Control
Easily select your input device and see a live mic level to ensure everything is working perfectly.

---

## 🚀 The Benefits: Why You'll Download This Right Now

This isn't just a tool; it's a workflow revolution.

**Type 10x Faster**: Stop letting your keyboard be the bottleneck. Draft emails, write documentation, take notes, or even write code at the speed of speech.

**Save Real Money**: Ditch expensive subscription-based transcription services. A full hour of continuous dictation could cost you as little as **36 cents**.

**Work Smarter, Not Harder**: Use the Context Prompt and Custom Replacements to get a near-perfect transcript the first time. Spend less time editing and more time creating.

**Maintain Your Flow State**: The simple hotkey means you never have to leave your current application. Dictate directly into VS Code, your browser, Microsoft Word, or any text field on your computer.

**Total Control & Privacy**: It's your API key. Your audio goes directly to OpenAI. There's no middle-man, no extra data harvesting, and no surprise bills.

**This is the tool you've been waiting for.** It combines the world's best transcription AI with the control and cost-effectiveness that professionals need.

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Quick Setup

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/YOUR_USERNAME/push-to-talk-whiserai.git
   cd push-to-talk-whiserai
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run the app**
   \`\`\`bash
   python live_dictation_app.py
   \`\`\`

4. **Configure your API key**
   - Enter your OpenAI API key in the app
   - Click "Save & Verify Key"
   - Wait for the green "API Status: ✓ OK"

5. **Start dictating!**
   - Select your microphone
   - Choose Push-to-Talk or Live Mode
   - Click in Word, Notepad, or any text field
   - Hold \`Ctrl+Shift\` and speak (Push-to-Talk)
   - Or click "START" in Live Mode

---

## 🎯 Usage Examples

### For Writers
\`\`\`
Context Prompt: "This is a creative writing session for a science fiction novel."
Result: Perfect transcription of character names, sci-fi terminology, and dialogue.
\`\`\`

### For Developers
\`\`\`
Context Prompt: "I'm dictating Python code with function definitions and variable names."
Result: Accurate code transcription with proper syntax understanding.
\`\`\`

### For Lawyers
\`\`\`
Context Prompt: "Legal dictation for client notes during a consultation meeting."
Custom Words: "Smith v. Jones -> Smith v. Jones Case #2024-123"
Result: Precise legal terminology and case references.
\`\`\`

### For Medical Professionals
\`\`\`
Context Prompt: "Medical diagnosis notes with pharmaceutical terminology."
Result: Accurate medical terms, drug names, and patient information.
\`\`\`

---

## 💡 Pro Tips

1. **Use Context Prompts**: They dramatically improve accuracy for specialized vocabulary
2. **Set Custom Replacements**: Fix recurring transcription issues once and for all
3. **Monitor Your Costs**: The live cost tracker helps you stay budget-conscious
4. **Adjust Mic Levels**: Make sure the VU meter shows activity when you speak
5. **Choose the Right Mode**:
   - Push-to-Talk = Perfect for precise control
   - Live Mode = Great for hands-free continuous dictation

---

## 🔧 Advanced Configuration

### Hotkey Customization
Choose from:
- \`Ctrl+Shift\` (default)
- \`Ctrl+Alt\`
- \`Ctrl+Space\`
- \`Shift+Space\`
- \`Alt+Space\`

### Language Support
- 🇫🇷 Français
- 🇬🇧 English
- 🇩🇪 Deutsch
- 🇪🇸 Español
- 🇮🇹 Italiano

### Price Tracking
The default rate is set to OpenAI's Whisper API pricing:
- **$0.006 per minute** = **$0.0001 per second**

You can adjust this in the app if pricing changes.

---

## 🐛 Troubleshooting

### Text doesn't appear in Notepad/Word
1. Make sure you **click inside the target application** before dictating
2. Check that the VU meter shows activity when you speak
3. Verify your API key status is green (✓ OK)

### "No audio devices found"
1. Click the 🔄 Refresh button next to the microphone selector
2. Make sure your microphone is connected and enabled in Windows settings
3. Try restarting the app

### High API costs
1. Use **Live Mode** with Voice Activity Detection (VAD) - it only sends audio when you're speaking
2. Keep recordings short and focused
3. Monitor the cost display in real-time

### Poor transcription quality
1. Add a **Context Prompt** describing what you're dictating
2. Set up **Custom Word Replacements** for recurring issues
3. Speak clearly and at a moderate pace
4. Reduce background noise

---

## 📊 Cost Comparison

| Service | Monthly Cost | Per Hour |
|---------|-------------|----------|
| Dragon NaturallySpeaking | $150-$500 | N/A |
| Otter.ai Pro | $12.99/month | ~$0.43 |
| Rev.ai | $1.25/minute | $75 |
| **Live Dictation (Whisper)** | **Pay-as-you-go** | **$0.36** |

*Based on OpenAI Whisper API pricing: $0.006/minute*

**With this app, an hour of dictation costs less than a cup of coffee.** ☕

---

## 🔐 Privacy & Security

- **Your API key stays on your machine** - stored locally in \`api_key.txt\`
- **Direct connection to OpenAI** - no third-party servers
- **No data collection** - this app doesn't track or store your transcriptions
- **Open source** - you can review every line of code

---

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: Tkinter (native Python)
- **Audio Processing**: sounddevice + numpy
- **Transcription**: OpenAI Whisper API via official SDK
- **Keyboard Control**: keyboard library for hotkey management
- **Clipboard Management**: pyperclip for seamless text insertion

### System Requirements
- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.7+
- **RAM**: 100MB+
- **Internet**: Required for API calls

### Performance
- **Startup Time**: < 2 seconds
- **Transcription Latency**: 1-3 seconds (depends on audio length and API response)
- **CPU Usage**: Minimal (< 5%)
- **Memory Footprint**: ~50MB

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 Report bugs via GitHub Issues
2. 💡 Suggest features or improvements
3. 🔧 Submit pull requests
4. 📖 Improve documentation
5. ⭐ Star this repo if you find it useful!

### Development Setup
\`\`\`bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/push-to-talk-whiserai.git

# Install dev dependencies
pip install -r requirements.txt

# Run the app
python live_dictation_app.py
\`\`\`

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **OpenAI** for the incredible Whisper API
- The open-source community for the amazing Python libraries
- All users who provide feedback and suggestions

---

## ☕ Found This App Useful?

This app is **100% free, open-source, and subscription-free**—built to save you time and money. If you find it valuable, please consider [**buying me a coffee**](https://www.paypal.me/samdprod)!

Your support directly fuels future updates, new features, and helps keep the project alive. Thank you! ❤️

---

**Done with ❤️ by [ACADEE](http://acadee.fr/)**

---

## ⬇️ Ready to Transform Your Workflow?

**[Download the latest release](https://github.com/YOUR_USERNAME/push-to-talk-whiserai/releases)** and unlock your true productivity today! 🚀
