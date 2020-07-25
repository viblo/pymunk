import os, os.path
import platform
import sys
import subprocess
from setuptools import setup
                        
# todo: add/remove/think about this list
classifiers = [
    'Development Status :: 5 - Production/Stable'
    , 'Intended Audience :: Developers'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Games/Entertainment'
    , 'Topic :: Software Development :: Libraries'   
    , 'Topic :: Software Development :: Libraries :: pygame'
    , 'Programming Language :: Python :: 2'
    , 'Programming Language :: Python :: 2.7'
    , 'Programming Language :: Python :: 3'
]

with(open('README.rst')) as f:
    long_description = f.read()

setup(
    name = 'pymunk',
    url = 'http://www.pymunk.org',
    author = 'Victor Blomqvist',
    author_email = 'vb@viblo.se',
    version = '6.0.0', # remember to change me for new versions!
    description = 'Pymunk is a easy-to-use pythonic 2d physics library',
    long_description = long_description,
    packages = ['pymunk','pymunkoptions', 'pymunk.tests'],
    include_package_data = True,
    license = 'MIT License',
    classifiers = classifiers,
    command_options={
        'build_sphinx': {
            'build_dir': ('setup.py', 'docs'),
            'source_dir': ('setup.py', 'docs/src')
        }
    },
    # Skip 1.13.1 becaus of issue reported to cffi here: 
    # https://bitbucket.org/cffi/cffi/issues/432/1131-breaks-pymunk-on-linux-in-a-subtle
    install_requires = ['cffi != 1.13.1'], 
    cffi_modules=['pymunk/pymunk_extension_build.py:ffibuilder'],
    extras_require = {'dev': ['pyglet','pygame','sphinx', 'aafigure', 'wheel']},    
    test_suite = "pymunk.tests",
)
