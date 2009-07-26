import distutils.ccompiler as cc
import os, os.path
import platform
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, Command, find_packages

def show_compilers ():
    from distutils.ccompiler import show_compilers
    show_compilers()

class build_chipmunk(Command):
    description = """build chipmunk to a shared library"""
    
    user_options = [('compiler=', 'c', 'specify the compiler type')]

    help_options = [
        ('help-compiler', None,
         "list available compilers", show_compilers),
        ]

    compiler = None  
        
    def initialize_options (self):
        self.compiler= None
        
    def finalize_options (self):
        pass
    
    def compile_chipmunk(self):
        print("compiling chipmunk...")
        
        compiler = cc.new_compiler(compiler=self.compiler)

        sources = [os.path.join('chipmunk_src',x) for x in os.listdir('chipmunk_src') if x[-1] == 'c']
        compiler_preargs = ['-O3', '-std=gnu99', '-ffast-math', '-fPIC']
        objs = compiler.compile(sources, extra_preargs=compiler_preargs)
        
        libname = 'chipmunk'
        if platform.system() == 'Darwin':
            libname = compiler.library_filename(libname, lib_type='dylib')
            compiler.set_executable('linker_so', ['cc', '-dynamiclib'])
        else:
            libname = compiler.library_filename(libname, lib_type='shared')
        linker_preargs = []
        if  platform.system() == 'Linux' and platform.machine() == 'x86_64':
            linker_preargs += ['-fPIC']
        
        compiler.link(cc.CCompiler.SHARED_LIBRARY, objs, libname, output_dir = 'pymunk', extra_preargs=linker_preargs)
    
    def run(self):
        self.compile_chipmunk()
        
# todo: add/remove/think about this list :)
classifiers = ['Development Status :: 4 - Beta'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Games/Entertainment'
    , 'Topic :: Software Development :: Libraries'   
]

long_description = """pymunk is wrapper for the 2d rigid body physics library Chipmunk"""

setup(
    name='pymunk'
    , url='http://pymunk.googlecode.com'
    , author='Victor Blomqvist'
    , author_email='vb@viblo.se'
    , version='0.8.3' # remember to change me for new versions!
    , description='A wrapper for the 2d physics library Chipmunk'
    , long_description=long_description
    , packages=['pymunk'] #find_packages(exclude=['*.tests']),
    , package_data = {'pymunk': ['chipmunk.dll'
                                , 'libchipmunk.so'
                                , 'libchipmunk.dylib']}
    , eager_resources = [os.path.join('pymunk','chipmunk.dll')
                            , os.path.join('pymunk','libchipmunk.so')
                            , os.path.join('pymunk','libchipmunk.dylib')]
    #, platforms=['win32']
    , license='MIT License'
    , classifiers=classifiers
    , include_package_data = True
    , cmdclass={'build_chipmunk':build_chipmunk}
    )