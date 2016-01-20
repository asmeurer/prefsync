#!/usr/bin/env python

from distutils.core import setup

setup(
    name='prefsync',
    version='1.2',
    description='''A little tool to help synchronize Mac OS X plist files
    (used for preferences for most Mac Apps) seamlessly, in a way that can
    be tracked by git.''',
    author='Aaron Meurer',
    author_email='asmeurer@gmail.com',
    url='https://github.com/asmeurer/prefsync',
    packages=['prefsync'],
    package_data={'prefsync': ['binarytoxml.plist', 'xmltobinary.plist', 'README']},
    scripts=['bin/prefsync'],
    long_description=open("README.md").read(),
    license="BSD",
    classifiers=[
        'Environment :: MacOS X',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],
)
