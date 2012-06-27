# Copyright 2012 Loop Lab
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
EXAMPLE APP
===========

In file myapp:

#!/bin/env python

from skal import Skal

class MyApp(SkalApp):
    @command
    def hello(self):
        print('hello')

    @command
    def yes(self):
        print('yes')

if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.run())


USAGE
=====

> myapp hello
hello

> myapp yes
yes


CUSTOM ARGUMENTS
================
Not yet implemented!

#!/bin/env python

from skal import Skal, arguments

class MyApp(Skal):
    \"\"\"Application description
    \"\"\"

    __arguments__ = {
        '-a': {'help': 'Help for a'},
        '-b': {'help': 'Help for b'}
    }

    @command
    @arguments({
        '-d': {'help': 'Help for d', 'alt': '--delete', 'action': 'store_true'}
    })
    def hello(self):
        \"\"\"Help for hello
        \"\"\"
        if (self.args.delete):
            print('deleting')
        print('hello')

    @command
    def yes(self):
        \"\"\"Help for yes
        \"\"\"
        print('yes')

if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.run())


"""

# TODO: Detect subcommands from another module
# TODO: Detect subcommands from each module in a package
# TODO: Create decorators for each subcommand to export


import sys
import errno
import argparse
import inspect
import types


class SkalApp(object):
    def __init__(self):
        self.__argparser = argparse.ArgumentParser(description = self.__doc__)
        self.__argparser.add_argument(
                '--version',
                action='version',
                version='%(prog)s 2.0')
        self.__subparser = self.__argparser.add_subparsers(dest = 'command')

        base_methods = inspect.getmembers(SkalApp, inspect.ismethod)
        reserved = [name for name, method in base_methods]
        for name, method in inspect.getmembers(self.__class__, inspect.ismethod):
            if name not in reserved:
                if (hasattr(method, 'skal_command')):
                    command = self.__subparser.add_parser(
                            name, help = inspect.getdoc(method))
                    bound_method = types.MethodType(method, self, self.__class__)
                    command.set_defaults(cmd = bound_method)

    def run(self):
        self.args = self.__argparser.parse_args()
        try:
            if 'cmd' in self.args:
                return self.args.cmd()
        except KeyboardInterrupt:
            return errno.EINTR


def command(f):
    """Decorator to tell Skal that the method/function is a command
    """
    f.skal_command = True
    return f


class MyApp(SkalApp):
    """Sloppy prototyping class, will do real tests soon
    """

    @command
    def test_a(self):
        """A valid command"""
        print('test output')

    def test_b(self):
        """Not a command"""
        print('test output')


if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.run())

