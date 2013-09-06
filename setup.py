#!/usr/bin/python

from distutils.core import setup

# are these needed?
import sys
sys.path.insert(0, '.')

from atomhopper import __version__, __author__, __author_email__, __license__

NAME = "atomhopper"
SHORT_DESC = "Python bindings or interacting with AtomHopper"


if __name__ == "__main__":
 
#    manpath    = "share/man/man1/"
#    data_files = [(manpath,  ["docs/%s.1.gz" % NAME])],
    data_files = None
    setup(
        name = NAME,
        version = __version__,
        author = __author__,
        author_email = __author_email__,
        url = "https://github.com/rackerlabs/python-%s" % NAME,
        license = __license__,
        scripts = ["scripts/%s" % NAME],
        package_dir = {NAME: NAME},
        packages = [NAME],
        data_files = data_files,
        description = SHORT_DESC,
    )
