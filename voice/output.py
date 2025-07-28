import pyttsx3
import threading
import queue
import time


class VoiceOutput:
    def __init__(self):
        self._speaking_thread = None
        self._should_stop = False
        self._text_queue = queue.Queue()
        self._is_streaming = False
        self._force_stop = False

    def _create_fresh_engine(self):
        """Create a completely fresh engine instance"""
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 175)
            engine.setProperty("volume", 0.9)
            return engine
        except Exception as e:
            print(f"TTS Engine error: {e}")
            return None

    def _streaming_worker(self):
        """Worker for streaming TTS - creates new engine for each sentence"""
        current_sentence = ""

        try:
            while (
                self._is_streaming or not self._text_queue.empty()
            ) and not self._force_stop:
                if self._should_stop or self._force_stop:
                    break

                try:
                    # Get text chunk with timeout
                    chunk = self._text_queue.get(timeout=0.1)
                    current_sentence += chunk

                    # Check if we have a complete sentence or enough text
                    if (
                        any(punct in chunk for punct in [".", "!", "?"])
                        or len(current_sentence.split()) > 15
                    ):
                        if (
                            current_sentence.strip()
                            and not self._should_stop
                            and not self._force_stop
                        ):
                            # Create fresh engine for each sentence
                            engine = self._create_fresh_engine()
                            if engine:
                                try:
                                    engine.say(current_sentence.strip())
                                    engine.runAndWait()
                                    engine.stop()
                                except Exception as e:
                                    print(f"Engine error: {e}")
                                finally:
                                    try:
                                        del engine
                                    except:
                                        pass
                            current_sentence = ""

                except queue.Empty:
                    continue

            # Speak any remaining text only if not stopped
            if (
                current_sentence.strip()
                and not self._should_stop
                and not self._force_stop
            ):
                engine = self._create_fresh_engine()
                if engine:
                    try:
                        engine.say(current_sentence.strip())
                        engine.runAndWait()
                        engine.stop()
                    except Exception as e:
                        print(f"Final engine error: {e}")
                    finally:
                        try:
                            del engine
                        except:
                            pass

        except Exception as e:
            print(f"Streaming speech error: {e}")

    def _speak_worker(self, text):
        """Worker function for regular speech - creates fresh engine"""
        if self._should_stop or self._force_stop:
            return

        engine = self._create_fresh_engine()
        if not engine:
            print(f"TTS not available, would say: {text}")
            return

        try:
            if not self._should_stop and not self._force_stop:
                engine.say(text)
                engine.runAndWait()
                engine.stop()
        except Exception as e:
            print(f"Speech error: {e}")
        finally:
            try:
                del engine
            except:
                pass

    def speak(self, text):
        """Speak text immediately"""
        if not text or not text.strip():
            return

        # Only stop if there's actually something speaking
        if self._speaking_thread and self._speaking_thread.is_alive():
            self.stop_speaking()
            time.sleep(0.2)

        self._should_stop = False
        self._force_stop = False

        self._speaking_thread = threading.Thread(
            target=self._speak_worker, args=(text,), daemon=True
        )
        self._speaking_thread.start()

    def start_streaming(self):
        """Start streaming TTS mode"""
        # Only stop if there's actually something speaking
        if self._speaking_thread and self._speaking_thread.is_alive():
            self.stop_speaking()
            time.sleep(0.2)

        self._should_stop = False
        self._force_stop = False
        self._is_streaming = True

        # Clear any old text in queue
        while not self._text_queue.empty():
            try:
                self._text_queue.get_nowait()
            except queue.Empty:
                break

        self._speaking_thread = threading.Thread(
            target=self._streaming_worker, daemon=True
        )
        self._speaking_thread.start()

    def add_text_chunk(self, chunk):
        """Add text chunk to streaming queue"""
        if (
            self._is_streaming
            and chunk.strip()
            and not self._should_stop
            and not self._force_stop
        ):
            self._text_queue.put(chunk)

    def stop_streaming(self):
        """Stop streaming mode"""
        self._is_streaming = False
        time.sleep(0.5)

    def stop_speaking(self):
        """Stop current speech immediately and forcefully"""
        # Only show message if there's actually something to stop
        if self._speaking_thread and self._speaking_thread.is_alive():
            print("🛑 Stopping speech...")

        self._should_stop = True
        self._force_stop = True
        self._is_streaming = False

        # Clear the queue
        while not self._text_queue.empty():
            try:
                self._text_queue.get_nowait()
            except queue.Empty:
                break

        # Wait for thread to finish
        if self._speaking_thread and self._speaking_thread.is_alive():
            self._speaking_thread.join(timeout=2.0)

        # Reset flags after a delay
        time.sleep(0.1)
        self._force_stop = False


# Global instance
voice_output = VoiceOutput()


def speak(text):
    voice_output.speak(text)


def start_streaming_speech():
    voice_output.start_streaming()


def add_speech_chunk(chunk):
    voice_output.add_text_chunk(chunk)


def stop_streaming_speech():
    voice_output.stop_streaming()


def stop_speaking():
    voice_output.stop_speaking()
