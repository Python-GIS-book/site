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

# Pybtex related imports for handling the reference styles
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.labels import BaseLabelStyle
import pybtex
from collections import Counter

from dataclasses import dataclass, field
import sphinxcontrib.bibtex.plugin

from sphinxcontrib.bibtex.style.referencing import BracketStyle
from sphinxcontrib.bibtex.style.referencing.author_year import AuthorYearReferenceStyle

# -- Project information -----------------------------------------------------
import time

current_year = time.localtime().tm_year

project = "Introduction to Python for Geographic Data Analysis"
copyright = f"2020-{current_year}, Henrikki Tenkanen, Vuokko Heikinheimo, David Whipp"
author = "Henrikki Tenkanen, Vuokko Heikinheimo, David Whipp"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinxcontrib.bibtex",
    "sphinx_thebe",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_theme_options = {
    # "external_links": [],
    "repository_url": "https://github.com/Python-GIS-book/site/",
    # "twitter_url": "https://twitter.com/pythongis",
    "google_analytics_id": "UA-159257488-1",
    "use_edit_page_button": True,
    "path_to_docs": "source/",
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "thebe": True,
        "notebook_interface": "jupyterlab",
    },
}

html_context = {"default_mode": "light"}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Hide title in left navbar
html_title = ""

# Do not execute cells
nb_execution_mode = "off"

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
    "css/custom-toggle-button.css",
    "css/custom-text-formatting.css",
]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/pythongis-logo.png"

# Add specification for master-doc
# Relates to RTD issue: https://github.com/readthedocs/readthedocs.org/issues/2569
master_doc = "index"

# LaTex conf
# Grouping the document tree into LaTeX files. List of tuples# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    (
        "index",
        "introductiontopythonforgeographicdataanalysis.tex",
        "Introduction to Python for Geographic Data Analysis",
        "Henrikki Tenkanen, Vuokko Heikinheimo and David Whipp",
        "krantz",
    ),
]

latex_additional_files = ["krantz/krantz.cls"]

# Latex elements
latex_elements = {"preamble": r"\usepackage{svg}"}

# ======================
# Bibtex configuration
# ======================

# ---------------------------------------
# Customizing reference list style (APA)
# ---------------------------------------
# Ref: https://github.com/mcmtroffaes/sphinxcontrib-bibtex/issues/201


class APALabelStyle(BaseLabelStyle):
    def format_labels(self, sorted_entries):
        labels = [self.format_label(entry) for entry in sorted_entries]
        count = Counter(labels)
        counted = Counter()
        for label in labels:
            if count[label] == 1:
                yield label
            else:
                yield label + chr(ord("a") + counted[label])
                counted.update([label])

    def format_label(self, entry):
        if entry.type == "book" or entry.type == "inbook":
            label = self.author_editor_key_label(entry)
        elif entry.type == "proceedings":
            label = self.editor_key_organization_label(entry)
        elif entry.type == "manual":
            label = self.author_key_organization_label(entry)
        else:
            label = self.author_key_label(entry)
        if "year" in entry.fields:
            return f"{label}, {entry.fields['year']}"
        else:
            return label

    def author_key_label(self, entry):
        # see alpha.bst author.key.label
        if not "author" in entry.persons:
            if not "key" in entry.fields:
                return entry.key[:3]  # entry.key is bst cite$
            else:
                # for entry.key, bst actually uses text.prefix$
                return entry.fields["key"][:3]
        else:
            return self.format_lab_names(entry.persons["author"])

    def author_editor_key_label(self, entry):
        # see alpha.bst author.editor.key.label
        if not "author" in entry.persons:
            if not "editor" in entry.persons:
                if not "key" in entry.fields:
                    return entry.key[:3]  # entry.key is bst cite$
                else:
                    # for entry.key, bst actually uses text.prefix$
                    return entry.fields["key"][:3]
            else:
                return self.format_lab_names(entry.persons["editor"])
        else:
            return self.format_lab_names(entry.persons["author"])

    def author_key_organization_label(self, entry):
        if not "author" in entry.persons:
            if not "key" in entry.fields:
                if not "organization" in entry.fields:
                    return entry.key[:3]  # entry.key is bst cite$
                else:
                    result = entry.fields["organization"]
                    if result.startswith("The "):
                        result = result[4:]
                    return result
            else:
                return entry.fields["key"][:3]
        else:
            return self.format_lab_names(entry.persons["author"])

    def editor_key_organization_label(self, entry):
        if not "editor" in entry.persons:
            if not "key" in entry.fields:
                if not "organization" in entry.fields:
                    return entry.key[:3]  # entry.key is bst cite$
                else:
                    result = entry.fields["organization"]
                    if result.startswith("The "):
                        result = result[4:]
                    return result
            else:
                return entry.fields["key"][:3]
        else:
            return self.format_lab_names(entry.persons["editor"])

    def format_lab_names(self, persons):
        name_cnt = len(persons)
        if name_cnt == 0:
            return ""

        elif name_cnt == 1:
            person = persons[0]
            person = person.prelast_names + person.last_names
            return " ".join(person)

        # "Name-1 & Name-2" -style
        elif name_cnt == 2:
            p1, p2 = persons[:2]
            person1 = p1.prelast_names + p1.last_names
            person1 = " ".join(person1)
            person2 = p2.prelast_names + p2.last_names
            person2 = " ".join(person2)
            return f"{person1} & {person2}"

        # "Lead-author et al." -style
        else:
            person = persons[0]
            person = person.prelast_names + person.last_names
            person = " ".join(person)
            return f"{person} et al."


class APAStyle(UnsrtStyle):
    default_label_style = APALabelStyle


# Register the plugin that controls how the Reference list will look like
pybtex.plugin.register_plugin("pybtex.style.formatting", "apa", APAStyle)

# -----------------------------------
# Customize the citation formatting:
# Use parentheses when citing
# -----------------------------------


def my_bracket_style() -> BracketStyle:
    return BracketStyle(
        left="",
        right="",
    )


@dataclass
class MyReferenceStyle(AuthorYearReferenceStyle):
    bracket_parenthetical: BracketStyle = field(default_factory=my_bracket_style)
    bracket_textual: BracketStyle = field(default_factory=my_bracket_style)
    bracket_author: BracketStyle = field(default_factory=my_bracket_style)
    bracket_label: BracketStyle = field(default_factory=my_bracket_style)
    bracket_year: BracketStyle = field(default_factory=my_bracket_style)


# Register the changes
sphinxcontrib.bibtex.plugin.register_plugin(
    "sphinxcontrib.bibtex.style.referencing",
    "author_year_no_brackets",
    MyReferenceStyle,
)

# Style which will be applied when citing (as part of the text)
bibtex_reference_style = "author_year_no_brackets"

# Files containing the bibliography info
bibtex_bibfiles = [
    # "part1/chapter-01/chapter-01-references.bib",
    # "part1/chapter-02/chapter-02-references.bib",
    # "part1/chapter-03/chapter-03-references.bib",
    "back-matter/references.bib",
]

# Specify what text is used with toggle-buttons
togglebutton_hint = "Show the solution"

# Add math config options for new version of MyST
myst_enable_extensions = ["dollarmath"]

# Include extra files not directly related to the documentation
html_extra_path = ["install.html"]
