import constants


def main():
  with open(constants.CIDR4_LIST_PATH, mode='r', encoding='utf-8') as cidr4_file:
    cidr4_list = cidr4_file.read().splitlines()

  with open(constants.CIDR6_LIST_PATH, mode='r', encoding='utf-8') as cidr6_file:
    cidr6_list = cidr6_file.read().splitlines()

  cidr6_count = len(cidr6_list)
  cidr4_count = len(cidr4_list)
  total_count = cidr4_count + cidr6_count

  with open(constants.ROUTER_OS_V4_LIST_PATH, mode='w', encoding='utf-8') as f4:
    router_os_ipv4_rules: list[str] = [
        '/ip firewall address-list\n',
        'remove [find list=youtube]\n'
    ]

    for cidr4 in cidr4_list:
      router_os_ipv4_rules.append(f'add list=youtube address={cidr4}\n')

    f4.writelines(router_os_ipv4_rules)

    # Also write the rules to the combined file
    with open(constants.ROUTER_OS_LIST_PATH, mode='w', encoding='utf-8') as f_all:
      f_all.writelines(router_os_ipv4_rules)

  print(
    f'Wrote {cidr4_count} IPv4 RouterOS rules to {constants.ROUTER_OS_V4_LIST_PATH}'
  )

  with open(constants.ROUTER_OS_V6_LIST_PATH, mode='w', encoding='utf-8') as f6:
    router_os_ipv6_rules: list[str] = [
        '/ipv6 firewall address-list\n'
        'remove [find list=youtube]\n'
    ]

    for cidr6 in cidr6_list:
      router_os_ipv6_rules.append(f'add list=youtube address={cidr6}\n')

    f6.writelines(router_os_ipv6_rules)

    # Also append the rules to the combined file
    with open(constants.ROUTER_OS_LIST_PATH, mode='a', encoding='utf-8') as f_all:
      f_all.write('\n')
      f_all.writelines(router_os_ipv6_rules)

  print(
    f'Wrote {cidr6_count} IPv6 RouterOS rules to {constants.ROUTER_OS_V6_LIST_PATH}'
  )

  print(
    f'Wrote combined {total_count} RouterOS rules to {constants.ROUTER_OS_LIST_PATH}'
  )


if __name__ == '__main__':
  main()
