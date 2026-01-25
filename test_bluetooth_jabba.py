import asyncio
from winsdk.windows.devices.enumeration import DeviceInformation
from winsdk.windows.devices.bluetooth import BluetoothDevice

async def find_jabba():
    print("Scanning for 'jabba'...")
    selector = BluetoothDevice.get_device_selector()
    # Ensure selector is a string? It should be.
    # The error 'str object cannot be interpreted as an integer' usually happens in Ctypes or similar when arguments are wrong.
    # Let's try to just list all devices without selector first, or check the docs.
    # Actually, find_all_async might be expecting something else in this python wrapper.
    # Let's try a simpler enumeration.
    devices = await DeviceInformation.find_all_async()
    
    print(f"Found {len(devices)} devices. Writing to devices.txt...")
    with open("devices.txt", "w", encoding="utf-8") as f:
        for d in devices:
            f.write(f"{d.name} | {d.id}\n")
            
    print("Done writing.")

if __name__ == "__main__":
    asyncio.run(find_jabba())
