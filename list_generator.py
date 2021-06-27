# executing this script will generate a lot of errors, ignore them
# errors in threads only close the thread that got the error

from dns import resolver
from threading import Thread
from urllib.request import urlretrieve as download

res = resolver.Resolver(configure=False)

res.nameservers = [
  '1.1.1.1', '1.0.0.1', '2606:4700:4700::1111', '2606:4700:4700::1001', #Cloudflare
  '8.8.8.8', '8.8.4.4', '2001:4860:4860::8888', '2001:4860:4860::8844', #Google Public DNS
  '208.67.222.222', '208.67.220.220', '2620:0:ccc::2', '2620:0:ccd::2', #OpenDNS
  '209.244.0.3', '209.244.0.4', #Level 3
  '64.6.64.6', '64.6.65.6', '2620:74:1b::1:1', '2620:74:1c::2:2', #Verisign
  '9.9.9.9', '149.112.112.112', '2620:fe::fe', '2620:fe::9', #Quad9
  '8.26.56.26', '8.20.247.20', #Comodo Secure DNS
  '84.200.69.80', '84.200.70.40', '2001:1608:10:25::1c04:b12f', '2001:1608:10:25::9249:d69b', #DNS.WATCH
  '199.85.126.10', '199.85.127.10', #Norton ConnectSafe
  '81.218.119.11', '209.88.198.133', #GreenTeamDNS
  '195.46.39.39', '195.46.39.40', #SafeDNS
  '185.121.177.177', '169.239.202.202', '2a05:dfc7:5::53', '2a05:dfc7:5353::53', #OpenNIC
  '208.76.50.50', '208.76.51.51', #SmartViper
  '80.80.80.80', '80.80.81.81', #Freenom World
  '216.146.35.35', '216.146.36.36', #Dyn
  '37.235.1.174', '37.235.1.177', #FreeDNS
  '198.101.242.72', '23.253.163.53', #Alternate DNS
  '77.88.8.8', '77.88.8.1', '2a02:6b8::feed:0ff', '2a02:6b8:0:1::feed:0ff', #Yandex.DNS
  '91.239.100.100', '89.233.43.71', '2001:67c:28a4::', '2a01:3a0:53:53::', #UncensoredDNS
  '74.82.42.42', '2001:470:20::2', #Hurricane Electric
  '109.69.8.51', '2a00:1508:0:4::9', #puntCAT
  '156.154.70.1', '156.154.71.1', '2610:a1:1018::1', '2610:a1:1019::1', #Neustar
  '1.2.4.8', '210.2.4.8', #CNNIC SDNS
  '240c::6666', '240c::6644', #CFIEC IPv6 Public DNS
  '223.5.5.5', '223.6.6.6', #AliDNS
  '180.76.76.76', '2400:da00::6666', #Baidu Public DNS
  '119.29.29.29', '119.28.28.28', #DNSPod Public DNS+
  '114.114.114.114', '114.114.115.115', #114DNS
  '117.50.11.11', '117.50.22.22', #OneDNS
  '101.226.4.6', '218.30.118.6',  #DNSpai
  '94.140.14.14', '94.140.15.15', '2a10:50c0::ad1:ff', '2a10:50c0::ad2:ff', #AdGuard DNS Default
  '94.140.14.15', '94.140.15.16', '2a10:50c0::bad1:ff', '2a10:50c0::bad2:ff', #AdGuard DNS Family protection
  '94.140.14.140', '94.140.14.141', '2a10:50c0::1:ff', '2a10:50c0::2:ff', #AdGuard DNS Non-filtering
  '45.90.28.167', '45.90.30.167', '2a07:a8c0::82:86df', '2a07:a8c1::82:86df' #NextDNS
]

# make a list of ips
ipv4List = []
ipv6List = []

# make a list of Threads
taskList = []

def fetch_ip(URL, Query, List):
  
  # get ips
  ips = res.resolve(URL, Query)
  
  # print ips
  print(URL, '==>', *ips)
  
  # append the ips for listing
  List += [str(i) for i in ips]

# download the youtubeparsed list
download('https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed', 'youtubeparsed')

# keep previous ips
with open('ipv4_list.txt', mode = 'r', encoding = 'utf-8') as f:
  for ip in f.readlines():
    ipv4List.append( ip.strip() )

with open('ipv6_list.txt', mode = 'r', encoding = 'utf-8') as f:
  for ip in f.readlines():
    ipv6List.append( ip.strip() )

# count and remember the number of previous entries
previousIpv4s = len(ipv4List)
previousIpv6s = len(ipv6List)

# open the youtubeparsed file
with open('youtubeparsed', mode = 'r', encoding = 'utf-8') as f:
  
  # for each url in the file
  for url in f.readlines():
    
    # ignore empty lines
    if url == '':
      continue
    
    # ignore if '#' character is found
    if url[0] == '#':
      continue
    
    # strip whitespaces and '.'
    url = url.strip()
    
    # make a thread for each fetch_ip call
    taskList.append(Thread(target=fetch_ip, args=(url, 'A', ipv4List)))
    taskList.append(Thread(target=fetch_ip, args=(url, 'AAAA', ipv6List)))

"""    
# start the tasks in threads
threads = 16
taskNumber = len(taskList)
for i in range(0, taskNumber, threads):
  for j in range(i, min(i + threads, taskNumber)):
    taskList[j].start()
  for j in range(i, min(i + threads, taskNumber)):
    taskList[j].join()
"""

# start the tasks all at once
for t in taskList:
  t.start()
# and wait for them to finish
for t in taskList:
  t.join()

# make sure no duplicate ip is available, de-duplicate list entries
ipv4List = list( set( ipv4List ) )
ipv6List = list( set( ipv6List ) )
ipv4List.sort()
ipv6List.sort()

# try to remove Empty strings if available
try:
  ipv4List.remove('')
except ValueError:
  pass

try:
  ipv6List.remove('')
except ValueError:
  pass

# calculate and print number of new entries
print('Number of new ipv4 addresses found:', len(ipv4List) - previousIpv4s)
print('Number of new ipv6 addresses found:', len(ipv6List) - previousIpv6s)

# now write the ips in files
with open('ipv4_list.txt', mode = 'w', encoding = 'utf-8') as f:
  
  f.write('\n'.join(ipv4List))

with open('ipv6_list.txt', mode = 'w', encoding = 'utf-8') as f:
  
  f.write('\n'.join(ipv6List))
