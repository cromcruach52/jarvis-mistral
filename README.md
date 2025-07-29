# 🤖 Jarvis-Mini AI Assistant

Your personal AI-powered voice and text assistant with smart automation, code analysis, and computer control capabilities.

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Smart Commands](#-smart-commands)
- [Voice Commands](#-voice-commands)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Advanced Features](#-advanced-features)

## ✨ Features

### 🎤 **Voice & Text Interaction**
- **Voice Mode**: Speak naturally to Jarvis
- **Text Mode**: Type commands for faster interaction
- **Smart Speech Recognition**: Handles speech recognition errors intelligently
- **Text-to-Speech**: Jarvis speaks responses back to you

### 🚀 **Smart Application Launcher**
- **Voice-Activated**: "Open Word", "Launch Chrome", "Start VS Code"
- **Intelligent Matching**: Handles speech recognition errors (e.g., "bs code" → "VS Code")
- **Website Opening**: "Open YouTube", "Show me Facebook"
- **Auto-Detection**: Finds applications even if not in standard locations

### 💻 **Code Assistant**
- **Workspace Analysis**: "Analyze my code", "Debug workspace"
- **VS Code Integration**: Open files, create projects, insert code
- **Error Detection**: "Find errors on screen", "Check for issues"
- **Code Explanation**: "Explain this code", "What does this do?"

### 🖥️ **Computer Automation**
- **Screen Control**: Click, type, press keys via voice commands
- **Screenshot Analysis**: "What's on my screen?", "Take screenshot"
- **Window Management**: Open/close applications intelligently
- **OCR Text Reading**: Extract and analyze text from screen

### 🧠 **Memory & Context**
- **Conversation Memory**: Remembers context across conversations
- **Fast Mode**: Quick responses without memory (faster)
- **Memory Mode**: Contextual responses with conversation history
- **Persistent Storage**: Saves conversations between sessions

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
1. **Download** the Jarvis folder to your computer
2. **Double-click** `Start Jarvis.bat` (Windows)
3. **Wait** for setup to complete automatically
4. **Start talking** to Jarvis!

### Option 2: Python Launch
\`\`\`bash
# Navigate to Jarvis folder
cd jarvis-ai-agent

# Install dependencies
pip install -r requirements.txt

# Run Jarvis
python main.py
\`\`\`

### Option 3: Create Desktop Shortcuts
\`\`\`bash
# Run the setup script
python create_shortcuts.py
\`\`\`
This creates desktop shortcuts, Start menu entries, and batch files.

## 📦 Installation

### Prerequisites
- **Python 3.7+** (Download from [python.org](https://python.org))
- **Microphone** (for voice commands)
- **Speakers/Headphones** (for voice responses)
- **Ollama** (for AI responses) - Install from [ollama.ai](https://ollama.ai)

### Required Python Packages
\`\`\`bash
pip install speechrecognition pyttsx3 requests pyaudio langchain langchain-community langchain-ollama pyautogui pygetwindow pytesseract Pillow winshell pywin32 psutil
\`\`\`

### Optional Dependencies
- **Tesseract OCR** (for screen text reading) - [Installation Guide](https://github.com/tesseract-ocr/tesseract)
- **Ollama Models** (for AI chat):
  \`\`\`bash
  ollama pull mistral
  ollama pull llama2
  \`\`\`

## 📖 Usage Guide

### Starting Jarvis
\`\`\`bash
python main.py
\`\`\`

### Initial Setup
1. **Microphone Calibration**: Jarvis automatically adjusts for ambient noise
2. **Mode Selection**: Starts in Voice + Memory mode
3. **Available Commands**: Jarvis shows available apps and websites

### Basic Interaction
\`\`\`
🎤 Voice Mode: Speak your commands
📝 Text Mode: Type your messages
⚡ Fast Mode: Quick responses, no memory
🧠 Memory Mode: Contextual responses with history
\`\`\`

## 🎯 Smart Commands

### 🚀 Application Launcher
| Command | Action | Examples |
|---------|--------|----------|
| `open [app]` | Launch application | "open word", "launch excel", "start vscode" |
| `close [app]` | Close application | "close chrome", "close current window" |
| `launch [app]` | Start application | "launch calculator", "launch notepad" |

**Supported Applications:**
- **Office**: Word, Excel, PowerPoint, Outlook, OneNote, Teams
- **Browsers**: Chrome, Firefox, Edge
- **Development**: VS Code, Visual Studio, CMD, PowerShell
- **System**: Calculator, Notepad, Paint, File Explorer, Task Manager
- **Media**: Spotify, VLC, Windows Media Player
- **Communication**: Discord, Skype, Zoom, Slack

### 🌐 Website Opener
| Command | Action | Examples |
|---------|--------|----------|
| `open [website]` | Open website | "open youtube", "show me facebook" |
| `go to [site]` | Navigate to site | "go to github", "visit reddit" |

**Supported Websites:**
YouTube, Google, Facebook, Twitter, Instagram, LinkedIn, Reddit, GitHub, Gmail, Netflix, Amazon, Wikipedia, ChatGPT, Claude

### 💻 Code Assistant
| Command | Action | Examples |
|---------|--------|----------|
| `debug my code` | Find and fix code issues | "debug workspace", "check for errors" |
| `analyze code` | Code quality analysis | "analyze this file", "review my code" |
| `explain code` | Code explanation | "what does this code do?", "explain this function" |
| `open file [name]` | Open file in VS Code | "open main.py", "open index.html" |
| `create project [name]` | Create new project | "create python project myapp" |

### 🖥️ Screen Control
| Command | Action | Examples |
|---------|--------|----------|
| `click at [x] [y]` | Click coordinates | "click at 100 200" |
| `type [text]` | Type text | "type hello world" |
| `press key [key]` | Press keyboard key | "press key enter", "press key tab" |
| `take screenshot` | Capture screen | "take a picture of my screen" |
| `what's on screen` | Analyze screen content | "describe my screen", "read my screen" |

### 🎛️ Mode Controls
| Command | Action | Examples |
|---------|--------|----------|
| `text mode` | Switch to typing | "switch to text mode" |
| `voice mode` | Switch to speech | "switch to voice mode" |
| `fast mode` | Enable fast responses | "enable fast mode", "speed mode" |
| `memory mode` | Enable context memory | "enable memory mode", "slow mode" |
| `clear memory` | Reset conversation | "forget everything", "clear memory" |

## 🎤 Voice Commands

### Getting Started
1. **Wait for Prompt**: Look for "🎤 Listening..."
2. **Speak Clearly**: Use normal speaking pace
3. **Wait for Processing**: "🔄 Processing speech..."
4. **See Results**: Jarvis shows what you said and responds

### Voice Tips
- **Speak naturally** - no need for robot voice
- **Wait for the prompt** before speaking
- **Use simple, clear commands**
- **Say "stop" to interrupt** Jarvis while speaking

### Common Voice Issues
| Problem | Solution |
|---------|----------|
| "Could not understand" | Speak more clearly, reduce background noise |
| No response | Check microphone permissions and connection |
| Wrong recognition | Use alternative phrases or switch to text mode |

## ⚙️ Configuration

### Voice Settings
```python
# Adjust timing in voice/input.py
configure_voice_timing(
    listen_timeout=60,      # How long to wait for speech
    phrase_time_limit=30,   # Max time for complete phrase
    pause_threshold=3.0,    # Silence before processing
    failure_cooldown=5      # Wait time after recognition failure
)
