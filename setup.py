#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='simplestack',
    version='0.0.3-1',
    description='A simple abstraction to deal with different hypervisors',
    author='Locaweb',
    url='http://github.com/locaweb/simplestack',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    data_files=[
        ('/usr/sbin', ['bin/simplestack']),
        ('/etc/simplestack', ['etc/simplestack.cfg']),
    ],
)
