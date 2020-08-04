import argparse
import sys
import io


def argument_parse(input_args: list):
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


def get_data_content(args: argparse.Namespace):
    if args.FILE is not None:
        data_source = args.FILE
    else:
        data_source = sys.stdin

    # Warning! This implementation is not memory effective for extreme file sizes
    content = data_source.readlines()
    if args.last is not None:
        content = content[-args.last:]
    elif args.first is not None:
        content = content[:args.first]
    return content


def main():
    args = argument_parse(sys.argv[1:])

    for line in get_data_content(args):
        print(line.strip('\n'))


if __name__ == '__main__':
    main()
