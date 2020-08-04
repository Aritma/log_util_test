import argparse
import re
import sys


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


def contains_timestamp(line: str):
    if re.search('([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])', line):
        return True
    return False


def get_ipv4_part(line: str):
    found = re.search("(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}"
                      "(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])([^0-9]|$)", line)
    if found:
        # Mid-line results have an additional non-digit character included
        if found.group(0)[-1].isdigit():
            return found.group(0)
        else:
            return found.group(0)[:-1]
    return None


def get_ipv6_part(line: str):
    # standard notation only
    found = re.search('(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', line)
    if found:
        return found.group(0)
    return None


def main():
    args = argument_parse(sys.argv[1:])

    for line in get_data_content(args):
        output = line
        if args.timestamps:
            if not contains_timestamp(output):
                continue

        if args.ipv4:
            ipv4str = get_ipv4_part(output)
            if ipv4str is not None:
                output = output.replace(ipv4str, '\033[4m{}\033[0m'.format(ipv4str))
            else:
                continue

        if args.ipv6:
            ipv6str = get_ipv6_part(output)
            if ipv6str is not None:
                output = output.replace(ipv6str, '\033[4m{}\033[0m'.format(ipv6str))
            else:
                continue

        print(output, end='')


if __name__ == '__main__':
    main()
