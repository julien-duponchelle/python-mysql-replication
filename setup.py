#!/usr/bin/env python

try:
    from setuptools import Command, setup
except ImportError:
    from distutils.core import Command, setup

import sys
from pathlib import Path


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
        import unittest

        from pymysqlreplication import tests

        unittest.main(tests, argv=sys.argv[:1])


version = "1.0.11"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mysql-replication",
    version=version,
    url="https://github.com/julien-duponchelle/python-mysql-replication",
    author="Julien Duponchelle",
    author_email="julien@duponchelle.info",
    description=(
        "Pure Python Implementation of MySQL replication protocol "
        "build on top of PyMYSQL."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2",
    packages=[
        "pymysqlreplication",
        "pymysqlreplication.constants",
        "pymysqlreplication.tests",
        "pymysqlreplication.util",
    ],
    cmdclass={"test": TestCommand},
    install_requires=[
        "packaging",
        "pymysql>=1.1.0",
    ],
)
