import threading
import queue
import sys


class TextInput:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.should_stop = False
        self.input_thread = None

    def start_text_input(self):
        """Start text input in a separate thread"""
        self.should_stop = False
        self.input_thread = threading.Thread(target=self._input_worker, daemon=True)
        self.input_thread.start()

    def _input_worker(self):
        """Worker thread for text input"""
        while not self.should_stop:
            try:
                print(
                    "💬 Type your message (or 'voice mode' to switch back): ",
                    end="",
                    flush=True,
                )
                user_input = input()
                if user_input.strip():
                    self.input_queue.put(user_input.strip())
            except (EOFError, KeyboardInterrupt):
                break

    def get_text_input(self):
        """Get text input if available"""
        try:
            return self.input_queue.get_nowait()
        except queue.Empty:
            return None

    def stop_text_input(self):
        """Stop text input"""
        self.should_stop = True


# Global instance
text_input = TextInput()


def start_text_mode():
    text_input.start_text_input()


def get_text():
    return text_input.get_text_input()


def stop_text_mode():
    text_input.stop_text_input()
