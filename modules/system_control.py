import os
import subprocess
import pyautogui
import psutil
from datetime import datetime

class SystemController:
    def open_app(self, app_name):
        app_name = app_name.lower()
        
        # 1. Try direct command mapping
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "spotify": "spotify.exe"
        }
        
        cmd = apps.get(app_name)
        if cmd:
            try:
                # Try running directly (works if in PATH)
                subprocess.Popen(cmd, shell=True)
                return f"Opening {app_name}."
            except:
                pass

        # 2. Try Windows 'start' command (handles many registered apps)
        try:
            os.system(f"start {app_name}")
            return f"Attempting to open {app_name}..."
        except:
            pass
            
        # 3. Specific path checks for common apps that might not be in PATH
        if "spotify" in app_name:
            user_path = os.path.expanduser("~")
            spotify_path = os.path.join(user_path, "AppData", "Roaming", "Spotify", "Spotify.exe")
            if os.path.exists(spotify_path):
                subprocess.Popen(spotify_path)
                return "Opening Spotify."
                
        return f"I couldn't find {app_name}. Try opening it manually first."

    def close_app(self, app_name):
        app_name = app_name.lower()
        try:
            # Simple taskkill by image name
            # Map common names to executables
            apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "chrome.exe",
                "spotify": "spotify.exe",
                "discord": "discord.exe"
            }
            
            exe_name = apps.get(app_name, f"{app_name}.exe")
            
            # Use taskkill /f /im
            result = subprocess.run(f"taskkill /f /im {exe_name}", shell=True, capture_output=True, text=True)
            
            if "SUCCESS" in result.stdout:
                return f"Closed {app_name}."
            elif "not found" in result.stderr:
                return f"{app_name} is not running."
            else:
                return f"Could not close {app_name}. Error: {result.stderr.strip()}"
                
        except Exception as e:
            print(f"Close App Error: {e}")
            return f"Error closing {app_name}."

    def get_system_info(self):
        battery = psutil.sensors_battery()
        percent = battery.percent if battery else "Unknown"
        time_now = datetime.now().strftime("%I:%M %p")
        return f"It is {time_now}. Battery is at {percent}%."

    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.abspath(filename)
        pyautogui.screenshot(filepath)
        return filepath

    def set_volume(self, level):
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            current_vol = volume.GetMasterVolumeLevelScalar() * 100
            
            target_vol = current_vol
            
            if isinstance(level, str):
                level = level.lower()
                if "mute" in level:
                    volume.SetMute(1, None)
                    return "Muted system volume."
                elif "unmute" in level:
                    volume.SetMute(0, None)
                    return "Unmuted system volume."
                elif "up" in level:
                    target_vol = min(100, current_vol + 10)
                elif "down" in level:
                    target_vol = max(0, current_vol - 10)
                elif "max" in level:
                    target_vol = 100
                else:
                    # Try to parse number
                    import re
                    nums = re.findall(r'\d+', level)
                    if nums:
                        target_vol = int(nums[0])
            else:
                target_vol = int(level)
                
            # Clamp
            target_vol = max(0, min(100, target_vol))
            volume.SetMasterVolumeLevelScalar(target_vol / 100, None)
            return f"Volume set to {int(target_vol)}%."
            
        except Exception as e:
            print(f"Volume Error: {e}")
            return "Could not adjust volume."

    def set_brightness(self, level):
        try:
            import screen_brightness_control as sbc
            
            current = sbc.get_brightness()
            if not current: return "Could not get current brightness."
            current_val = current[0]
            
            target_val = current_val
            
            if isinstance(level, str):
                level = level.lower()
                if "up" in level:
                    target_val = min(100, current_val + 10)
                elif "down" in level:
                    target_val = max(0, current_val - 10)
                elif "max" in level:
                    target_val = 100
                else:
                    import re
                    nums = re.findall(r'\d+', level)
                    if nums:
                        target_val = int(nums[0])
            else:
                target_val = int(level)
                
            sbc.set_brightness(target_val)
            return f"Brightness set to {int(target_val)}%."
            
        except Exception as e:
            print(f"Brightness Error: {e}")
            return "Could not adjust brightness."
