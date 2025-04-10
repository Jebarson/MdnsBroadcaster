import threading
import time

from MdnsDetector import MdnsDetector
from MdnsForwarder import create_mdns_socket, forward_mdns_traffic_all

def main():
    # Start the repeater to list all the services discovered in the network
    repeater = MdnsDetector()
    repeater.start()
    time.sleep(5)

    # List of network interface IPs to bind to
    with open('iplist.txt','r') as file:
        interfaces = file.readlines() #Ips are read from the file. One ip per line.

    # Create mDNS sockets for each interface
    sockets = []
    for interface_ip in interfaces:
        try:
            interface_ip = interface_ip.strip()
            mdns_socket = create_mdns_socket(interface_ip)
            sockets.append(mdns_socket)
        except Exception as e:
            print(f"Failed to create mDNS socket on {interface_ip}: {e}")

    # Use a single thread to monitor all sockets
    threading.Thread(target=forward_mdns_traffic_all, args=(sockets,), daemon=True).start()

    print("mDNS repeater is running. Press Ctrl+C to stop.", flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down mDNS repeater...", flush=True)
        for sock in sockets:
            sock.close()


if __name__ == "__main__":
    main()
