from modules.bluetooth_control import BluetoothController
import time

print("Testing Jabba Connection Logic...")
bt = BluetoothController()

# 1. Check status
print("Checking status...")
status = bt.check_jabba_status()
print(f"Is Jabba connected? {status}")

# 2. Simulate Connect Command
print("Simulating 'Connect Jabba' command...")
msg = bt.connect_jabba()
print(f"Response Message: {msg}")

if "already connected" in msg:
    print("SUCCESS: Detected Jabba is connected.")
elif "opened settings" in msg:
    print("SUCCESS: Fallback to settings worked (if Jabba was disconnected).")
else:
    print("WARNING: Unexpected response.")
