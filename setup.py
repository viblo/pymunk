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


print "os.environ !!!!!!!!!!!!!!!!!!!"
print os.environ

d = {'READELF': 'arm-linux-androideabi-readelf', 'CXXFLAGS': '-DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm', 'PATH': '/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b:/media/sf_code/kivytest/tools_r25.2.3-linux/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games', 'ARCH': 'armeabi', 'LD': 'arm-linux-androideabi-ld', 'NM': 'arm-linux-androideabi-nm', 'LDFLAGS': '-lm -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_15/armeabi -llog -lc -lm -landroid --sysroot=/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm', 'STRIP': 'arm-linux-androideabi-strip --strip-unneeded', 'NDK_CCACHE': '/usr/bin/ccache', 'CC': '/usr/bin/ccache arm-linux-androideabi-gcc -DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm', 'PYTHONPATH': '/home/kivy/.local/share/python-for-android/build/other_builds/hostpython2/desktop/hostpython2/Lib:/home/kivy/.local/share/python-for-android/build/other_builds/hostpython2/desktop/hostpython2/Lib/site-packages:/home/kivy/.local/share/python-for-android/build/other_builds/hostpython2/desktop/hostpython2/build/lib.linux-x86_64-2.7:/home/kivy/.local/share/python-for-android/build/other_builds/hostpython2/desktop/hostpython2/build/scripts-2.7:/home/kivy/.local/share/python-for-android/build/other_builds/hostpython2/desktop/hostpython2/build/temp.linux-x86_64-2.7', 'PYTHONNOUSERSITE': '1', 'RANLIB': 'arm-linux-androideabi-ranlib', 'BUILDLIB_PATH': '/home/kivy/.local/share/python-for-android/build/other_builds/hostpython2/desktop/hostpython2/build/lib.linux-x86_64-2.7', 'AR': 'arm-linux-androideabi-ar', 'TOOLCHAIN_PREFIX': 'arm-linux-androideabi', 'CXX': '/usr/bin/ccache arm-linux-androideabi-g++ -DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm', 'MAKE': 'make -j5', 'USE_CCACHE': '1', 'CFLAGS': '-DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm', 'PYTHON_ROOT': '/home/kivy/.local/share/python-for-android/build/python-installs/unnamed_dist_15', 'TOOLCHAIN_VERSION': '4.9'}

print "DEBUG LINE XXXXXXXXXXXXXXXXXXXXX"
msg = ""
keys = ["LD", "PATH", "LDFLAGS", "CFLAGS", "CC"]
for key in keys:
    msg += ' ' + key + '="'+ d[key] +'"'
msg += " python setup.py build_ext"
print msg

