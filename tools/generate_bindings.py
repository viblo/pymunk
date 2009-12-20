import sys, re
from os.path import abspath, join
from optparse import OptionParser
from ctypeslib import h2xml
from ctypeslib import xml2py

default_path_to_chipmunk_include = join("..","chipmunk_src")
default_output = join("..", "pymunk", "_chipmunk.py")
default_path_to_chipmunk_lib = join("..", "pymunk", "chipmunk.dll")
def main(argv=None):
    """A small script which runs h2xml, xml2py (from ctypeslib) and then does 
    basic replacements.
    """
    if argv is None:
        argv = sys.argv
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-i"
                        ,dest="chipmunk_includes"
                        ,help="path to chipmunk include files (if not specified, '" + default_path_to_chipmunk_include + "' will be used)"
                        ,default=default_path_to_chipmunk_include
                        )
    
    parser.add_option("-o"
                        ,dest="output"
                        ,help="output filename (if not specified, '" + default_output + "' will be used)"
                        ,default=default_output
                        )

    parser.add_option("-l"
                        ,dest="lib"
                        ,help="chipmunk library path (if not specified, '" + default_path_to_chipmunk_lib + "' will be used)"
                        ,default=default_path_to_chipmunk_lib
                        )
                        
    options, files = parser.parse_args(argv[1:])
        
    h2xml_args = [""
                    , abspath( join(options.chipmunk_includes, "chipmunk.h") )
                    , abspath( join(options.chipmunk_includes, "chipmunk_unsafe.h") )
                    ,"-c" 
                    ,"-o", "chipmunk.xml"]

    h2xml.main(h2xml_args)
    print("h2xml done")

    xml2py_args = ["generate_bindings.py"
                    ,"-l", options.lib
                    ,"-o", options.output
                    ,"chipmunk.xml"]
    
    xml2py.main(argv = xml2py_args)
    print("xml2py done")

    custom_head = """
from ctypes import * 
from vec2d import Vec2d
cpVect = Vec2d

from libload import load_library, platform_specific_functions
_lib_debug = True #Set to True to print the Chipmunk path.
chipmunk_lib = load_library("chipmunk", print_path=_lib_debug)
function_pointer = platform_specific_functions()['function_pointer']
"""

    chipmunkpy = open(options.output, 'r').read()

    # change head, remove cpVect, and replace _libraries index with chipmunk_lib
    # also change to use the platform specific function pointer
    head_match = re.compile(r"from.*?\)", re.DOTALL)
    cpVect_classdef_match = re.compile(r"class cpVect.*?pass", re.DOTALL)
    cpVect_fields_match = re.compile(r"cpVect._fields_.*?]", re.DOTALL)
    lib_match = re.compile(r"_libraries.*?]")
    function_pointer_cdecl = re.compile(r"CFUNCTYPE", re.DOTALL)
    function_pointer_stddecl = re.compile(r"WINFUNCTYPE", re.DOTALL)
    
    chipmunkpy = head_match.sub(custom_head, chipmunkpy)
    chipmunkpy = cpVect_classdef_match.sub("#cpVect class def removed", chipmunkpy)
    chipmunkpy = cpVect_fields_match.sub("#cpVect _fields_ def removed", chipmunkpy)
    chipmunkpy = lib_match.sub("chipmunk_lib", chipmunkpy)
    chipmunkpy = function_pointer_cdecl.sub("function_pointer", chipmunkpy)
    chipmunkpy = function_pointer_stddecl.sub("function_pointer", chipmunkpy)
    f = open(options.output, 'w').write(chipmunkpy)
    print("replacement done")

if __name__ == "__main__":
    sys.exit(main())

