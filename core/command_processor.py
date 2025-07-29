from core.intelligent_parser import parse_and_execute
from automation.code_assistant import handle_code_command


class CommandProcessor:
    def __init__(self):
        pass

    def process_command(self, user_input):
        """Process commands and return action type"""
        lowered = user_input.lower().strip()

        # Try code assistance first
        code_result = handle_code_command(user_input)
        if code_result:
            return "code_command_executed", code_result

        # Try intelligent parsing
        smart_result = parse_and_execute(user_input)
        if smart_result:
            return "smart_command_executed", smart_result

        # System configuration commands
        if "set timeout" in lowered:
            return "configure_timeout", user_input
        if "voice settings" in lowered or "timing settings" in lowered:
            return "show_voice_settings", user_input

        # Mode switching commands
        if "text mode" in lowered or "type mode" in lowered:
            return "switch_to_text", user_input
        if "voice mode" in lowered or "speech mode" in lowered:
            return "switch_to_voice", user_input
        if "fast mode" in lowered or "speed mode" in lowered:
            return "enable_fast_mode", user_input
        if "memory mode" in lowered or "slow mode" in lowered:
            return "enable_memory_mode", user_input

        # Exit and control commands
        if any(
            word in lowered
            for word in ["exit", "quit", "goodbye", "shut down", "shutdown"]
        ):
            return "exit", user_input
        if any(
            word in lowered
            for word in ["stop", "cancel", "quiet", "silence", "shut up", "enough"]
        ):
            return "stop", user_input

        # Memory commands
        if "clear memory" in lowered or "forget everything" in lowered:
            return "clear_memory", user_input
        if "memory status" in lowered or "what do you remember" in lowered:
            return "memory_status", user_input

        # Screen control commands
        if "click at" in lowered or "click on" in lowered:
            return "click_command", user_input
        if "type" in lowered and ("text" in lowered or "message" in lowered):
            return "type_command", user_input
        if "press" in lowered and "key" in lowered:
            return "press_key_command", user_input
        if "mouse position" in lowered or "where is mouse" in lowered:
            return "mouse_position", user_input

        # Screen analysis commands
        if any(
            phrase in lowered
            for phrase in ["screenshot", "take picture", "take a screenshot"]
        ):
            return "take_screenshot", user_input
        if any(
            phrase in lowered
            for phrase in [
                "analyze screen",
                "what's on screen",
                "describe screen",
                "read my screen",
                "what's on my screen",
                "can you see my screen",
                "what do you see",
            ]
        ):
            return "analyze_screen", user_input
        if any(
            phrase in lowered
            for phrase in ["find errors", "check for errors", "look for errors"]
        ):
            return "find_errors", user_input
        if any(
            phrase in lowered
            for phrase in ["read screen", "extract text", "what text is on screen"]
        ):
            return "extract_text", user_input

        # Default: process as normal AI command
        return "process", user_input
