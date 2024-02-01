from ipaddress import ip_address, ip_network, IPv4Address, IPv6Address, summarize_address_range

def read_ips(ipv4List, ipv6List):
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

def makeCIDRRangesList(ipList, maskLastNBits = 8):
  maskLen = 1<<maskLastNBits
  def getFirstLastIps(ip):
    isIPv4 = type(ip) == IPv4Address
    mask = (1<<32) - (1<<maskLastNBits) if isIPv4 else (1<<64) - (1<<maskLastNBits)
    first = int(ip) & mask
    first = IPv4Address(first) if isIPv4 else IPv6Address(first)
    return first, first + (maskLen-1)
  CIDRRangesList = []
  firstip, lastip = None, None
  for ip in ipList:
    if firstip == None:
      firstip, lastip = getFirstLastIps(ip)
      continue

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
  ipv4List = []
  ipv6List = []
  read_ips(ipv4List, ipv6List)
  cidr4 = makeCIDRRangesList(ipv4List)
  # does not work for now
  # cidr6 = makeCIDRRangesList(ipv6List)
  # print(cidr4)
  with open('cidr4.txt', mode = 'w', encoding = 'utf-8') as f:

    f.write('\n'.join(map(str, cidr4)) + '\n')

if __name__ == '__main__':
  main()
