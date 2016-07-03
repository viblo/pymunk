Installation
============
.. _installation:

.. tip::
    You will find the latest released version at pypi:  
    https://pypi.python.org/pypi/pymunk

Install pymunk
----------------

pymunk can be installed with pip install::

    > pip install pymunk

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
    

.. _compile-chipmunk:

Compile Chipmunk
----------------
If a compiled binary library of Chipmunk that works on your platform is not 
included in the release you will need to compile Chipmunk yourself. Another 
reason to compile chipmunk is if you want to run it in release mode to get 
rid of the debug prints it generates. 

To compile Chipmunk::

    > python setup.py build_ext 

If you got the source and just want to use it directly you probably want to 
compile Chipmunk inplace, that way the output is put directly into the correct
place in the source folder::

    > python setup.py build_ext --inplace

On Windows you will need to use a gcc-compatible compiler. The prebuilt version
distributed with pymunk were compiled with the mingwpy GCC compiler at 
https://mingwpy.github.io/ 
  
.. seealso:: 

    Module :py:mod:`pymunkoptions` 
        Options module that control runtime options of pymunk such as debug 
        settings. Use pymunkoptions together with release mode compilation to 
        remove all debugs prints.
