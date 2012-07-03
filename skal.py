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


__version__ = '0.1.0'
__project_url__ = 'https://github.com/looplab/skal'


import sys
import errno
import argparse
import inspect
import types


class SkalApp(object):
    """A base class for command-subcommand apps.

    This class is meant to be used as a base class for the actual application
    class in which methods are defined that represents the subcommands.

    Consider a simple case:
    >>> class MyApp(SkalApp):
    ...     @command
    ...     def first(self):
    ...         print("first")
    ...
    >>> app = MyApp()
    >>> app.run()

    This will create a simple app which has one method that is made a command
    by uisng the @command decorator. If run from the command line it will
    respond to a call like this: "python myapp.py first"

    """
    def __init__(self):
        """Creates the argparser using metadata from decorators.

        """
        main_module = sys.modules['__main__']
        version = ''
        if hasattr(main_module, '__version__'):
            version = str(main_module.__version__)

        # Add main parser and help
        self.__argparser = argparse.ArgumentParser(description = self.__doc__)
        self.__argparser.add_argument(
                '--version',
                action = 'version',
                version = ('%(prog)s v' + version))

        # Add all global arguments from the __args__ dictionary
        if hasattr(self.__class__, '__args__'):
            _add_arguments(self.__class__.__args__, self.__argparser)

        # Add all subcommands by introspection
        self.__subparser = self.__argparser.add_subparsers(dest = 'command')
        methods = inspect.getmembers(self.__class__, inspect.ismethod)
        for name, method in methods:
            if (hasattr(method, '_args')):
                command = self.__subparser.add_parser(
                        name, help = inspect.getdoc(method))
                _add_arguments(method._args, command)
                bound_method = types.MethodType(method, self, self.__class__)
                command.set_defaults(cmd = bound_method)


    def run(self, args = None):
        """Applicatin starting point.

        This will run the associated method/function/module or print a help
        list if it's an unknown keyword or the syntax is incorrect.

        The suggested usage is as an argument to sys.exit():
        >>> sys.exit(app.run())

        Keyword arguments:
        args -- Custom application arguments (default sys.argv)

        """
        self.args = self.__argparser.parse_args(args = args)
        try:
            if 'cmd' in self.args:
                return self.args.cmd()
        except KeyboardInterrupt:
            return errno.EINTR


def command(func_or_args = None):
    """Decorator to tell Skal that the method/function is a command.

    """
    def decorator(f):
        f._args = args
        return f
    if type(func_or_args) == type(decorator):
        args = {}
        return decorator(func_or_args)
    args = func_or_args
    return decorator


def default():
    """Decorator to tell Skal that the method/function is the default.

    """
    raise NotImplementedError


def _add_arguments(args, argparser):
    for k in args:
        arg = []
        if type(k) == str:
            arg.append(k)
        elif type(k) == tuple:
            short, full = k
            if type(short) == str:
                arg.append(short)
            if type(full) == str:
                arg.append(full)
        options = args[k]
        argparser.add_argument(*arg, **options)
