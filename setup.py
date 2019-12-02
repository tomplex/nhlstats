__author__ = 'tcaruso'

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

try:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:
    from pip.req import parse_requirements
    from pip.download import PipSession
except Exception:
    from pip import __version__ as __pip_version__

    msg = """Sorry, could not install due to a pip import error. Please open an issue on the repo 
    with this message and the error so it can be addressed.
    pip version: {}
    python version: {}
    """.format(__pip_version__, '.'.join(sys.version_info))
    raise EnvironmentError(msg)

here = os.path.abspath(os.path.dirname(__file__))

# ------------------------------------------------

# Package meta-data.
# PACKAGE_NAME is the name of the package directory and the import path. If you use my_package then when installed, you
# will import the package like `import my_package`.
PACKAGE_NAME = 'nhlstats'
DESCRIPTION = 'Tools for collecting NHL play-by-play stats.'
URL = 'https://github.com/tomplex/nhlstats'
EMAIL = 'carusot42@gmail.com'
AUTHOR = 'Tom Caruso'
# The minimum Python version required
REQUIRES_PYTHON = (3, 5, 0)
# PYPI_NAME is the name of the package on pypi. You'll use this name to install the package.
PYPI_NAME = '{}'.format(PACKAGE_NAME)

# ------------------------------------------------
# Check Python version we're installing against. Bail if it's not correct. This will blow up both when we build the
# package and when someone tries to install it.

if sys.version_info < REQUIRES_PYTHON:
    # Raise if we're trying to install on an unsupported Python version
    raise Exception("Package {} requires python >= {}.".format(PYPI_NAME, '.'.join(map(str, REQUIRES_PYTHON))))

REQUIRES_PYTHON = '>=' + '.'.join(map(str, REQUIRES_PYTHON))


# ------------------------------------------------
# Requirements gathering.

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status("Installing required build packages...")
        os.system('{0} -m pip install wheel twine'.format(sys.executable))

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to pypi via Twine…')
        os.system('{0} -m twine upload dist/* '.format(sys.executable))

        sys.exit()


setup(
    name=PYPI_NAME,
    version='0.0.1',
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    install_requires=[str(requirement.req) for requirement in requirements],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    entry_points={
        'console_scripts': ['nhl=nhlstats.cli.core:cli'],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    # setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
