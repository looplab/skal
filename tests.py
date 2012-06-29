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

debug_output = True


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
    global captured_stdout, captured_stderr
    sys.stdout = real_stdout
    sys.stderr = real_stderr
    if debug_output:
        if captured_stdout.getvalue() != "":
            print('\nStdout:\n%s' % captured_stdout.getvalue())
        if captured_stderr.getvalue() != "":
            print('\nStderr:\n%s' % captured_stderr.getvalue())
    captured_stdout = None
    captured_stderr = None


# --- Skal test class ---------------------------------------------------------


class TestApp(SkalApp):

    __skal__ = {
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


# --- Test cases --------------------------------------------------------------


# Decorator tests

def test_decorator_command():
    @command
    def test():
        pass
    assert hasattr(test, 'skal_meta'), (
            'function should have Skal metadata')


# Command tests

@with_setup(start_capture, stop_capture)
def test_command_existance():
    value = 'first'
    args = [value]
    TestApp().run(args)
    assert value in captured_stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(start_capture, stop_capture)
def test_command_help():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    doc = TestApp.first.__doc__
    assert doc in captured_stdout.getvalue(), (
            'help string should be "%s"' % doc)


@raises(SystemExit)
@with_setup(start_capture, stop_capture)
def test_command_without_decorator():
    args = ['second']
    TestApp().run(args)


@raises(SystemExit)
@with_setup(start_capture, stop_capture)
def test_invalid_command():
    args = ['third']
    TestApp().run(args)


# Global argument tests

@with_setup(start_capture, stop_capture)
def test_global_argument_existance():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    arg = 'b'
    assert arg in captured_stdout.getvalue(), (
            'help should contain variable "%s"' % arg)


@with_setup(start_capture, stop_capture)
def test_global_argument_help():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    arg = 'b'
    assert arg in captured_stdout.getvalue(), (
            'help should contain variable "%s"' % arg)


@with_setup(start_capture, stop_capture)
def test_global_argument_value_bool():
    args = ['-b', 'first']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    value = 'b'
    assert value in captured_stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(start_capture, stop_capture)
def test_global_argument_value_string():
    value = 'test'
    args = ['--string='+value, 'first']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    assert value in captured_stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(start_capture, stop_capture)
def test_global_argument_value_bool_and_string():
    value1 = 'b'
    value2 = 'test'
    args = ['-b', '--string='+value2, 'first']
    try:
        TestApp().run(args)
    except SystemExit:
        pass
    assert value1 in captured_stdout.getvalue(), (
            'output should contain "%s"' % value1)
    assert value2 in captured_stdout.getvalue(), (
            'output should contain "%s"' % value2)
