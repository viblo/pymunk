# ----------------------------------------------------------------------------
# Copyright (c) 2007-2025 Victor Blomqvist
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

__docformat__ = "reStructuredText"

import ast
import os
from typing import Any, List, Optional

import sphinx.application
from docutils import statemachine, utils
from docutils.parsers.rst import Directive, directives


def setup(app: sphinx.application.Sphinx) -> None:
    app.add_directive("autoexample", AutoExampleDirective)


def parse_example(
    basepath: str,
    filename: str,
    img_folder: Optional[str],
    img_folder_os: Optional[str],
    source_url: str,
) -> List[str]:
    path = os.path.join(basepath, filename)
    with open(path) as f:
        content = f.read().strip()
    n = ast.parse(content)
    docstring = ast.get_docstring(n)
    if docstring is None:
        return []

    s = []

    # Header
    s.append(".. _" + filename + ":")
    s.append("")
    header = filename
    s += [header, "".ljust(len(header), "-")]

    # Location
    folder = os.path.basename(basepath)
    s.append("Source: `%s/%s <%s/%s>`_" % (folder, filename, source_url, filename))

    # Docstring
    s.append("")
    s.append(docstring)
    s.append("")

    # Screenshot
    img_name, _ = os.path.splitext(filename)
    img_name += ".png"
    if img_folder is not None and img_folder_os is not None:
        # print os.path.abspath(img_folder)
        # print os.path.abspath(img_folder_os)
        img_path = os.path.join(img_folder, img_name)
        img_path_os = os.path.join(img_folder_os, img_name)
        # img_path = os.path.join("../", img_path)
        img_path = img_path.replace("\\", "/")
        if os.path.isfile(img_path_os):
            s.append("")
            s.append(".. image:: " + img_path)
            s.append("")

    s.append("")
    return s


def parse_folder_example(
    basepath: str,
    foldername: str,
    img_folder: Optional[str],
    img_folder_os: Optional[str],
    source_url: str,
) -> List[str]:
    path = os.path.join(basepath, foldername, "main.py")
    if not os.path.isfile(path):
        return []
    with open(path) as f:
        content = f.read().strip()
    n = ast.parse(content)
    docstring = ast.get_docstring(n)
    if docstring is None:
        return []

    s = []

    # Header
    s.append(".. _" + foldername + ":")
    s.append("")
    header = foldername
    s += [header, "".ljust(len(header), "-")]

    # Location
    folder = os.path.basename(basepath)
    s.append("Source: `%s/%s <%s/%s>`_" % (folder, foldername, source_url, foldername))

    # Docstring
    s.append("")
    s.append(docstring)
    s.append("")

    # Screenshot
    img_name, _ = os.path.splitext(foldername)
    img_name += ".png"
    if img_folder is not None and img_folder_os is not None:
        # print os.path.abspath(img_folder)
        # print os.path.abspath(img_folder_os)
        img_path = os.path.join(img_folder, img_name)
        img_path_os = os.path.join(img_folder_os, img_name)
        img_path = img_path.replace("\\", "/")
        if os.path.isfile(img_path_os):
            s.append("")
            s.append(".. image:: " + img_path)
            s.append("")

    s.append("")
    return s


def parse_examples(
    path: str, img_folder: Optional[str], img_folder_os: Optional[str], source_url: str
) -> str:
    lines = []
    print("autoexample: documenting files in " + path)
    # print os.getcwd()

    for name in sorted(os.listdir(path)):
        if name.startswith("__"):
            continue
        fullpath = os.path.join(path, name)
        if os.path.isfile(fullpath):
            _, ext = os.path.splitext(fullpath)
            if ext != ".py":
                continue
            print("autoexample: documenting " + name)
            lines += parse_example(path, name, img_folder, img_folder_os, source_url)
        elif os.path.isdir(fullpath):
            print("autoexample: documenting folder " + name)
            lines += parse_folder_example(
                path, name, img_folder, img_folder_os, source_url
            )
    return "\n".join(lines)


class AutoExampleDirective(Directive):
    # this enables content in the directive
    # has_content = True
    required_arguments = 1
    option_spec = {
        "image_folder": str,
        "source_url": str,
    }

    def run(self) -> List[Any]:
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1
        )
        source_dir = os.path.dirname(os.path.abspath(source))
        path = directives.path(self.arguments[0])
        path = os.path.normpath(os.path.join(source_dir, path))

        path = utils.relative_path(None, path)
        img_folder = None
        img_folder_os = None
        if "image_folder" in self.options:
            # This is extremly messy..
            # To be able to test if file exist in path we need to use img_path_os
            # But that cannot be used for the .. image:: tag, instead we need to use the raw option!
            img_folder_os = os.path.normpath(
                os.path.join(source_dir, self.options["image_folder"])
            )
            img_folder = self.options["image_folder"]
        rawtext = parse_examples(
            path, img_folder, img_folder_os, self.options["source_url"]
        )

        include_lines = statemachine.string2lines(
            rawtext, self.state.document.settings.tab_width, convert_whitespace=True
        )

        self.state_machine.insert_input(include_lines, path)
        return []
