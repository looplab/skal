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


class OutputCapture(object):
    def __init__(self):
        self.debug_output = False

    def start(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.stdout = StringIO.StringIO()
        self.stderr = StringIO.StringIO()
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def stop(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        if self.debug_output:
            if self.stdout.getvalue() != "":
                print('\nStdout:\n%s' % self.stdout.getvalue())
            if self.stderr.getvalue() != "":
                print('\nStderr:\n%s' % self.stderr.getvalue())
        self.stdout = None
        self.stderr = None
