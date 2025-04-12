import socket
import struct
import select
import threading

# mDNS multicast address and port
MDNS_ADDRESS = "224.0.0.251"
MDNS_PORT = 5353
BUFFER_SIZE = 1024  # Buffer size for incoming packets

def create_mdns_socket(interface_ip):
    """
    Create a socket bound to the specific network interface for mDNS traffic.
    """
    try:
        mdns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        mdns_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mdns_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        mdns_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        # Bind to the interface's local IP and mDNS port
        mdns_socket.bind((interface_ip, MDNS_PORT))
        print(f"Socket bound successfully to {interface_ip} on port {MDNS_PORT}.", flush=True)

        # Join multicast group on the specified interface
        multicast_request = struct.pack("4s4s", socket.inet_aton(MDNS_ADDRESS), socket.inet_aton(interface_ip))
        mdns_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request)

        return mdns_socket
    except Exception as e:
        print(f"Failed to create mDNS socket on {interface_ip}: {e}", flush=True)
        return None



stop_event = threading.Event()  # Event to signal loop termination

def forward_mdns_traffic_all(sockets):
    """
    Monitor all sockets and forward mDNS traffic between them using a single thread.
    """
    while not stop_event.is_set():  # Run until stop_event is set
        try:
            readable, _, _ = select.select(sockets, [], [], 5)  # Wait up to 5 seconds
            for source_socket in readable:
                data, sender_address = source_socket.recvfrom(BUFFER_SIZE)
                for target_socket in sockets:
                    if target_socket != source_socket:  # Avoid sending back to the source
                        target_socket.sendto(data, (MDNS_ADDRESS, MDNS_PORT))
        except Exception as e:
            print(f"Error in forwarding mDNS traffic: {e}")
