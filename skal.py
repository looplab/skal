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


# TODO: Implement tests and remove sloppy test class and main
# TODO: Detect subcommands from another module
# TODO: Detect subcommands from each module in a package
# TODO: Don't crash app if a subcommand is broken, just don't add it
# TODO: Create decorators for each subcommand to export


__version__ = "0.0.1"
__project_url__ = "https://github.com/looplab/skal"


import sys
import errno
import argparse
import inspect
import types


class SkalApp(object):
    def __init__(self):
        main_module = sys.modules['__main__']
        version = ''
        if hasattr(main_module, '__version__'):
            version = str(main_module.__version__)

        self.__argparser = argparse.ArgumentParser(description = self.__doc__)
        self.__argparser.add_argument(
                '--version',
                action = 'version',
                version = ('%(prog)s v' + version))
        self.__subparser = self.__argparser.add_subparsers(dest = 'command')

        methods = inspect.getmembers(self.__class__, inspect.ismethod)
        for name, method in methods:
            if (hasattr(method, 'skal_meta')):
                command = self.__subparser.add_parser(
                        name, help = inspect.getdoc(method))
                bound_method = types.MethodType(method, self, self.__class__)
                command.set_defaults(cmd = bound_method)

    def run(self, args = None):
        self.args = self.__argparser.parse_args(args = args)
        try:
            if 'cmd' in self.args:
                return self.args.cmd()
        except KeyboardInterrupt:
            return errno.EINTR


def command(f):
    """Decorator to tell Skal that the method/function is a command
    """
    f.skal_meta = {}
    return f

