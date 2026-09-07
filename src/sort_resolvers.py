import yaml
import ipaddress


def main():

  # Unsure how it works
  # The purpose if to add 2 spaces before '-'
  class IndentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
      return super().increase_indent(flow, False)

  def ip_sort_key(ip_str):
    ip = ipaddress.ip_address(ip_str)
    return (ip.version, ip)

  with open("dns_resolvers.yml", "r") as file:
    resolvers = yaml.safe_load(file)

  for key in resolvers:
    resolvers[key] = sorted(resolvers[key], key=ip_sort_key)

  yml = yaml.dump(
      resolvers,
      sort_keys=True,
      Dumper=IndentDumper,
  )

  with open("dns_resolvers.yml", "w") as file:
    file.write(yml)


if __name__ == "__main__":
  main()
