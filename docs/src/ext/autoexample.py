# ----------------------------------------------------------------------------
# Copyright (c) 2007-2012 Victor Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------

"""This sphinx helper module parse docstrings of python files in a folder and 
put in a document.

It takes a folder and extract the top level docstrings for each .py file 
found. It will also look inside the (optional) image folder for a .png file 
with the same name and if exists add that as an illustration of the python 
file.

Typical use (copied from pymunk examples)::
    
    .. autoexample:: ../../examples
        :image_folder: _static/examples

"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import ast,os
from docutils import nodes, statemachine, utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.nodes import fully_normalize_name

def setup(app):
    app.add_directive('autoexample', AutoExampleDirective)

def parse_example(basepath, filename, img_folder, img_folder_os):
    path = os.path.join(basepath, filename)
    with open(path) as f:
        content = f.read().strip()
    n = ast.parse(content)
    docstring = ast.get_docstring(n)
    if docstring == None:
        return []

    # Header
    s = [filename, "".ljust(len(filename), '-')]
    
    # Location 
    folder = os.path.basename(basepath)
    s.append("Location: *%s/%s*" % (folder, filename))
    
    # Docstring
    s.append("")
    s.append(docstring)
    s.append("")
    
    # Screenshot
    img_name,_ = os.path.splitext(filename)
    img_name += ".png"
    if img_folder != None:
        #print os.path.abspath(img_folder)
        #print os.path.abspath(img_folder_os)
        img_path = os.path.join(img_folder, img_name)
        img_path_os = os.path.join(img_folder_os, img_name)
        if os.path.isfile(img_path_os):
            s.append("")
            s.append(".. image:: " + img_path)
            s.append("")
            
    s.append("")
    return s
    
def parse_examples(path, img_folder, img_folder_os):
    lines = []
    print("autoexample: documenting files in " + path)
    #print os.getcwd()
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            if not os.path.isfile(path):
                continue
            _, ext = os.path.splitext(path)
            if ext != ".py":
                continue
            print("autoexample: documenting " + file)
            lines += parse_example(root, file, img_folder, img_folder_os)

    return "\n".join(lines)
    
class AutoExampleDirective(Directive):
    # this enables content in the directive
    #has_content = True
    required_arguments = 1
    option_spec = {'image_folder': str}
    
    def run(self):
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        path = directives.path(self.arguments[0])
        path = os.path.normpath(os.path.join(source_dir, path))
        
        path = utils.relative_path(None, path)
        path = nodes.reprunicode(path)
        img_folder = None
        img_folder_os = None
        if "image_folder" in self.options:
            # This is extremly messy.. 
            # To be able to test if file exist in path we need to use img_path_os
            # But that cannot be used for the .. image:: tag, instead we need to use the raw option!
            img_folder_os = os.path.normpath(os.path.join(source_dir, self.options["image_folder"]))
            img_folder = self.options["image_folder"]
        rawtext = parse_examples(path, img_folder, img_folder_os)

        include_lines = statemachine.string2lines(rawtext, self.state.document.settings.tab_width,
                                                  convert_whitespace=True)
        
        self.state_machine.insert_input(include_lines, path)
        return []