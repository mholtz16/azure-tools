from ipaddress import ip_address,ip_network

class azureip_network:
    network=None
    mask=None
    broadcast=None
    cidr=None
    status='Unknown'

    def contains_network(self,other) -> bool:
        network=ip_network(other)
        return(self.cidr.supernet_of(network))
    
    def contains_ip(self,ip) -> bool:
        i = ip_address(ip)
        return(i in self.cidr.hosts())

    def __init__(self) -> None:
        pass

    def __init__(self,ip,status='Unknown') -> None:
        self.cidr=ip_network(ip)
        self.network = self.cidr.network_address
        self.broadcast = self.cidr.broadcast_address
        self.mask = self.cidr.netmask
        self.status=status

    

a = azureip_network('10.0.0.0/8')
print(a.cidr)
print(a.network)
print(a.mask)

print(a.contains_network('10.0.1.0/24'))
print(a.contains_ip('110.0.1.1'))