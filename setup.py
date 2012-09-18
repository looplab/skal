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

from setuptools import setup
import sys
from skal import __version__


requirements = []
if sys.version_info < (2, 7):
    requirements.append('argparse')


setup(
    name = "skal",
    version = __version__,
    description = "Class based command line wrapper",
    author = "Max Persson",
    author_email = "max@looplab.se",
    url = "https://github.com/looplab/skal",
    license = "Apache License 2.0",
    py_modules = ["skal"],
    install_requires = requirements,
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
