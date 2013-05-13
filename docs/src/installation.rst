Installation
============
.. _installation:

.. tip::
    You will find the latest version at 
    http://code.google.com/p/pymunk/downloads/list

pymunk does not need to be installed. However, you might need to compile the 
chipmunk library that pymunk uses internally if a precompiled library was not 
included for your platform. The default pymunk distribution ships with at least
32-bit Windows and 32- and 64-bit Linux versions. But even if a compiled 
library is not shipped you should not despair! It is very easy to compile 
chipmunk as long as you have a gcc-compatible c compiler installed. 

.. _without-install:

Without installation
--------------------

You might want to test pymunk before you install it on your development 
machine, or maybe decide to not install it at all. The easiest way to do this 
is to download the source release of pymunk and extract the archive to the 
folder where your code is and then tell python where to find it. 

For example, lets say you have main.py and a folder named pymunk-3.0.0 that 
contain the full source of pymunk (files, including setup.py, README.txt and 
a folder named pymunk). Then you can add this before you include::

    import os, sys

    current_path = os.getcwd()
    sys.path.insert(0, os.path.join( current_path, "pymunk-3.0.0" ) )
    
    import pymunk
    
For a working demo, check out the run.py file in the examples folder of 
pymunk. It uses this exact technique to allow running the examples using the 
pymunk located on level up.

Install pymunk
----------------

pymunk can be installed with pip install::

    > pip install pymunk

Another option is to install pymunk with one of the prebuilt installers if 
available (Windows) or you can use the standard setup.py way::

    > python setup.py install

If you are on Mac OS X or Linux you will probably need to run as a privileged 
user; for example using sudo::
    
    > sudo python setup.py install
    
Once installed you should be able to to import pymunk just as any other 
installed library. pymunk should also work just fine with virtualenv in case 
you want it installed in a contained environment.
    
.. note::
    The setup will not check if the correct Chipmunk library was included or 
    already compiled for you. It might be a good idea to first check that 
    pymunk works before you actually install it. See :ref:`without-install`

.. _compile-chipmunk:

Compile Chipmunk
----------------
If a compiled binary library of Chipmunk that works on your platform is not 
included in the release you will need to compile Chipmunk yourself. Another 
reason to compile chipmunk is if you want to run it in release mode to get 
rid of the debug prints it generates. 

To compile Chipmunk::

    > python setup.py build_chipmunk

On Windows you will need to use a gcc-compatible compiler. The precompiled 
included windows binaries were compiled with a GCC installed from the TDM-GCC 
package http://tdm-gcc.tdragon.net/ To set the compiler use the compiler 
argument::

    > python setup.py build_chipmunk --compiler=mingw32
    
To compile Chipmunk in Release mode use the release argument (Useful to 
avoid some debug prints and asserts)::

    > python setup.py build_chipmunk --release
  
.. seealso:: 

    Module :py:mod:`pymunkoptions` 
        Options module that control runtime options of pymunk such as debug 
        settings. Use pymunkoptions together with release mode compilation to 
        remove all debugs prints.
