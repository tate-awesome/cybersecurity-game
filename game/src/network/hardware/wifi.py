import os, subprocess
from ..buffer import Buffer

class Wifi:
    def __init__(self, buffer: Buffer):
        self.buffer = buffer
        self.is_connected = False
        self.previous_network = None

    def get_network_history(self):
        path = "/etc/NetworkManager/system-connections/"
        output = []
        
        # Check if the directory exists
        if not os.path.exists(path):
            print("NetworkManager directory not found. Are you using a different network manager?")
            return

        try:
            # List all configuration files in the directory
            files = os.listdir(path)
            
            if not files:
                print("No saved Wi-Fi networks found.")
                return

            for file in files:
                # NetworkManager profiles usually end with .nmconnection or have no extension
                if file.endswith(".nmconnection"):
                    output.append(f"{file.replace('.nmconnection', '')}")
                else:
                    output.append(f"{file}")

        except PermissionError:
            print("Permission denied. Please run this script with 'sudo'.")
        finally:
            return output

    def get_current_ssid(self) -> str:
        try:
            # Run nmcli to get only the active Wi-Fi connection name
            result = subprocess.run(
                ["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Loop through lines to find the active network
            for line in result.stdout.strip().split("\n"):
                if line.startswith("yes:"):
                    # Split 'yes:NetworkName' and return the network name
                    return line.split(":", 1)[1]
                    
            return "Not connected to Wi-Fi"
        except subprocess.CalledProcessError:
            return "Error: NetworkManager is not running or accessible"

    def get_available_networks(self) -> list[str]:
        try:
            # Run nmcli to list nearby Wi-Fi networks
            # The '--fields' flag extracts just the SSID (network name) and BSSID
            cmd = ['nmcli', '-f', 'SSID', 'dev', 'wifi']
            output = subprocess.check_output(cmd).decode('utf-8', errors='ignore')
            
            # Split output into lines and clean them up
            lines = [line.strip() for line in output.split('\n') if line.strip()]
            
            # Remove the header row "SSID"
            if lines:
                lines.pop(0)
                
            # Filter out empty or hidden SSIDs (often displayed as '--')
            networks = set(line for line in lines if line and line != '--')
            for network in networks:
                network = f"{network.replace("Auto ", "")}"
            
            return networks
                
        except FileNotFoundError:
            print("Error: 'nmcli' command not found. Ensure NetworkManager is installed.")
        except subprocess.CalledProcessError:
            print("Error: Failed to scan for Wi-Fi networks.")

    def connect_to_saved_wifi(self, ssid):
        try:
            # Run the nmcli command to bring up the saved connection
            result = subprocess.run(
                ["nmcli", "connection", "up", ssid],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Success: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect: {e.stderr.strip()}")
            return False

    def start(self, match_name: str):
        if self.is_running():
            self.buffer.put("wifi", "WiFi is already connected")
        else:
            if self.previous_network is None:
                self.previous_network = self.get_current_ssid()
                self.buffer.put("wifi", f"Saved current connection: {self.previous_network}")
            else:
                self.buffer.put("wifi", f"Using saved connection: {self.previous_network}")

            available = self.get_available_networks()
            self.buffer.put("wifi", "Available Networks:")
            target_available = None
            for network in available:
                self.buffer.put("wifi", f"      {network}")
                if match_name in network:
                    target_available = network
            self.buffer.put("wifi", f"Found matching available connection: {target_available}")

            history = self.get_network_history()
            self.buffer.put("wifi", "Historical Connections:")
            target_history = None
            for network in history:
                self.buffer.put("wifi", f"      {network}")
                if target_available in network:
                    target_history = network
            self.buffer.put("wifi", f"Found matching historical connection: {target_history}")

            self.buffer.put("wifi", f"Connecting to: {target_history}")
            self.connect_to_saved_wifi(target_history)
            self.is_connected = True

    def is_running(self):
        return self.is_connected

    def stop(self):
        if not self.is_running():
            self.buffer.put("wifi", f"Wifi is already disconnected.")
        else:
            if self.previous_network:
                self.buffer.put("wifi", f"Connecting to saved connection: {self.previous_network}")
                self.connect_to_saved_wifi(self.previous_network)
            self.is_connected = False