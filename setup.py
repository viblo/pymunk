import os, os.path
import platform
import sys
from distutils.command.build_ext import build_ext
import distutils.ccompiler as cc
from setuptools import Extension
from setuptools import setup


def get_arch():
    if sys.maxsize > 2**32:
        arch = 64
    else:
        arch = 32
    return arch

def get_library_name():
    libname = 'chipmunk'
    if get_arch() == 64 and platform.system() != 'Darwin':
        libname += '64'
    if platform.system() == 'Darwin':
        libname = "lib" + libname + ".dylib"
    elif platform.system() == 'Linux':
        libname = "lib" + libname + ".so"
    elif platform.system() == 'Windows':
        libname += ".dll"
    else:
        libname += ".so"
    return libname
    
class build_chipmunk(build_ext, object):

    def finalize_options(self):
        if platform.system() == 'Windows':
            print("Running on Windows. GCC will be forced used")
            self.compiler = "mingw32"
        
        return super(build_chipmunk, self).finalize_options()

    def get_outputs(self):
        x = super(build_chipmunk, self).get_outputs()
        
        #print("get_outputs", x)
        #print("get_outputs xoutputs", self.xoutputs)
        return self.xoutputs

    def run(self):
        self.compiler = cc.new_compiler(compiler=self.compiler)
        
        compiler_preargs = ['-std=gnu99', 
                            '-ffast-math', 
                            '-DCHIPMUNK_FFI', 
                            '-g',
                            #'-Wno-unknown-pragmas', 
                            #'-fPIC', 
                            '-DCP_USE_CGPOINTS=0',
                            # '-DCP_ALLOW_PRIVATE_ACCESS']
                            ]
        if not self.debug:
            compiler_preargs.append('-DNDEBUG')
        
        if get_arch() == 64 and platform.system() == 'Linux':
            compiler_preargs += ['-m64', '-fPIC', '-O3']
        elif get_arch() == 32 and platform.system() == 'Linux':
            compiler_preargs += ['-m32', '-fPIC', '-O3']
        elif platform.system() == 'Darwin':
            #No -O3 on OSX. There's a bug in the clang compiler when using O3.
            compiler_preargs += ['-arch', 'i386', '-arch', 'x86_64']
        
        if platform.system() == 'Windows':
            compiler_preargs += ['-shared']
                                            
            if get_arch() == 32:
                # We set the stack boundary with -mincoming-stack-boundary=2
                # from 
                # https://mingwpy.github.io/issues.html#choice-of-msvc-runtime 
                compiler_preargs += ['-O3', 
                                    '-mincoming-stack-boundary=2',
                                    '-m32']
            if get_arch() == 64:
                compiler_preargs += ['-O3', '-m64']
            
        for x in self.compiler.executables:
            args = getattr(self.compiler, x)
            try:
                args.remove('-mno-cygwin') #Not available on newer versions of gcc 
                args.remove('-mdll')
            except:
                pass
                
        source_folders = [os.path.join('chipmunk_src','src')]
        sources = []
        for folder in source_folders:
            for fn in os.listdir(folder):
                fn_path = os.path.join(folder, fn)
                if fn[-1] == 'c':
                    # Ignore cpHastySpace since it depends on pthread which 
                    # doesnt work in mingwpy gcc (it uses win32 threads)
                    # Will prevent the code from being multithreaded, would be
                    # good if some tests could be made to verify the performance
                    # of this.
                    if platform.system() != 'Windows' or fn != "cpHastySpace.c":
                        sources.append(fn_path)
                elif fn[-1] == 'o':
                    os.remove(fn_path)
        
        include_dirs = [os.path.join('chipmunk_src','include')]
        
        objs = self.compiler.compile(sources, 
            include_dirs=include_dirs, extra_preargs=compiler_preargs)
            
        if platform.system() == 'Darwin':
            self.compiler.set_executable('linker_so', 
                ['cc', '-dynamiclib', '-arch', 'i386', '-arch', 'x86_64'])
        linker_preargs = []
        if platform.system() == 'Linux' and platform.machine() == 'x86_64':
            linker_preargs += ['-fPIC']
        if platform.system() == 'Windows':
            if get_arch() == 32:
                linker_preargs += ['-m32']
            else:
                linker_preargs += ['-m64']
            # remove link against msvcr*. this is a bit ugly maybe.. :)
            self.compiler.dll_libraries = [lib for lib in self.compiler.dll_libraries if not lib.startswith("msvcr")]
        #here = os.path.abspath(os.path.dirname(__file__))
        #print("here", here)
        
        #print("self.inplace", self.inplace)
        if not self.inplace:
            package_dir = os.path.join(self.build_lib, "pymunk")
        else:
            build_py = self.get_finalized_command('build_py')
            package_dir = os.path.abspath(build_py.get_package_dir(".pymunk"))
        self.xoutputs = [os.path.join(package_dir, get_library_name())]
        #package_dir = self.build_lib
        #print("package_dir", package_dir)
        #outpath = os.path.join(package_dir, get_library_name()) 
        self.compiler.link(
            cc.CCompiler.SHARED_LIBRARY, 
            objs, get_library_name(),
            output_dir = package_dir, extra_preargs=linker_preargs)    
                
                        
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

from distutils.command import bdist
bdist.bdist.format_commands += ['msi']
bdist.bdist.format_command['msi'] = ('bdist_msi', "Microsoft Installer") 

with(open('README.rst')) as f:
    long_description = f.read()

source_folders = [os.path.join('chipmunk_src','src')]
sources = []
for folder in source_folders:
    for fn in os.listdir(folder):
        fn_path = os.path.join(folder, fn)
        if fn_path[-1] == 'c':
            sources.append(fn_path)
        elif fn_path[-1] == 'o':
            os.remove(fn_path)
            
extensions = [("pymunk.chipmunk", {
    'sources': sources,
    'include_dirs': [os.path.join('chipmunk_src','include')]
})]

extensions = [Extension("pymunk.chipmunk", sources)]

setup(
    name = 'pymunk',
    url = 'http://www.pymunk.org',
    author = 'Victor Blomqvist',
    author_email = 'vb@viblo.se',
    version = '5.1.0', # remember to change me for new versions!
    description = 'Pymunk is a easy-to-use pythonic 2d physics library',
    long_description = long_description,
    packages = ['pymunk','pymunkoptions'],
    
    include_package_data = True,
    license = 'MIT License',
    classifiers = classifiers,
    cmdclass = {'build_ext': build_chipmunk},
    install_requires = ['cffi'],
    extras_require = {'dev': ['pyglet','pygame','sphinx']},    
    test_suite = "tests",
    ext_modules = extensions,
)
