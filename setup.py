from setuptools import setup
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

from trendt import __version__, __description__, __program__

setup(
    name = __program__,
    version = __version__,
    packages = [__program__],
    description = __description__,
    url = 'https://git.compsoc.lancs.ac.uk/a.jung/trendy-t',
    author = 'Alexander Jung',
    author_email = 'a.jung@lancs.ac.uk',
    license = 'MIT',
    entry_points = """
        [console_scripts]
        {program} = trendt.trendt:main
        """.format(program = __program__),
    keywords = [],
    tests_require = ['pytest', 'coveralls'],
    zip_safe = False
)
