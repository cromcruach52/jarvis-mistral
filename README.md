# 🧠 Jarvis-Mistral

A local, voice-enabled AI assistant powered by [Ollama](https://ollama.com/) and the **Mistral** model. Designed to assist with coding, answer queries, and interact through voice — all while running entirely offline on your machine.

---

## ✨ Features

- 💬 Chat with a local LLM (Mistral via Ollama)
- 🎙️ Voice input & output using SpeechRecognition and pyttsx3
- 🧠 Memory management & fallback prompts
- 💻 Built for local coding assistance and automation

---

## 🛠️ Requirements

> Tested on: **Windows 10+, Python 3.10+**, with **GTX 1080 GPU**

### 📦 Python Dependencies (in `requirements.txt`)

```txt
python-dotenv
ollama
requests
pyttsx3
SpeechRecognition
keyboard
