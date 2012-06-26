#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='simplestack',
    version='0.0.1',
    description='A simple abstraction to deal with different hypervisors',
    author='Locaweb',
    url='http://github.com/locaweb/simplestack',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    data_files=[
        ('/usr/sbin', ['src/bin/simplestack']),
        ('/etc/init.d', ['src/init/simplestack']),
        ('/etc', ['src/conf/simplestack.conf']),
    ]
)
