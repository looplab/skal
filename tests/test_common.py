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


from nose.tools import raises, with_setup
from helpers import OutputCapture
from skalclass import TestApp
from skal import command, default


__version__ = '0.1'


capture = OutputCapture(debug=False)


# --- Test cases --------------------------------------------------------------


# Decorator tests

@with_setup(capture.start, capture.stop)
def test_decorator():
    @command
    def test():
        pass
    assert hasattr(test, '__args__'), (
        'function should have metadata')


@with_setup(capture.start, capture.stop)
def test_decorator_with_string_argument():
    @command({
        '-t': {}
    })
    def test():
        pass
    assert hasattr(test, '__args__'), (
        'function should have metadata')
    assert '-t' in test.__args__, (
        'metadata should have "-t" key')
    assert test.__args__['-t'] == {}, (
        'value of metadata "-t" should be a dict')


@with_setup(capture.start, capture.stop)
def test_decorator_with_tuple_argument():
    @command({
        ('-t', '--test'): {}
    })
    def test():
        pass
    assert hasattr(test, '__args__'), (
        'function should have metadata')
    assert ('-t', '--test') in test.__args__, (
        'metadata should have ("-t", "--test") key')
    assert test.__args__[('-t', '--test')] == {}, (
        'metadata of ("-t", "--test") should be a dict')


@with_setup(capture.start, capture.stop)
@raises(NotImplementedError)
def test_decorator_default():
    @default
    def test():
        pass


# Global tests

@with_setup(capture.start, capture.stop)
@raises(KeyboardInterrupt)
def test_keyboard_interrupt():
    args = ['ctrlc']
    TestApp().run(args)
