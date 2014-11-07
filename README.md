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

# Usage

    usage: prefsync [-h] [-t THROTTLE_INTERVAL] PREFFILE DEST

For example

    prefsync ~/Library/Preferences/preferencefile.plist preferencefile.xml

The `-t` flag sets the throttle interval for syncing the file, in seconds. The
default is 10 seconds.

# Installing

You can install it with conda using

    conda install -c asmeurer prefsync

Or using pip

    pip install prefsync

Or from the git source

    python setup.py install

Or you can just run it from the checkout, with

    python -m prefsync

Once you install it, use the command `prefsync`.

# How it works

It's actually quite simple. The heavy work is done for us by the operating
system and tools it provides. The main tools are
[plutil](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/plutil.1.html),
which allows to convert binary plist files to xml plist files and xml plist
files back to binary, and [launchd](http://en.wikipedia.org/wiki/Launchd),
which provides a facility to automatically run a script when a file changes.

There are some catches, though.

First, if you just do this, it will run cyclically forever, because as soon as
the binary file is updated, it will write to the xml version, which will
register as a change, causing it to write the binary plist, and so on.

We get around this by writing a special extended attribute to each file when
it is written, and ignoring files if they have that attribute (so that only
changes by other things will register).  This will break if something somehow
preserves these attributes. In my tests, they don't, but you can easily test
if your program does by running

    xattr -w test:Test test ~/Library/Preferences/preferencefile.plist

then, make a change to the preferences, and see if the atttribute is still there

    xattr ~/Library/Preferences/preferencefile.plist

Second, in Mac OS X 10.9, preferences are cached, meaning that even if a
program is closed and the plist file is written to, it will be overridden with
the original preferences when it is opened again if the cache was not
flushed.

Getting around this is easy: we just call

    defaults read com.reversedns.preference

(where `com.reversedns.preference` is the reverse DNS for the preference file
in question). This flushes the cache.

Finally, it generally doesn't work to update the binary preference file while
a program is running.  You may be able to just close and reopen the program,
but it may write to the preferences when you do that, overwriting the
changes.

Therefore, it is *highly* recommended to track the XML changes in git, so that
if they are overwritten they can be easily recovered.  To force the changes to
be written to the binary, the easiest way is to close the program, make sure
the xml changes are the same (i.e., closing the program didn't cause the
preferences to be written and synced over to the xml), and then touch the xml
file.

Note that the synchronization in each direction may take up to 10 seconds by
default to take place. You can change this by setting the `-t` flag when
running `prefsync`.

# Gotchas

According to
[this page](http://managingosx.wordpress.com/2006/05/10/launchd-gotcha/)
launchd will stop watching a path if it ceases to exist.  You can reset the
process by logging out and logging back in, or by restarting.  You can also
try using `launchctl`, though this may not work reliably.

# TODO

There is currently no easy way to remove a sync. The best way is to open
Lingon and delete the syncs for the preferences you no longer want to sync. Be
sure to delete both `binarytoxml` and `xmltobinary`. You will need to log out
and log back in or restart for changes to take effect.

# Acknowledgments

The Lingon program is invaluable when working with launchd (the older, free
version works just fine).

StackOverflow and Mac OS X Hints helped me debug some of the strangeness
when trying to get this to work.

# License

MIT (see the LICENSE file).
