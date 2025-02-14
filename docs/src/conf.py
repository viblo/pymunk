# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Pymunk"
copyright = "2013-2025, Victor Blomqvist"
author = "Victor Blomqvist"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


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

# Font
html_theme_options = {
    "font_family": '"Lucida Grande",Arial,sans-serif',
    "head_font_family": '"Lucida Grande",Arial,sans-serif',
}

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

html_js_files = [
    (
        "//gc.zgo.at/count.js",
        {"async": "async", "data-goatcounter": "https://pymunk.goatcounter.com/count"},
    )
]

# -- Other ------------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
    # "member-order": "bysource",
    # "special-members": "__init__, __add__"
    #'exclude-members': '__weakref__'
    "exclude-members": "index, count",
}

autodoc_preserve_defaults = True

autodoc_mock_imports = [
    "_chipmunk_cffi",  # mock to make enums like DYNAMIC be documented properly
    "pymunk._chipmunk",
    "_cffi_backend",
    "matplotlib",
    "matplotlib.pyplot",
    "pygame",
    "pygame.locals",
    "pygame.color",
    "pyglet",
]
