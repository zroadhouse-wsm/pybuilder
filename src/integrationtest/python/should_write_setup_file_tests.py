#  This file is part of PyBuilder
#
#  Copyright 2011 The PyBuilder Team
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

from integrationtest_support import IntegrationTestSupport


class Test (IntegrationTestSupport):

    def test(self):
        self.write_build_file("""
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.distutils")

name = "integration-test"
default_task = "publish"

@init
def init (project):
    project.depends_on("spam")
    project.depends_on("pyassert", url="https://github.com/downloads/halimath/pyassert/pyassert-0.2.2.tar.gz")
    project.depends_on("eggs", "==0.2.3")
    project.build_depends_on("eggy")
""")
        self.create_directory("src/main/python/spam")
        self.write_file("src/main/python/spam/__init__.py", "")
        self.write_file("src/main/python/spam/eggs.py", """
def spam ():
    pass
""")

        reactor = self.prepare_reactor()
        reactor.build()

        self.assert_directory_exists("target/dist/integration-test-1.0-SNAPSHOT")
        self.assert_directory_exists("target/dist/integration-test-1.0-SNAPSHOT/spam")
        self.assert_file_empty("target/dist/integration-test-1.0-SNAPSHOT/spam/__init__.py")
        self.assert_file_content("target/dist/integration-test-1.0-SNAPSHOT/spam/eggs.py", """
def spam ():
    pass
""")

        setup_py = "target/dist/integration-test-1.0-SNAPSHOT/setup.py"

        self.assert_file_exists(setup_py)
        self.assert_file_permissions(0o755, setup_py)
        self.assert_file_content(setup_py, """#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'integration-test',
          version = '1.0-SNAPSHOT',
          description = '',
          long_description = '''''',
          author = "",
          author_email = "",
          license = '',
          url = '',
          scripts = [],
          packages = ['spam'],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
             #  data files
             # package data
          install_requires = [ "eggs==0.2.3", "spam" ],
          dependency_links = [ "https://github.com/downloads/halimath/pyassert/pyassert-0.2.2.tar.gz" ],
          zip_safe=True
    )
""")


if __name__ == "__main__":
    unittest.main()
