import time
from automation.screen_control import (
    click_at,
    type_text,
    press_key,
    key_combo,
    get_mouse_pos,
)
from automation.vscode_integration import (
    open_file_in_vscode,
    open_folder_in_vscode,
    create_new_file,
    create_project,
    insert_code,
)
from vision.screen_analysis import (
    take_screenshot,
    analyze_screen,
    find_errors,
    extract_screen_text,
    find_text,
)
from voice.output import speak


class CommandHandlers:
    def __init__(self, text_mode=False):
        self.text_mode = text_mode

    def set_text_mode(self, text_mode):
        self.text_mode = text_mode

    def handle_automation_commands(self, action, user_input):
        """Handle automation-related commands"""
        try:
            message = ""

            if action == "click_command":
                words = user_input.lower().split()
                coords = [word for word in words if word.isdigit()]
                if len(coords) >= 2:
                    x, y = int(coords[0]), int(coords[1])
                    success = click_at(x, y)
                    message = f"Clicked at ({x}, {y})" if success else "Click failed"
                else:
                    message = "Please specify coordinates like 'click at 100 200'"

            elif action == "type_command":
                if "type" in user_input.lower():
                    text_start = user_input.lower().find("type") + 4
                    text_to_type = user_input[text_start:].strip().strip("\"'")
                    if text_to_type:
                        success = type_text(text_to_type)
                        message = (
                            f"Typed: {text_to_type}" if success else "Typing failed"
                        )
                    else:
                        message = "Please specify text to type"
                else:
                    message = "Please specify text to type"

            elif action == "press_key_command":
                words = user_input.lower().split()
                if "key" in words:
                    key_index = words.index("key") + 1
                    if key_index < len(words):
                        key = words[key_index]
                        success = press_key(key)
                        message = (
                            f"Pressed key: {key}" if success else "Key press failed"
                        )
                    else:
                        message = "Please specify which key to press"
                else:
                    message = "Please specify which key to press"

            elif action == "mouse_position":
                x, y = get_mouse_pos()
                message = f"Mouse is at position ({x}, {y})"

            print(f"🤖 {message}")
            if not self.text_mode:
                speak(message)

        except Exception as e:
            error_msg = f"Automation error: {e}"
            print(f"❌ {error_msg}")
            if not self.text_mode:
                speak(error_msg)

    def handle_vscode_commands(self, action, user_input):
        """Handle VS Code related commands"""
        try:
            message = ""

            if action == "open_file":
                words = user_input.split()
                file_path = None
                for i, word in enumerate(words):
                    if word.lower() in ["file", "open"] and i + 1 < len(words):
                        file_path = " ".join(words[i + 1 :])
                        break

                if file_path:
                    success = open_file_in_vscode(file_path.strip("\"'"))
                    message = (
                        f"Opened file: {file_path}"
                        if success
                        else "Failed to open file"
                    )
                else:
                    message = "Please specify a file path"

            elif action == "open_folder":
                words = user_input.split()
                folder_path = None
                for i, word in enumerate(words):
                    if word.lower() in ["folder", "project"] and i + 1 < len(words):
                        folder_path = " ".join(words[i + 1 :])
                        break

                if folder_path:
                    success = open_folder_in_vscode(folder_path.strip("\"'"))
                    message = (
                        f"Opened folder: {folder_path}"
                        if success
                        else "Failed to open folder"
                    )
                else:
                    message = "Please specify a folder path"

            elif action == "create_file":
                words = user_input.split()
                file_name = None
                for i, word in enumerate(words):
                    if word.lower() in ["file", "create"] and i + 1 < len(words):
                        file_name = " ".join(words[i + 1 :])
                        break

                if file_name:
                    success = create_new_file(file_name.strip("\"'"))
                    message = (
                        f"Created file: {file_name}"
                        if success
                        else "Failed to create file"
                    )
                else:
                    message = "Please specify a file name"

            elif action == "create_project":
                words = user_input.lower().split()
                project_name = None
                project_type = "python"

                for i, word in enumerate(words):
                    if word in ["project", "create"] and i + 1 < len(words):
                        remaining = words[i + 1 :]
                        if "python" in remaining:
                            project_type = "python"
                            remaining.remove("python")
                        elif "javascript" in remaining or "js" in remaining:
                            project_type = "javascript"
                            if "javascript" in remaining:
                                remaining.remove("javascript")
                            if "js" in remaining:
                                remaining.remove("js")
                        elif "react" in remaining:
                            project_type = "react"
                            remaining.remove("react")

                        project_name = " ".join(remaining).strip()
                        break

                if project_name:
                    success = create_project(project_name, project_type)
                    message = (
                        f"Created {project_type} project: {project_name}"
                        if success
                        else "Failed to create project"
                    )
                else:
                    message = "Please specify a project name"

            elif action == "insert_code":
                if "code" in user_input.lower():
                    code_start = user_input.lower().find("code") + 4
                    code_to_insert = user_input[code_start:].strip().strip("\"'")
                    if code_to_insert:
                        success = insert_code(code_to_insert)
                        message = (
                            "Code inserted" if success else "Failed to insert code"
                        )
                    else:
                        message = "Please specify code to insert"
                else:
                    message = "Please specify code to insert"

            print(f"💻 {message}")
            if not self.text_mode:
                speak(message)

        except Exception as e:
            error_msg = f"VS Code error: {e}"
            print(f"❌ {error_msg}")
            if not self.text_mode:
                speak(error_msg)

    def handle_vision_commands(self, action, user_input):
        """Handle screen analysis commands"""
        try:
            message = ""

            if action == "take_screenshot":
                screenshot_path = take_screenshot()
                message = (
                    f"Screenshot saved: {screenshot_path}"
                    if screenshot_path
                    else "Screenshot failed"
                )

            elif action == "analyze_screen":
                print("🔍 Analyzing screen content...")
                analysis = analyze_screen()
                message = f"Screen analysis: {analysis}"

            elif action == "find_errors":
                print("🔍 Looking for errors on screen...")
                error_analysis = find_errors()
                message = f"Error check: {error_analysis}"

            elif action == "extract_text":
                print("📝 Extracting text from screen...")
                screen_text = extract_screen_text()
                message = f"Screen text: {screen_text[:200]}{'...' if len(screen_text) > 200 else ''}"

            elif action == "find_text":
                words = user_input.lower().split()
                search_text = None
                for i, word in enumerate(words):
                    if word in ["find", "text"] and i + 1 < len(words):
                        search_text = " ".join(words[i + 1 :]).strip("\"'")
                        break

                if search_text:
                    found = find_text(search_text)
                    message = f"Text '{search_text}' {'found' if found else 'not found'} on screen"
                else:
                    message = "Please specify text to search for"

            print(f"👁️ {message}")
            if not self.text_mode:
                speak(message)

        except Exception as e:
            error_msg = f"Vision error: {e}"
            print(f"❌ {error_msg}")
            if not self.text_mode:
                speak(error_msg)

    def handle_system_commands(self, action, user_input):
        """Handle system automation commands"""
        try:
            message = ""

            if action == "open_file_explorer":
                success = key_combo("win", "e")
                message = (
                    "Opened File Explorer"
                    if success
                    else "Failed to open File Explorer"
                )

            elif action == "open_calculator":
                success = key_combo("win", "r")
                if success:
                    time.sleep(0.5)
                    type_text("calc")
                    press_key("enter")
                    message = "Opened Calculator"
                else:
                    message = "Failed to open Calculator"

            elif action == "open_notepad":
                success = key_combo("win", "r")
                if success:
                    time.sleep(0.5)
                    type_text("notepad")
                    press_key("enter")
                    message = "Opened Notepad"
                else:
                    message = "Failed to open Notepad"

            elif action == "open_browser":
                browsers = ["chrome", "firefox", "msedge", "iexplore"]
                success = False
                for browser in browsers:
                    try:
                        success = key_combo("win", "r")
                        if success:
                            time.sleep(0.5)
                            type_text(browser)
                            press_key("enter")
                            message = f"Opened {browser.title()}"
                            break
                    except:
                        continue

                if not success:
                    message = "Failed to open browser"

            print(f"🖥️ {message}")
            if not self.text_mode:
                speak(message)

        except Exception as e:
            error_msg = f"System command error: {e}"
            print(f"❌ {error_msg}")
            if not self.text_mode:
                speak(error_msg)
