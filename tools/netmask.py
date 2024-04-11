#!/usr/bin/env python
from functools import reduce


class NetworkAddress:
    def __init__(self, addr: str, cidr: int = 32) -> None:
        self.cidr = cidr
        self.max_hosts = 2 ** (32 - cidr) - 1
        self.max_real_host = self.max_hosts - 2
        self._host = self._ip_to_int([int(octet) for octet in addr.split('.')])
        self._netmask = self._cidr_to_netmask_int(cidr)
        self._network = self._host & self._netmask
        self._broadcast = self._network | (1 << 32 - self.cidr) - 1
        self._min_host = self._network + 1
        self._max_host = self._broadcast - 1

    def _string_address_from_int(self, ip: int) -> str:
        return '{}.{}.{}.{}'.format(ip >> 24, ip >> 16 & 0x00ff, ip >> 8 & 0x0000ff, ip & 0x000000ff)

    def _string_bin_address_from_int(self, ip: int) -> str:
        return '{}.{}.{}.{}'.format(
            bin(ip >> 24)[2:].zfill(8), bin(ip >> 16 & 0x00ff)[2:].zfill(8),
            bin(ip >> 8 & 0x0000ff)[2:].zfill(8), bin(ip & 0x000000ff)[2:].zfill(8)
        )

    def _ip_to_int(self, address: list[int]) -> int:
        return reduce(lambda ret, octet: ret << 8 | octet, address)

    def _cidr_to_netmask_int(self, cidr: int) -> int:
        return 0xffffffff >> (32 - cidr) << (32 - cidr)

    def _binary_address(self, addr: int) -> str:
        return '{}'.format('.'.join([bin(octet)[2:].zfill(8) for octet in addr]))

    def print(self) -> None:
        print(f'Address: {self._string_address_from_int(self._host):15} => {self._string_bin_address_from_int(self._host)}')
        print(f'Netmask: {self._string_address_from_int(self._netmask):15} => {self._string_bin_address_from_int(self._netmask)}')
        print(f'Network: {self._string_address_from_int(self._network):15} => {self._string_bin_address_from_int(self._network)}')
        print(f'Brdcast: {self._string_address_from_int(self._broadcast):15} => {self._string_bin_address_from_int(self._broadcast)}')
        print(f'Total addresses: {self.max_hosts}')
        print(f'Total hosts: {self.max_real_host}')
        print(f'Min host: {self._string_address_from_int(self._min_host):15}')
        print(f'Max host: {self._string_address_from_int(self._max_host):15}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Need subnet in format xxx.xxx.xxx.xxx/yy\n')
        sys.exit(1)

    ip, mask = sys.argv[1].split('/')
    net_address = NetworkAddress(ip, int(mask))
    net_address.print()
