from setuptools import setup, Extension, find_packages

# todo: add/remove/think about this list :)
classifiers = ['Development Status :: 3 - Alpha'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Games/Entertainment'
    , 'Topic :: Software Development :: Libraries'   
]

setup(
    name='pymunk',
    url='http://pymunk.googlecode.com',
    author='Victor Blomqvist',
    author_email='vb@viblo.se',
    version='0.6',
    description='A wrapper for the Chipmunk 2D physics library',
    long_description='A Python ctypes wrapper for the Chipmunk 2D rigid body '
                     'physics library',
    packages=find_packages(exclude=['*.tests']),
    platforms=['any'],
    license='MIT License',
    classifiers=classifiers
    )