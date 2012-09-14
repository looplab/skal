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


__version__ = '0.1.3'
__project_url__ = 'https://github.com/looplab/skal'


import sys
import argparse
import inspect
import types


class SkalApp(object):
    """A base class for command-subcommand apps.

    This class is meant to be used either as a base class for a complete
    application or on its own loading the application commands from modules and
    packages. See README.md for usage info.

    Keyword arguments:
    description        -- The main help text, if None the subclass docstring
    command_modules    -- List, functions from each module will be subcommands
    subcommand_modules -- List, each module will be a subcommand

    """
    def __init__(self,
                 description=None,
                 version=None,
                 command_modules=[],
                 subcommand_modules=[]):
        """Creates the argparser using metadata from decorators.

        """
        # Get the application description
        # TODO: Set the doc to none and warn if we are not a subclass and no
        # other description is given
        if self.__class__ is SkalApp:
            if description:
                description = inspect.cleandoc(description)
        else:
            description = inspect.getdoc(self)
            # Add the version flag if a version is defined
            main_module = sys.modules[self.__class__.__module__]
            if hasattr(main_module, '__version__'):
                version = str(main_module.__version__)
        if not description:
            sys.stderr.write('Warning: no documentation is defined \n')

        # Add the main parser
        self.__parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        # Add a version if there was one
        if version:
            self.__parser.add_argument(
                '--version',
                action='version',
                version=('%(prog)s v' + version))
        else:
            sys.stderr.write('Warning: no version is defined \n')

        # Add main subcommand parser
        self.__subparsers = self.__parser.add_subparsers(dest='command')

        # Add all class arguments and commands
        if hasattr(self.__class__, '__args__'):
            _add_arguments(self.__class__.__args__, self.__parser)
        methods = inspect.getmembers(self.__class__, inspect.ismethod)
        for name, method in methods:
            bound_method = types.MethodType(method, self, self.__class__)
            _add_parser(name, bound_method, self.__subparsers)

        # Add all module arguments and functions as commands
        for name in command_modules:
            try:
                module = __import__(name)
            except SyntaxError as e:
                sys.stderr.write('Warning: skipping "%s"\n' % e.filename)
                sys.stderr.write(e)
                sys.stderr.write('\n')
                break
            if hasattr(module, '__args__'):
                _add_arguments(module.__args__, self.__parser)
            functions = inspect.getmembers(module, inspect.isfunction)
            for name, function in functions:
                _add_parser(name, function, self.__subparsers)

        # Add all module arguments and functions as sub commands
        for name in subcommand_modules:
            try:
                module = __import__(name)
            except SyntaxError as e:
                sys.stderr.write('Warning: skipping "%s"\n' % e.filename)
                sys.stderr.write(e)
                sys.stderr.write('\n')
                break
            module_subparser, module_subparsers = _add_subparsers(
                name, module, self.__subparsers)
            if hasattr(module, '__args__'):
                _add_arguments(module.__args__, module_subparser)
            functions = inspect.getmembers(module, inspect.isfunction)
            for name, function in functions:
                _add_parser(name, function, module_subparsers)

    def run(self, args=None):
        """Applicatin starting point.

        This will run the associated method/function/module or print a help
        list if it's an unknown keyword or the syntax is incorrect.

        Keyword arguments:
        args -- Custom application arguments (default sys.argv)

        """
        self.args = self.__parser.parse_args(args=args)
        if 'cmd' in self.args:
            if inspect.isfunction(self.args.cmd):
                self.args.cmd(args=self.args)
            else:
                self.args.cmd()


def command(func_or_args=None):
    """Decorator to tell Skal that the method/function is a command.

    """
    def decorator(f):
        f.__args__ = args
        return f
    if type(func_or_args) == type(decorator):
        args = {}
        return decorator(func_or_args)
    args = func_or_args
    return decorator


def default(f):
    """Decorator to tell Skal that the method/function is the default.

    """
    raise NotImplementedError


def _add_parser(name, function, parent_parser):
    if hasattr(function, '__args__'):
        longhelp = inspect.getdoc(function)
        if not longhelp:
            sys.stderr.write('Warning: no documentation is defined\n')
            longhelp = ''
            shorthelp = ''
        else:
            shorthelp = longhelp.split('\n')[0]
        parser = parent_parser.add_parser(
            name,
            description=longhelp,
            help=shorthelp)
        _add_arguments(function.__args__, parser)
        parser.set_defaults(cmd=function)
        return parser


def _add_subparsers(name, module, parent_parser):
    longhelp = inspect.getdoc(module)
    if not longhelp:
        sys.stderr.write('Warning: no documentation is defined\n')
        longhelp = ''
        shorthelp = ''
    else:
        shorthelp = longhelp.split('\n')[0]
    subparser = parent_parser.add_parser(
        name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=longhelp,
        help=shorthelp)
    subparsers = subparser.add_subparsers(dest='sub_command')
    return subparser, subparsers


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
