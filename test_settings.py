from modules.bluetooth_control import BluetoothController
import time

print("Testing Bluetooth Settings Launch...")
bt = BluetoothController()
result = bt.open_bluetooth_settings()
print(f"Result: {result}")
print("Check if the Bluetooth Settings window opened.")
time.sleep(2)
