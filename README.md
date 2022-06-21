# iplist-youtube
An attempt list of all IPs that youtube uses.

This is a list that keeps all ipv4 and ipv6 addresses used by Youtube.
We use DNS Lookups to achieve this and the lists are automatically updated approximately every 5 minutes.
The project is currently STABLE BETA.
So, not all IPs might be available.
At present, it has a collection of
**11205**
YouTube IPs.

Ipv4 list raw link => [Here!](https://raw.githubusercontent.com/touhidurrr/iplist-youtube/main/ipv4_list.txt)

Ipv6 list raw link => [Here!](https://raw.githubusercontent.com/touhidurrr/iplist-youtube/main/ipv6_list.txt)

Used open source lists:
  1. https://github.com/nickspaargaren/no-google/blob/master/categories/youtubeparsed

#### How to make the lists manually.
There are two scripts in the repository root, `list_generator.sh` and `list_generator.py`.
Running any of these scripts should generate two files with a list of **IPv4** and **IPv6** addresses with the filenames `ipv4_list.txt` and `ipv6_list.txt`.
Note that the `list_generator.py` is recommended although `list_generator.sh` should run better.
This is because the `list_generator.sh` uses an underlining tool called `dig` which is a troubleshooting tool not intended to be used for production purposes.
It has a little chance of listing some wrong **IPs** In some cases.
With a warning or error.

to use the `list_generator.sh` file run this commands in the folder cantainng the files.
```bash
chmod +x list_generator.sh
./list_generator.sh
```
If this doesn't work, run the following before using it.
It should only be necessary once.
```bash
sudo apt install sort dig grep parallel aria2c
```
For the `.py` file, you need to install `dnspython`.
Version `2.1.0` is recommended.
Recent versions might also work although not tested.
This is only necessary once.
```bash
pip3 install -I dnspython==2.1.0
```
Then run:
```bash
chmod +x list_generator.py
./list_generator.py
```
If this doesn't work, try:
```bash
python3 list_generator.py
```
#### Important Notes
Using any of these scripts once is not enough.
This is because **IPs** returned by DNS Queries are not consistent.
They are changed at fixed or unfixed intervals.
Although all **IPs** are not returned at the same time, all have the same purpose.
And different computers use different **IPs** at the same time.
And so, running the scripts, again and again, is a necessity.
If you run the scripts more **IPs** should be automatic.
Personally recommend running the scripts at least **100** times at the interval of **5** minutes or **300** seconds (Google's TTL).
For reasonable performance, run it **1000** times before using it for production.
I use such Cron jobs to populate the lists.
```cron
*/5 * * * * /path/to/the/script
```
