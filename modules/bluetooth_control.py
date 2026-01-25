import asyncio
import os
from winsdk.windows.devices.enumeration import DeviceInformation, DeviceClass
from winsdk.windows.devices.bluetooth import BluetoothDevice
from pycaw.pycaw import AudioUtilities

class BluetoothController:
    async def list_paired_devices_async(self):
        # Find all paired Bluetooth devices
        # Selector for Bluetooth devices
        selector = BluetoothDevice.get_device_selector()
        devices = await DeviceInformation.find_all_async(selector)
        
        paired_devices = []
        for d in devices:
            # We can check properties if needed, but for now just name
            paired_devices.append(d.name)
        return paired_devices

    def list_paired_devices(self):
        try:
            return asyncio.run(self.list_paired_devices_async())
        except Exception as e:
            print(f"Bluetooth Scan Error: {e}")
            return []

    def open_bluetooth_settings(self):
        try:
            import webbrowser
            webbrowser.open("ms-settings:bluetooth")
            return "Opening Bluetooth settings. Please select your device."
        except Exception as e:
            print(f"Error opening settings: {e}")
            return "I couldn't open the settings page."

    def is_device_connected(self, device_name):
        # Check audio endpoints (speakers)
        try:
            devices = AudioUtilities.GetSpeakers()
            # This gets the default, we want all
            # Actually pycaw is a bit limited for enumeration of ALL devices easily without comtypes magic
            # But we can try to see if the default device matches
            
            # Better approach: Use sounddevice if available, or just check if default device changed
            # For now, let's just return True if we assume the user connected it
            pass
        except:
            pass
            
        # Fallback: Check if device is in the list of "connected" bluetooth devices via winsdk
        # This requires async again
        return self.check_connection_status(device_name)

    async def _get_device_by_name(self, name):
        # Use AQS filter to find device by name (contains match)
        # This is much faster and broader than specific selectors
        aqs = f"System.ItemNameDisplay ~~ \"{name}\""
        devices = await DeviceInformation.find_all_async(aqs)
        
        # Prioritize connected devices or those that look like Bluetooth
        for d in devices:
            # print(f"DEBUG: Found candidate {d.name} ({d.id})")
            return d # Return the first match for now
            
        return None

    async def _get_jabba_status(self):
        d = await self._get_device_by_name("Jabba")
        if d:
            try:
                bt_device = await BluetoothDevice.from_id_async(d.id)
                # print(f"DEBUG: Jabba Status: {bt_device.connection_status}")
                return bt_device.connection_status == 1 # Connected
            except Exception as e:
                print(f"DEBUG: Error checking status: {e}")
                return False
        return False

    def check_jabba_status(self):
        try:
            return asyncio.run(self._get_jabba_status())
        except:
            return False

    def connect_jabba(self):
        # Try to check status first
        if self.check_jabba_status():
            return "Jabba is already connected and ready to rock."
            
        # If not connected, we can try to 'poke' it by creating the object
        # This sometimes triggers Windows to auto-connect known devices
        try:
            asyncio.run(self._get_jabba_status())
        except:
            pass
            
        # Fallback to settings
        self.open_bluetooth_settings()
        return "I've opened settings. Please select Jabba to connect."
