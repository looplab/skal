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
    def first(self):
        """first command"""
        print('first')
        if self.args.b:
            print('b')
        if self.args.string:
            print(self.args.string)

    def second(self):
        """second command"""
        print('second')

    @command({
        '-i': {'help': 'bool argument', 'action': 'store_true'},
        ('-t', '--test'): {'help': 'string argument with long name'}
    })
    def third(self):
        """third command"""
        print('third')
        if self.args.i:
            print('i')
        if self.args.test:
            print(self.args.test)

    @command
    def ctrlc(self):
        """ctrl c test"""
        raise KeyboardInterrupt
