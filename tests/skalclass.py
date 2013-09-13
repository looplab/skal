# Copyright (c) 2012-2013 - Max Persson <max@looplab.se>
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


from skal import SkalApp, command


__version__ = '0.1'


class TestApp(SkalApp):
    """main help string

    more help here
    """

    __args__ = {
        '-b': {'help': 'bool argument', 'action': 'store_true'},
        ('-s', '--string'): {'help': 'string argument with long name'}
    }

    @command
    def first(self, **args):
        """first command"""
        print('first')
        if 'b' in args:
            print('b')
        if 'string' in args:
            print(args['string'])

    def second(self, **args):
        """second command"""
        print('second')

    @command({
        '-i': {'help': 'bool argument', 'action': 'store_true'},
        ('-t', '--test'): {'help': 'string argument with long name'}
    })
    def third(self, **args):
        """third command"""
        print('third')
        if 'i' in args:
            print('i')
        if 'test' in args:
            print(args['test'])

    @command
    def ctrlc(self, **args):
        """ctrl c test"""
        raise KeyboardInterrupt

    @command
    def no_doc(self, **args):
        print('there are no docs for this function')

    @command
    def args_dict(self, **args):
        if 'b' in args:
            print('b')
        if 'string' in args:
            print(args['string'])

    @command
    def args_mixed(self, b, **args):
        if b:
            print('b')
        if 'string' in args:
            print(args['string'])

    @command
    def args_unpack(self, b, string):
        if b:
            print('b')
        if string:
            print(string)
