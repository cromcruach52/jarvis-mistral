import time
import signal
import sys
from voice.input import listen, stop_listening, reset_listening, configure_voice_timing
from voice.output import speak, stop_speaking
from input.text_input import start_text_mode, get_text, stop_text_mode
from llm.chat import chat_with_ollama
from memory.langchain_memory import clear_conversation_memory, get_memory_info


class JarvisAI:
    def __init__(self):
        self.running = True
        self.consecutive_failures = 0
        self.max_consecutive_failures = 3
        self.text_mode = False
        self.memory_enabled = True
        self.fast_mode = False

        # Configure voice timing on startup
        configure_voice_timing(
            listen_timeout=60,  # Wait 60 seconds for speech
            phrase_time_limit=30,  # Allow 30 seconds for complete phrase
            pause_threshold=3.0,  # Wait 3 seconds of silence
            failure_cooldown=5,  # Wait 5 seconds after failure
        )

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C and other termination signals"""
        print("\n🛑 Shutting down Jarvis...")
        self.shutdown()
        sys.exit(0)

    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        stop_speaking()
        stop_listening()
        stop_text_mode()
        speak("Goodbye!")
        time.sleep(3)

    def handle_voice_input(self, user_input):
        """Process voice input and return action"""
        if not user_input:
            return "continue"

        if user_input == "UNKNOWN":
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.max_consecutive_failures:
                print(
                    f"Too many recognition failures. Taking a {self.max_consecutive_failures * 2} second break..."
                )
                time.sleep(self.max_consecutive_failures * 2)
                self.consecutive_failures = 0
            return "continue"

        # Reset failure counter on successful recognition
        self.consecutive_failures = 0

        print(f"You said: {user_input}")
        return self.process_command(user_input)

    def handle_text_input(self, user_input):
        """Process text input and return action"""
        print(f"You typed: {user_input}")
        return self.process_command(user_input)

    def process_command(self, user_input):
        """Process commands regardless of input method"""
        lowered = user_input.lower().strip()

        # Timing configuration commands
        if "set timeout" in lowered:
            return "configure_timeout"

        if "voice settings" in lowered or "timing settings" in lowered:
            return "show_voice_settings"

        # Mode switching commands
        if "text mode" in lowered or "type mode" in lowered:
            return "switch_to_text"

        if "voice mode" in lowered or "speech mode" in lowered:
            return "switch_to_voice"

        # Speed mode commands - FIXED LOGIC
        if "fast mode" in lowered or "speed mode" in lowered:
            return "enable_fast_mode"

        if "memory mode" in lowered or "slow mode" in lowered:
            return "enable_memory_mode"

        # Exit commands
        if any(
            word in lowered
            for word in ["exit", "quit", "goodbye", "shut down", "shutdown"]
        ):
            return "exit"

        # Stop commands (only for voice mode)
        if any(
            word in lowered
            for word in ["stop", "cancel", "quiet", "silence", "shut up", "enough"]
        ):
            return "stop"

        # Memory commands
        if "clear memory" in lowered or "forget everything" in lowered:
            return "clear_memory"

        if "memory status" in lowered or "what do you remember" in lowered:
            return "memory_status"

        # Process normal command
        return "process"

    def configure_timeout_interactive(self):
        """Interactive timeout configuration"""
        try:
            print("\n⏱️ Current Voice Settings:")
            print("1. Listen timeout: How long to wait for you to start speaking")
            print("2. Phrase limit: How long you can speak continuously")
            print("3. Pause threshold: How long to wait for silence before processing")
            print("4. Failure cooldown: How long to wait after recognition failure")

            print("\nEnter new values (press Enter to keep current):")

            timeout_input = input("Listen timeout (current: 60s): ").strip()
            phrase_input = input("Phrase time limit (current: 30s): ").strip()
            pause_input = input("Pause threshold (current: 3.0s): ").strip()
            cooldown_input = input("Failure cooldown (current: 5s): ").strip()

            # Apply new settings
            timeout = int(timeout_input) if timeout_input else None
            phrase = int(phrase_input) if phrase_input else None
            pause = float(pause_input) if pause_input else None
            cooldown = int(cooldown_input) if cooldown_input else None

            configure_voice_timing(timeout, phrase, pause, cooldown)
            print("✅ Voice settings updated!")

        except ValueError:
            print("❌ Invalid input. Settings not changed.")
        except Exception as e:
            print(f"❌ Error updating settings: {e}")

    def show_voice_settings(self):
        """Show current voice settings"""
        from voice.input import voice_input

        print("\n⏱️ Current Voice Settings:")
        print(f"   Listen timeout: {voice_input.listen_timeout} seconds")
        print(f"   Phrase time limit: {voice_input.phrase_time_limit} seconds")
        print(f"   Pause threshold: {voice_input.pause_threshold} seconds")
        print(f"   Failure cooldown: {voice_input.failure_cooldown} seconds")
        print("\n💡 Say 'set timeout' to change these settings")

    def switch_to_text_mode(self):
        """Switch to text input mode"""
        self.text_mode = True
        stop_listening()
        start_text_mode()
        print("📝 Switched to TEXT mode. Type your messages.")
        print("💡 Say 'voice mode' to switch back to voice input")
        speak("Switched to text mode")

    def switch_to_voice_mode(self):
        """Switch to voice input mode"""
        self.text_mode = False
        stop_text_mode()
        reset_listening()
        print("🎤 Switched to VOICE mode. Speak your commands.")
        print("💡 Say 'text mode' to switch to typing")
        speak("Switched to voice mode")

    def enable_fast_mode(self):
        """Enable fast mode (no memory)"""
        if not self.fast_mode:
            self.fast_mode = True
            self.memory_enabled = False
            print("⚡ FAST MODE enabled - No memory, faster responses")
            if not self.text_mode:
                speak("Fast mode enabled")
        else:
            print("⚡ Already in FAST MODE")
            if not self.text_mode:
                speak("Already in fast mode")

    def enable_memory_mode(self):
        """Enable memory mode (with context)"""
        if self.fast_mode:
            self.fast_mode = False
            self.memory_enabled = True
            print("🧠 MEMORY MODE enabled - Slower but remembers context")
            if not self.text_mode:
                speak("Memory mode enabled")
        else:
            print("🧠 Already in MEMORY MODE")
            if not self.text_mode:
                speak("Already in memory mode")

    def get_current_mode_status(self):
        """Get current mode status for display"""
        speed_mode = "⚡ Fast" if self.fast_mode else "🧠 Memory"
        input_mode = "📝 Text" if self.text_mode else "🎤 Voice"
        return f"{speed_mode} + {input_mode}"

    def run(self):
        """Main application loop"""
        print("🔊 Jarvis is starting up...")
        print(f"📚 {get_memory_info()}")
        print(f"🎤 Starting in VOICE mode with MEMORY enabled")
        print(f"Current mode: {self.get_current_mode_status()}")
        print("💡 Commands:")
        print("   - 'text mode' / 'voice mode' - Switch input methods")
        print("   - 'fast mode' - Enable fast responses (no memory)")
        print("   - 'memory mode' - Enable memory (slower but contextual)")
        print("   - 'voice settings' - Show current timing settings")
        print("   - 'set timeout' - Configure voice timing")
        print("   - 'clear memory' / 'memory status' - Memory management")

        speak(
            "Hello! Jarvis is ready in memory mode. Say fast mode for quicker responses."
        )
        time.sleep(4)

        while self.running:
            try:
                user_input = None

                if self.text_mode:
                    # Text input mode
                    user_input = get_text()
                    if user_input:
                        action = self.handle_text_input(user_input)
                    else:
                        time.sleep(0.1)  # Small delay to prevent CPU spinning
                        continue
                else:
                    # Voice input mode
                    reset_listening()
                    user_input = listen()
                    action = self.handle_voice_input(user_input)

                # Handle actions
                if action == "exit":
                    self.shutdown()
                    break
                elif action == "stop" and not self.text_mode:
                    print("🛑 Stopping current speech...")
                    stop_speaking()
                    time.sleep(2)
                    print("🎤 Ready for next command...")
                    continue
                elif action == "configure_timeout":
                    self.configure_timeout_interactive()
                    continue
                elif action == "show_voice_settings":
                    self.show_voice_settings()
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
                elif action == "process":
                    # Get AI response
                    current_mode = self.get_current_mode_status()
                    print(f"🤖 Processing... ({current_mode})")

                    response = chat_with_ollama(
                        user_input,
                        use_memory=self.memory_enabled,
                        text_mode=self.text_mode,
                        fast_mode=self.fast_mode,
                    )

                    if response and response.strip():
                        time.sleep(0.2)

                # Small delay to prevent overwhelming the system
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
