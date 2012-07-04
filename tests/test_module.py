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

from skal import SkalApp


capture = OutputCapture(debug = True)


# --- Test cases --------------------------------------------------------------


# Command tests

@with_setup(capture.start, capture.stop)
def test_command_existance():
    value = 'first'
    args = [value]
    SkalApp(modules = ['skalmodule']).run(args)
    assert value in capture.stdout.getvalue(), (
            'output should contain "%s"' % value)


@with_setup(capture.start, capture.stop)
def test_command_help():
    args = ['-h']
    try:
        SkalApp(modules = ['skalmodule']).run(args)
    except SystemExit as e:
        assert e.code == 0, 'exit code should be 0'
    import skalmodule
    doc = skalmodule.first.__doc__
    assert doc in capture.stdout.getvalue(), (
            'help string should be "%s"' % doc)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_command_without_decorator():
    args = ['second']
    SkalApp(modules = ['skalmodule']).run(args)


@raises(SystemExit)
@with_setup(capture.start, capture.stop)
def test_invalid_command():
    args = ['other']
    SkalApp(modules = ['skalmodule']).run(args)
