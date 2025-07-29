import re
from automation.smart_launcher import launch_app, open_website, close_app, close_tab


class IntelligentParser:
    def __init__(self):
        # Action patterns
        self.open_patterns = [
            r"open\s+(.+)",
            r"launch\s+(.+)",
            r"start\s+(.+)",
            r"run\s+(.+)",
            r"show\s+me\s+(.+)",
        ]

        self.close_patterns = [
            r"close\s+(.+)",
            r"exit\s+(.+)",
            r"quit\s+(.+)",
            r"shut\s+down\s+(.+)",
            r"close\s+this",
            r"close\s+it",
            r"close\s+tab",
            r"close\s+current\s+tab",
        ]

        self.website_indicators = [
            "youtube",
            "google",
            "facebook",
            "twitter",
            "instagram",
            "linkedin",
            "reddit",
            "github",
            "gmail",
            "netflix",
            "amazon",
            "wikipedia",
            "chatgpt",
            "claude",
            ".com",
            ".org",
            ".net",
        ]

        self.app_indicators = [
            "word",
            "excel",
            "powerpoint",
            "outlook",
            "notepad",
            "calculator",
            "paint",
            "chrome",
            "firefox",
            "vscode",
            "spotify",
            "discord",
            "teams",
            "file explorer",
        ]

        self.browser_names = ["chrome", "firefox", "edge", "browser"]

    def parse_smart_command(self, user_input):
        """Parse user input intelligently"""
        user_input = user_input.lower().strip()

        # Check for open/launch commands
        for pattern in self.open_patterns:
            match = re.search(pattern, user_input)
            if match:
                target = match.group(1).strip()
                return self._determine_action(target, "open")

        # Check for close commands
        for pattern in self.close_patterns:
            match = re.search(pattern, user_input)
            if match:
                if "tab" in user_input:
                    return ("close_tab", "")
                elif match.groups():
                    target = match.group(1).strip()
                    # Check if it's a website being closed (close tab instead)
                    if any(site in target for site in self.website_indicators):
                        return ("close_tab", target)
                    return ("close_app", target)
                else:
                    return ("close_current", "")

        # Check for implicit commands
        if any(indicator in user_input for indicator in self.website_indicators):
            # Likely a website
            return ("open_website", user_input)

        if any(indicator in user_input for indicator in self.app_indicators):
            # Likely an application
            return ("open_app", user_input)

        return None

    def _determine_action(self, target, action_type):
        """Determine if target is an app or website"""
        target = target.lower().strip()

        # Check if it's clearly a website
        if (
            any(indicator in target for indicator in self.website_indicators)
            or "." in target
            or target.startswith("http")
        ):
            return ("open_website", target)

        # Check if it's clearly an app
        if any(indicator in target for indicator in self.app_indicators):
            return ("open_app", target)

        # Default to app for open commands
        if action_type == "open":
            return ("open_app", target)

        return ("unknown", target)

    def execute_smart_command(self, action, target):
        """Execute the parsed command"""
        try:
            if action == "open_app":
                success = launch_app(target)
                return f"{'Opened' if success else 'Failed to open'} {target}"

            elif action == "open_website":
                success = open_website(target)
                return f"{'Opened' if success else 'Failed to open'} {target}"

            elif action == "close_app":
                success = close_app(target)
                return f"{'Closed' if success else 'Failed to close'} {target}"

            elif action == "close_tab":
                success = close_tab()
                return f"{'Closed current tab' if success else 'Failed to close tab'}"

            elif action == "close_current":
                success = close_app()
                return f"{'Closed current window' if success else 'Failed to close window'}"

            else:
                return f"Unknown action: {action}"

        except Exception as e:
            return f"Error executing command: {e}"


# Global instance
intelligent_parser = IntelligentParser()


def parse_and_execute(user_input):
    result = intelligent_parser.parse_smart_command(user_input)
    if result:
        action, target = result
        return intelligent_parser.execute_smart_command(action, target)
    return None