cmd = '''

nm -g /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-21/arch-arm/usr/lib/*.so | grep __

chipmunk_src/include/chipmunk/chipmunk_types.h:121: error: undefined reference to '__aeabi_dcmpge'
chipmunk_src/include/chipmunk/chipmunk_types.h:127: error: undefined reference to '__aeabi_dcmple'
chipmunk_src/include/chipmunk/chipmunk_types.h:153: error: undefined reference to '__aeabi_dsub'
chipmunk_src/include/chipmunk/chipmunk_types.h:153: error: undefined reference to '__aeabi_dmul'
chipmunk_src/include/chipmunk/chipmunk_types.h:153: error: undefined reference to '__aeabi_dmul'
chipmunk_src/include/chipmunk/chipmunk_types.h:153: error: undefined reference to '__aeabi_dadd'
chipmunk_src/include/chipmunk/chipmunk_types.h:159: error: undefined reference to '__aeabi_dsub'
chipmunk_src/include/chipmunk/chipmunk_types.h:159: error: undefined reference to '__aeabi_dadd'




/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/lib/gcc/arm-linux-androideabi/4.9.x/


PATH="/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b:/media/sf_code/kivytest/tools_r25.2.3-linux/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games" LD="arm-linux-androideabi-ld"  LDFLAGS="-march=armv7-a -lm -L-llog -lc -landroid -L/lib/gcc/arm-linux-androideabi/4.9.x/armv7-a -L/media/sf_code/kivytest/ndk/lib/gcc/arm-linux-androideabi/4.9.x/armv7-a -lgcc --sysroot /media/sf_code/kivytest/ndk/sysroot" CFLAGS="-DANDROID -mandroid -fomit-frame-pointer -march=armv7-a -m   float-abi=softfp -mfpu=vfpv3-d16" CC="/usr/bin/ccache arm-linux-androideabi-gcc -DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/ndk/sysroot" python setup.py build_ext



cmake -DCMAKE_TOOLCHAIN_FILE=/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/build/cmake/android.toolchain.cmake \
      -DANDROID_NDK=/media/sf_code/kivytest/ndk \
      -DCMAKE_BUILD_TYPE=Release \
      -DANDROID_ABI="armeabi" .



LD="arm-linux-androideabi-ld" PATH="/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b:/media/sf_code/kivytest/tools_r25.2.3-linux/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games" LDFLAGS="-lm -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_15/armeabi -L/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/lib/gcc/arm-linux-androideabi/4.9.x/ -llibgcc -llog -lc -landroid --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm" CFLAGS="-DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm" CC="/usr/bin/ccache arm-linux-androideabi-gcc -DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm" python setup.py build_ext


LD="/usr/local/lib/python2.7/dist-packages/pythonforandroid/tools/liblink.sh" PATH="/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b:/media/sf_code/kivytest/tools_r25.2.3-linux/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games" LDFLAGS="-lm -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_15/armeabi -llog -lc -lm -landroid --sysroot=/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm" CFLAGS="-DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm" CC="/usr/bin/ccache arm-linux-androideabi-gcc -DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm" python setup.py build_ext



/usr/local/lib/python2.7/dist-packages/pythonforandroid/tools/liblink.sh -lm -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_16/armeabi -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_16/armeabi -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_16 -L/home/kivy/.local/share/python-for-android/build/bootstrap_builds/sdl2-python2/obj/local/armeabi -DANDROID -mandroid -fomit-frame-pointer --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm build/temp.linux-x86_64-2.7/cymunk/cymunk.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSpatialIndex.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSpaceHash.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpPivotJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpConstraint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpSlideJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpRotaryLimitJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpGrooveJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpGearJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpRatchetJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpSimpleMotor.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpDampedRotarySpring.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpPinJoint.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/constraints/cpDampedSpring.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSpaceStep.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpArray.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpArbiter.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpCollision.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpBBTree.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSweep1D.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/chipmunk.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSpaceQuery.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpBB.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpShape.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSpace.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpVect.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpPolyShape.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpSpaceComponent.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpBody.o build/temp.linux-x86_64-2.7/cymunk/Chipmunk-Physics/src/cpHashSet.o -L/home/kivy/.local/share/python-for-android/build/other_builds/python2/armeabi/python2/python-install/lib -lpython2.7 -o build/lib.linux-x86_64-2.7/cymunk/cymunk.so



PATH="/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/:/media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b:/media/sf_code/kivytest/tools_r25.2.3-linux/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games" arm-linux-androideabi-ld -lm -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_15/armeabi -llog -lc -landroid --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm chipmunk_src/src/chipmunk.o chipmunk_src/src/cpArbiter.o chipmunk_src/src/cpArray.o chipmunk_src/src/cpBBTree.o chipmunk_src/src/cpBody.o chipmunk_src/src/cpCollision.o chipmunk_src/src/cpConstraint.o chipmunk_src/src/cpDampedRotarySpring.o chipmunk_src/src/cpDampedSpring.o chipmunk_src/src/cpGearJoint.o chipmunk_src/src/cpGrooveJoint.o chipmunk_src/src/cpHashSet.o chipmunk_src/src/cpHastySpace.o chipmunk_src/src/cpMarch.o chipmunk_src/src/cpPinJoint.o chipmunk_src/src/cpPivotJoint.o chipmunk_src/src/cpPolyline.o chipmunk_src/src/cpPolyShape.o chipmunk_src/src/cpRatchetJoint.o chipmunk_src/src/cpRobust.o chipmunk_src/src/cpRotaryLimitJoint.o chipmunk_src/src/cpShape.o chipmunk_src/src/cpSimpleMotor.o chipmunk_src/src/cpSlideJoint.o chipmunk_src/src/cpSpace.o chipmunk_src/src/cpSpaceComponent.o chipmunk_src/src/cpSpaceDebug.o chipmunk_src/src/cpSpaceHash.o chipmunk_src/src/cpSpaceQuery.o chipmunk_src/src/cpSpaceStep.o chipmunk_src/src/cpSpatialIndex.o chipmunk_src/src/cpSweep1D.o -o build/lib.linux-x86_64-2.7/pymunk/libchipmunk64.so


LIBLINK_PATH="/media/sf_code/gh/pymunk/chipmunk_src/src/" /usr/local/lib/python2.7/dist-packages/pythonforandroid/tools/liblink.sh -lm -L/home/kivy/.local/share/python-for-android/build/libs_collections/unnamed_dist_15/armeabi -llog -lc -lm -landroid --sysroot /media/sf_code/kivytest/android-ndk-r13b-linux-x86_64/android-ndk-r13b/platforms/android-19/arch-arm chipmunk_src/src/chipmunk.o chipmunk_src/src/cpArbiter.o chipmunk_src/src/cpArray.o chipmunk_src/src/cpBBTree.o chipmunk_src/src/cpBody.o chipmunk_src/src/cpCollision.o chipmunk_src/src/cpConstraint.o chipmunk_src/src/cpDampedRotarySpring.o chipmunk_src/src/cpDampedSpring.o chipmunk_src/src/cpGearJoint.o chipmunk_src/src/cpGrooveJoint.o chipmunk_src/src/cpHashSet.o chipmunk_src/src/cpHastySpace.o chipmunk_src/src/cpMarch.o chipmunk_src/src/cpPinJoint.o chipmunk_src/src/cpPivotJoint.o chipmunk_src/src/cpPolyline.o chipmunk_src/src/cpPolyShape.o chipmunk_src/src/cpRatchetJoint.o chipmunk_src/src/cpRobust.o chipmunk_src/src/cpRotaryLimitJoint.o chipmunk_src/src/cpShape.o chipmunk_src/src/cpSimpleMotor.o chipmunk_src/src/cpSlideJoint.o chipmunk_src/src/cpSpace.o chipmunk_src/src/cpSpaceComponent.o chipmunk_src/src/cpSpaceDebug.o chipmunk_src/src/cpSpaceHash.o chipmunk_src/src/cpSpaceQuery.o chipmunk_src/src/cpSpaceStep.o chipmunk_src/src/cpSpatialIndex.o chipmunk_src/src/cpSweep1D.o -o build/lib.linux-x86_64-2.7/pymunk/libchipmunk64.so
'''



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
        print self.compiler.executables

        if "AR" in os.environ:
            self.compiler.set_executable("archiver", os.environ["AR"])

        if "CC" in os.environ:
            self.compiler.set_executable("compiler", os.environ["CC"])
            self.compiler.set_executable("compiler_so", os.environ["CC"])
            
        if "LD" in os.environ:
            self.compiler.set_executable("linker_so", os.environ["LD"])

        


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
        
        if "CFLAGS" in os.environ:
            compiler_preargs.append(os.environ["CFLAGS"])
        else:
            if platform.system() == 'Linux':
                compiler_preargs += ['-fPIC', '-O3']
                if get_arch() == 64 and not platform.machine().startswith('arm'):
                    compiler_preargs += ['-m64']
                elif get_arch() == 32 and not platform.machine().startswith('arm'):
                    compiler_preargs += ['-m32']

            elif platform.system() == 'Darwin':
                #No -O3 on OSX. There's a bug in the clang compiler when using O3.
                compiler_preargs += ['-arch', 'i386', '-arch', 'x86_64']
            
            elif platform.system() == 'Windows':
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
        if "LDFLAGS" in os.environ:
            for l in os.environ["LDFLAGS"].split():
                
                linker_preargs.append(l)
            #linker_preargs.append("-shared")
        else:
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
