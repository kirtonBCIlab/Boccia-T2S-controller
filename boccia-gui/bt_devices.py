import subprocess
from subprocess import CREATE_NO_WINDOW
import re
import sys

class BluetoothDevices:

    def get_paired_bluetooth_devices(self):
        # Run PowerShell command to get devices paired with this device with Bluetooth
        powershell_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        cmd = [
            powershell_path,
            "-Command",
            "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select-Object FriendlyName, InstanceId, Description"
        ]
        is_frozen = getattr(sys, 'frozen', False)
        creationflags = CREATE_NO_WINDOW if is_frozen else 0
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=creationflags)
        output = result.stdout

        devices = []
        debug_lines = []
        for line in output.splitlines():
            if (
                "FriendlyName" in line or
                "InstanceId" in line or
                "Description" in line or
                not line.strip()
            ):
                continue

            # Filter out unnecessary items
            if any(x in line for x in ["Service", "Enumerator", "Adapter", "Transport", "RFCOMM"]):
                continue

            # Try to match three columns first, then two columns
            match = re.match(r'^(.*?)\s{2,}(\S+)\s{2,}(.*)$', line.strip())
            if not match:
                match = re.match(r'^(.*?)\s{2,}(\S+)$', line.strip())
                if match:
                    name = match.group(1).strip()
                    instance_id = match.group(2).strip()
                    description = ""
                else:
                    debug_lines.append(f"NO MATCH: {line.strip()}")
                    continue
            else:
                name = match.group(1).strip()
                instance_id = match.group(2).strip()
                description = match.group(3).strip()

            mac_match = re.search(r'([0-9A-F]{12})', instance_id, re.I)
            if mac_match:
                mac_raw = mac_match.group(1).upper()
                mac_address = ':'.join(mac_raw[i:i+2] for i in range(0, 12, 2))
                devices.append((name, mac_address, description))
                debug_lines.append(f"ADDED: {name} | {mac_address} | {description}")
            else:
                debug_lines.append(f"SKIPPED (no MAC): {name} | {instance_id} | {description}")
        
        with open("debug_log.txt", "w") as f:
            f.write("\n".join(debug_lines))

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