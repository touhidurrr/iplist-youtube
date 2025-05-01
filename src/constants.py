from pathlib import Path

LISTS_DIR = Path('lists')
LISTS_DIR.mkdir(exist_ok=True)

IPv4_LIST_PATH = LISTS_DIR / 'ipv4.txt'
IPv6_LIST_PATH = LISTS_DIR / 'ipv6.txt'
CIDR4_LIST_PATH = LISTS_DIR / 'cidr4.txt'
CIDR6_LIST_PATH = LISTS_DIR / 'cidr6.txt'
ROUTER_OS_LIST_PATH = LISTS_DIR / 'routeros.rsc'

DNS_RESOLVER_LIST_PATH = Path('dns_resolvers.yml')
