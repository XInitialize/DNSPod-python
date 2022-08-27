import argparse
from typing import Union

from dnspod.servers import DnsPodServer
import yaml
from dnspod.iptools import get_ipv4_address


def parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("function")
    parser.add_argument("-y", "--yaml", type=str, required=False)
    return parser


def main():
    parser = parse()
    args = parser.parse_args()
    print(args.__dict__)
    # init yaml
    with open(args.yaml, "r") as f:
        configs: Union[None, dict] = yaml.safe_load(f)
    if args.function.lower() == "ddns":
        dnspod_server = DnsPodServer(**configs)
        value = get_ipv4_address(configs["ethernet"])
        print(f"get ethernet: {configs['ethernet']} inet4 address: {value}")
        static_ddns = configs.get("static_ddns")
        static_ddns["value"] = value
        print(dnspod_server.static_ddns(**static_ddns))


if __name__ == '__main__':
    main()
