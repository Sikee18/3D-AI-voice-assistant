import asyncio
from winsdk.windows.devices.enumeration import DeviceInformation
from winsdk.windows.devices.bluetooth import BluetoothDevice

async def find_jabba_connected():
    print("Scanning for 'jabba' (expecting it to be connected)...")
    devices = await DeviceInformation.find_all_async()
    
    found = False
    for d in devices:
        if "jabba" in d.name.lower():
            print(f"FOUND: {d.name} | ID: {d.id}")
            found = True
            try:
                bt_device = await BluetoothDevice.from_id_async(d.id)
                print(f"  - Connection Status: {bt_device.connection_status}")
            except:
                pass
                
    if not found:
        print("Still not finding 'jabba'. Listing ALL connected/paired Bluetooth devices:")
        for d in devices:
             # Check if it looks like a bluetooth device ID (usually starts with BTHENUM or BTHLE)
             if "BTH" in d.id:
                 print(f"  - {d.name} ({d.id})")

if __name__ == "__main__":
    asyncio.run(find_jabba_connected())
