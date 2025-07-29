import os
import re
from pathlib import Path
from automation.advanced_vscode import advanced_vscode
from llm.chat import chat_with_ollama_fast


class IntelligentCodeAssistant:
    def __init__(self):
        self.common_issues = {
            "python": [
                "syntax errors",
                "indentation",
                "import issues",
                "variable scope",
                "exception handling",
                "performance",
                "code style",
            ],
            "javascript": [
                "syntax errors",
                "async/await",
                "promises",
                "scope issues",
                "null/undefined",
                "performance",
                "es6 features",
            ],
            "general": [
                "logic errors",
                "performance",
                "security",
                "best practices",
                "code organization",
                "documentation",
            ],
        }

    def parse_code_command(self, user_input):
        """Parse natural language code-related commands"""
        user_input = user_input.lower().strip()

        # Debug/fix commands
        if any(
            word in user_input
            for word in ["debug", "fix", "error", "issue", "problem", "bug"]
        ):
            if "file" in user_input:
                return "debug_file"
            return "debug_workspace"

        # Analysis commands
        if any(
            word in user_input for word in ["analyze", "review", "check", "look at"]
        ):
            if "file" in user_input or any(
                ext in user_input for ext in [".py", ".js", ".html", ".css"]
            ):
                return "analyze_file"
            return "analyze_workspace"

        # Code reading commands
        if any(
            phrase in user_input
            for phrase in ["read my code", "what does this code do", "explain code"]
        ):
            return "explain_code"

        # Improvement suggestions
        if any(
            word in user_input
            for word in ["improve", "optimize", "better", "suggestions"]
        ):
            return "suggest_improvements"

        # File operations
        if "open" in user_input and ("file" in user_input or "folder" in user_input):
            return "open_in_vscode"

        # Workspace overview
        if any(
            phrase in user_input
            for phrase in ["workspace", "project overview", "what files"]
        ):
            return "workspace_overview"

        return None

    def execute_code_command(self, command, user_input):
        """Execute the parsed code command"""
        try:
            if command == "debug_workspace":
                return self._debug_workspace(user_input)

            elif command == "debug_file":
                return self._debug_specific_file(user_input)

            elif command == "analyze_workspace":
                return self._analyze_workspace()

            elif command == "analyze_file":
                return self._analyze_specific_file(user_input)

            elif command == "explain_code":
                return self._explain_code(user_input)

            elif command == "suggest_improvements":
                return self._suggest_improvements(user_input)

            elif command == "open_in_vscode":
                return self._open_in_vscode(user_input)

            elif command == "workspace_overview":
                return self._get_workspace_overview()

            return "Unknown code command"

        except Exception as e:
            return f"Error executing code command: {e}"

    def _debug_workspace(self, user_input):
        """Debug issues in the entire workspace"""
        print("🔍 Analyzing workspace for issues...")

        # Find Python files first
        python_files = advanced_vscode.find_files_in_workspace("*.py", 5)

        if not python_files:
            return "No Python files found in workspace to debug."

        issues_found = []

        for file_path in python_files[:3]:  # Analyze first 3 files
            print(f"🔍 Checking {os.path.basename(file_path)}...")

            analysis = advanced_vscode.analyze_code_file(
                file_path, "Find bugs, syntax errors, and potential issues in this code"
            )

            if analysis and "error" not in analysis.lower()[:50]:
                issues_found.append(f"📄 {os.path.basename(file_path)}:\n{analysis}\n")

        if issues_found:
            return "🐛 Issues found in workspace:\n\n" + "\n".join(issues_found)
        else:
            return "✅ No major issues found in the analyzed files!"

    def _debug_specific_file(self, user_input):
        """Debug a specific file mentioned in the input"""
        # Extract file name from input
        words = user_input.split()
        file_name = None

        for word in words:
            if "." in word and any(
                ext in word for ext in [".py", ".js", ".html", ".css", ".txt"]
            ):
                file_name = word
                break

        if not file_name:
            # Try to find main.py or similar
            common_files = ["main.py", "app.py", "index.py", "script.py"]
            workspace = advanced_vscode.get_current_workspace()

            for common_file in common_files:
                file_path = os.path.join(workspace, common_file)
                if os.path.exists(file_path):
                    file_name = common_file
                    break

        if not file_name:
            return "Please specify which file to debug, or I couldn't find a main file."

        print(f"🔍 Debugging {file_name}...")

        analysis = advanced_vscode.analyze_code_file(
            file_name,
            "Debug this code. Find syntax errors, logic issues, and potential bugs. Provide specific fixes.",
        )

        return f"🐛 Debug analysis for {file_name}:\n\n{analysis}"

    def _analyze_workspace(self):
        """Analyze the entire workspace"""
        overview = advanced_vscode.get_workspace_overview()

        # Get code quality summary
        python_files = advanced_vscode.find_files_in_workspace("*.py", 3)

        if python_files:
            print("📊 Analyzing code quality...")

            quality_analysis = advanced_vscode.analyze_code_file(
                python_files[0],
                "Assess code quality, structure, and provide improvement suggestions",
            )

            return f"{overview}\n\n📊 Code Quality Analysis:\n{quality_analysis}"

        return overview

    def _analyze_specific_file(self, user_input):
        """Analyze a specific file"""
        # Similar to debug_specific_file but focused on analysis
        words = user_input.split()
        file_name = None

        for word in words:
            if "." in word:
                file_name = word
                break

        if not file_name:
            return "Please specify which file to analyze."

        print(f"📊 Analyzing {file_name}...")

        analysis = advanced_vscode.analyze_code_file(
            file_name,
            "Analyze this code for quality, structure, performance, and best practices",
        )

        return f"📊 Analysis for {file_name}:\n\n{analysis}"

    def _explain_code(self, user_input):
        """Explain what the code does"""
        # Find the most likely main file
        workspace = advanced_vscode.get_current_workspace()
        main_files = ["main.py", "app.py", "index.py", "__init__.py"]

        target_file = None
        for main_file in main_files:
            file_path = os.path.join(workspace, main_file)
            if os.path.exists(file_path):
                target_file = main_file
                break

        if not target_file:
            python_files = advanced_vscode.find_files_in_workspace("*.py", 1)
            if python_files:
                target_file = python_files[0]

        if not target_file:
            return "No code files found to explain."

        print(f"📖 Explaining {os.path.basename(target_file)}...")

        explanation = advanced_vscode.analyze_code_file(
            target_file,
            "Explain what this code does in simple terms. Describe its purpose, main functions, and how it works.",
        )

        return (
            f"📖 Code Explanation for {os.path.basename(target_file)}:\n\n{explanation}"
        )

    def _suggest_improvements(self, user_input):
        """Suggest code improvements"""
        python_files = advanced_vscode.find_files_in_workspace("*.py", 2)

        if not python_files:
            return "No Python files found to improve."

        print("💡 Generating improvement suggestions...")

        suggestions = advanced_vscode.analyze_code_file(
            python_files[0],
            "Suggest specific improvements for this code: performance optimizations, better practices, cleaner structure, and modern Python features.",
        )

        return f"💡 Improvement Suggestions:\n\n{suggestions}"

    def _open_in_vscode(self, user_input):
        """Open file or folder in VS Code"""
        words = user_input.split()

        # Look for file/folder name
        target = None
        for i, word in enumerate(words):
            if word.lower() in ["open", "file", "folder"] and i + 1 < len(words):
                target = words[i + 1]
                break

        if target:
            success = advanced_vscode.launch_vscode(target)
            return f"{'Opened' if success else 'Failed to open'} {target} in VS Code"
        else:
            success = advanced_vscode.launch_vscode()
            return f"{'Opened' if success else 'Failed to open'} VS Code"

    def _get_workspace_overview(self):
        """Get workspace overview"""
        return advanced_vscode.get_workspace_overview()


# Global instance
code_assistant = IntelligentCodeAssistant()


def handle_code_command(user_input):
    """Main function to handle code-related commands"""
    command = code_assistant.parse_code_command(user_input)
    if command:
        return code_assistant.execute_code_command(command, user_input)
    return None
