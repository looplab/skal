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


from nose.tools import with_setup
import inspect
from helpers import OutputCapture
import skalclass
from skalclass import TestApp


capture = OutputCapture(debug=False)


# --- Test cases --------------------------------------------------------------


# Global tests

@with_setup(capture.start, capture.stop)
def test_description():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    doc = inspect.getdoc(TestApp)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_version():
    args = ['--version']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    version = str(skalclass.__version__)
    assert version in capture.stderr.getvalue(), (
        'version should be "%s"' % version)


@with_setup(capture.start, capture.stop)
def test_override_description():
    args = ['-h']
    doc = 'new description'
    try:
        TestApp(description=doc).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_override_version():
    args = ['--version']
    version = '0.0.9'
    try:
        TestApp(version=version).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert version in capture.stderr.getvalue(), (
        'version should be "%s"' % version)


# Argument tests

@with_setup(capture.start, capture.stop)
def test_argument_existing():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    arg = '-b'
    assert arg in capture.stdout.getvalue(), (
        'help should list argument "%s"' % arg)


@with_setup(capture.start, capture.stop)
def test_argument_doc():
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
def test_argument_value_bool():
    value = 'b'
    args = ['-b', 'first']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_argument_value_string():
    value = 'test'
    args = ['--string=' + value, 'first']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_argument_value_bool_and_string():
    value1 = 'b'
    value2 = 'test'
    args = ['-b', '--string=' + value2, 'first']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value2)


@with_setup(capture.start, capture.stop)
def test_argument_passing_dict():
    value1 = 'b'
    value2 = 'test'
    args = ['-b', '--string=' + value2, 'args_dict']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value2)


@with_setup(capture.start, capture.stop)
def test_argument_passing_mixed():
    value1 = 'b'
    value2 = 'test'
    args = ['-b', '--string=' + value2, 'args_mixed']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value2)


@with_setup(capture.start, capture.stop)
def test_argument_passing_unpack():
    value1 = 'b'
    value2 = 'test'
    args = ['-b', '--string=' + value2, 'args_unpack']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value2)


# Command tests

@with_setup(capture.start, capture.stop)
def test_command_existing():
    value = 'first'
    args = [value]
    TestApp().run(args)
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_non_existing():
    args = ['other']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code != 0, 'exit code should not be 0'


@with_setup(capture.start, capture.stop)
def test_command_doc():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    doc = inspect.getdoc(TestApp.first)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_command_no_doc():
    args = ['-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'no_doc' in capture.stderr.getvalue(), (
        'there should be a warning about missing documentation')


@with_setup(capture.start, capture.stop)
def test_command_without_decorator():
    args = ['second']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code != 0, 'exit code should not be 0'


# Command argument tests

@with_setup(capture.start, capture.stop)
def test_command_argument_existing():
    args = ['third', '-h']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    arg = '-i'
    assert arg in capture.stdout.getvalue(), (
        'help should list argument "%s"' % arg)


@with_setup(capture.start, capture.stop)
def test_command_argument_doc():
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
def test_command_argument_value_bool():
    value = 'i'
    args = ['third', '-i']
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_argument_value_string():
    value = 'test'
    args = ['third', '--test=' + value]
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_argument_value_bool_and_string():
    value1 = 'i'
    value2 = 'test'
    args = ['third', '-i', '--test=' + value2]
    try:
        TestApp().run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value1 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value1)
    assert value2 in capture.stdout.getvalue(), (
        'output should contain "%s"' % value2)
