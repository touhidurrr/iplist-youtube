#!/bin/bash

YOUTUBE_PARSED='https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed'
YOUTUBE_HOSTNAMES=$(curl -G $YOUTUBE_PARSED)

echo $YOUTUBE_HOSTNAMES | dig +short -4 >> ipv4_list.txt
echo $YOUTUBE_HOSTNAMES | dig +short -6 >> ipv6_list.txt

sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n ipv4_list.txt -o ipv4_list.txt
sort ipv6_list.txt -o ipv6_list.txt # for now
