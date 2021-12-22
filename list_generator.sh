#!/bin/bash

wget 'https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed'
echo "$(grep -oP '^([\w\d.-]+\.)+([\w\d.-]+)?' youtubeparsed)" > youtubeparsed

parallel -P "$(nproc)" -a youtubeparsed '\
line="{}"
if [[ ! (-z "$line" || $line =~ \#) ]]; then
  echo "digging $line ..."
  dig +noall +short $line -4 >> ipv4_list.txt
  dig +noall +short $line -6 >> ipv6_list.txt
fi
'

sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n ipv4_list.txt -o ipv4_list.txt
sort ipv6_list.txt -o ipv6_list.txt # for now
