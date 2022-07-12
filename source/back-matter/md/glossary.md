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

# Glossary

```{glossary}
Collection
  A group of data types known as containers, where multiple values can be stored together. The built-in container data types in Python are dictionary, list, set, and tuple.

Computer
  We use the definition of a computer given by {cite}`Zelle2017`: "A machine that stores and manipulates information under the control of a changeable program."
  
Data model
  A data model is an conceptual (abstract) model that shows how elements of data are organized and how they relate to one another in a standardized manner and how the data relate to properties of real-world entities. Examples of data models are e.g. vector data model consisting of points, lines and areas; and raster data model constituted of a grid-like structure that hold the values for each grid cell.    

Data type
  An attribute defining the characteristics of a value in a program.
  For example, type `int` is an integer (whole number).
  
DateOffsets
  A specific pandas object that represents a duration of time following calendar duration rules, such as a week ("W"). 
  
DatetimeIndex
  An immutable array of datetime64 data that is specified as the index of the DataFrame. Can be used for indexing and grouping data based on time.
  
Dependency
  Python packages are often linked to other Python libraries. These other packages (i.e. dependencies) are typically needed to be installed for a given Python package to work. 

Docstring
  A text string used to document a section of code.
  Docstrings are frequently used for functions to describe what the function does as well as providing information about input parameters and function outputs.
  You are encouraged to create docstrings when making functions as they can be used with the Python help function to show users how functions work.

Function
  A reusable piece of code that performs a single action.
  
IDE
  See `{term}Integrated Development Environment`.

Index
  A number indicating the location of a specific value stored in Python lists or tuples. The first index value of list is always 0.
  
Integrated Development Environment
  An integrated development environment or IDE is a software program or package that provides a set of tools for writing, testing, and debugging software in a convenient, practical interface
  
Interpreter
  An interpreter is a computer program that is used to execute program instructions written in Python (or other languages). The interpreter reads your statements of code and based on these instructions actually does the work that has been assigned to it. 

Jupyter Notebook
  A web application that allows users to combine rich-formtted text with code cells in an interactive document.
  Jupyter Notebooks can contain nicely formatted text, equations, images, interactive visualizations, and more.
  More information can be found at <https://jupyter.org/>.

Library
  A group of related modules. See definition of a *{term}`module`*.

List
  A data type in Python that can be used to store collections of values. Values in Python lists can be added, removed, or modified, and the list items do not need to be the same data types. Python lists are enclosed in square brackets (`[` `]`) and list items are separated by commas.

Loop
  A programming construct that allows a section of code to be repeated a finite number of times or until a given condition is met.

Markdown
  A lightweight markup language used to convert plain text input to rich-formatted output.
  Markdown can, for example, be used to create simple documentation with different heading levels, text in bold and/or italics, text in lists, or documentation that includes hyperlinks.
  More information can be found at <https://en.wikipedia.org/wiki/Markdown>.

Module
  A file containing Python definitions and statements. Module files have the ``.py`` file extension.

Program
  A detailed list of step-by-step instructions that tell the computer exactly what to do.
  
Programming language
  A set of exact and unambiguous instructions that can be understood by the computer.

Script
  A Python script is a collection of commands in a file that can be executed like a program. 

Semantics
  The exact meaning of a component in a programming language, such as a statement or a function. For example, the `len()` function in Python is used to determine the length of a data structure that is defined in memory.

Software
  Another name for a {term}`program`.

Spatial resolution
  The spatial resolution of a raster refers typically to the size of the cells in a raster dataset. It can also mean the ratio of screen pixels to image pixels at the current map scale. 
  
Spatio-temporal data model
  A data model that incorporates time (t) as an additional dimension to the geographical dimension (x, y). 

Subplots
  The term used in Matplotlib to refer to individual plots when more than one plot is part of a single figure.

Syntax
  The precise form of a component in a programming language. For example, the print function in Python expects the syntax `print('hello')` in order to have the word hello displayed on the screen.
  
Tuple
  [Tuple](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) is a Python data structure that consists of a number of values separated by commas. Coordinate pairs are often represented as a tuple, such as: `(60.192059, 24.945831)`. Tuples belong to [sequence data types](https://docs.python.org/3/library/stdtypes.html#typesseq) in Python. Other sequence data types are lists and ranges. Tuples have many similarities with lists and ranges, but they are often used for different purposes. The main difference between tuples and lists is that tuples are [immutable](https://docs.python.org/3/glossary.html#term-immutable), which means that the contents of a tuple cannot be altered (while lists are mutable; you can, for example, add and remove values from lists).

Variable
  A way of storing values in the memory of the computer using specific names that you define.
  
Virtual environment
  A virtual environment is a Python programming environment which works in a way that the Python interpreter, libraries and scripts installed into it are isolated from the ones installed in other virtual environments, as well as from (possible) system Python, i.e., one which is installed as part of your operating system.
  
Well-known binary
  Well-known binary (WKB) is a format for representing vector geometry objects in compressed binary format which is useful for computer processing. The human-readable equivalent for WKB is `Well-known text` format. WKB can represent various geometric objects: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, Triangle, PolyhedralSurface, TIN (Triangulated irregular network) and GeometryCollection. Coordinates for the geometries can be represented in 2D, 3D or 4D (x,y,z,m).

Well-known text
  Well-known text (WKT) is a text markup language for representing vector geometry objects. WKT can represent various geometric objects: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, Triangle, PolyhedralSurface, TIN (Triangulated irregular network) and GeometryCollection. Coordinates for the geometries can be represented in 2D, 3D or 4D (x,y,z,m). The binary equivalent for WKT is `Well-known binary` format.

  
```
