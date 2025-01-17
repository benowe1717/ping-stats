#!/usr/bin/env python3
"""
Gather statistics about all IPs in your route to a destination
"""

import sys

from src.classes.parseargs import ParseArgs


def main():
    """Main program loop"""
    args = sys.argv
    parseargs = ParseArgs(args)

    if len(parseargs.ips) == 0:
        print('ERROR: No IPs found!')
        sys.exit(1)


if __name__ == '__main__':
    main()
