#!/usr/bin/python

from setuptools import setup

import sys
sys.path.insert(0, '.')

from atomhopper import __version__, __author__, __author_email__, __license__

NAME = "atomhopper"
SHORT_DESC = "Python bindings or interacting with AtomHopper"


if __name__ == "__main__":
 
    setup(
        name = NAME,
        version = __version__,
        author = __author__,
        author_email = __author_email__,
        url = "https://github.com/rackerlabs/python-%s" % NAME,
        license = __license__,
        packages = [NAME],
        package_dir = {NAME: NAME},
        package_data = {NAME: ['templates/*.j2']},
        install_package_data = True,
        description = SHORT_DESC,
        entry_points={
            'console_scripts': [ 'ahc = atomhopper.cli:run' ],
        }
    )
