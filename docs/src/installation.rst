============
Installation
============
.. _installation:

.. tip::
    You will find the latest released version at pypi:  
    https://pypi.python.org/pypi/pymunk


Install Pymunk
==============

Pymunk can be installed with pip install::

    > pip install pymunk
    
Pymunk can also be installed with conda install, from the conda-forge channel::

    > conda install -c conda-forge pymunk

Once Pymunk is installed you can verify that the installation works by running 
the tests::

    > python -m pymunk.tests test

Sometimes on more uncommon platforms you will need to have a GCC-compatible 
c-compiler installed. 

On OSX you can install one with::

    > xcode-select --install

On Linux you can install one with the package manager, for example on Ubuntu 
with::

    > sudo apt-get install build-essential


Examples & Documentation
========================

Because of their size are the examples and documentation available in the 
source distribution of Pymunk, but not the wheels. The source distribution is 
available from PyPI at https://pypi.org/project/pymunk/#files (Named
pymunk-x.y.z.zip)


Troubleshooting?????
====================

Check that no files are named pymunk.py

Check that conda install works
https://stackoverflow.com/questions/39811929/package-installed-by-conda-python-cannot-find-it

Advanced - Android Install
==========================

Pymunk can run on Android phones/tablets/computers. 

Kivy
----

`Kivy <https://kivy.org>`_ is a open source Python library for rapid 
development of applications that make use of innovative user interfaces, such 
as multi-touch apps, and can run on Android (and a number of other platforms 
such as Linux, Windows, OS X, iOS and Raspberry Pi).

Pymunk should work out of the box when used with Kivy. Note however that the 
recipe used to build Pymunk specifies a specific version of Pymunk that might 
not be the latest, see the recipe script here:
https://github.com/kivy/python-for-android/blob/master/pythonforandroid/recipes/pymunk/__init__.py


Termux
------

`Termux <https://termux.com/>`_ is an Android terminal emulator and Linux 
environment app that works directly with no rooting or setup required. 

There are no binary wheels of pymunk for Termux/Android, or for its dependency 
cffi, so you will need to install a couple of packages first, before pymunk can 
be installed.

1. Install python and other needed dependencies (run inside Termux)::

    $ pkg install python python-dev clang libffi-dev

2. Install pymunk with pip::

    $ pip install pymunk 

3. Verify that it works::

    $ python -m pymunk.tests test


Advanced - Install
==================

Another option is to use the standard setup.py way, in case you have downloaded
the source distribution::

    > python setup.py install

Note that this require a GCC compiler, which can be a bit tricky on Windows. 
If you are on Mac OS X or Linux you will probably need to run as a privileged 
user; for example using sudo::
    
    > sudo python setup.py install
    
Once installed you should be able to to import pymunk just as any other 
installed library. pymunk should also work just fine with virtualenv in case 
you want it installed in a contained environment.
 

Advanced - Running without installation
---------------------------------------

If you do not want to install Pymunk, for example because you want to bundle it
with your code, its also possible to run it directly inplace. Given that you 
have the source code the first thing to do is to compile chipmunk with the 
inplace option, as described in the :ref:`compile-chipmunk` section. 

To actually import pymunk from its folder you need to do a small path hack, 
since the pymunk root folder (where setup.py and the README are located) is not 
part of the package. Instead you should add the path to the pymunk package 
folder (where files such as space.py and body.py are located)::

    mycodefolder/
    |-- mycode.py
    |-- ...
    |-- pymunk/
    |   |-- README.rst
    |   |-- setup.py
    |   |-- pymunk/
    |   |   |-- space.py
    |   |   |-- body.py
    |   |   |-- ...
    |   |-- ... 

Then inside you code file (`mycode.py`) import sys and add the pymunk folder to
the path::

    import sys
    sys.path.insert(1, 'pymunk')
    import pymunk

The same trick can be used to import pymunk for a script that is not in the 
direct parent folder, see for example `run.py` in the examples which update 
the path to simplify development.


.. _compile-chipmunk:

Compile Chipmunk
================

If a compiled binary library of Chipmunk that works on your platform is not 
included in the release you will need to compile Chipmunk yourself. Another 
reason to compile chipmunk is if you want to run it in release mode to get 
rid of the debug prints it generates. If you just use pip install the 
compilation will happen automatically given that a compiler is available. You 
can also specifically compile Chipmunk as described below.

To compile Chipmunk::

    > python setup.py build_ext 

If you got the source and just want to use it directly you probably want to 
compile Chipmunk in-place, that way the output is put directly into the correct
place in the source folder::

    > python setup.py build_ext --inplace

On Windows you will need to use a gcc-compatible compiler. The pre-built version
distributed with pymunk were compiled with the MinGW-w64 GCC compiler at 
https://www.msys2.org/
  
.. seealso:: 

    Module :py:mod:`pymunkoptions` 
        Options module that control runtime options of Pymunk such as debug 
        settings. Use pymunkoptions together with release mode compilation to 
        remove all debugs prints.


CFFI Installation
=================

Sometimes you need to manually install the (non-python) dependencies of CFFI. 
Usually you will notice this as a installation failure when pip tries to 
install CFFI since CFFI is a dependency of Pymunk. This is not really part of 
Pymunk, but a brief description is available for your convenience. 

You need to install two extra dependencies for CFFI to install properly. This 
can be handled by the package manager. The dependencies are `python-dev` and 
`libffi-dev`. Note that they might have slightly different names depending on 
the distribution, this is for Debian/Ubuntu. Just install them the normal way, 
for example like this if you use apt and Pip should be able to install CFFI 
properly::

    > sudo apt-get install python-dev libffi-dev
