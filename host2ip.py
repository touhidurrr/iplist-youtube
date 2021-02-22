from socket import gethostbyname as get_ip
from threading import Thread

# make a list of ips
ipList = []

# make a list of Threads
taskList = []

def fetch_ip(url):
	
	#get ip
	ip = get_ip( url )
	
	# append ip for listing
	ipList.append( ip )


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
		url = url.strip().lstrip('.')
		
		# make a thread that will save the ip
		# ... and save it to taskList
		taskList.append(Thread(target=fetch_ip, args=(url,)))
		
# start the tasks
for t in taskList:
		t.start()

# wait for the tasks to end
for t in taskList:
		t.join()
		

# make sure no repeating ip is available
# this line of code will remove repeatation
# ... of the same ip from the list
ipList = list( set( ipList ) )

# now just print the & create a new file of
# ... fetched ip's

# this will show the ips
print(*ipList, sep='\n')

# this will create a file 'youtube_iplist.txt'
# ... with the list of the ips
with open('iplist.txt', mode = 'w', encoding = 'utf-8') as f:
	
	f.write('\n'.join(ipList))
