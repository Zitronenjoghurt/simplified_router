ROUTING_TABLE = [
    # target|gateway|netmask(CIDR)|interface #
    "120.34.23.128|192.168.23.47|25|eth1",
    "134.109.192.0|0.0.0.0|24|eth0",
    "192.168.0.0|0.0.0.0|16|eth1",
    "10.0.0.0|134.109.192.23|8|eth0",
    "default|132.109.192.254|0|eth0"
]

class Router:
    localhost = "127.0.0.1"

    def __init__(self) -> None:
        self.entries = []

        for entry in ROUTING_TABLE:
            target, gateway, netmask, interface = entry.split("|")
            self.entries.append(RoutingEntry(target, gateway, netmask, interface))

    # route a package to the given ip address #
    def transmit(self, ip: str) -> str:
        if ip == self.localhost:
            return "0.0.0.0 lo"

        for entry in self.entries:
            if entry.in_range(ip):
                return f"{entry.gateway} {entry.interface}"

        return "Can't find target."

class RoutingEntry:
    def __init__(self, target: str, gateway: str, netmask: str, interface: str) -> None:
        self.target = target
        self.gateway = gateway
        self.netmask = int(netmask)
        self.interface = interface

    # checks if a given ip address is in the address range of this entry #
    def in_range(self, ip: str) -> bool:
        if (self.target == "default"):
            return True
        return ip_to_bin(self.target)[:self.netmask] == ip_to_bin(ip)[:self.netmask]

# converts an IP address into its binary representation #
def ip_to_bin(ip: str) -> int:
    ip_parts = list(map(int, ip.split('.')))
    return ''.join([format(part, '08b') for part in ip_parts])

# validates a given IP address #
def validate_ip(ip: str) -> bool:
    try:
        ip_parts = list(map(int, ip.split('.')))
        return len(ip_parts) == 4
    except ValueError:
        return False

# part that gets executed when main.py is run #
if __name__ == "__main__":
    router = Router()
    while True:
        ip_input = input("router< ")

        # validate input ip address #
        if (validate_ip(ip_input) is False):
            print("invalid IP-address")
            continue

        # if ip address is valid => ask router for direction #
        print(f"{router.transmit(ip_input)}")
