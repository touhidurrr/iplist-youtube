from ipaddress import (IPv4Address, IPv6Address, ip_address,
                       summarize_address_range)

from list_generator import IPList, read_ips


def makeCIDRRangesList(ipList: IPList, maskLastNBits=8):
  maskLen = 1 << maskLastNBits

  def getFirstLastIps(ip):
    isIPv4 = type(ip) == IPv4Address
    mask = (1 << 32) - maskLen if isIPv4 else (1 << 128) - maskLen
    first = int(ip) & mask
    first = IPv4Address(first) if isIPv4 else IPv6Address(first)
    return first, first + (maskLen - 1)

  CIDRRangesList = []

  firstIP, lastIP = getFirstLastIps(ipList[0])
  for ip in ipList:
    if ip <= lastIP:
      continue

    if int(ip) - int(lastIP) < maskLen:
      _, lastIP = getFirstLastIps(ip)
      continue

    CIDRRangesList += summarize_address_range(firstIP, lastIP)
    firstIP, lastIP = getFirstLastIps(ip)

  CIDRRangesList += summarize_address_range(firstIP, lastIP)
  return CIDRRangesList


def main():
  ipv4List, ipv6List = read_ips()
  ipv4List.sort()
  ipv6List.sort()

  cidr4 = makeCIDRRangesList(ipv4List)
  # for IPv6, a 64 bit mask is not extensive
  cidr6 = makeCIDRRangesList(ipv6List, 64)

  with open('cidr4.txt', mode='w', encoding='utf-8') as f:

    f.write('\n'.join(map(str, cidr4)) + '\n')

  with open('cidr6.txt', mode='w', encoding='utf-8') as f:

    f.write('\n'.join(map(str, cidr6)) + '\n')


if __name__ == '__main__':
  main()
