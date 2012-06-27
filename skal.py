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
    def hello(self):
        print('hello')

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

#!/bin/env python

from skal import Skal, arguments

class MyApp(Skal):
    \"\"\"Application description
    \"\"\"

    __arguments__ = {
        '-a': {'help': 'Help for a'},
        '-b': {'help': 'Help for b'}
    }

    @arguments({
        '-d': {'help': 'Help for d', 'alt': '--delete', 'action': 'store_true'}
    })
    def hello(self):
        \"\"\"Help for hello
        \"\"\"
        if (self.args.delete):
            print('deleting')
        print('hello')

    def yes(self):
        \"\"\"Help for yes
        \"\"\"
        print('yes')

if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.run())


"""

import sys
from argparse import ArgumentParser
import inspect


class SkalApp(object):
    def __init__(self):
        self.__argparser = ArgumentParser(description = self.__doc__)
        self.__argparser.add_argument(
                '--version',
                action='version',
                version='%(prog)s 2.0')
        self.__subparser = self.__argparser.add_subparsers(
                dest = 'command',
                help = "Operation mode")

        # command = self.__subparser.add_parser('ls', help = "List jobs")
        # command.set_defaults(cmd = cmd.list_jobs)


    def run(self):
        reserved = [name for name, method in inspect.getmembers(SkalApp, inspect.ismethod)]
        for name, method in inspect.getmembers(self.__class__, inspect.ismethod):
            if name not in reserved:
                method(self)
                print name


class MyApp(SkalApp):
    def test(self):
        print('test output')

if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.run())

