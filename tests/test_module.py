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


from nose.tools import with_setup
import inspect
from helpers import OutputCapture
from skal import SkalApp


capture = OutputCapture(debug=False)
module = 'skalmodule'


# --- Test cases --------------------------------------------------------------


# Global tests

@with_setup(capture.start, capture.stop)
def test_description():
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
def test_no_description():
    args = ['-h']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'no main documentation' in capture.stderr.getvalue(), (
        'there should be a warning about missing main documentation')


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


@with_setup(capture.start, capture.stop)
def test_no_version():
    args = ['-h']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'no version set' in capture.stderr.getvalue(), (
        'there should be a warning about no version set')


@with_setup(capture.start, capture.stop)
def test_missing_module():
    args = ['-h']
    try:
        SkalApp(command_modules=['missing_module']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'does not exist' in capture.stderr.getvalue(), (
        'there should be a warning about module not existing')


# Argument tests

@with_setup(capture.start, capture.stop)
def test_argument_existing():
    args = ['-h']
    try:
        SkalApp(
            args={
                '-b': {'help': 'bool argument', 'action': 'store_true'},
                ('-s', '--string'): {'help': 'string argument with long name'}
            },
            command_modules=[module]).run(args)
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
        SkalApp(
            args={
                '-b': {'help': 'bool argument', 'action': 'store_true'},
                ('-s', '--string'): {'help': 'string argument with long name'}
            },
            command_modules=[module]).run(args)
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
        SkalApp(
            args={
                '-b': {'help': 'bool argument', 'action': 'store_true'},
                ('-s', '--string'): {'help': 'string argument with long name'}
            },
            command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_argument_value_string():
    value = 'test'
    args = ['--string=' + value, 'first']
    try:
        SkalApp(
            args={
                '-b': {'help': 'bool argument', 'action': 'store_true'},
                ('-s', '--string'): {'help': 'string argument with long name'}
            },
            command_modules=[module]).run(args)
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
        SkalApp(
            args={
                '-b': {'help': 'bool argument', 'action': 'store_true'},
                ('-s', '--string'): {'help': 'string argument with long name'}
            },
            command_modules=[module]).run(args)
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
    SkalApp(command_modules=[module]).run(args)
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_non_existing():
    args = ['other']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code != 0, 'exit code should not be 0'
    assert 'ImportError' not in capture.stderr.getvalue(), (
        'output should not contain ImportError')


@with_setup(capture.start, capture.stop)
def test_command_doc():
    args = ['first', '-h']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    import skalmodule
    doc = inspect.getdoc(skalmodule.first)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_command_no_doc():
    args = ['no_doc']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'no_doc' in capture.stderr.getvalue(), (
        'there should be a warning about missing documentation')


@with_setup(capture.start, capture.stop)
def test_command_without_decorator():
    args = ['second']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code != 0, 'exit code should not be 0'


@with_setup(capture.start, capture.stop)
def test_command_duplicate():
    args = ['-h']
    try:
        SkalApp(command_modules=[module, 'skalmodule_nodoc']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'duplicate' in capture.stderr.getvalue(), (
        'duplicate commands should print warning and be skipped')
    assert 'first command, second instance' not in capture.stdout.getvalue(), (
        'duplicate commands should not be added')


@with_setup(capture.start, capture.stop)
def test_command_import_error():
    args = ['-h']
    try:
        SkalApp(command_modules=['skalmodule_importerror']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'ImportError' in capture.stderr.getvalue(), (
        'output should contain ImportError')


@with_setup(capture.start, capture.stop)
def test_command_syntax_error():
    args = ['-h']
    try:
        SkalApp(command_modules=['skalmodule_syntaxerror']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'SyntaxError' in capture.stderr.getvalue(), (
        'output should contain SyntaxError')


@with_setup(capture.start, capture.stop)
def test_command_name_error():
    args = ['-h']
    try:
        SkalApp(command_modules=['skalmodule_nameerror']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'NameError' in capture.stderr.getvalue(), (
        'output should contain NameError')


# Subcommand tests

@with_setup(capture.start, capture.stop)
def test_subcommand_doc():
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
def test_subcommand_no_doc():
    args = ['-h']
    try:
        SkalApp(subcommand_modules=['skalmodule_nodoc']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'skalmodule_nodoc' in capture.stderr.getvalue(), (
        'there should be a warning about missing documentation')


@with_setup(capture.start, capture.stop)
def test_subcommand_import_error():
    args = ['-h']
    try:
        SkalApp(subcommand_modules=['skalmodule_importerror']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'ImportError' in capture.stderr.getvalue(), (
        'output should contain ImportError')


@with_setup(capture.start, capture.stop)
def test_subcommand_syntax_error():
    args = ['-h']
    try:
        SkalApp(subcommand_modules=['skalmodule_syntaxerror']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'SyntaxError' in capture.stderr.getvalue(), (
        'output should contain SyntaxError')


@with_setup(capture.start, capture.stop)
def test_subcommand_name_error():
    args = ['-h']
    try:
        SkalApp(subcommand_modules=['skalmodule_nameerror']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'NameError' in capture.stderr.getvalue(), (
        'output should contain NameError')


@with_setup(capture.start, capture.stop)
def test_subcommand_command_existing():
    value = 'first'
    args = [module, value]
    SkalApp(subcommand_modules=[module]).run(args)
    assert value in capture.stdout.getvalue(), (
        'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_subcommand_command_non_existing():
    args = [module, 'other']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code != 0, 'exit code should not be 0'


@with_setup(capture.start, capture.stop)
def test_subcommand_command_doc():
    args = [module, 'first', '-h']
    try:
        SkalApp(subcommand_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    import skalmodule
    doc = inspect.getdoc(skalmodule.first)
    assert doc in capture.stdout.getvalue(), (
        'help string should be "%s"' % doc)


@with_setup(capture.start, capture.stop)
def test_subcommand_command_no_doc():
    args = [module, 'no_doc']
    try:
        SkalApp(subcommand_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    assert 'no_doc' in capture.stderr.getvalue(), (
        'there should be a warning about missing documentation')


@with_setup(capture.start, capture.stop)
def test_subcommand_command_without_decorator():
    args = [module, 'second']
    try:
        SkalApp(command_modules=[module]).run(args)
    except SystemExit as e:
        assert e.code != 0, 'exit code should not be 0'
