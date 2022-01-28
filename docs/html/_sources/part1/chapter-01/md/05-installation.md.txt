---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Installation and setup

In order to be able to follow and reproduce the examples in the rest of the book, here we present some information about how to install Python on your own computer along with all of the recommended software libraries we use. This is not strictly necessary, as it is possible to use the Binder cloud computing platform from [the book website](https://pythongis.org/) to interact with the book materials. However, if you would like to get the most out of the book and ensure you're easily able to continue with Python afterward, we strongly recommend you install Python and Jupyter on your own computer.

In the sections that follow, we provide instructions for the installation of the Python using [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for the Windows, macOS, and Linux operating systems. Miniconda is a lightweight installer for Python packages that includes a minimal Python environment. You should first install Miniconda and then you can use the a [Python environment file we provide]() to set up a Python environment with all of the software libraries used in this book. We provide instructions for both steps below.


## Which Python version to install?

This book assumes you are using **Python 3**, so for all operating systems we recommend you install Miniconda based on Python 3. At the time of writing of this book, Python 3.8 is the Python version that is recommended (e.g., Figure 1.12), however future versions of Python 3.X should also be suitable. Importantly, the coding examples we present will not work with Python 2.X, so be careful to install the correct version of Miniconda!


## Windows


### Installing Miniconda

To get started, you should first download the version of Miniconda based on Python 3 that is suitable for your computer. Most likely you should choose the 64-bit installer, though those using a 32-bit operating systems should download the 32-bit version.

![_**Figure 1.12**. Miniconda versions available for Windows.](../img/miniconda-windows.png)

_**Figure 1.12**. Miniconda versions available for Windows._

Once you have downloaded the installer, double click on the installer file to install it. You can use the default options, but be aware of the installation types below.

- Single-user installation: Select "**Just Me**" during the installation and Miniconda will only be available for the current user. This should not require administrator rights for the installation.
- System-wide installation: Select "**All Users**" during the installation. This will require administrator rights.

After the installation has completed you can test that the `conda` package manager works by opening the Anaconda Prompt from the Start menu and running a command such as `conda --version`. If the command returns a version number of conda (e.g. `conda 4.9.0`) then everything is working correctly.

You can find some additional tips on installing Miniconda for Windows on the [Miniconda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).


### Setting up your Python environment

There are three steps to install the software libraries needed in this book.

1. Download a copy of our Python environment configuration file `python-gis-book.yml` that is available on the book website at [WEBSITE]().

2. Once you have downloaded the environment file you need, you can install it at the Anaconda Prompt by typing

    ```bash
    $ conda env create -f python-gis-book.yml
    ```

    This will create the Python environment by installing the required software. Please note that the downloaded file should be in the same directory where the Anaconda Prompt is running, and that the installation may take some time.
   
3. Finally, you can activate the new Python environment by typing

    ```bash
    $ conda activate python-gis-book
    ```

    in the Anaconda Prompt. You should now have all of the software needed to proceed with the book.


## macOS


### Installing Miniconda

We recommend downloading the version of Miniconda that offers installation using a graphical installer (e.g., `Miniconda MacOSX 64-bit pkg`), and make sure you download the Python 3 package (Figure 1.13).

![_**Figure 1.13**. Miniconda versions available for macOS.](../img/miniconda-macos.png)

_**Figure 1.13**. Miniconda versions available for macOS._

Once you have downloaded the installer, double click on the installer file to install it. You can use the default options, but be aware of the installation types below.

- Single-user installation: Select "**Just Me**" during the installation and Miniconda will only be available for the current user. This should not require administrator rights for the installation.
- System-wide installation: Select "**All Users**" during the installation. This will require administrator rights.

After the installation has completed you can test that the `conda` package manager works by opening Terminal or the Anaconda Prompt and running a command such as `conda --version`. If the command returns a version number of conda (e.g. `conda 4.9.0`) then everything is working correctly.

In case you have any problems with the Miniconda installation, you can find some installation tips on the [Miniconda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html).


### Setting up your Python environment

There are three steps to install the software libraries needed in this book.

1. Download a copy of our Python environment configuration file `python-gis-book.yml` that is available on the book website at [WEBSITE]().

2. Once you have downloaded the environment file you need, you can install it using Terminal or the Anaconda Prompt by typing

    ```bash
    $ conda env create -f python-gis-book.yml
    ```

    This will create the Python environment by installing the required software. Please note that the downloaded file should be in the same directory where the Anaconda Prompt is running, and that the installation may take some time.
   
3. Finally, you can activate the new Python environment by typing

    ```bash
    $ conda activate python-gis-book
    ```

    in the Anaconda Prompt. You should now have all of the software needed to proceed with the book.


## Linux


### Installing Miniconda

Start by downloading the Miniconda installer for Linux from the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) (Figure 1.14). Be sure you download the Python 3 package.

![_**Figure 1.14**. Miniconda versions available for Linux.](../img/miniconda-linux.png)

_**Figure 1.14**. Miniconda versions available for Linux._

Once you have downloaded the installer, you can open a terminal window and type a command to start the installation. You should use the default installer options, but be aware that the command you run will differ depending on the installation type.

- Single-user installation: Start by running the following:

    ```bash
    $ bash Miniconda3-latest-Linux-x86_64.sh
    ```

   Miniconda will only be available for the current user and the installation directory must be a location where that user has write permissions. This should not require administrator rights for the installation.

- System-wide installation: For a system-wide install, run:

    ```bash
    $ sudo bash Miniconda3-latest-Linux-x86_64.sh
    ```

    You will be propted for your password and must have administrator rights to install this way.

After the installation has completed you can test that the `conda` package manager works by opening a terminal and running a command such as `conda --version`. If the command returns a version number of conda (e.g. `conda 4.9.0`) then everything is working correctly.

In case you have any problems with the Miniconda installation, you can find some installation tips on the [Miniconda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).


### Setting up your Python environment

There are three steps to install the software libraries needed in this book.

1. Download a copy of our Python environment configuration file `python-gis-book.yml` that is available on the book website at [WEBSITE]().

2. Once you have downloaded the environment file you need, you can install it using a terminal by typing

    ```bash
    $ conda env create -f python-gis-book.yml
    ```

    This will create the Python environment by installing the required software. Please note that the downloaded file should be in the same directory where the Anaconda Prompt is running, and that the installation may take some time.
   
3. Finally, you can activate the new Python environment by typing

    ```bash
    $ conda activate python-gis-book
    ```

    in the Anaconda Prompt. You should now have all of the software needed to proceed with the book.
