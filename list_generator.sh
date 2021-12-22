#!/bin/bash

aria2c -o youtubeparsed --allow-overwrite \
  'https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed'

echo "$(grep -oP '^([\w\d.-]+\.)+([\w\d.-]+)?' youtubeparsed)" > youtubeparsed

parallel -P "$(nproc)" -j0 -a youtubeparsed '\
line="{}"
dig +short A $line | grep -v "\.$" >> ipv4_list.txt
dig +short AAAA $line | grep -v "\.$" >> ipv6_list.txt
echo "dig complete for $line ..."
'

sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n ipv4_list.txt -o ipv4_list.txt
sort ipv6_list.txt -o ipv6_list.txt # for now
