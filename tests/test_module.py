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
import inspect
from helpers import OutputCapture
from skal import SkalApp


capture = OutputCapture(debug=False)
module = 'skalmodule'


# --- Test cases --------------------------------------------------------------


# Global tests

@with_setup(capture.start, capture.stop)
def test_help():
    args = ['-h']
    doc = """main help string

    more help here
    """
    try:
        SkalApp(command_modules=[module], description=doc).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    doc = inspect.cleandoc(doc)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_version():
    args = ['--version']
    version = '0.5.2'
    try:
        SkalApp(command_modules=[module], version=version).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert version in capture.stderr.getvalue(), (
        'version should be "%s"' % version)


# Command tests

@with_setup(capture.start, capture.stop)
def test_command_existance():
    value = 'first'
    args = [value]
    SkalApp(command_modules=[module]).run(args)
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_help():
    args = ['first', '-h']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    import skalmodule
    doc = inspect.getdoc(skalmodule.first)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_command_without_decorator():
    args = ['second']
    SkalApp(command_modules=[module]).run(args)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_command_non_existing():
    args = ['other']
    SkalApp(command_modules=[module]).run(args)


@with_setup(capture.start, capture.stop)
def test_command_no_doc():
    args = ['no_doc']
    SkalApp(command_modules=[module]).run(args)


@with_setup(capture.start, capture.stop)
def test_command_syntax_error():
    args = ['-h']
    try:
        SkalApp(command_modules=['skalmodule_error']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'skipping' in capture.stderr.getvalue(), (
        'syntax errors should be found')


# Subcommand tests

@with_setup(capture.start, capture.stop)
def test_subcommand_existance():
    value = 'first'
    args = [module, value]
    SkalApp(subcommand_modules=[module]).run(args)
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_subcommand_help():
    args = [module, '-h']
    try:
        SkalApp(subcommand_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    import skalmodule
    doc = inspect.getdoc(skalmodule)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_subcommand_command_help():
    args = [module, '-h']
    try:
        SkalApp(subcommand_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    import skalmodule
    doc = inspect.getdoc(skalmodule)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_subcommand_without_decorator():
    args = [module, 'second']
    SkalApp(subcommand_modules=[module]).run(args)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_subcommand_non_existing():
    args = [module, 'other']
    SkalApp(subcommand_modules=[module]).run(args)


@with_setup(capture.start, capture.stop)
def test_subcommand_no_doc():
    args = [module, 'no_doc']
    SkalApp(subcommand_modules=[module]).run(args)


@with_setup(capture.start, capture.stop)
def test_subcommand_syntax_error():
    args = ['-h']
    try:
        SkalApp(subcommand_modules=['skalmodule_error']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'skipping' in capture.stderr.getvalue(), (
        'syntax errors should be found')
