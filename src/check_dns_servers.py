import asyncio
from ipaddress import ip_address

from yaml import load

import constants

try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader


async def check_dns_ip(group, ip):
  try:
    _, writer = await asyncio.open_connection(host=ip, port=53)
    print(f'[Success] {ip} ({group})')
    writer.close()
    await writer.wait_closed()
  except Exception as e:
    print(f'[Failure] {ip} ({group}), Error: {e}')


async def main():
  with open(constants.DNS_RESOLVER_LIST_PATH, mode='r', encoding='utf-8') as f:
    ip_groups = load(f, Loader=Loader)

  tasks = []
  for group in ip_groups:
    for ip in ip_groups[group]:
      try:
        ip_address(ip)
      except ValueError:
        print(f'[Invalid IP] {ip} ({group})')
        continue

      tasks.append(check_dns_ip(group, ip))

  await asyncio.gather(*tasks)

if __name__ == "__main__":
  asyncio.run(main())
