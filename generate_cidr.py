from ipaddress import ip_address, IPv4Address, IPv6Address, summarize_address_range

type IPList = list[IPv4Address | IPv6Address]

def read_ips(ipv4List: list[IPv4Address], ipv6List: list[IPv6Address]):
  with open('ipv4_list.txt', mode = 'r', encoding = 'utf-8') as f:
    for ip in f.readlines():
      ip = ip.strip()
      try:
        ip = ip_address( ip )
        ipv4List.append( ip )
      except ValueError:
        if ip != '':
          print('%s is not a valid IPv4 address!' % ip)

  with open('ipv6_list.txt', mode = 'r', encoding = 'utf-8') as f:
    for ip in f.readlines():
      ip = ip.strip()
      try:
        ip = ip_address( ip )
        ipv6List.append( ip )
      except ValueError:
        if ip != '':
          print('%s is not a valid IPv6 address!' % ip)

def makeCIDRRangesList(ipList: list[IPv4Address | IPv6Address], maskLastNBits = 8):
  maskLen = 1 << maskLastNBits

  def getFirstLastIps(ip):
    isIPv4 = type(ip) == IPv4Address
    mask = (1<<32) - maskLen if isIPv4 else (1<<128) - maskLen
    first = int(ip) & mask
    first = IPv4Address(first) if isIPv4 else IPv6Address(first)
    return first, first + (maskLen - 1)

  CIDRRangesList = []

  firstip, lastip = getFirstLastIps(ipList[0])
  for ip in ipList:
    if ip <= lastip:
      continue

    if int(ip) - int(lastip) < maskLen:
      _, lastip = getFirstLastIps(ip)
      continue

    CIDRRangesList += summarize_address_range(firstip, lastip)
    firstip, lastip = getFirstLastIps(ip)

  CIDRRangesList += summarize_address_range(firstip, lastip)
  return CIDRRangesList


def main():
  ipv4List: list[IPv4Address] = []
  ipv6List: list[IPv6Address] = []

  read_ips(ipv4List, ipv6List)

  cidr4 = makeCIDRRangesList(ipv4List)
  cidr6 = makeCIDRRangesList(ipv6List)

  with open('cidr4.txt', mode = 'w', encoding = 'utf-8') as f:

    f.write('\n'.join(map(str, cidr4)) + '\n')

  with open('cidr6.txt', mode = 'w', encoding = 'utf-8') as f:

    f.write('\n'.join(map(str, cidr6)) + '\n')

if __name__ == '__main__':
  main()
