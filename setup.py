#!/usr/bin/python
from distutils.core import setup

setup(
    name='simplestack',
    version='0.0.1',
    description='A simple abstraction to deal with different hypervisors',
    author='Locaweb',
    url='http://github.com/locaweb/simplestack',
    packages=['simplestack']
    package_dir={'simplestack': 'src/simplestack'},
    data_files=[
        ('/usr/sbin', ['src/bin/simplestack']),
        ('/etc/init.d', ['src/init/simplestack']),
        ('/etc', ['src/conf/simplestack.conf']),
    ]
)
