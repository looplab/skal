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
import StringIO
from nose.tools import raises, with_setup

from skal import SkalApp, command


# --- Stderr output helpers ---------------------------------------------------


real_stdout = None
real_stderr = None

captured_stdout = None
captured_stderr = None


def start_capture():
    global real_stdout, real_stderr
    global captured_stdout, captured_stderr
    real_stdout = sys.stdout
    real_stderr = sys.stderr
    captured_stdout = StringIO.StringIO()
    captured_stderr = StringIO.StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr


def stop_capture():
    sys.stdout = real_stdout
    sys.stderr = real_stderr


# --- Skal test class ---------------------------------------------------------


class TestApp(SkalApp):
    @command
    def first(self):
        """first command"""
        print('first')

    def second(self):
        """second command"""
        print('second')


# --- Test cases --------------------------------------------------------------


@with_setup(start_capture, stop_capture)
def test_valid_command():
    args = ['first']
    TestApp().run(args)
    assert 'first' in captured_stdout.getvalue(), (
            'output should be first')


@raises(SystemExit)
@with_setup(start_capture, stop_capture)
def test_not_a_command():
    args = ['second']
    TestApp().run(args)


@raises(SystemExit)
@with_setup(start_capture, stop_capture)
def test_not_a_method():
    args = ['third']
    TestApp().run(args)


def test_decorator_command():
    @command
    def test():
        pass
    assert hasattr(test, 'skal_meta'), (
            'function should have Skal metadata')


@with_setup(start_capture, stop_capture)
def test_valid_help_string():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    docstring = TestApp.first.__doc__
    assert docstring in captured_stdout.getvalue(), (
            'output should be "%s"' % docstring)
