import argparse
import sys


def argument_parse(input_args):
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTION]... [FILE]',
    )

    exclusive_args = parser.add_mutually_exclusive_group()
    exclusive_args.add_argument(
        '-f', '--first',
        metavar='NUM',
        type=int,
        help='Print first NUM lines'
    )
    exclusive_args.add_argument(
        '-l', '--last',
        metavar='NUM',
        type=int,
        help='Print last NUM lines'
    )

    parser.add_argument(
        'FILE',
        type=argparse.FileType('r'),
        nargs='?',
        help='Filename to use. If missing, data is read from STDOUT'
    )
    parser.add_argument(
        '-t', '--timestamps',
        action='store_true',
        help='Print lines that contain a timestamp in HH:MM:SS format'
    )
    parser.add_argument(
        '-i', '--ipv4',
        action='store_true',
        help='Print lines that contain an IPv4 address, matching IPs are highlighted'
    )
    parser.add_argument(
        '-I', '--ipv6',
        action='store_true',
        help='Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted'
    )

    return parser.parse_args(input_args)


def print_results(lines: list):
    for line in lines:
        print(line)


def main():
    argument_parse(sys.argv[1:])
    print_results(['test'])


if __name__ == '__main__':
    main()
