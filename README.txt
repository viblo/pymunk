== pymunk ==

ABOUT

    pymunk is a python wrapper for the 2d physics library Chipmunk
    2007 - 2008, Victor Blomqvist - vb@viblo.se, MIT License

    This dev release is based on the latest pymunk release (0.6.1), 
    using chipmunk-4.0.2 (also latest, source included)
    
	IRC: #pymunk on irc.freenode.net
    Homepage: http://pymunk.googlecode.com/
    Forum: http://www.slembcke.net/forums/viewforum.php?f=6
	
    Getting the latest SVN copy:
      svn checkout http://pymunk.googlecode.com/svn/trunk pymunk-read-only

    Chipmunk: http://wiki.slembcke.net/main/published/Chipmunk

HOW TO USE

    Currently is only little documentation except this readme and the demos.
    There are also a few tutorials on the googlecode page and in the forum.
    
    One easy way to get started is to check out the examples/ directory,
    and run 'python demo_contact.py' and so on, and see what it does :)

EXAMPLE

    See the included demos (in examples/)

DEPENDENCIES/REQUIREMENTS

    * ctypes (included in python 2.5)
    * python 2.5 (optional, used by the pymunk.util module)
    * pygame (optional, you need it to run most of the demos)
    * pyglet (optional, you need it to run the moon buggy demo)
    * ctypeslib & GCC_XML (optional, you need them to generate new bindings)
    * Pymunk ships with a set of chipmunk libraries (for win, linux32/64 bit and osx)

CHIPMUNK

    Compiled libraries of Chipmunk compatible Windows, Linux and Mac OSX are distributed
    with pymunk, a windows library is also available at http://pymunk.googlecode.com/.
    The chipmunk source is included and can easily be compiled by hand. A how-to can be 
    found in chipmunk_src/README.txt

HOW TO GENERATE BINDINGS
(optional -- if you want to experiment :)

    You will need the ctypes code generator, it is part of the ctypeslib 
    package. You will also need GCC_XML. See the ctypes wiki for instructions
    on how to set it up: http://starship.python.net/crew/theller/wiki/CodeGenerator
    When ctypeslib (h2xml and xml2py) and gcc_xml is installed then run

        >python generate_bindings.py

    (use --help to display options, you will most probably want to change the include
    path and possibly the lib path) you have now created a _chipmunk.py file with
    generated bindings.

