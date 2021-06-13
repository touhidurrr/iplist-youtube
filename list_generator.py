# executing this script will generate a lot
# ... of errors. Ignore those errors.


from socket import gethostbyname as get_ip
from threading import Thread
from urllib.request import urlretrieve as download

# make a list of ips
ipList = []

# make a list of Threads
taskList = []

def fetch_ip(url):
  
  #get ip
  ip = get_ip( url )
  
  # append ip for listing
  ipList.append( ip )

# download the youtubeparsed list
download('https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed', 'youtubeparsed')

# keep previous ips
with open('ipv4_list.txt', mode = 'r', encoding = 'utf-8') as f:
  for ip in f.readlines():
    ipList.append( ip.strip() )

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
    
    # make a thread that will save the ip
    # ... and save it to taskList
    #taskList.append(Thread(target=fetch_ip, args=(url,)))
    try:
      fetch_ip(url)
    else:
      pass
    
# start the tasks
"""
threads = 16
taskNumber = len(taskList)
for i in range(0, taskNumber, threads):
  for j in range(i, min(i + threads, taskNumber)):
    taskList[j].start()
  for j in range(i, min(i + threads, taskNumber)):
    taskList[j].join()
"""
# make sure no repeating ip is available
# this line of code will remove repeatation
# ... of the same ip from the list
ipList = list( set( ipList ) )
ipList.sort()

# remove Empty strings if available
try:
  ipList.remove('')
except ValueError:
  pass

# now just print the & create a new file of
# ... fetched ip's

# this will show the ips
print(*ipList, sep='\n')

# this will create a file 'youtube_iplist.txt'
# ... with the list of the ips
with open('ipv4_list.txt', mode = 'w', encoding = 'utf-8') as f:
  
  f.write('\n'.join(ipList))
