#!/usr/bin/env python3
import time
import random
import sys
import argparse
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeReq, RadioTap

class WiFiProber:
    def __init__(self, interface, target_ssid="i love a3spaaaa", interval=1.0):
        self.interface = interface
        self.target_ssid = target_ssid
        self.interval = interval
        self.src_mac = self.get_random_mac()
        
    def get_random_mac(self):
        """Generate a random MAC address for anonymity"""
        return "02:00:00:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    
    def create_probe_request(self, ssid=""):
        """
        Create a 802.11 probe request packet
        If ssid is empty, creates a broadcast probe request
        """
        # RadioTap header (for monitor mode)
        radiotap = RadioTap()
        
        # 802.11 header
        dot11 = Dot11(
            type=0,        # Management frame
            subtype=4,     # Probe request
            addr1="ff:ff:ff:ff:ff:ff",  # Destination (broadcast)
            addr2=self.src_mac,         # Source
            addr3="ff:ff:ff:ff:ff:ff"   # BSSID (broadcast)
        )
        
        # Probe request layer
        probe_req = Dot11ProbeReq()
        
        # Information Elements
        essid_ie = Dot11Elt(ID="SSID", info=ssid.encode(), len=len(ssid))
        
        # Supported rates (common rates)
        rates = b'\x82\x84\x8b\x96\x0c\x12\x18\x24'
        rates_ie = Dot11Elt(ID="Rates", info=rates, len=len(rates))
        
        # Extended supported rates
        ext_rates = b'\x30\x48\x60\x6c'
        ext_rates_ie = Dot11Elt(ID="ESRates", info=ext_rates, len=len(ext_rates))
        
        # Combine all layers
        packet = radiotap / dot11 / probe_req / essid_ie / rates_ie / ext_rates_ie
        
        return packet
    
    def send_probe_request(self, targeted=True):
        """
        Send probe request
        targeted: True for specific SSID, False for broadcast
        """
        try:
            if targeted:
                packet = self.create_probe_request(self.target_ssid)
                print(f"[{time.strftime('%H:%M:%S')}] Sending targeted probe for: '{self.target_ssid}'")
            else:
                packet = self.create_probe_request("")
                print(f"[{time.strftime('%H:%M:%S')}] Sending broadcast probe request")
            
            # Send packet
            sendp(packet, iface=self.interface, verbose=0)
            
            # Randomize MAC occasionally for better anonymity
            if random.randint(1, 10) == 1:
                self.src_mac = self.get_random_mac()
                
        except Exception as e:
            print(f"Error sending probe request: {e}")
    
    def start_probing(self, mix_broadcast=True):
        """
        Start continuous probing
        mix_broadcast: Also send broadcast probes occasionally
        """
        print(f"Starting WiFi probing on interface: {self.interface}")
        print(f"Target SSID: '{self.target_ssid}'")
        print(f"Probe interval: {self.interval} seconds")
        print(f"Source MAC: {self.src_mac}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Send targeted probe
                self.send_probe_request(targeted=True)
                
                # Occasionally send broadcast probe (helps with discovery)
                if mix_broadcast and random.randint(1, 5) == 1:
                    time.sleep(0.1)
                    self.send_probe_request(targeted=False)
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\nStopping probe requests...")
        except Exception as e:
            print(f"Error during probing: {e}")

def list_interfaces():
    """List available network interfaces"""
    try:
        interfaces = get_if_list()
        print("Available network interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  {i}: {iface}")
        return interfaces
    except Exception as e:
        print(f"Error listing interfaces: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="WiFi Probe Request Generator")
    parser.add_argument("-i", "--interface", required=True, 
                       help="WiFi interface in monitor mode (e.g., wlan0mon)")
    parser.add_argument("-s", "--ssid", default="i love a3spaaaa",
                       help="Target SSID to probe for")
    parser.add_argument("-t", "--interval", type=float, default=1.0,
                       help="Interval between probes in seconds")
    parser.add_argument("--list-interfaces", action="store_true",
                       help="List available network interfaces")
    
    args = parser.parse_args()
    
    if args.list_interfaces:
        list_interfaces()
        return
    
    # Check if running as root (required for packet injection)
    if os.geteuid() != 0:
        print("Error: This script requires root privileges for packet injection")
        print("Please run with sudo")
        sys.exit(1)
    
    # Validate interface
    available_interfaces = get_if_list()
    if args.interface not in available_interfaces:
        print(f"Error: Interface '{args.interface}' not found")
        print("Available interfaces:")
        for iface in available_interfaces:
            print(f"  - {iface}")
        sys.exit(1)
    
    # Create and start prober
    prober = WiFiProber(
        interface=args.interface,
        target_ssid=args.ssid,
        interval=args.interval
    )
    
    prober.start_probing()

if __name__ == "__main__":
    main()
