import pyautogui
import time
import pygetwindow as gw
from typing import Optional, Tuple, List

class ScreenController:
    def __init__(self):
        # Configure PyAutoGUI settings
        pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
        pyautogui.PAUSE = 0.5  # Pause between actions
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"🖥️ Screen resolution: {self.screen_width}x{self.screen_height}")
    
    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> bool:
        """Click at specific coordinates"""
        try:
            if 0 <= x <= self.screen_width and 0 <= y <= self.screen_height:
                pyautogui.click(x, y, clicks=clicks, button=button)
                print(f"🖱️ Clicked at ({x}, {y}) with {button} button")
                return True
            else:
                print(f"❌ Coordinates ({x}, {y}) are out of screen bounds")
                return False
        except Exception as e:
            print(f"❌ Click error: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """Type text with specified interval between characters"""
        try:
            pyautogui.write(text, interval=interval)
            print(f"⌨️ Typed: {text[:50]}{'...' if len(text) > 50 else ''}")
            return True
        except Exception as e:
            print(f"❌ Typing error: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """Press a specific key"""
        try:
            pyautogui.press(key)
            print(f"🔑 Pressed key: {key}")
            return True
        except Exception as e:
            print(f"❌ Key press error: {e}")
            return False
    
    def key_combination(self, *keys) -> bool:
        """Press key combination (e.g., ctrl+c)"""
        try:
            pyautogui.hotkey(*keys)
            print(f"🔑 Pressed combination: {'+'.join(keys)}")
            return True
        except Exception as e:
            print(f"❌ Key combination error: {e}")
            return False
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Scroll at current mouse position or specified coordinates"""
        try:
            if x is not None and y is not None:
                pyautogui.scroll(clicks, x=x, y=y)
            else:
                pyautogui.scroll(clicks)
            print(f"🖱️ Scrolled {clicks} clicks")
            return True
        except Exception as e:
            print(f"❌ Scroll error: {e}")
            return False
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> bool:
        """Drag from start coordinates to end coordinates"""
        try:
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button='left')
            print(f"🖱️ Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
        except Exception as e:
            print(f"❌ Drag error: {e}")
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        pos = pyautogui.position()
        print(f"🖱️ Mouse position: ({pos.x}, {pos.y})")
        return pos.x, pos.y
    
    def find_window(self, title_contains: str) -> Optional[object]:
        """Find window by title"""
        try:
            windows = gw.getWindowsWithTitle(title_contains)
            if windows:
                window = windows[0]
                print(f"🪟 Found window: {window.title}")
                return window
            else:
                print(f"❌ No window found containing: {title_contains}")
                return None
        except Exception as e:
            print(f"❌ Window search error: {e}")
            return None
    
    def activate_window(self, title_contains: str) -> bool:
        """Activate/focus a window by title"""
        try:
            window = self.find_window(title_contains)
            if window:
                window.activate()
                time.sleep(0.5)  # Wait for window to activate
                print(f"🪟 Activated window: {window.title}")
                return True
            return False
        except Exception as e:
            print(f"❌ Window activation error: {e}")
            return False

# Global instance
screen_controller = ScreenController()

def click_at(x: int, y: int, button: str = 'left'):
    return screen_controller.click(x, y, button)

def type_text(text: str):
    return screen_controller.type_text(text)

def press_key(key: str):
    return screen_controller.press_key(key)

def key_combo(*keys):
    return screen_controller.key_combination(*keys)

def activate_window(title: str):
    return screen_controller.activate_window(title)

def get_mouse_pos():
    return screen_controller.get_mouse_position()
