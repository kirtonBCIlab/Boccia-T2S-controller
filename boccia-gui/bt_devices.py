import subprocess
import re

class BluetoothDevices:
    def __init__(self):
        self.devices = []

    def get_paired_bluetooth_devices(self):
        # Run PowerShell command to get paired Bluetooth devices
        cmd = [
            "powershell",
            "-Command",
            "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select-Object FriendlyName, InstanceId, Description"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        print(f"Command output: {output}")

        self.devices = []
        for line in output.splitlines():
            if "FriendlyName" in line or "InstanceId" in line or "Description" in line or not line.strip():
                continue
            # Use regex to extract fields: name, instance_id, description
            match = re.match(r'^(.*?)\s+(\S+)\s+(.*)$', line.strip())
            if match:
                name = match.group(1).strip()
                instance_id = match.group(2).strip()
                description = match.group(3).strip()
                mac_match = re.search(r'([0-9A-F]{12})', instance_id, re.I)
                if mac_match:
                    mac_raw = mac_match.group(1).upper()
                    mac_address = ':'.join(mac_raw[i:i+2] for i in range(0, 12, 2))
                    self.devices.append((name, mac_address, description))
        
        if not self.devices:
            print("No paired Bluetooth devices found.")
        else:
            print("Paired Bluetooth devices:")
            for name, mac, desc in self.devices:
                print(f"Device Name: {name}, MAC Address: {mac}, Description: {desc}")
    
if __name__ == "__main__":
    discovery = BluetoothDevices()
    discovery.get_paired_bluetooth_devices()

