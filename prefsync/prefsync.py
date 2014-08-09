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
    curdir = os.path.split(__file__)[0]

    with open(os.path.join(curdir, "README")) as f:
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
    xml = os.path.abspath(os.path.expanduser(args.destination))
    if os.path.isdir(xml):
        xml = os.path.join(xml, filename)
    xml = quote(xml)
    throttleinterval = quote(str(args.throttle_interval))
    prefname = os.path.basename(binary).rpartition('.plist')[0]
    binarytoxml_label = '.'.join([reverse_DNS, prefname, 'binarytoxml', 'plist'])
    xmltobinary_label = '.'.join([reverse_DNS, prefname, 'xmltobinary', 'plist'])

    # Make sure the xml file exists, since launchd won't work if it doesn't
    subprocess.check_call(['plutil', '-convert', 'xml1', binary, '-o', xml])

    with open(os.path.join(curdir, "binarytoxml.plist")) as f:
        binarytoxml = f.read()

    binarytoxml = binarytoxml.replace("{BINARY}", binary)
    binarytoxml = binarytoxml.replace("{XML}", xml)
    binarytoxml = binarytoxml.replace("{THROTTLEINTERVAL}", throttleinterval)
    binarytoxml = binarytoxml.replace("{LABEL}", binarytoxml_label)

    with open(os.path.join(curdir, "xmltobinary.plist")) as f:
        xmltobinary = f.read()

    xmltobinary = xmltobinary.replace("{BINARY}", binary)
    xmltobinary = xmltobinary.replace("{XML}", xml)
    xmltobinary = xmltobinary.replace("{THROTTLEINTERVAL}", throttleinterval)
    xmltobinary = xmltobinary.replace("{LABEL}", xmltobinary_label)
    xmltobinary = xmltobinary.replace("{PREFNAME}", prefname)

    binarytoxml_agent = os.path.expanduser("~/Library/LaunchAgents/" + binarytoxml_label)
    xmltobinary_agent = os.path.expanduser("~/Library/LaunchAgents/" + xmltobinary_label)

        # We only support OS X, so don't bother with os.path.join
    with open(binarytoxml_agent, 'w') as f:
        f.write(binarytoxml)

    with open(xmltobinary_agent, 'w') as f:
        f.write(xmltobinary)

    ret = (subprocess.check_call(['launchctl', 'load', binarytoxml_agent]) or
    subprocess.check_call(['launchctl', 'load', xmltobinary_agent]))

    print("Logout and log back in or restart for changes to take effect")

    return ret

if __name__ == '__main__':
    sys.exit(main())
