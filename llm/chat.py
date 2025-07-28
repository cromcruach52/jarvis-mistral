import requests
import json
from voice.output import (
    start_streaming_speech,
    add_speech_chunk,
    stop_streaming_speech,
    speak,
)
from memory.langchain_memory import chat_with_memory


def chat_with_ollama_streaming(prompt, model_name="mistral:latest"):
    """Fast streaming function for direct Ollama calls (no memory)"""
    try:
        start_streaming_speech()

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "num_predict": 512,  # Limit response length
                    "temperature": 0.7,
                    "top_p": 0.9,
                },
            },
            stream=True,
        )

        print("Jarvis: ", end="", flush=True)
        full_response = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    token = data.get("response", "")
                    print(token, end="", flush=True)
                    full_response += token

                    add_speech_chunk(token)

                except json.JSONDecodeError:
                    continue

        print()
        stop_streaming_speech()
        return full_response

    except Exception as e:
        stop_streaming_speech()
        print(f"Error talking to Ollama: {e}")
        return "I'm sorry, I'm having trouble processing that request right now."


def chat_with_ollama_fast(prompt, model_name="mistral:latest"):
    """Fast non-streaming function for text mode"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 512, "temperature": 0.7, "top_p": 0.9},
            },
        )

        data = response.json()
        return data.get("response", "No response received")

    except Exception as e:
        print(f"Error talking to Ollama: {e}")
        return "I'm sorry, I'm having trouble processing that request right now."


def chat_with_ollama(prompt, use_memory=True, text_mode=False, fast_mode=False):
    """Main chat function with multiple modes"""
    try:
        if fast_mode:
            # Fast mode - no memory, direct Ollama
            if text_mode:
                response = chat_with_ollama_fast(prompt)
                print(f"Jarvis: {response}")
                return response
            else:
                return chat_with_ollama_streaming(prompt)

        elif use_memory:
            # Memory mode - slower but remembers context
            print("Jarvis: ", end="", flush=True)
            response = chat_with_memory(prompt)
            print(response)

            if not text_mode:
                # Speak the response in voice mode
                speak(response)

            return response
        else:
            # No memory mode
            if text_mode:
                response = chat_with_ollama_fast(prompt)
                print(f"Jarvis: {response}")
                return response
            else:
                return chat_with_ollama_streaming(prompt)

    except Exception as e:
        print(f"Error in chat: {e}")
        error_msg = "I'm sorry, I'm having trouble processing that request right now."
        print(f"Jarvis: {error_msg}")
        return error_msg
