#!/bin/python3
from dns import resolver
from threading import Thread
from ipaddress import ip_address
from urllib.request import urlretrieve as download

def get_ip_fetcher():
  from yaml import load
  try:
    from yaml import CLoader as Loader
  except ImportError:
    from yaml import Loader

  res = resolver.Resolver(configure=False)

  # load resolvers from dns_resolvers.yaml
  resolvers_file = open('dns_resolvers.yml', mode = 'r', encoding = 'utf-8')
  res.nameservers = load(resolvers_file, Loader=Loader)
  resolvers_file.close()

  # make ip_fetcher
  def ip_fetcher(domain, query, ipList):
    # get ips
    try:
      ips = res.resolve(domain, query)
    except Exception as e:
      print(str(e))
      return

    ips = [str(i) for i in ips]

    # print ips format 'example.com IN A [192.0.2.1, ...]'
    print(domain, 'IN', query, ips)

    # append the ips for listing
    ipList += ips

  return ip_fetcher

def read_ips(ipv4List, ipv6List):
  with open('ipv4_list.txt', mode = 'r', encoding = 'utf-8') as f:
    for ip in f.readlines():
      ip = ip.strip()
      try:
        ip = str( ip_address( ip ) )
        ipv4List.append( ip )
      except ValueError:
        if ip != '':
          print('%s is not a valid IPv4 address!' % ip)

  with open('ipv6_list.txt', mode = 'r', encoding = 'utf-8') as f:
    for ip in f.readlines():
      ip = ip.strip()
      try:
        ip = str( ip_address( ip ) )
        ipv6List.append( ip )
      except ValueError:
        if ip != '':
          print('%s is not a valid IPv6 address!' % ip)

  # de-duplicate list entries
  ipv4List = list( set( ipv4List ) )
  ipv6List = list( set( ipv6List ) )

# download youtubeparsed
def download_youtubeparsed():
  url = 'https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed'
  download(url, 'youtubeparsed')

def get_threads(ipv4List, ipv6List, ip_fetcher):
  # make a list of threads
  threads = []

  # open the youtubeparsed file
  with open('youtubeparsed', mode = 'r', encoding = 'utf-8') as f:

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
      threads.append(Thread(target=ip_fetcher, args=(url, 'A', ipv4List)))
      threads.append(Thread(target=ip_fetcher, args=(url, 'AAAA', ipv6List)))

  return threads

def write_ips(ipv4List, ipv6List):
  # de-duplicate list entries
  ipv4List = list( set( ipv4List ) )
  ipv6List = list( set( ipv6List ) )

  # sort ips before writing
  ipv4List.sort(key=ip_address)
  ipv6List.sort(key=ip_address)

  with open('ipv4_list.txt', mode = 'w', encoding = 'utf-8') as f:

    f.write('\n'.join(ipv4List) + '\n')

  with open('ipv6_list.txt', mode = 'w', encoding = 'utf-8') as f:

    f.write('\n'.join(ipv6List) + '\n')

def main():
  # make a list of ips
  ipv4List = []
  ipv6List = []

  # read previous ips
  read_ips(ipv4List, ipv6List)

  # count and remember the number of previous entries
  previousIpv4s = len(ipv4List)
  previousIpv6s = len(ipv6List)

  # download youtubeparsed
  download_youtubeparsed()

  # get ip fetcher
  ip_fetcher = get_ip_fetcher()

  # get threads list
  threads = get_threads(ipv4List, ipv6List, ip_fetcher)

  # start all threads
  for t in threads:
    t.start()
  # and wait for them to finish
  for t in threads:
    t.join()

  # de-duplicate list entries
  ipv4List = list( set( ipv4List ) )
  ipv6List = list( set( ipv6List ) )

  # calculate and print changes
  print('Read', previousIpv4s, 'ipv4\'s from ipv4_list.txt')
  print('Number of new ipv4 addresses found:', len(ipv4List) - previousIpv4s)
  print('Read', previousIpv6s, 'ipv6\'s from ipv6_list.txt')
  print('Number of new ipv6 addresses found:', len(ipv6List) - previousIpv6s)

  # read ips again (resolves some errors)
  read_ips(ipv4List, ipv6List)

  # now write the ips in files
  write_ips(ipv4List, ipv6List)

if __name__ == '__main__':
  main()
