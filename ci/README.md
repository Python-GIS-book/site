# PythonGIS book environments

The *Introduction to Python for Geographic Data Analysis* book uses several different Python environments for different purposes. As the environment can be a bit confusing, this document aims to explain the purposes of the different environment files, where they are stored, and how to update the book's Python environment.

## Book building environment for authors

Filename and location: `site/ci/py312-book-building.yaml`

This is the environment file used by the book authors to create book content and locally build copies of the PDF version of the book.

Last updated: 15.3.2025.

## Website building environment for GitHub Actions

Filename and location: `site/ci/build-website.yaml`

This is the environment file used by GitHub Actions to update the website at <https://pythongis.org>.

Last updated: 15.3.2025.

## Python environment for book readers

Filename and location: `site/ci/environment.yml`

This is the Python environment file that allows users to create a local Python environment including the necessary versions of all libraries used in the book.
Automatically updated by running the Python script `update_environment.py`.

### Updating the build environment on the CSC Allas system

The book users can access the book environment file at https://pythongis.org/environment.
The environment file can be automatically updated by setting the parameter `upload=True` in the `copy_env_to_allas()` function in the `update_environment.py` script file. Instructions for creating the connection to the CSC Allas system, which is necessary to do the update, can be found at https://docs.csc.fi/data/Allas/using_allas/python_boto3/. The associated CSC project is `project_2005859`.

## Binder environment

Filename and location: `site/binder/environment.yml`

This Python environment is used by Binder for users interacting with the book content online.
Automatically updated by running the Python script `update_environment.py`.

Last updated: 15.3.2025.

## Readthedocs environment

Filename and location: `site/readthedocs/requirements.txt` (referenced by `site/.readthedocs.yml`)

This environment file is used for building the web version of the book on <https://readthedocs.org/>.

Last updated: 15.3.2025.

## PDF book building environment (different repo!)

Filename and location: `book-building/ci/build-book.yaml`

This environment file is used to create a PDF version of the book when updates are pushed to the <https://github.com/Python-GIS-book/book-building> repository.

Last updated: 15.3.2025.