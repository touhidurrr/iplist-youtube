#!/bin/bash

wget https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed

dig +short -4 -f youtubeparsed >> ipv4_list.txt
dig +short -6 -f youtubeparsed >> ipv6_list.txt

sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n ipv4_list.txt -o ipv4_list.txt
sort ipv6_list.txt -o ipv6_list.txt # for now
