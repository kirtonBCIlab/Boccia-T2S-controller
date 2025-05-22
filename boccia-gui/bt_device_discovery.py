import subprocess
import re

class BluetoothDeviceDiscovery:
    def __init__(self):
        self.devices = []

    def get_paired_bluetooth_devices(self):
        # Run PowerShell command to get paired Bluetooth devices
        cmd = [
            "powershell",
            "-Command",
            "(Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select_Object FriendlyName, InstanceId"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Result: {result}")
        output = result.stdout

        self.devices = []
        for line in output.splitlines():
            if "FriendlyName" in line or "InstanceId" in line or not line.strip():
                continue
            # Extract device name and MAC address
            parts = line.strip().split("None", 1)
            if len(parts) == 2:
                name, instance_id = parts
                mac_match = re.search(r"([0-9A-F]{2}_){5}[0-9A-F]{2}", instance_id)
                if mac_match:
                    mac_address = mac_match.group(0).replace("_", ":")
                    self.devices.append((name, mac_address))
        
        for name, mac in self.devices:
            print(f"Device Name: {name}, MAC Address: {mac}")
    
if __name__ == "__main__":
    discovery = BluetoothDeviceDiscovery()
    discovery.get_paired_bluetooth_devices()

