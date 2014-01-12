#!/usr/bin/env python

"""
Tool to sync preferences

See the README for more info

"""

from __future__ import print_function

import argparse
import sys

def main():
    with open("README.md") as f:
        help = f.read()
    parser = argparse.ArgumentParser(description=help,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('preffile', metavar='PREFFILE', action='store',
        help="""The (binary) preference file""")
    parser.add_argument('destination', metavar='DEST', action='store',
        help="""The destination for the converted xml file""")
    parser.add_argument('-t', '--throttle-time', help="""Throttle time for the
    synchronization, in seconds (default: %(default)s)""", default=10)

    args = parser.parse_args()



if __name__ == '__main__':
    sys.exit(main())
