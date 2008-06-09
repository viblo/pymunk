import distutils.ccompiler as cc
import os, os.path
import sys, platform
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, Command, find_packages

def show_compilers ():
    from distutils.ccompiler import show_compilers
    show_compilers()

class build_chipmunk(Command):
    description = """compile Chipmunk to a shared library"""
    
    user_options = [('compiler=', 'c', 'specify the compiler type')
        ,('no-osx-hack', None, 'do not use the mac osx hack')]

    help_options = [
        ('help-compiler', None,
         "list available compilers", show_compilers),
        ]

    compiler = None
    no_osx_hack = False
    
    def initialize_options (self):
        self.compiler= None
    def finalize_options (self):
        #self.compiler='mingw32'
        pass
        
    def run(self):
        print "compiling chipmunk..."
        compiler = cc.new_compiler(compiler=self.compiler)

        sources = [os.path.join('chipmunk_src',x) for x in os.listdir('chipmunk_src') if x[-1] == 'c']
        compiler_preargs = ['-O3', '-std=gnu99', '-ffast-math']
        objs = compiler.compile(sources, extra_preargs=compiler_preargs)
        libname = 'chipmunk'
        link_preargs = []
        if platform.system() == 'Darwin' and not self.no_osx_hack:
            link_preargs.append("-dynamiclib")
        compiler.link_shared_lib(objs, libname, output_dir='pymunk', extra_preargs=link_preargs)

# todo: add/remove/think about this list :)
classifiers = ['Development Status :: 3 - Alpha'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Games/Entertainment'
    , 'Topic :: Software Development :: Libraries'   
]

setup(
    name='pymunk'
    , url='http://pymunk.googlecode.com'
    , author='Victor Blomqvist'
    , author_email='vb@viblo.se'
    , version='0.7.2' # remember to change me for new versions!
    , description='A wrapper for the 2d physics library Chipmunk'
    , long_description='A wrapper for the 2d rigid body physics library Chipmunk'
    , packages=['pymunk'] #find_packages(exclude=['*.tests']),
    , package_data = {'pymunk': ['libchipmunk.dll', 'libchipmunk32.so', 'libchipmunk64.so', 'libchipmunk.so', 'libchipmunk.dylib']}
    , platforms=['any']
    , license='MIT License'
    , classifiers=classifiers
    , include_package_data = True
    , cmdclass={'build_chipmunk':build_chipmunk}
    )
    
    








