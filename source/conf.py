# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Introduction to Python for Geographic Data Analysis'
copyright = '2020, Henrikki Tenkanen, Vuokko Heikinheimo, and David Whipp'
author = 'Henrikki Tenkanen, Vuokko Heikinheimo, and David Whipp'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.githubpages',
    #'jupyter_sphinx.execute',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'

html_theme_options = {
    #"external_links": [],
    "repository_url": "https://github.com/Python-GIS-book/site/",
    #"twitter_url": "https://twitter.com/pythongis",
    #"google_analytics_id": "UA-159257488-1",
    "use_edit_page_button": True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org/v2/gh/Python-GIS-book/site/master",
        "thebelab": True,
        "notebook_interface": "jupyterlab",
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for nbsphinx --
nbsphinx_allow_errors = True


# -- Options for Jupyter-Sphinx --
# jupyter_sphinx_thebelab_config = {
#     'requestKernel': True,
#     'binderOptions': {
#         'repo': "binder-examples/requirements",
#     },
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/pythongis.css",
]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/pythongis-logo.png"

# Add specification for master-doc
# Relates to RTD issue: https://github.com/readthedocs/readthedocs.org/issues/2569
master_doc = 'index'
