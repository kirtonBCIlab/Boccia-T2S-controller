import subprocess
import re

class BluetoothDevices:

    def get_paired_bluetooth_devices(self):
        # Run PowerShell command to get paired Bluetooth devices
        cmd = [
            "powershell",
            "-Command",
            "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select-Object FriendlyName, InstanceId, Description"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        # print(f"Command output: {output}")

        devices = []
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
                    devices.append((name, mac_address, description))
        
        return devices

    def get_local_bluetooth_adapter(self):
        # Run PowerShell command to get local Bluetooth device
        cmd = [
            "powershell",
            "-Command",
            "Get-NetAdapter | Where-Object { $_.InterfaceDescription -like '*Bluetooth*' } | Select-Object Name, MacAddress, InterfaceDescription"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        # print(f"Command output: {output}")

        local_adapters = []
        for line in output.splitlines():
            if "Name" in line or "MacAddress" in line or "InterfaceDescription" in line or not line.strip():
                continue
            # Use regex to extract fields: name, mac, description
            match = re.match(r'^(.*?)\s+([0-9A-F:-]{17})\s+(.*)$', line.strip())
            if match:
                name = match.group(1).strip()
                mac = match.group(2).strip().replace("-", ":")
                desc = match.group(3).strip()
                local_adapters.append((name, mac, desc))
        return local_adapters 

    
if __name__ == "__main__":
    bluetooth_devices = BluetoothDevices()

    paired_devices = bluetooth_devices.get_paired_bluetooth_devices()
    if not paired_devices:
        print("No paired Bluetooth devices found.")
    else:
        print("Paired Bluetooth devices:")
        for name, mac, desc in paired_devices:
            print(f"Device Name: {name}, MAC Address: {mac}, Description: {desc}")

    local_bluetooth_adapter = bluetooth_devices.get_local_bluetooth_adapter()
    if not local_bluetooth_adapter:
        print("No local Bluetooth adapters found.")
    else:
        print("Local Bluetooth adapter:")
        for name, mac, desc in local_bluetooth_adapter:
            print(f"Adapter Name: {name}, MAC Address: {mac}, Description: {desc}")