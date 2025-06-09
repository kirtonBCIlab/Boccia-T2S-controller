import subprocess
from subprocess import CREATE_NO_WINDOW
import re

class BluetoothDevices:

    def get_paired_bluetooth_devices(self):
        # Run PowerShell command to get devices paired with this device with Bluetooth
        cmd = [
            "powershell",
            "-Command",
            "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select-Object FriendlyName, InstanceId, Description"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        output = result.stdout

        with open("debug.txt", "w") as f:
            f.write("STDOUT:\n" + output)
            f.write("STDERR:\n" + result.stderr)

        devices = []
        for line in output.splitlines():
            if "FriendlyName" in line or "InstanceId" in line or "Description" in line or not line.strip():
                continue
            # Extract fields from the output using regex
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
        
        # Return the list of paired Bluetooth devices
        return devices

    def get_local_bluetooth_adapter(self):
        # Run PowerShell command to get local Bluetooth device
        cmd = [
            "powershell",
            "-Command",
            "Get-NetAdapter | Where-Object { $_.InterfaceDescription -like '*Bluetooth*' } | Select-Object Name, MacAddress, InterfaceDescription"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        output = result.stdout

        local_adapters = []
        for line in output.splitlines():
            if "Name" in line or "MacAddress" in line or "InterfaceDescription" in line or not line.strip():
                continue
            # Extract fields from the output using regex
            match = re.match(r'^(.*?)\s+([0-9A-F:-]{17})\s+(.*)$', line.strip())
            if match:
                name = match.group(1).strip()
                mac = match.group(2).strip().replace("-", ":")
                desc = match.group(3).strip()
                # Do not include Ethernet adapters
                if "Ethernet" in name:
                    continue
                local_adapters.append((name, mac, desc))
        
        # Return the local adapter
        return local_adapters 