import constants


def main():
  with open(constants.CIDR4_LIST_PATH, mode='r', encoding='utf-8') as cidr4_file:
    cidr4_list = cidr4_file.read().splitlines()

  with open(constants.CIDR6_LIST_PATH, mode='r', encoding='utf-8') as cidr6_file:
    cidr6_list = cidr6_file.read().splitlines()

  total_count = len(cidr4_list) + len(cidr6_list)

  with open(constants.ROUTER_OS_LIST_PATH, mode='w', encoding='utf-8') as f:
    f.write('/ip firewall address-list\n')
    f.write('remove [find list=youtube]\n')
    for cidr4 in cidr4_list:
      f.write(f'add list=youtube address={cidr4}\n')

    f.write('\n/ipv6 firewall address-list\n')
    f.write('remove [find list=youtube]\n')
    for cidr6 in cidr6_list:
      f.write(f'add list=youtube address={cidr6}\n')

  print(f'Wrote combined {total_count} RouterOS rules to {constants.ROUTER_OS_LIST_PATH}')

  with open(constants.ROUTER_OS_V4_LIST_PATH, mode='w', encoding='utf-8') as f4:
    f4.write('/ip firewall address-list\n')
    f4.write('remove [find list=youtube]\n')
    for cidr4 in cidr4_list:
      f4.write(f'add list=youtube address={cidr4}\n')

  print(f'Wrote {len(cidr4_list)} IPv4 RouterOS rules to {constants.ROUTER_OS_V4_LIST_PATH}')

  with open(constants.ROUTER_OS_V6_LIST_PATH, mode='w', encoding='utf-8') as f6:
    f6.write('/ipv6 firewall address-list\n')
    f6.write('remove [find list=youtube]\n')
    for cidr6 in cidr6_list:
      f6.write(f'add list=youtube address={cidr6}\n')

  print(f'Wrote {len(cidr6_list)} IPv6 RouterOS rules to {constants.ROUTER_OS_V6_LIST_PATH}')


if __name__ == '__main__':
  main()
