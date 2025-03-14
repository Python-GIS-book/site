# PythonGIS book environments

The *Introduction to Python for Geographic Data Analysis* book uses several different Python environments for different purposes. As the environment can be a bit confusing, this document aims to explain the purposes of the different environment files, where they are stored, and how to update the book's Python environment.

## Book building environment for authors

Filename and location: `site/ci/py312-book-building.yaml`

This is the environment file used by the book authors to create book content and locally build copies of the PDF version of the book.

## Website building environment for GitHub Actions

Filename and location: `site/ci/build-website.yaml`

This is the environment file used by GitHub Actions to update the website at <https://pythongis.org>.

## Python environment for book readers

Filename and location: `site/ci/environment.yml`

This is the Python environment file that allows users to create a local Python environment including the necessary versions of all libraries used in the book.

### Future plans

- This file could be generated in the future automatically by parsing the book building environment and removing unneeded libraries (e.g., those used for converting the notebooks to web content).
- It would also be nice to automatically update the version of this file in Allas when it is updated.

## Binder environment

Filename and location: `site/environment.yml`

This Python environment is used by Binder for users interacting with the book content online.

### Future plans

This file could be moved into the `.binder` folder so it is more clear what its purpose is.

## Readthedocs environment

Filename and location: `site/source/requirements.txt` (referenced by `site/.readthedocs.yml`)

This environment file is used for building the web version of the book on <https://readthedocs.org/>.

## PDF book building environment (different repo!)

Filename and location: `book-building/ci/build-book.yaml`

This environment file is used to create a PDF version of the book when updates are pushed to the <https://github.com/Python-GIS-book/book-building> repository.