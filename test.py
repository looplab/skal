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


import sys
from nose.tools import raises, with_setup

from skal import SkalApp, command


# --- Stderr output helpers ---------------------------------------------------


save_stderr = None


def disable_stderr():
    global save_stderr
    save_stderr = sys.stderr
    class Devnull(object):
        def write(self, _): pass
    sys.stderr = Devnull()


def enable_stderr():
    global save_stderr
    sys.stderr = save_stderr


# --- Skal test class ---------------------------------------------------------


class TestApp(SkalApp):
    @command
    def first(self):
        """A command"""
        print('first')

    def second(self):
        """Not a command"""
        print('second')


# --- Test cases --------------------------------------------------------------


def test_valid_command():
    args = ['first']
    TestApp().run(args)


@raises(SystemExit)
@with_setup(disable_stderr, enable_stderr)
def test_not_a_command():
    args = ['second']
    TestApp().run(args)


@raises(SystemExit)
@with_setup(disable_stderr, enable_stderr)
def test_not_a_method():
    args = ['third']
    TestApp().run(args)


def test_decorator_command():
    @command
    def test():
        pass
    assert(hasattr(test, 'skal_meta'))


# def test_valid_docstring():
#     args = ['first']
#     TestApp().run(args)

