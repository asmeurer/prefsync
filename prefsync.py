#!/usr/bin/env python

"""
Tool to sync preferences

See the README for more info

"""

from __future__ import print_function

import argparse
import sys
import os
import subprocess

if sys.version_info < (3,):
    import pipes
    quote = pipes.quote
else:
    import shlex
    quote = shlex.quote

__version__ = '1.0'

reverse_DNS = 'com.asmeurer.prefsync'

def main():
    with open("README.md") as f:
        help = f.read()
    parser = argparse.ArgumentParser(description=help,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('preffile', metavar='PREFFILE', action='store',
        help="""The (binary) preference file""")
    parser.add_argument('destination', metavar='DEST', action='store',
        help="""The destination for the converted xml file""")
    parser.add_argument('-t', '--throttle-interval', help="""Throttle interval
        for the synchronization, in seconds (default: %(default)s)""",
        default=10)

    args = parser.parse_args()

    if sys.platform != 'darwin':
        print("Warning: This script has only been tested on Mac OS X")

    binary = os.path.abspath(os.path.expanduser(args.preffile))
    filename = os.path.basename(binary)
    binary = quote(binary)
    xml = quote(os.path.join(os.path.abspath(os.path.expanduser(args.destination)), filename))
    throttleinterval = quote(str(args.throttle_interval))

    # Make sure the xml file exists, since launchd won't work if it doesn't
    with open(xml, 'a'):
        pass

    with open("binarytoxml.plist") as f:
        binarytoxml = f.read()

    binarytoxml = binarytoxml.replace("{BINARY}", binary)
    binarytoxml = binarytoxml.replace("{XML}", xml)
    binarytoxml = binarytoxml.replace("{THROTTLEINTERVAL}", throttleinterval)

    with open("xmltobinary.plist") as f:
        xmltobinary = f.read()

    xmltobinary = xmltobinary.replace("{BINARY}", binary)
    xmltobinary = xmltobinary.replace("{XML}", xml)
    xmltobinary = xmltobinary.replace("{THROTTLEINTERVAL}", throttleinterval)

    prefname = os.path.basename(binary).rpartition('.plist')[0]

    binarytoxml_agent = os.path.expanduser("~/Library/LaunchAgents/" + '.'.join([reverse_DNS,
        prefname, 'binarytoxml']))
    xmltobinary_agent = os.path.expanduser("~/Library/LaunchAgents/" +
        '.'.join([reverse_DNS, prefname, 'xmltobinary']))

        # We only support OS X, so don't bother with os.path.join
    with open(binarytoxml_agent, 'w') as f:
        f.write(binarytoxml)

    with open(xmltobinary_agent, 'w') as f:
        f.write(xmltobinary)

    return (subprocess.check_call(['launchctl', 'load', binarytoxml_agent]) or
    subprocess.check_call(['launchctl', 'load', xmltobinary_agent]))

if __name__ == '__main__':
    sys.exit(main())
