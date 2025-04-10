from zeroconf import Zeroconf, ServiceBrowser # type: ignore

class MdnsDetector:
    def __init__(self):
        self.zeroconf = Zeroconf()

    def start(self):
        print("Starting mDNS Detector...")
        ServiceBrowser(self.zeroconf, "_services._dns-sd._udp.local.", self)

    def add_service(self, zeroconf, type_, name):
        print(f"Service added: {name}", flush=True)

    def remove_service(self, zeroconf, type_, name):
        print(f"Service removed: {name}", flush=True)

    def update_service(self, zeroconf, type_, name):
        print(f"Service updated: {name}", flush=True)