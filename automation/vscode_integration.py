import os
import subprocess
import time
import json
from pathlib import Path
from automation.screen_control import activate_window, key_combo, type_text, press_key

class VSCodeIntegration:
    def __init__(self):
        self.vscode_commands = {
            'windows': 'code',
            'darwin': 'code',  # macOS
            'linux': 'code'
        }
        
    def is_vscode_installed(self) -> bool:
        """Check if VS Code is installed and accessible"""
        try:
            result = subprocess.run(['code', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ VS Code is installed and accessible")
                return True
            else:
                print("❌ VS Code command not found")
                return False
        except Exception as e:
            print(f"❌ VS Code check failed: {e}")
            return False
    
    def open_file(self, file_path: str) -> bool:
        """Open a file in VS Code"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ File does not exist: {file_path}")
                return False
            
            result = subprocess.run(['code', file_path], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"📂 Opened file in VS Code: {file_path}")
                time.sleep(2)  # Wait for VS Code to open
                return True
            else:
                print(f"❌ Failed to open file: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error opening file: {e}")
            return False
    
    def open_folder(self, folder_path: str) -> bool:
        """Open a folder/project in VS Code"""
        try:
            if not os.path.exists(folder_path):
                print(f"❌ Folder does not exist: {folder_path}")
                return False
            
            result = subprocess.run(['code', folder_path], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"📁 Opened folder in VS Code: {folder_path}")
                time.sleep(3)  # Wait for VS Code to open
                return True
            else:
                print(f"❌ Failed to open folder: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error opening folder: {e}")
            return False
    
    def create_new_file(self, file_path: str, content: str = "") -> bool:
        """Create a new file and open it in VS Code"""
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                print(f"📁 Created directory: {directory}")
            
            # Create the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"📄 Created file: {file_path}")
            
            # Open in VS Code
            return self.open_file(file_path)
            
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return False
    
    def create_project(self, project_name: str, project_type: str = "python", base_path: str = ".") -> bool:
        """Create a new project structure"""
        try:
            project_path = os.path.join(base_path, project_name)
            
            if os.path.exists(project_path):
                print(f"❌ Project already exists: {project_path}")
                return False
            
            # Create project directory
            os.makedirs(project_path)
            print(f"📁 Created project directory: {project_path}")
            
            # Create project structure based on type
            if project_type.lower() == "python":
                self._create_python_project(project_path, project_name)
            elif project_type.lower() == "javascript" or project_type.lower() == "js":
                self._create_js_project(project_path, project_name)
            elif project_type.lower() == "react":
                return self._create_react_project(project_path, project_name)
            else:
                # Generic project
                self._create_generic_project(project_path, project_name)
            
            # Open project in VS Code
            return self.open_folder(project_path)
            
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            return False
    
    def _create_python_project(self, project_path: str, project_name: str):
        """Create Python project structure"""
        files_to_create = {
            "main.py": f'#!/usr/bin/env python3\n"""\n{project_name} - Main module\n"""\n\ndef main():\n    print("Hello from {project_name}!")\n\nif __name__ == "__main__":\n    main()\n',
            "requirements.txt": "# Add your dependencies here\n",
            "README.md": f"# {project_name}\n\nDescription of your project.\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n\n## Usage\n\n```bash\npython main.py\n```\n",
            ".gitignore": "__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\n"
        }
        
        for filename, content in files_to_create.items():
            file_path = os.path.join(project_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"🐍 Created Python project structure")
    
    def _create_js_project(self, project_path: str, project_name: str):
        """Create JavaScript project structure"""
        package_json = {
            "name": project_name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "description": "",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }
        
        files_to_create = {
            "package.json": json.dumps(package_json, indent=2),
            "index.js": f'console.log("Hello from {project_name}!");\n',
            "README.md": f"# {project_name}\n\nDescription of your project.\n\n## Installation\n\n```bash\nnpm install\n```\n\n## Usage\n\n```bash\nnpm start\n```\n",
            ".gitignore": "node_modules/\n*.log\n.env\n"
        }
        
        for filename, content in files_to_create.items():
            file_path = os.path.join(project_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"📜 Created JavaScript project structure")
    
    def _create_react_project(self, project_path: str, project_name: str) -> bool:
        """Create React project using create-react-app"""
        try:
            print(f"⚛️ Creating React project (this may take a few minutes)...")
            result = subprocess.run(['npx', 'create-react-app', project_name], 
                                  cwd=os.path.dirname(project_path),
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ React project created successfully")
                return True
            else:
                print(f"❌ Failed to create React project: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ React project creation timed out")
            return False
        except Exception as e:
            print(f"❌ Error creating React project: {e}")
            return False
    
    def _create_generic_project(self, project_path: str, project_name: str):
        """Create generic project structure"""
        files_to_create = {
            "README.md": f"# {project_name}\n\nDescription of your project.\n",
            ".gitignore": "*.log\n.env\n"
        }
        
        for filename, content in files_to_create.items():
            file_path = os.path.join(project_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"📁 Created generic project structure")
    
    def insert_code_at_cursor(self, code: str) -> bool:
        """Insert code at current cursor position in VS Code"""
        try:
            # Activate VS Code window
            if not activate_window("Visual Studio Code"):
                print("❌ Could not activate VS Code window")
                return False
            
            time.sleep(0.5)
            
            # Type the code
            if type_text(code):
                print(f"💻 Inserted code at cursor position")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error inserting code: {e}")
            return False
    
    def run_vscode_command(self, command: str) -> bool:
        """Run a VS Code command via Command Palette"""
        try:
            # Activate VS Code
            if not activate_window("Visual Studio Code"):
                return False
            
            time.sleep(0.5)
            
            # Open Command Palette (Ctrl+Shift+P)
            key_combo('ctrl', 'shift', 'p')
            time.sleep(0.5)
            
            # Type command
            type_text(command)
            time.sleep(0.5)
            
            # Press Enter
            press_key('enter')
            
            print(f"🎯 Executed VS Code command: {command}")
            return True
            
        except Exception as e:
            print(f"❌ Error running VS Code command: {e}")
            return False

# Global instance
vscode = VSCodeIntegration()

def open_file_in_vscode(file_path: str):
    return vscode.open_file(file_path)

def open_folder_in_vscode(folder_path: str):
    return vscode.open_folder(folder_path)

def create_new_file(file_path: str, content: str = ""):
    return vscode.create_new_file(file_path, content)

def create_project(name: str, project_type: str = "python"):
    return vscode.create_project(name, project_type)

def insert_code(code: str):
    return vscode.insert_code_at_cursor(code)
