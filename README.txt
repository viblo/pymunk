== pymunk ==
A python wrapper for the 2d physics library Chipmunk
2007 - 2008, Victor Blomqvist - vb@viblo.se

ABOUT
pymunk is a wrapper around the 2d physics library Chipmunk, 
http://wiki.slembcke.net/main/published/Chipmunk

HOW TO USE
Currently there are no documentation except this readme, the included
demo file(s) and the chipmunk documentation found here:
http://files.slembcke.net/chipmunk/chipmunk-docs.html

EXAMPLE
-

DEPENDENCIES/REQUIREMENTS
* A dynamic lib of Chipmunk
* ctypes (included in python 2.5)
* pygame (optional, you need it to run the demo)
* ctypeslib & GCC_XML (optional, you need them to generate new bindings)

A compiled windows dll of Chipmunk compatible with pymunk is available at 
http://pymunk.googlecode.com/ 
You can also compile a dll or *NIX/OSX version of chipmunk on you own.
Download the source of Chipmunk and follow the instructions. :)

OTHER

HOW TO GENERATE BINDINGS
You will need the ctypes code generator, it is part of the ctypeslib 
package. You will also need GCC_XML.
See the ctypes wiki for instructions on how to set it up:
http://starship.python.net/crew/theller/wiki/CodeGenerator
When ctypeslib (h2xml and xml2py) and gcc_xml is installed then run

>python generate_bindings.py
(use --help to display options, you will most probably want to 
change the include path and possibly the lib path)

you have now created a _chipmunk.py file with generated bindings.
