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


import errno
from nose.tools import raises, with_setup

from helpers import OutputCapture

from skal import SkalApp, command


__version__ = '0.1'


capture = OutputCapture()


# --- Skal test class ---------------------------------------------------------


class TestApp(SkalApp):
    """main help string"""

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


# --- Test cases --------------------------------------------------------------


# Decorator tests

def test_decorator():
    @command
    def test():
        pass
    assert hasattr(test, '_args'), (
            'function should have metadata')


def test_decorator_with_string_argument():
    @command({
        '-t': {}
    })
    def test():
        pass
    assert hasattr(test, '_args'), (
            'function should have metadata')
    assert '-t' in test._args, (
            'metadata should have "-t" key')
    assert test._args['-t'] == {}, (
            'value of metadata "-t" should be a dict')


def test_decorator_with_tuple_argument():
    @command({
        ('-t', '--test'): {}
    })
    def test():
        pass
    assert hasattr(test, '_args'), (
            'function should have metadata')
    assert ('-t', '--test') in test._args, (
            'metadata should have ("-t", "--test") key')
    assert test._args[('-t', '--test')] == {}, (
            'metadata of ("-t", "--test") should be a dict')


# Global tests

@with_setup(capture.start, capture.stop)
def test_global_help():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    doc = TestApp.__doc__
    assert doc in capture.stdout.getvalue(), (
            'help string should be "%s"' % doc)


def test_version_output():
    pass


def test_keyboard_interrupt():
    args = ['ctrlc']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == errno.EINTR, (
                'exit code should be 2 (interrupted)')



# Command tests

@with_setup(capture.start, capture.stop)
def test_command_existance():
    value = 'first'
    args = [value]
    TestApp().run(args)
    assert value in capture.stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_help():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    doc = TestApp.first.__doc__
    assert doc in capture.stdout.getvalue(), (
            'help string should be "%s"' % doc)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_command_without_decorator():
    args = ['second']
    TestApp().run(args)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_invalid_command():
    args = ['other']
    TestApp().run(args)


# Global argument tests

@with_setup(capture.start, capture.stop)
def test_global_argument_existance():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    arg = '-b'
    assert arg in capture.stdout.getvalue(), (
            'help should list argument "%s"' % arg)


@with_setup(capture.start, capture.stop)
def test_global_argument_help():
    # TODO: fix this test
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    arg = '-b'
    doc = 'bool argument'
    assert doc in capture.stdout.getvalue(), (
            'help string for "%s" should be "%s"' % (arg, doc))


@with_setup(capture.start, capture.stop)
def test_global_argument_value_bool():
    value = 'b'
    args = ['-b', 'first']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_global_argument_value_string():
    value = 'test'
    args = ['--string='+value, 'first']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_global_argument_value_bool_and_string():
    value1 = 'b'
    value2 = 'test'
    args = ['-b', '--string='+value2, 'first']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
            'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
            'output should contain "%s"' % value2)


# Command argument tests

@with_setup(capture.start, capture.stop)
def test_argument_existance():
    args = ['third', '-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    arg = '-i'
    assert arg in capture.stdout.getvalue(), (
            'help should list argument "%s"' % arg)


@with_setup(capture.start, capture.stop)
def test_argument_help():
    args = ['third', '-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    arg = '-b'
    doc = 'bool argument'
    assert doc in capture.stdout.getvalue(), (
            'help string for "%s" should be "%s"' % (arg, doc))


@with_setup(capture.start, capture.stop)
def test_argument_value_bool():
    value = 'i'
    args = ['third', '-i']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_argument_value_string():
    value = 'test'
    args = ['third', '--test='+value]
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_argument_value_bool_and_string():
    value1 = 'i'
    value2 = 'test'
    args = ['third', '-i', '--test='+value2]
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
            'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
            'output should contain "%s"' % value2)
