#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

import sys

install_requires = ['pymysql']

# add unittest2 to install_requires for python < 2.7
if sys.version_info < (2, 7):
    install_requires.append("unittest2")


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """
        Finds all the tests modules in tests/, and runs them.
        """
        from pymysqlreplication import tests
        import unittest

        unittest.main(tests, argv=sys.argv[:1])


version = "0.9"

setup(
    name="mysql-replication",
    version=version,
    url="https://github.com/noplay/python-mysql-replication",
    author="Julien Duponchelle",
    author_email="julien@duponchelle.info",
    description=("Pure Python Implementation of MySQL replication protocol "
                 "build on top of PyMYSQL."),
    license="Apache 2",
    packages=["pymysqlreplication",
              "pymysqlreplication.constants",
              "pymysqlreplication.tests"],
    cmdclass={"test": TestCommand},
    install_requires=install_requires,
)
