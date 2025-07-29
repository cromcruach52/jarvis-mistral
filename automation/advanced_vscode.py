import os
import subprocess
import time
import json
import psutil
import winreg
from pathlib import Path
from automation.screen_control import activate_window, key_combo, type_text, press_key
from llm.chat import chat_with_ollama_fast


class AdvancedVSCodeIntegration:
    def __init__(self):
        self.vscode_paths = self._find_vscode_installations()
        self.current_workspace = None
        self.current_file = None

    def _find_vscode_installations(self):
        """Find all possible VS Code installation paths"""
        possible_paths = [
            # User installation
            os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
            # System installation
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            # Insiders version
            os.path.expanduser(
                r"~\AppData\Local\Programs\Microsoft VS Code Insiders\Code - Insiders.exe"
            ),
            # Portable version
            r"C:\VSCode\Code.exe",
        ]

        # Check registry
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Code.exe",
            ) as key:
                reg_path, _ = winreg.QueryValueEx(key, "")
                if os.path.exists(reg_path):
                    possible_paths.insert(0, reg_path)
        except (FileNotFoundError, OSError):
            pass

        # Filter existing paths
        existing_paths = [path for path in possible_paths if os.path.exists(path)]

        if existing_paths:
            print(f"✅ Found VS Code installations: {len(existing_paths)}")
            for path in existing_paths:
                print(f"   📁 {path}")
        else:
            print("❌ No VS Code installations found")

        return existing_paths

    def is_vscode_running(self):
        """Check if VS Code is currently running"""
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if "code" in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def launch_vscode(self, path=None):
        """Launch VS Code with better detection"""
        if not self.vscode_paths:
            print("❌ VS Code not found. Please install VS Code first.")
            return False

        try:
            vscode_exe = self.vscode_paths[0]  # Use first found installation

            if path:
                # Open specific file or folder
                cmd = [vscode_exe, path]
            else:
                # Just open VS Code
                cmd = [vscode_exe]

            subprocess.Popen(cmd, shell=False)
            time.sleep(3)  # Wait for VS Code to start

            print(f"✅ Launched VS Code: {vscode_exe}")
            if path:
                print(f"📂 Opened: {path}")

            return True

        except Exception as e:
            print(f"❌ Failed to launch VS Code: {e}")
            return False

    def get_current_workspace(self):
        """Try to detect current VS Code workspace"""
        try:
            # Look for .vscode folder in current directory and parent directories
            current_dir = Path.cwd()

            for parent in [current_dir] + list(current_dir.parents):
                vscode_dir = parent / ".vscode"
                if vscode_dir.exists():
                    self.current_workspace = str(parent)
                    print(f"📁 Detected workspace: {self.current_workspace}")
                    return self.current_workspace

            # Fallback to current directory
            self.current_workspace = str(current_dir)
            return self.current_workspace

        except Exception as e:
            print(f"❌ Error detecting workspace: {e}")
            return None

    def read_file_content(self, file_path):
        """Read content of a file"""
        try:
            if not os.path.isabs(file_path):
                # Make relative path absolute
                workspace = self.get_current_workspace()
                if workspace:
                    file_path = os.path.join(workspace, file_path)

            if not os.path.exists(file_path):
                return None

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            print(f"📖 Read file: {file_path} ({len(content)} characters)")
            return content

        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return None

    def find_files_in_workspace(self, pattern="*.py", limit=20):
        """Find files in current workspace"""
        try:
            workspace = self.get_current_workspace()
            if not workspace:
                return []

            workspace_path = Path(workspace)
            files = []

            # Find files matching pattern
            for file_path in workspace_path.rglob(pattern):
                if file_path.is_file():
                    # Skip common ignore patterns
                    if any(
                        ignore in str(file_path)
                        for ignore in [
                            "__pycache__",
                            ".git",
                            "node_modules",
                            ".vscode",
                            "venv",
                            "env",
                            ".pytest_cache",
                        ]
                    ):
                        continue

                    files.append(str(file_path))
                    if len(files) >= limit:
                        break

            print(f"🔍 Found {len(files)} files matching '{pattern}'")
            return files

        except Exception as e:
            print(f"❌ Error finding files: {e}")
            return []

    def analyze_code_file(self, file_path, question="Analyze this code for issues"):
        """Analyze a code file using AI"""
        try:
            content = self.read_file_content(file_path)
            if not content:
                return "Could not read the file."

            # Limit content size for AI processing
            if len(content) > 8000:
                content = content[:8000] + "\n... (truncated)"

            # Detect language from file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            language_map = {
                ".py": "python",
                ".js": "javascript",
                ".ts": "typescript",
                ".html": "html",
                ".css": "css",
                ".java": "java",
                ".cpp": "cpp",
                ".c": "c",
                ".go": "go",
                ".rs": "rust",
            }
            language = language_map.get(file_ext, "text")

            prompt = f"""I'm analyzing a {language} code file: {os.path.basename(file_path)}

CODE CONTENT:
\`\`\`{language}
{content}
\`\`\`

ANALYSIS REQUEST: {question}

Please provide:
1. Code quality assessment
2. Potential bugs or issues
3. Suggestions for improvement
4. Best practices recommendations
5. Security considerations (if applicable)

Keep your response practical and actionable. Focus on the most important issues first."""

            response = chat_with_ollama_fast(prompt)
            return response

        except Exception as e:
            return f"Error analyzing code: {e}"

    def get_workspace_overview(self):
        """Get an overview of the current workspace"""
        try:
            workspace = self.get_current_workspace()
            if not workspace:
                return "No workspace detected."

            workspace_path = Path(workspace)

            # Count different file types
            file_counts = {}
            total_files = 0
            total_size = 0

            for file_path in workspace_path.rglob("*"):
                if file_path.is_file():
                    # Skip ignored directories
                    if any(
                        ignore in str(file_path)
                        for ignore in [
                            "__pycache__",
                            ".git",
                            "node_modules",
                            ".vscode",
                            "venv",
                            "env",
                            ".pytest_cache",
                            "dist",
                            "build",
                        ]
                    ):
                        continue

                    ext = file_path.suffix.lower()
                    file_counts[ext] = file_counts.get(ext, 0) + 1
                    total_files += 1

                    try:
                        total_size += file_path.stat().st_size
                    except:
                        pass

            # Format size
            if total_size > 1024 * 1024:
                size_str = f"{total_size / (1024 * 1024):.1f} MB"
            elif total_size > 1024:
                size_str = f"{total_size / 1024:.1f} KB"
            else:
                size_str = f"{total_size} bytes"

            # Create overview
            overview = f"📁 Workspace: {workspace_path.name}\n"
            overview += f"📊 Total files: {total_files}\n"
            overview += f"💾 Total size: {size_str}\n\n"
            overview += "File types:\n"

            for ext, count in sorted(
                file_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]:
                if ext:
                    overview += f"  {ext}: {count} files\n"
                else:
                    overview += f"  (no extension): {count} files\n"

            return overview

        except Exception as e:
            return f"Error getting workspace overview: {e}"

    def execute_vscode_command(self, command):
        """Execute VS Code command via Command Palette"""
        try:
            if not self.is_vscode_running():
                print("VS Code is not running. Launching...")
                if not self.launch_vscode():
                    return False
                time.sleep(2)

            # Activate VS Code window
            if not activate_window("Visual Studio Code"):
                if not activate_window("Code"):
                    print("❌ Could not activate VS Code window")
                    return False

            time.sleep(0.5)

            # Open Command Palette
            key_combo("ctrl", "shift", "p")
            time.sleep(0.5)

            # Type command
            type_text(command)
            time.sleep(0.5)

            # Execute
            press_key("enter")

            print(f"🎯 Executed VS Code command: {command}")
            return True

        except Exception as e:
            print(f"❌ Error executing VS Code command: {e}")
            return False


# Global instance - THIS WAS MISSING!
advanced_vscode = AdvancedVSCodeIntegration()


# Export functions
def launch_vscode(path=None):
    return advanced_vscode.launch_vscode(path)


def analyze_current_file(question="Analyze this code"):
    workspace = advanced_vscode.get_current_workspace()
    if workspace:
        python_files = advanced_vscode.find_files_in_workspace("*.py", 5)
        if python_files:
            return advanced_vscode.analyze_code_file(python_files[0], question)
    return "No code files found to analyze"


def get_workspace_info():
    return advanced_vscode.get_workspace_overview()


def find_code_files(pattern="*.py"):
    return advanced_vscode.find_files_in_workspace(pattern)


def analyze_specific_file(file_path, question="Analyze this code"):
    return advanced_vscode.analyze_code_file(file_path, question)
