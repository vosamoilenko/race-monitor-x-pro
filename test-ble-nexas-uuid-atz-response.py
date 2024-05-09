
# --- BLE ---
import pygatt
import time

# The MAC address of the Bluetooth device
DEVICE_ADDRESS = "8C:DE:52:DD:84:FE"
# List of UUIDs
uuids = [
    '00002a00-0000-1000-8000-00805f9b34fb',
'00002a01-0000-1000-8000-00805f9b34fb',
'00002a04-0000-1000-8000-00805f9b34fb',
'00002a29-0000-1000-8000-00805f9b34fb',
'00002a24-0000-1000-8000-00805f9b34fb',
'00002a25-0000-1000-8000-00805f9b34fb',
'00002a27-0000-1000-8000-00805f9b34fb',
'00002a26-0000-1000-8000-00805f9b34fb',
'00002a28-0000-1000-8000-00805f9b34fb',
'00002a23-0000-1000-8000-00805f9b34fb',
'00002a2a-0000-1000-8000-00805f9b34fb',
'49535343-6daa-4d02-abf6-19569aca69fe',
'49535343-aca3-481c-91ec-d85e28a60318',
'49535343-4c8a-39b3-2f49-511cff073b7e',
'0000fff1-0000-1000-8000-00805f9b34fb',
'0000fff2-0000-1000-8000-00805f9b34fb',
'00001800-0000-1000-8000-00805f9b34fb',
'0000180a-0000-1000-8000-00805f9b34fb',
'49535343-fe7d-4ae5-8fa9-9fafd205e455',
'0000fff0-0000-1000-8000-00805f9b34fb',
]

def main():
    adapter = pygatt.GATTToolBackend()

    try:
        adapter.start()
        device = adapter.connect(DEVICE_ADDRESS)

        for uuid in uuids:
            try:
                print(f"Writing to UUID: {uuid}")
                # Writing ATZ command
                device.char_write(uuid, b"ATZ\r", wait_for_response=True)
                
                # Reading from the same UUID (if supported)
                print(f"Reading from UUID: {uuid}")
                response = device.char_read(uuid)
                print(f"Response: {response}")

                time.sleep(1)  # Sleep between commands if necessary
            except Exception as e:
                print(f"Failed to write or read from {uuid}: {str(e)}")

    finally:
        adapter.stop()

if __name__ == "__main__":
    main()
