import distutils.ccompiler as cc
import os, os.path
import platform
import ctypes
import distutils.cmd
from distutils.core import setup

class build_chipmunk(distutils.cmd.Command):
    description = """build chipmunk to a shared library"""
    
    user_options = [('compiler=', 'c', 'specify the compiler type. It must understand GCC arguments')
                    ,('release', 'r', 'build chipmunk without debug asserts')
                    ]
    
    boolean_options = ['release']
    
    help_options = [
        ('help-compiler', None, "list available compilers", cc.show_compilers)
        ]

    compiler = None  
        
    def initialize_options (self):
        self.compiler = None
        self.release = False
        
    def finalize_options (self):
        pass
    
    def compile_chipmunk(self):
        if self.release:
            print("compiling chipmunk in Release mode (No debug output or asserts)" )
        else:
            print("compiling chipmunk in Debug mode (Defualt, prints debug output and asserts)")
        
        compiler = cc.new_compiler(compiler=self.compiler)

        source_folders = ['chipmunk_src', os.path.join('chipmunk_src','constraints')]
        sources = []
        for folder in source_folders:
            for fn in os.listdir(folder):
                fn_path = os.path.join(folder, fn)
                if fn_path[-1] == 'c':
                    sources.append(fn_path)
                elif fn_path[-1] == 'o':
                    os.remove(fn_path)
                    
        include_folders = [os.path.join('chipmunk_src','include','chipmunk')]
        
        compiler_preargs = ['-std=gnu99', '-ffast-math', '-DCHIPMUNK_FFI', '-Wno-unknown-pragmas', '-fPIC', '-DCP_USE_CGPOINTS=0'] # '-DCP_ALLOW_PRIVATE_ACCESS']
        
        if self.release:
            compiler_preargs.append('-DNDEBUG')
        
        # check if we are on a 64bit python
        arch = ctypes.sizeof(ctypes.c_voidp) * 8
        
        if arch == 64 and platform.system() == 'Linux':
            compiler_preargs += ['-m64', '-O3']
        elif arch == 32 and platform.system() == 'Linux':
            compiler_preargs += ['-m32', '-O3']
        elif platform.system() == 'Darwin':
            #No -O3 on OSX. There's a bug in the clang compiler when using O3.
            compiler_preargs += ['-arch', 'i386', '-arch', 'x86_64']
        
        if platform.system() in ('Windows', 'Microsoft'):
            # Compile with stddecl instead of cdecl (-mrtd). 
            # Using cdecl cause a missing bytes issue in some cases
            # Because -mrtd and -fomit-frame-pointer (which is included in -O)
            # gives problem with function pointer to the sdtlib free function
            # we also have to use -fno-omit-frame-pointer
            compiler_preargs += ['-mrtd', '-O3', '-shared', '-fno-omit-frame-pointer'] 
        
        if arch == 64 and platform.system() in ('Windows', 'Microsoft'):
            compiler_preargs += ['-m64']
        if arch == 32 and platform.system() in ('Windows', 'Microsoft'):
            compiler_preargs += ['-m32']
            
        for x in compiler.executables:
            args = getattr(compiler, x)
            try:
                args.remove('-mno-cygwin') #Not available on newer versions of gcc 
                args.remove('-mdll')
            except:
                pass
        
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
            # link with stddecl instead of cdecl
            linker_preargs += ['-mrtd'] 
            # remove link against msvcr*. this is a bit ugly maybe.. :)
            compiler.dll_libraries = [lib for lib in compiler.dll_libraries if not lib.startswith("msvcr")]
        compiler.link(cc.CCompiler.SHARED_LIBRARY, objs, libname, output_dir = 'pymunk', extra_preargs=linker_preargs)
        
    def run(self):
        self.compile_chipmunk()
        
# todo: add/remove/think about this list
classifiers = ['Development Status :: 5 - Production/Stable'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Games/Entertainment'
    , 'Topic :: Software Development :: Libraries'   
    , 'Topic :: Software Development :: Libraries :: pygame'
]

from distutils.command import bdist
bdist.bdist.format_commands += ['msi']
bdist.bdist.format_command['msi'] = ('bdist_msi', "Microsoft Installer") 


setup(
    name='pymunk'
    , url='http://www.pymunk.org'
    , author='Victor Blomqvist'
    , author_email='vb@viblo.se'
    , version='4.0.0' # remember to change me for new versions!
    , description='pymunk is a easy-to-use pythonic 2d physics library built on top of Chipmunk'
    , long_description=open('README.txt').read()
    , packages=['pymunk','pymunkoptions']
    , package_data = {'pymunk': ['chipmunk.dll'
                                , 'chipmunk64.dll'
                                , 'libchipmunk.so'
                                , 'libchipmunk64.so'
                                , 'libchipmunk.dylib']}
    , license='MIT License'
    , classifiers=classifiers
    , cmdclass={'build_chipmunk':build_chipmunk}
    )
