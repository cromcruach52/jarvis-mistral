import pyautogui
import pytesseract
import os
import tempfile
from datetime import datetime
from PIL import Image
from llm.chat import chat_with_ollama_fast

class ScreenAnalyzer:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.screenshot_count = 0
        
        # Try to configure tesseract path (Windows)
        self._configure_tesseract()
    
    def _configure_tesseract(self):
        """Configure tesseract OCR path"""
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            '/usr/bin/tesseract',  # Linux
            '/opt/homebrew/bin/tesseract',  # macOS with Homebrew
            '/usr/local/bin/tesseract'  # macOS
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"✅ Found Tesseract at: {path}")
                return
        
        print("⚠️ Tesseract not found. OCR features may not work.")
        print("💡 Install Tesseract: https://github.com/tesseract-ocr/tesseract")
    
    def take_screenshot(self, region=None, save_path=None) -> str:
        """Take a screenshot and return the file path"""
        try:
            # Take screenshot
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            # Generate filename if not provided
            if not save_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.screenshot_count += 1
                filename = f"jarvis_screenshot_{timestamp}_{self.screenshot_count}.png"
                save_path = os.path.join(self.temp_dir, filename)
            
            # Save screenshot
            screenshot.save(save_path)
            print(f"📸 Screenshot saved: {save_path}")
            
            return save_path
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def extract_text_from_screen(self, region=None) -> str:
        """Extract text from screen using OCR"""
        try:
            screenshot_path = self.take_screenshot(region)
            if not screenshot_path:
                return None
            
            # Open image and extract text
            image = Image.open(screenshot_path)
            text = pytesseract.image_to_string(image)
            
            # Clean up temporary file
            try:
                os.remove(screenshot_path)
            except:
                pass
            
            if text.strip():
                print(f"📝 Extracted text from screen ({len(text)} characters)")
                return text.strip()
            else:
                print("📝 No text found on screen")
                return "No text detected on screen"
                
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return f"Error extracting text: {e}"
    
    def analyze_screen_with_ai(self, region=None, question="What do you see on this screen?") -> str:
        """Take screenshot, extract text, and analyze with AI"""
        try:
            print("🔍 Analyzing screen...")
            
            # Extract text from screen
            screen_text = self.extract_text_from_screen(region)
            
            if not screen_text or screen_text.startswith("Error"):
                return "I couldn't read any text from the screen. The screen might be mostly graphical or the OCR failed."
            
            # Create prompt for AI analysis
            prompt = f"""I took a screenshot of my computer screen and extracted the following text using OCR:

TEXT FROM SCREEN:
{screen_text}

USER QUESTION: {question}

Please analyze this screen content and provide a helpful response. Focus on:
1. What applications or content appear to be visible
2. Any errors, issues, or important information
3. Suggestions or next steps if relevant

Keep your response concise and practical."""

            # Get AI analysis
            response = chat_with_ollama_fast(prompt)
            
            print("🤖 Screen analysis complete")
            return response
            
        except Exception as e:
            print(f"❌ Screen analysis error: {e}")
            return f"Error analyzing screen: {e}"
    
    def find_text_on_screen(self, search_text: str) -> bool:
        """Check if specific text exists on screen"""
        try:
            screen_text = self.extract_text_from_screen()
            if screen_text and search_text.lower() in screen_text.lower():
                print(f"✅ Found text on screen: '{search_text}'")
                return True
            else:
                print(f"❌ Text not found on screen: '{search_text}'")
                return False
                
        except Exception as e:
            print(f"❌ Text search error: {e}")
            return False
    
    def get_screen_info(self) -> dict:
        """Get basic screen information"""
        try:
            screen_size = pyautogui.size()
            mouse_pos = pyautogui.position()
            
            info = {
                "screen_width": screen_size.width,
                "screen_height": screen_size.height,
                "mouse_x": mouse_pos.x,
                "mouse_y": mouse_pos.y,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"🖥️ Screen: {info['screen_width']}x{info['screen_height']}, Mouse: ({info['mouse_x']}, {info['mouse_y']})")
            return info
            
        except Exception as e:
            print(f"❌ Screen info error: {e}")
            return {}
    
    def describe_screen(self) -> str:
        """Get a description of what's currently on screen"""
        return self.analyze_screen_with_ai(question="Describe what's currently visible on this screen. What applications are open and what is the user likely doing?")
    
    def find_errors_on_screen(self) -> str:
        """Look for errors or issues on screen"""
        return self.analyze_screen_with_ai(question="Look for any errors, warnings, or issues visible on this screen. Are there any problems that need attention?")
    
    def cleanup_screenshots(self):
        """Clean up old screenshot files"""
        try:
            count = 0
            for filename in os.listdir(self.temp_dir):
                if filename.startswith("jarvis_screenshot_") and filename.endswith(".png"):
                    file_path = os.path.join(self.temp_dir, filename)
                    try:
                        os.remove(file_path)
                        count += 1
                    except:
                        pass
            
            if count > 0:
                print(f"🧹 Cleaned up {count} old screenshots")
                
        except Exception as e:
            print(f"❌ Cleanup error: {e}")

# Global instance
screen_analyzer = ScreenAnalyzer()

def take_screenshot(region=None):
    return screen_analyzer.take_screenshot(region)

def analyze_screen(question="What do you see on this screen?"):
    return screen_analyzer.analyze_screen_with_ai(question=question)

def describe_screen():
    return screen_analyzer.describe_screen()

def find_errors():
    return screen_analyzer.find_errors_on_screen()

def extract_screen_text():
    return screen_analyzer.extract_text_from_screen()

def find_text(search_text: str):
    return screen_analyzer.find_text_on_screen(search_text)
