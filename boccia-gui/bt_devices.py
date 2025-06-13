# Import libraries
import subprocess
from subprocess import CREATE_NO_WINDOW
import re
import sys

class BluetoothDevices:
    """ Class that handles Bluetooth device operations.
    Supports the BluetoothClient and BluetoothServer classes.
    Contains methods to get paired Bluetooth devices and the local Bluetooth adapters.
    """

    def get_paired_bluetooth_devices(self):
        """ Retrieves a list of devices currently paired via Bluetooth to this device.

        Paired devices are retrieved using a PowerShell command.
        The output is parsed to extract the name, MAC address, and description of each paired device.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list of tuples containing the name, MAC address, and description of each paired device.
        """
        # RUN POWERSHELL COMMAND
        # Default path to Windows PowerShell
        powershell_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        
        # PowerShell command to get devices paired via Bluetooth to this device
            # Get-PnpDevice -Class Bluetooth: Lists Bluetooth devices
            # Where-Object { $_.Status -eq 'OK' }: Filters out devices without 'OK' status (i.e. not paired/connected)
            # Select-Object FriendlyName, InstanceId, Description: Selects relevant properties only
        cmd = [
            powershell_path,
            "-Command",
            "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select-Object FriendlyName, InstanceId, Description"
        ]

        # This is needed to prevent a console window when the app is running as a .exe
        is_frozen = getattr(sys, 'frozen', False)
        creationflags = CREATE_NO_WINDOW if is_frozen else 0

        # Run the command and store the output
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=creationflags)
        output = result.stdout

        devices = [] # List to store paired devices

        # PARSE OUTPUT
        # Parses the output by iterating through each line
        for line in output.splitlines():
            # Skipping column headers and empty lines
            if ("FriendlyName" in line or "InstanceId" in line or "Description" in line or not line.strip()):
                continue

            # Skipping non-device items from the output (these are not actual devices)
            if any(x in line for x in ["Service", "Enumerator", "Adapter", "Transport", "RFCOMM"]):
                continue

            # EXTRACT DEVICE DETAILS WITH REGEX
            # The line should contain 3 columns separated by 2 or more spaces
            # The first column is the name, the second is the instance ID, and the third is the device description
            # (The instance ID is the identifer assigned to the device by Windows)
            # Sometimes the command returned lines with only two columns (no device description)
            # Try to match 3 columns first
            match = re.match(r'^(.*?)\s{2,}(\S+)\s{2,}(.*)$', line.strip())
            if not match:
                # Then try to match 2 columns if it did not have 3
                match = re.match(r'^(.*?)\s{2,}(\S+)$', line.strip())
                if match:
                    # Extract the name, instance ID, and leave description blank
                    name = match.group(1).strip()
                    instance_id = match.group(2).strip()
                    description = ""
                else:
                    # Skipping lines that don't match the format
                    continue
            else:
                # Extract the name, instance ID, and description
                name = match.group(1).strip()
                instance_id = match.group(2).strip()
                description = match.group(3).strip()

            # EXTRACT MAC ADDRESS FROM INSTANCE ID WITH REGEX
            # (MAC stands for Media Access Control. The MAC address is needed to connect to the device)
            # The PowerShell command would not directly provide the MAC address since this is for external paired devices.
            # So the MAC address is extracted from the device's instance ID.
            mac_match = re.search(r'([0-9A-F]{12})', instance_id, re.I)
            if mac_match:
                mac_raw = mac_match.group(1).upper()
                mac_address = ':'.join(mac_raw[i:i+2] for i in range(0, 12, 2))

                # Add the device's details to the list
                devices.append((name, mac_address, description))
        
        # Return the list of paired Bluetooth devices
        return devices

    def get_local_bluetooth_adapter(self):
        """ Retrieves the Bluetooth adapter on the local device.

        Adapter(s) are retrieved using a PowerShell command.
        The output is parsed to extract the name, MAC address, and description of each adapter.

        Should return a list containing only 1 item: the Bluetooth adapter of the local device.

        Parameters
        ----------
        None

        Returns
        -------
        list
            A list of tuples containing the name, MAC address, and description of each adapter.
        """
        # RUN POWERSHELL COMMAND
        # Default path to Windows PowerShell
        powershell_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        
        # PowerShell command to get local Bluetooth adapters
        cmd = [
            powershell_path,
            "-Command",
            "Get-NetAdapter | Where-Object { $_.InterfaceDescription -like '*Bluetooth*' } | Select-Object Name, MacAddress, InterfaceDescription"
        ]

        # Run the command and store the output
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        output = result.stdout

        local_adapters = [] # Stores the local adapter

        # PARSE OUTPUT
        # Parses the output by iterating through each line
        for line in output.splitlines():
            # Skipping column headers and empty lines
            if "Name" in line or "MacAddress" in line or "InterfaceDescription" in line or not line.strip():
                continue

            # EXTRACT ADAPTER DETAILS WITH REGEX
            # The line should contain 3 columns separated by 2 or more spaces
            # The first column is the adapter name, the second is the MAC address, and the third is the adapter description
            # (MAC stands for Media Access Control. The MAC address is needed to connect to the device)
            # Use regex to extract adapter details
            match = re.match(r'^(.*?)\s+([0-9A-F:-]{17})\s+(.*)$', line.strip())
            if match:
                # Extract the adapter name, MAC address, and description
                name = match.group(1).strip() 
                mac = match.group(2).strip().replace("-", ":") # Format the MAC address with colons
                desc = match.group(3).strip() 

                # Skip Ethernet adapters
                if "Ethernet" in name:
                    continue

                # Add the adapter's details to the list
                local_adapters.append((name, mac, desc))
        
        # Return the local adapter
        return local_adapters 