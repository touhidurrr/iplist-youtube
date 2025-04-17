import constants


def main():
  with open(constants.ROUTER_OS_LIST_PATH, mode='w', encoding='utf-8') as f:
    with open(constants.CIDR4_LIST_PATH, mode='r', encoding='utf-8') as cidr4_file:
      cidr4_list = cidr4_file.read().splitlines()

      for cidr4 in cidr4_list:
        f.write(f'ip firewall address-list add list=youtube address={cidr4}\n')

    with open(constants.CIDR6_LIST_PATH, mode='r', encoding='utf-8') as cidr6_file:
      cidr6_list = cidr6_file.read().splitlines()

      for cidr6 in cidr6_list:
        f.write(
          f'ipv6 firewall address-list add list=youtube address={cidr6}\n')

    print(
      f'Wrote {len(cidr4_list) + len(cidr6_list)} RouterOS rules to {constants.ROUTER_OS_LIST_PATH}')


if __name__ == '__main__':
  main()
