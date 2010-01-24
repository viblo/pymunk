import distutils.ccompiler as cc
import os, os.path
import platform
import ctypes
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

        source_folders = ['chipmunk_src', 'chipmunk_src/constraints']
        sources = []
        for folder in source_folders:
            sources += [os.path.join(folder,x) for x in os.listdir(folder) if x[-1] == 'c']
        
        include_folders = ['chipmunk_src/include']
        
        compiler_preargs = ['-O3', '-std=gnu99', '-ffast-math', '-fPIC', '-DNDEBUG']
        
        # check if we are on a 64bit python
        arch = ctypes.sizeof(ctypes.c_voidp) * 8
        
        if arch == 64 and platform.system() == 'Linux':
            compiler_preargs += ['-m64']
        elif arch == 32 and platform.system() == 'Linux':
            compiler_preargs += ['-m32']
        elif platform.system() == 'Darwin':
            compiler_preargs += ['-arch', 'i386', '-arch', 'x86_64']
        ### because mingw only ships with gcc 3 we don't add any -mXX argument on Windows
        
        if platform.system() in ('Windows', 'Microsoft'):
            compiler_preargs += ['-mrtd'] # compile with stddecl instead of cdecl
        
        objs = compiler.compile(sources, include_dirs=include_folders, extra_preargs=compiler_preargs)
        
        libname = 'chipmunk'
        if arch == 64 and platform.system() != 'Darwin':
            libname += '64'
        if platform.system() == 'Darwin':
            libname = compiler.library_filename(libname, lib_type='dylib')
            compiler.set_executable('linker_so', ['cc', '-dynamiclib', '-arch', 'i386', '-arch', 'x86_64'])
        else:
            libname = compiler.library_filename(libname, lib_type='shared')
        linker_preargs = []
        if platform.system() == 'Linux' and platform.machine() == 'x86_64':
            linker_preargs += ['-fPIC']
        if platform.system() in ('Windows', 'Microsoft'):
            linker_preargs += ['-mrtd'] # link with stddecl instead of cdecl
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

long_description = """pymunk is a easy-to-use pythonic 2d physics library that can be used whenever you need 2d rigid body physics from Python. It is build on top of the very nice 2d physics library Chipmunk, http://code.google.com/p/chipmunk-physics/"""

from distutils.command import bdist
bdist.bdist.format_commands += ['msi']
bdist.bdist.format_command['msi'] = ('bdist_msi', "Microsoft Installer") 
setup(
    name='pymunk'
    , url='http://code.google.com/p/pymunk/'
    , author='Victor Blomqvist'
    , author_email='vb@viblo.se'
    , version='0.9.0' # remember to change me for new versions!
    , description='A wrapper for the 2d physics library Chipmunk'
    , long_description=long_description
    , packages=['pymunk'] #find_packages(exclude=['*.tests']),
    , package_data = {'pymunk': ['chipmunk.dll'
                                , 'chipmunk64.dll'
                                , 'libchipmunk.so'
                                , 'libchipmunk64.so'
                                , 'libchipmunk.dylib']}
    , eager_resources = [os.path.join('pymunk','chipmunk.dll')
                            , os.path.join('pymunk','chipmunk64.dll')
                            , os.path.join('pymunk','libchipmunk.so')
                            , os.path.join('pymunk','libchipmunk64.so')
                            , os.path.join('pymunk','libchipmunk.dylib')]
    #, platforms=['win32']
    , license='MIT License'
    , classifiers=classifiers
    , include_package_data = True
    , cmdclass={'build_chipmunk':build_chipmunk}
    , test_suite = "tests"
    )
