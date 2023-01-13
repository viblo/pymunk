# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Pymunk"
copyright = "2013-2022, Victor Blomqvist"
author = "Victor Blomqvist"
release = "2.3"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# To allow readthedocs.org build documentation without the chipmunk library file


class Mock(object):
    # __package__ = 'pymunk._chipmunk_cffi_abi'
    def __init__(self, *args, **kwargs):
        # print("init", args, kwargs)
        pass

    def __call__(self, *args, **kwargs):
        # print("call", args, kwargs)
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        # print("getattr", cls, name)
        if name in ("__file__", "__path__"):
            return "/dev/null"
        elif name[0] == name[0].upper():
            return type(name, (), {})
        else:
            return Mock()


MOCK_MODULES = [
    # 'pymunk._chipmunk_cffi',
    #'pymunk._chipmunk_cffi_abi',
    #'_chipmunk_cffi',
    #'_chipmunk_cffi_abi',
    #'._chipmunk_cffi','_chipmunk_cffi',
    "pymunk._chipmunk",
    # "_cffi_backend",
    "matplotlib",
    "matplotlib.pyplot",
    "pygame",
    "pygame.locals",
    "pygame.color",
    "pyglet",
]


class MockFinder(object):
    def find_module(self, fullname, path=None):
        # if "cffi" in fullname:
        #    print("CFFI!!!", fullname, path)
        if fullname in MOCK_MODULES:
            # print("fm: fullname", fullname, self)
            return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        # print("lm: fullname", fullname, self)
        return Mock()


# sys.meta_path.insert(0, MockFinder())

# print(sys.meta_path)

for m in MOCK_MODULES:
    sys.modules[m] = Mock()

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("../.."))

extensions = [  #'sphinx.ext.autodoc',
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "ext.autoexample",
    "aafigure.sphinxext",
]


templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/pymunk_logo_sphinx.png"
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/pymunk_favicon.ico"

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    "**": [
        "badges.html",
        "globaltoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
    ],
}

# -- Other ------------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
    # "member-order": "bysource",
    # "special-members": "__init__, __add__"
    #'exclude-members': '__weakref__'
}