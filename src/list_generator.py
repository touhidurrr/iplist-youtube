#!/bin/python3
import asyncio
from ipaddress import IPv4Address, IPv6Address, ip_address
from os import getenv
from random import choice, shuffle
from socket import has_ipv6
from urllib.request import urlretrieve as download

from dns import asyncresolver

import constants

type IP = IPv4Address | IPv6Address
type IPList = list[IP]


def isGlobalIP(ip: IP) -> bool:
  return ip.is_global


def get_ip_fetcher():
  from yaml import load
  try:
    from yaml import CLoader as Loader
  except ImportError:
    from yaml import Loader

  ares = asyncresolver.Resolver(configure=False)

  # load resolvers from dns_resolvers.yaml
  with open(constants.DNS_RESOLVER_LIST_PATH, mode='r', encoding='utf-8') as resolvers_file:
    dns_resolvers: dict[str, list[str]] = load(resolvers_file, Loader=Loader)

    filter_ipv6 = False
    if not has_ipv6:
      # if ipv6 is not supported, take only ipv4 addresses
      print('No IPv6 is support detected, disabling IPv6 resolvers...')
      filter_ipv6 = True
    elif getenv('GITHUB_ACTIONS') == 'true':
      # IPv6 does not work properly in GitHub Actions
      print('Running in GitHub Actions, disabling IPv6 resolvers...')
      filter_ipv6 = True

    dns_resolver_ips = []
    for ips in dns_resolvers.values():
      if filter_ipv6:
        ips = list(filter(lambda ip: isinstance(
          ip_address(ip), IPv4Address), ips))

      # choose a resolver from each group
      if len(ips) > 0:
        dns_resolver_ips.append(choice(ips))

    # shuffle the list to possibly get more ips
    shuffle(dns_resolver_ips)

    ares.nameservers = dns_resolver_ips

  # specify timeout and lifetime
  ares.timeout = 10
  ares.lifetime = 10

  # make ip_fetcher
  async def ip_fetcher(domain: str, query: str, ipList: IPList):
    # get ips
    try:
      ips = await ares.resolve(domain, query)
    except Exception as e:
      print(str(e))
      return

    ips = [ip_address(i) for i in ips]

    # print ips format 'example.com IN A [192.0.2.1, ...]'
    print(domain, 'IN', query, ips)

    # append the ips for listing
    ipList += list(filter(isGlobalIP, ips))

  return ip_fetcher


def read_ips(
  ipv4List: list[IPv4Address] = [],
  ipv6List: list[IPv6Address] = []
) -> tuple[list[IPv4Address], list[IPv6Address]]:
  ipv4Set: set[IPv4Address] = set(ipv4List)
  ipv6Set: set[IPv6Address] = set(ipv6List)

  with open(constants.IPv4_LIST_PATH, mode='r', encoding='utf-8') as f:
    for ip in f.readlines():
      ip = ip.strip()
      try:
        ip = ip_address(ip)
        if ip.is_global:
          ipv4Set.add(ip)
      except ValueError:
        if ip != '':
          print(f'{ip} is not a valid IPv4 address!')

  with open(constants.IPv6_LIST_PATH, mode='r', encoding='utf-8') as f:
    for ip in f.readlines():
      ip = ip.strip()
      try:
        ip = ip_address(ip)
        if ip.is_global:
          ipv6Set.add(ip)
      except ValueError:
        if ip != '':
          print(f'{ip} is not a valid IPv6 address!')

  return list(ipv4Set), list(ipv6Set)

# download youtubeparsed


def download_youtubeparsed():
  url = 'https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed'
  download(url, '.youtubeparsed')


def get_coroutines(
  ipv4List: list[IPv4Address],
  ipv6List: list[IPv6Address],
        ip_fetcher):
  # make a list of threads
  coroutines = []

  # open the youtubeparsed file
  with open('.youtubeparsed', mode='r', encoding='utf-8') as f:

    # for each url in the file
    for url in f.readlines():

      # strip whitespaces and '.'
      url = url.strip()

      # ignore empty lines
      if url == '':
        continue

      # ignore if the line starts with '#'
      if url.startswith('#'):
        continue

      # make a thread for each fetch_ip call
      coroutines.append(ip_fetcher(url, 'A', ipv4List))
      coroutines.append(ip_fetcher(url, 'AAAA', ipv6List))

  return coroutines


def write_ips(ipv4List: list[IPv4Address], ipv6List: list[IPv6Address]):
  # filter non-global ips
  ipv4List = list(filter(isGlobalIP, ipv4List))
  ipv6List = list(filter(isGlobalIP, ipv6List))

  # sort ips before writing
  ipv4List.sort()
  ipv6List.sort()

  with open(constants.IPv4_LIST_PATH, mode='w', encoding='utf-8') as f:

    f.write('\n'.join(map(str, ipv4List)) + '\n')

  with open(constants.IPv6_LIST_PATH, mode='w', encoding='utf-8') as f:

    f.write('\n'.join(map(str, ipv6List)) + '\n')


async def main():
  # make a list of ips
  ipv4List, ipv6List = read_ips()

  # count and remember the number of previous entries
  previousIpv4s = len(ipv4List)
  previousIpv6s = len(ipv6List)

  # download youtubeparsed
  download_youtubeparsed()

  # get ip fetcher
  ip_fetcher = get_ip_fetcher()

  # get coroutines
  coroutines = get_coroutines(ipv4List, ipv6List, ip_fetcher)

  # wait for coroutines to finish
  await asyncio.gather(*coroutines)

  # de-duplicate list entries
  ipv4List = list(set(ipv4List))
  ipv6List = list(set(ipv6List))

  # calculate and print changes
  print(f'Read {previousIpv4s} ipv4\'s from {constants.IPv4_LIST_PATH}')
  print('Number of new ipv4 addresses found:', len(ipv4List) - previousIpv4s)
  print(f'Read {previousIpv6s} ipv6\'s from {constants.IPv6_LIST_PATH}')
  print('Number of new ipv6 addresses found:', len(ipv6List) - previousIpv6s)

  # read ips again (resolves some errors)
  ipv4List, ipv6List = read_ips(ipv4List, ipv6List)

  # now write the ips in files
  write_ips(ipv4List, ipv6List)

if __name__ == '__main__':
  asyncio.run(main())
