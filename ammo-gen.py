import sys
import argparse
from os import path
from string import ascii_lowercase
from urllib.parse import quote_plus
from random import choice, getrandbits
from ipaddress import IPv4Address, IPv6Address

def get_list_from_file(fname):
    if not path.exists(fname):
        sys.exit("No user-agent file: {}".format(fname))
    return open(fname, encoding="utf8",
        errors="ignore").read().splitlines()

def get_random_ip():
    bits = getrandbits(32)
    return str(IPv4Address(bits))

def get_random_string(length):
   letters = ascii_lowercase
   return ''.join(choice(letters) for i in range(length))

def parse_cli_arguments():
    parser = argparse.ArgumentParser(description='Ammo.txt generator for Yandex-Tank')
    parser.add_argument('-c', '--count',
            dest='count',
            type=int,
            default=100,
            help='Ammo count (default: 100)')
    parser.add_argument('-f','--file',
            dest='file',
            default="ammo.txt",
            help='Output file (default: ammo.txt)')
    parser.add_argument('-H','--hosts',
            dest='host',
            default="127.0.0.1",
            help='Hostnames used in Host header (default: 127.0.0.1, comma-separated)')
    parser.add_argument('--header-connection',
            dest='hdr_connection',
            default="keep-alive",
            choices=["close","keep-alive"],
            help='Connection header: close, keep-alive (default)')
    parser.add_argument('-u', '--user-agent',
            dest='user_agent',
            default=None,
            help='File with list of user_agents')
    parser.add_argument('-a', '--attacks',
            dest='attacks',
            default=None,
            help='File with list of attack samples')
    parser.add_argument('-p', '--params',
            dest='params',
            default=None,
            help='File with list of parameter names')
    parser.add_argument('-A', '--attack-percent',
            dest='attack_percent',
            type=int,
            default=100,
            help='Percent of attacks (default: 100)')
    parser.add_argument('-i', '--ip',
            dest='ip_header',
            default=None,
            help='Specify header where to send IP-address from client')
    parser.add_argument('-P', '--random-params',
            dest='random_params',
            action="store_true",
            help='Enable random parameters for attacks')
    parser.add_argument('-U', '--random-path',
            dest='random_path',
            action="store_true",
            help='Enable random path for requests')
    args=parser.parse_args()
    args.host=args.host.split(",")
    return args


def main():
    args=parse_cli_arguments()
    if args.attack_percent > 100 or args.attack_percent < 0:
        sys.exit("Invalid attack percentage value: should be between 0 and 100")
    params=["test"]
    attacks=[]
    user_agents=["Yandex-Tank"]
    if args.user_agent:
        user_agents=get_list_from_file(args.user_agent)
    if args.attacks:
        attacks=get_list_from_file(args.attacks)
    if args.params:
        attacks=get_list_from_file(args.params)
    sample="""GET {} HTTP/1.1
Host: {}
User-Agent: {}{}
Connection: {}
"""
    attack_count=0
    with open(args.file,"w") as f:
        for i in range(0,args.count):
            query="/"
            if args.random_path:
                query="{}{}/".format(query,get_random_string(10))
            if args.attacks and i % int(100 / args.attack_percent) == 0:
                attack_count+=1
                query="{}?{}={}".format(
                    query,
                    get_random_string(5) if args.random_params else choice(params),
                    quote_plus(choice(attacks)))
            attack=sample.format(
                query,
                choice(args.host),
                choice(user_agents),
                "\n{}: {}".format(args.ip_header,get_random_ip()) if args.ip_header else "",
                args.hdr_connection)
            f.write("{}\n{}\n".format(len(attack)+1, attack))
    print("Done! {} requests ({} attacks) written in {}".format(
        args.count, attack_count, args.file))

if __name__ == '__main__':
    main()
