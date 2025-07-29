import subprocess
import os
import time
import webbrowser
import psutil
import winreg
from automation.screen_control import key_combo, type_text, press_key

class SmartLauncher:
    def __init__(self):
        # Common applications and their launch commands
        self.applications = {
            # Microsoft Office - multiple possible commands
            'word': [
                'winword.exe', 'winword', 'WINWORD.EXE', 
                r'"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"',
                r'"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE"',
                r'"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE"',
                'Microsoft Word'
            ],
            'excel': [
                'excel.exe', 'excel', 'EXCEL.EXE',
                r'"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"',
                r'"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE"',
                r'"C:\Program Files\Microsoft Office\Office16\EXCEL.EXE"',
                'Microsoft Excel'
            ],
            'powerpoint': [
                'powerpnt.exe', 'powerpnt', 'POWERPNT.EXE',
                r'"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"',
                r'"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE"',
                r'"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE"',
                'Microsoft PowerPoint'
            ],
            'outlook': [
                'outlook.exe', 'outlook', 'OUTLOOK.EXE',
                r'"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"',
                r'"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"',
                r'"C:\Program Files\Microsoft Office\Office16\OUTLOOK.EXE"',
                'Microsoft Outlook'
            ],
            'onenote': [
                'onenote.exe', 'onenote', 'ONENOTE.EXE',
                r'"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE"',
                r'"C:\Program Files (x86)\Microsoft Office\root\Office16\ONENOTE.EXE"',
                'Microsoft OneNote'
            ],
            'teams': [
                'ms-teams.exe', 'Teams.exe', 'teams.exe',
                r'"C:\Users\%USERNAME%\AppData\Local\Microsoft\Teams\current\Teams.exe"',
                'Microsoft Teams'
            ],
            
            # Browsers - better detection
            'chrome': [
                'chrome.exe', 'chrome',
                r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
                r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"',
                'Google Chrome'
            ],
            'firefox': [
                'firefox.exe', 'firefox',
                r'"C:\Program Files\Mozilla Firefox\firefox.exe"',
                r'"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"',
                'Mozilla Firefox'
            ],
            'edge': [
                'msedge.exe', 'msedge', 'microsoft-edge',
                r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"',
                'Microsoft Edge'
            ],
            
            # Development tools - FIXED VS CODE DETECTION
            'vscode': [
                r'"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
                r'"C:\Program Files\Microsoft VS Code\Code.exe"',
                r'"C:\Program Files (x86)\Microsoft VS Code\Code.exe"',
                'code.exe',
                'Visual Studio Code'
            ],
            'vs code': [
                r'"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
                r'"C:\Program Files\Microsoft VS Code\Code.exe"',
                r'"C:\Program Files (x86)\Microsoft VS Code\Code.exe"',
                'code.exe',
                'Visual Studio Code'
            ],
            'visual studio code': [
                r'"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
                r'"C:\Program Files\Microsoft VS Code\Code.exe"',
                r'"C:\Program Files (x86)\Microsoft VS Code\Code.exe"',
                'code.exe',
                'Visual Studio Code'
            ],
            'visual studio': ['devenv.exe', 'devenv', 'Visual Studio'],
            'cmd': ['cmd.exe', 'cmd', 'Command Prompt'],
            'powershell': ['powershell.exe', 'powershell', 'PowerShell'],
            
            # System apps
            'notepad': ['notepad.exe', 'notepad', 'Notepad'],
            'calculator': ['calc.exe', 'calc', 'Calculator'],
            'paint': ['mspaint.exe', 'mspaint', 'Paint'],
            'file explorer': ['explorer.exe', 'explorer', 'File Explorer'],
            'task manager': ['taskmgr.exe', 'taskmgr', 'Task Manager'],
            'control panel': ['control.exe', 'control', 'Control Panel'],
            'settings': ['ms-settings:', 'Settings'],
            
            # Media
            'spotify': [
                'spotify.exe', 'spotify',
                r'"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe"',
                'Spotify'
            ],
            'vlc': ['vlc.exe', 'vlc', 'VLC Media Player'],
            'windows media player': ['wmplayer.exe', 'wmplayer', 'Windows Media Player'],
            
            # Communication
            'discord': [
                'discord.exe', 'discord',
                r'"C:\Users\%USERNAME%\AppData\Local\Discord\app-*\Discord.exe"',
                'Discord'
            ],
            'skype': ['skype.exe', 'skype', 'Skype'],
            'zoom': ['zoom.exe', 'zoom', 'Zoom'],
            'slack': ['slack.exe', 'slack', 'Slack'],
        }
        
        # Common websites
        self.websites = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://instagram.com',
            'linkedin': 'https://linkedin.com',
            'reddit': 'https://reddit.com',
            'github': 'https://github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'gmail': 'https://gmail.com',
            'outlook web': 'https://outlook.live.com',
            'netflix': 'https://netflix.com',
            'amazon': 'https://amazon.com',
            'ebay': 'https://ebay.com',
            'wikipedia': 'https://wikipedia.org',
            'chatgpt': 'https://chat.openai.com',
            'claude': 'https://claude.ai',
        }
        
        # Track opened applications for better closing
        self.opened_apps = []
    
    def _find_office_installation(self):
        """Find Microsoft Office installation paths"""
        office_paths = []
        possible_roots = [
            r"C:\Program Files\Microsoft Office",
            r"C:\Program Files (x86)\Microsoft Office",
        ]
        
        for root in possible_roots:
            if os.path.exists(root):
                # Look for different Office versions
                for version in ['root\\Office16', 'Office16', 'Office15', 'Office14']:
                    full_path = os.path.join(root, version)
                    if os.path.exists(full_path):
                        office_paths.append(full_path)
        
        return office_paths
    
    def _try_registry_lookup(self, app_name):
        """Try to find application path in Windows registry"""
        try:
            # Common registry locations for applications
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"
            ]
            
            for reg_path in registry_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{reg_path}\\{app_name}.exe") as key:
                        app_path, _ = winreg.QueryValueEx(key, "")
                        if os.path.exists(app_path):
                            return app_path
                except (FileNotFoundError, OSError):
                    continue
        except Exception:
            pass
        return None
    
    def _find_vscode_path(self):
        """Find VS Code installation path specifically"""
        possible_paths = [
            os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code Insiders\Code - Insiders.exe"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
    
    # Try registry
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Code.exe") as key:
                reg_path, _ = winreg.QueryValueEx(key, "")
                if os.path.exists(reg_path):
                    return reg_path
        except (FileNotFoundError, OSError):
            pass
    
        return None
    
    def launch_application(self, app_name):
        """Launch an application by name"""
        app_name = app_name.lower().strip()
        
        # Handle common variations
        if app_name in ['vs code', 'vscode', 'visual studio code']:
            app_name = 'vscode'
        elif app_name in ['bs code']:  # Handle speech recognition errors
            app_name = 'vscode'
        
        # Direct match
        if app_name in self.applications:
            return self._try_launch_app(app_name, self.applications[app_name])
        
        # Fuzzy match
        for key in self.applications:
            if app_name in key or key in app_name:
                return self._try_launch_app(key, self.applications[key])
        
        # Try as direct command - but with better error handling
        return self._try_direct_launch(app_name)
    
    def _try_launch_app(self, app_name, commands):
        """Try different methods to launch an app"""
        print(f"🚀 Attempting to launch {app_name}...")
        
        # Special handling for VS Code
        if app_name in ['vscode', 'vs code', 'visual studio code']:
            vscode_path = self._find_vscode_path()
            if vscode_path:
                try:
                    process = subprocess.Popen([vscode_path], shell=False)
                    self.opened_apps.append({'name': app_name, 'pid': process.pid})
                    print(f"✅ Launched VS Code using: {vscode_path}")
                    return True
                except Exception as e:
                    print(f"Failed to launch VS Code directly: {e}")
        
        # Method 1: Try registry lookup first for Office apps and VS Code
        if 'office' in app_name.lower() or app_name in ['word', 'excel', 'powerpoint', 'outlook', 'vscode']:
            registry_path = self._try_registry_lookup(commands[0].split('.')[0])
            if registry_path:
                try:
                    process = subprocess.Popen([registry_path], shell=False)
                    self.opened_apps.append({'name': app_name, 'pid': process.pid})
                    print(f"✅ Launched {app_name} from registry: {registry_path}")
                    return True
                except Exception:
                    pass
        
        # Method 2: Try direct subprocess with different commands
        for cmd in commands:
            try:
                # Expand environment variables
                expanded_cmd = os.path.expandvars(cmd)
                
                # Skip display names (they're not executable commands)
                if any(word in expanded_cmd for word in ['Visual Studio Code', 'Microsoft Word', 'Microsoft Excel', 'Google Chrome', 'Mozilla Firefox']):
                    continue
                
                # Try executable paths first
                if expanded_cmd.endswith('.exe'):
                    exe_path = expanded_cmd.strip('"')
                    if os.path.exists(exe_path):
                        process = subprocess.Popen([exe_path], shell=False)
                        self.opened_apps.append({'name': app_name, 'pid': process.pid})
                        print(f"✅ Launched {app_name} using: {exe_path}")
                        return True
                
                # Try simple commands that we know exist
                elif expanded_cmd in ['notepad', 'calc', 'mspaint', 'explorer', 'taskmgr', 'control', 'cmd', 'powershell']:
                    try:
                        # Verify command exists first
                        result = subprocess.run(f'where {expanded_cmd}', shell=True, capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            process = subprocess.Popen(expanded_cmd, shell=True)
                            self.opened_apps.append({'name': app_name, 'pid': process.pid})
                            print(f"✅ Launched {app_name} using command: {expanded_cmd}")
                            return True
                    except Exception:
                        continue
                
                # Try .exe commands
                elif expanded_cmd.endswith('.exe') and not '\\' in expanded_cmd:
                    try:
                        # Check if command exists in PATH
                        result = subprocess.run(f'where {expanded_cmd}', shell=True, capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            process = subprocess.Popen(expanded_cmd, shell=True)
                            self.opened_apps.append({'name': app_name, 'pid': process.pid})
                            print(f"✅ Launched {app_name} using: {expanded_cmd}")
                            return True
                    except Exception:
                        continue
                
            except Exception as e:
                continue
        
        # Method 3: Windows Run dialog (only for simple commands)
        simple_commands = [cmd for cmd in commands if not any(word in cmd for word in ['Visual Studio Code', 'Microsoft', 'Google', 'Mozilla']) and not '\\' in cmd]
        if simple_commands:
            try:
                key_combo('win', 'r')
                time.sleep(0.5)
                type_text(simple_commands[0])
                press_key('enter')
                print(f"✅ Launched {app_name} via Run dialog")
                return True
            except Exception:
                pass
        
        # Method 4: Start menu search
        try:
            press_key('win')
            time.sleep(0.5)
            # Use the full application name for better search results
            search_term = app_name
            if app_name == 'vscode':
                search_term = 'Visual Studio Code'
            elif app_name == 'vs code':
                search_term = 'Visual Studio Code'
            
            type_text(search_term)
            time.sleep(1.5)  # Wait longer for search results
            press_key('enter')
            print(f"✅ Launched {app_name} via Start menu")
            return True
        except Exception:
            pass
        
        print(f"❌ Failed to launch {app_name}")
        return False
    
    def _try_direct_launch(self, app_name):
        """Try to launch app directly by name with better error handling"""
        try:
            # First check if the command exists
            result = subprocess.run(f'where {app_name}', shell=True, capture_output=True, text=True)
            if result.returncode == 0:  # Command exists
                process = subprocess.Popen(app_name, shell=True)
                self.opened_apps.append({'name': app_name, 'pid': process.pid})
                print(f"✅ Launched {app_name} directly")
                return True
            else:
                # Command doesn't exist, try Start menu search
                try:
                    press_key('win')
                    time.sleep(0.5)
                    type_text(app_name)
                    time.sleep(1.5)
                    press_key('enter')
                    print(f"✅ Launched {app_name} via Start menu search")
                    return True
                except:
                    print(f"❌ Could not launch {app_name}")
                    return False
        except:
            print(f"❌ Could not launch {app_name}")
            return False
    
    def open_website(self, site_name):
        """Open a website by name"""
        site_name = site_name.lower().strip()
        
        # Direct match
        if site_name in self.websites:
            url = self.websites[site_name]
            webbrowser.open(url)
            print(f"🌐 Opened {site_name}: {url}")
            return True
        
        # Fuzzy match
        for key in self.websites:
            if site_name in key or key in site_name:
                url = self.websites[key]
                webbrowser.open(url)
                print(f"🌐 Opened {key}: {url}")
                return True
        
        # Try as direct URL or search
        if '.' in site_name or site_name.startswith('http'):
            # Looks like a URL
            if not site_name.startswith('http'):
                site_name = 'https://' + site_name
            webbrowser.open(site_name)
            print(f"🌐 Opened URL: {site_name}")
            return True
        else:
            # Search on Google
            search_url = f"https://google.com/search?q={site_name.replace(' ', '+')}"
            webbrowser.open(search_url)
            print(f"🔍 Searched for: {site_name}")
            return True
    
    def close_application(self, app_name=None):
        """Close an application - improved version"""
        try:
            if app_name:
                app_name = app_name.lower().strip()
                
                # Try to close specific application by process name
                closed = False
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        proc_name = proc.info['name'].lower()
                        
                        # Check if process name matches the app
                        if (app_name in proc_name or 
                            proc_name.startswith(app_name) or
                            any(app_name in cmd for cmd in self.applications.get(app_name, []))):
                            
                            proc.terminate()
                            print(f"🔴 Closed {proc_name} (PID: {proc.info['pid']})")
                            closed = True
                            
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if closed:
                    return True
            
            # Fallback: Close current window with Alt+F4
            key_combo('alt', 'f4')
            print(f"🔴 Sent close command to current window")
            return True
            
        except Exception as e:
            print(f"❌ Failed to close application: {e}")
            return False
    
    def close_browser_tab(self):
        """Close current browser tab instead of entire browser"""
        try:
            key_combo('ctrl', 'w')
            print(f"🔴 Closed current browser tab")
            return True
        except Exception as e:
            print(f"❌ Failed to close browser tab: {e}")
            return False
    
    def get_available_apps(self):
        """Get list of available applications"""
        return list(self.applications.keys())
    
    def get_available_websites(self):
        """Get list of available websites"""
        return list(self.websites.keys())

# Global instance
smart_launcher = SmartLauncher()

def launch_app(app_name):
    return smart_launcher.launch_application(app_name)

def open_website(site_name):
    return smart_launcher.open_website(site_name)

def close_app(app_name=None):
    return smart_launcher.close_application(app_name)

def close_tab():
    return smart_launcher.close_browser_tab()

def get_available_apps():
    return smart_launcher.get_available_apps()

def get_available_websites():
    return smart_launcher.get_available_websites()
