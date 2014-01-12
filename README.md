prefsync
========

A little tool to help synchronize Mac OS X plist files (used for preferences
for most Mac Apps) seamlessly, in a way that can be tracked by git.

# Background

Quite a few of us on GitHub upload our
[dotfiles](http://en.wikipedia.org/wiki/Configuration_file)
([here are mine](https://github.com/asmeurer/dotfiles)). It's a nice way to
share configuration, track it with git, and with symlinking, it makes for a
nice semi-manual synchronization scheme.

This trick doesn't work so well with Mac OS X preferences. The issue is that
as of Mac OS X 10.4, [plist files](http://en.wikipedia.org/wiki/Plist) are
binary by default, making them very difficult to track with git.

A typical solution to this file is to symlink the plist files to Dropbox---and
as far as I know that works.  But you lose the ability to easily share your
settings, and perhaps most importantly, track them with git.

The good news is that it's actually possible to use binary plist files, and
automatically convert them back and forth to human-readable (and git
trackable) XML, using some tools that come with Mac OS X.

# How it works

It's actually quite simple. The heavy work is done for us by the operating
system and tools it provides. The main tools are
[plutil](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/plutil.1.html),
which allows to convert binary plist files to xml plist files and xml plist
files back to binary, and [launchd](http://en.wikipedia.org/wiki/Launchd),
which provides a facility to automatically run a script when a path changes.

# Gotchas

According to
[this page](http://managingosx.wordpress.com/2006/05/10/launchd-gotcha/) will
stop watching a path if it ceases to exist.
