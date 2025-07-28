import speech_recognition as sr
import time


class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.should_stop = False

        # Timing configuration - ADJUST THESE VALUES
        self.listen_timeout = 60  # Wait 60 seconds for speech to start
        self.phrase_time_limit = 30  # Allow 30 seconds for complete phrase
        self.pause_threshold = 3.0  # Wait 3 seconds of silence before processing
        self.failure_cooldown = 5  # Wait 5 seconds after recognition failure

        # Adjust for ambient noise once at startup
        with self.microphone as source:
            print("Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone calibrated.")

        # Adjust recognition settings for better accuracy
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.phrase_threshold = 0.1
        self.recognizer.non_speaking_duration = 1.5

    def listen(self, timeout=None, phrase_time_limit=None):
        """Listen for voice input with proper error handling"""
        if self.should_stop:
            return None

        # Use configured timeouts if not specified
        if timeout is None:
            timeout = self.listen_timeout
        if phrase_time_limit is None:
            phrase_time_limit = self.phrase_time_limit

        try:
            with self.microphone as source:
                print(f"🎤 Listening... (speak within {timeout} seconds)")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )

            if self.should_stop:
                return None

            print("🔄 Processing speech...")
            command = self.recognizer.recognize_google(audio)
            return command.strip()

        except sr.WaitTimeoutError:
            print(f"⏰ No speech detected within {timeout} seconds, continuing...")
            return None
        except sr.UnknownValueError:
            print(
                f"❓ Could not understand audio - waiting {self.failure_cooldown} seconds before next attempt..."
            )
            time.sleep(self.failure_cooldown)  # Wait before trying again
            return "UNKNOWN"
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service: {e}")
            time.sleep(self.failure_cooldown)
            return None
        except Exception as e:
            print(f"Unexpected error in speech recognition: {e}")
            time.sleep(self.failure_cooldown)
            return None

    def configure_timing(
        self,
        listen_timeout=None,
        phrase_time_limit=None,
        pause_threshold=None,
        failure_cooldown=None,
    ):
        """Configure timing parameters"""
        if listen_timeout is not None:
            self.listen_timeout = listen_timeout
            print(f"⏱️ Listen timeout set to {listen_timeout} seconds")

        if phrase_time_limit is not None:
            self.phrase_time_limit = phrase_time_limit
            print(f"⏱️ Phrase time limit set to {phrase_time_limit} seconds")

        if pause_threshold is not None:
            self.pause_threshold = pause_threshold
            self.recognizer.pause_threshold = pause_threshold
            print(f"⏱️ Pause threshold set to {pause_threshold} seconds")

        if failure_cooldown is not None:
            self.failure_cooldown = failure_cooldown
            print(f"⏱️ Failure cooldown set to {failure_cooldown} seconds")

    def stop(self):
        """Stop listening"""
        self.should_stop = True

    def reset(self):
        """Reset the stop flag"""
        self.should_stop = False


# Global instance
voice_input = VoiceInput()


def listen():
    return voice_input.listen()


def stop_listening():
    voice_input.stop()


def reset_listening():
    voice_input.reset()


def configure_voice_timing(
    listen_timeout=None,
    phrase_time_limit=None,
    pause_threshold=None,
    failure_cooldown=None,
):
    """Configure voice input timing"""
    voice_input.configure_timing(
        listen_timeout, phrase_time_limit, pause_threshold, failure_cooldown
    )
