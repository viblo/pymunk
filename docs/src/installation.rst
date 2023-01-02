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

    > python -m pymunk.tests -f test

Sometimes on more uncommon platforms you will need to have a GCC-compatible 
c-compiler installed to install pymunk in case no prebuilt wheel exist. 

On OSX you can install one with::

    > xcode-select --install

On Linux you can install one with the package manager, for example on Ubuntu 
with::

    > sudo apt-get install build-essential


Examples & Documentation
========================

The examples are included in the wheel. Note that some requires additional 
libraries such as pygame or pyglet. To list the available examples run::

    > python -m pymunk.examples -l

Then to run an example, for example the breakout example run::

    > python -m pymunk.examples.breakout


Troubleshooting
===============

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


Advanced - Development
======================

For development one convenient way is to install Pymunk in 
editable / development mode. Get the source (i.e. git checkout from Github) 
and then go to the source folder. Then install in pip editable mode::

    > python -m pip install -e .

Note that this requires a suitable c compiler, e.g. Visual Studio on Windows. 
Once installed you should be able to to import pymunk just as any other 
installed library. pymunk should also work just fine with virtualenv in case 
you want it installed in a contained environment.

Remember that if you update Chipmunk (the c code), you will have to recompile 
Chipmunk for the changes to apply. See 

.. _compile-chipmunk:

Compile Chipmunk
================

Pymunk is built on top of the c library Chipmunk. It uses CFFI to interface
with the Chipmunk library file. Because of this Chipmunk has to be compiled
together with Pymunk as an extension module. 

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

On Windows you will need to use Visual Studio matching your Python version. 


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
