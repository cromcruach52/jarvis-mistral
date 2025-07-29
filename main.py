import time
import signal
import sys
from voice.input import listen, stop_listening, reset_listening, configure_voice_timing
from voice.output import speak, stop_speaking
from input.text_input import start_text_mode, get_text, stop_text_mode
from llm.chat import chat_with_ollama
from memory.langchain_memory import clear_conversation_memory, get_memory_info
from core.command_processor import CommandProcessor
from core.command_handlers import CommandHandlers
from automation.smart_launcher import get_available_apps, get_available_websites


class JarvisAI:
    def __init__(self):
        self.running = True
        self.consecutive_failures = 0
        self.max_consecutive_failures = 3
        self.text_mode = False
        self.memory_enabled = True
        self.fast_mode = False

        # Initialize components
        self.command_processor = CommandProcessor()
        self.command_handlers = CommandHandlers(self.text_mode)

        # Configure voice timing
        configure_voice_timing(
            listen_timeout=60,
            phrase_time_limit=30,
            pause_threshold=3.0,
            failure_cooldown=5,
        )

        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("\n🛑 Shutting down Jarvis...")
        self.shutdown()
        sys.exit(0)

    def shutdown(self):
        self.running = False
        stop_speaking()
        stop_listening()
        stop_text_mode()
        speak("Goodbye!")
        time.sleep(3)

    def handle_input(self, user_input):
        if not user_input:
            return "continue", ""

        if user_input == "UNKNOWN":
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.max_consecutive_failures:
                print(
                    f"Too many recognition failures. Taking a {self.max_consecutive_failures * 2} second break..."
                )
                time.sleep(self.max_consecutive_failures * 2)
                self.consecutive_failures = 0
            return "continue", ""

        self.consecutive_failures = 0
        print(f"{'You said' if not self.text_mode else 'You typed'}: {user_input}")

        result = self.command_processor.process_command(user_input)
        if isinstance(result, tuple):
            return result
        else:
            return result, user_input

    def switch_to_text_mode(self):
        self.text_mode = True
        self.command_handlers.set_text_mode(True)
        stop_listening()
        start_text_mode()
        print("📝 Switched to TEXT mode. Type your messages.")
        speak("Switched to text mode")

    def switch_to_voice_mode(self):
        self.text_mode = False
        self.command_handlers.set_text_mode(False)
        stop_text_mode()
        reset_listening()
        print("🎤 Switched to VOICE mode. Speak your commands.")
        speak("Switched to voice mode")

    def enable_fast_mode(self):
        if not self.fast_mode:
            self.fast_mode = True
            self.memory_enabled = False
            print("⚡ FAST MODE enabled - No memory, faster responses")
            if not self.text_mode:
                speak("Fast mode enabled")
        else:
            print("⚡ Already in FAST MODE")

    def enable_memory_mode(self):
        if self.fast_mode:
            self.fast_mode = False
            self.memory_enabled = True
            print("🧠 MEMORY MODE enabled - Slower but remembers context")
            if not self.text_mode:
                speak("Memory mode enabled")
        else:
            print("🧠 Already in MEMORY MODE")

    def get_current_mode_status(self):
        speed_mode = "⚡ Fast" if self.fast_mode else "🧠 Memory"
        input_mode = "📝 Text" if self.text_mode else "🎤 Voice"
        return f"{speed_mode} + {input_mode}"

    def run(self):
        print("🔊 Jarvis is starting up...")
        print(f"📚 {get_memory_info()}")
        print(f"🎤 Starting in VOICE mode with MEMORY enabled")
        print(f"Current mode: {self.get_current_mode_status()}")
        print("💡 Smart Commands Available:")
        print("   🚀 Apps: 'open word' / 'launch excel' / 'start vscode'")
        print("   🌐 Web: 'open youtube' / 'show me facebook'")
        print("   💻 Code: 'debug my code' / 'analyze workspace' / 'explain code'")
        print("   📱 System: 'what's on my screen' / 'take screenshot'")
        print("   🎛️ Modes: 'text mode' / 'fast mode' / 'memory mode'")

        # Show available apps and websites
        apps = get_available_apps()[:10]  # Show first 10
        websites = get_available_websites()[:10]  # Show first 10
        print(f"📱 Available apps: {', '.join(apps)}")
        print(f"🌐 Available websites: {', '.join(websites)}")

        speak(
            "Hello! Jarvis is ready with smart commands. Try saying open word or open youtube."
        )
        time.sleep(4)

        while self.running:
            try:
                user_input = None

                if self.text_mode:
                    user_input = get_text()
                    if user_input:
                        action, data = self.handle_input(user_input)
                    else:
                        time.sleep(0.1)
                        continue
                else:
                    reset_listening()
                    user_input = listen()
                    action, data = self.handle_input(user_input)

                # Handle actions
                if action == "exit":
                    self.shutdown()
                    break
                elif action == "stop" and not self.text_mode:
                    print("🛑 Stopping current speech...")
                    stop_speaking()
                    time.sleep(2)
                    continue
                elif action == "smart_command_executed":
                    # Smart command was already executed, just show result
                    print(f"🤖 {data}")
                    if not self.text_mode:
                        speak(data)
                    continue
                elif action == "code_command_executed":
                    # Code command was already executed, just show result
                    print(f"💻 {data}")
                    if not self.text_mode:
                        speak(data)
                    continue
                elif action == "switch_to_text":
                    self.switch_to_text_mode()
                    continue
                elif action == "switch_to_voice":
                    self.switch_to_voice_mode()
                    continue
                elif action == "enable_fast_mode":
                    self.enable_fast_mode()
                    continue
                elif action == "enable_memory_mode":
                    self.enable_memory_mode()
                    continue
                elif action == "clear_memory":
                    clear_conversation_memory()
                    message = "Memory cleared successfully!"
                    print(f"🧹 {message}")
                    if not self.text_mode:
                        speak(message)
                    continue
                elif action == "memory_status":
                    status = get_memory_info()
                    print(f"📚 {status}")
                    if not self.text_mode:
                        speak(status)
                    continue
                elif action == "continue":
                    continue
                elif action in [
                    "click_command",
                    "type_command",
                    "press_key_command",
                    "mouse_position",
                ]:
                    self.command_handlers.handle_automation_commands(action, data)
                    continue
                elif action in [
                    "open_file",
                    "open_folder",
                    "create_file",
                    "create_project",
                    "insert_code",
                ]:
                    self.command_handlers.handle_vscode_commands(action, data)
                    continue
                elif action in [
                    "take_screenshot",
                    "analyze_screen",
                    "find_errors",
                    "extract_text",
                    "find_text",
                ]:
                    self.command_handlers.handle_vision_commands(action, data)
                    continue
                elif action == "process":
                    current_mode = self.get_current_mode_status()
                    print(f"🤖 Processing... ({current_mode})")

                    response = chat_with_ollama(
                        data,
                        use_memory=self.memory_enabled,
                        text_mode=self.text_mode,
                        fast_mode=self.fast_mode,
                    )

                    if response and response.strip():
                        time.sleep(0.2)

                time.sleep(0.1)

            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                self.shutdown()
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(1)


def main():
    jarvis = JarvisAI()
    jarvis.run()


if __name__ == "__main__":
    main()
