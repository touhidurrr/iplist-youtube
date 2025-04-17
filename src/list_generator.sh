#!/bin/bash

aria2c -o .youtubeparsed --allow-overwrite \
  'https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/youtubeparsed'

echo "$(grep -oP '^([\w\d.-]+\.)+([\w\d.-]+)?' .youtubeparsed)" > .youtubeparsed

parallel -P "$(nproc)" -j0 -a .youtubeparsed '\
line="{}"
dig +short A $line | grep -v "\.$" >> lists/ipv4.txt
dig +short AAAA $line | grep -v "\.$" >> lists/ipv6.txt
echo "dig complete for $line ..."
'

sort -u -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n lists/ipv4.txt -o lists/ipv4.txt
sort -u lists/ipv6.txt -o lists/ipv6.txt # for now
