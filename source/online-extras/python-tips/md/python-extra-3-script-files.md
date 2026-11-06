---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Using Python script files


Though most of the book content focuses on using Jupyter Notebooks, it is not uncommon to use Python script files for data analysis. We introduced using script files in {doc}`Chapter 2.7 </part1/chapter-02/nb/06-writing-scripts.ipynb>` and here we expand on that with some tips about how to format script files for improved readability and features you may want to include in your script files. In addition, we briefly comment on how to produce command-line interfaces for Python software you may develop.


# GCP 4 - Writing our scripts the "right" way

The script example for functions we have seen so far works, but one of the big advantages of using scripts is including features that make the code easier to read and understand.
These include comments in the code that explain what the code does, but are not executed when the code is run.
As your scripts get longer and more complicated, features such as comments will become essential.
Below are some suggestions to make sure your code is formatted nicely and easy to understand.

Note that we also suggest you follow [the PEP 8 Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

<!-- #region -->
## Inline comments

Inline comments are comments within the code that explain what certain lines of the code do.
To you, it may seem obvious how the code works, but if you share it with another person perhaps they will not feel the same way.
This is particularly true when you start using scripts instead of Jupyter notebooks, where you might not feel you can include as much text describing your code.
Because we want to teach you to code in an effective way, it is a very good idea to make your scripts as easy to read as possible for people.
Consider the example below.

```python
# Finnish Meterological Institute observation station name and location data
# Station name for the station in Kaivopuisto, Helsinki, Finland
stationName = 'Helsinki Kaivopuisto'
# Station latitude and longitude - Latitude is north, longitude is east
stationLat = 60.15
stationLong = 24.96
# Print station name and location to the screen
print("The", stationName, "station is located at", stationLat, "N,", stationLong, "E")
```

Here, we have provided a a bit more information about the data in this script by adding inline comments.
Inline comments begin with a `#` (number sign or hash), and all characters that follow on that line will be ignored by Python.
Adding comments to scripts is essential for scientists like ourselves to both help us remember how a script works and to make it easier to share with colleagues.
It is best to get into the habit of adding comments as you write, especially if you're not using a Jupyter notebook.
<!-- #endregion -->

<!-- #region -->
## Use line breaks wisely

*Line breaks*, or blank lines, in your scripts can greatly improve readability, and help divide different sections of the script.
Perhaps it is obvious, but Python will ignore blank lines in a script.

```python
# Finnish Meterological Institute observation station name and location data

# Station name for the station in Kaivopuisto, Helsinki, Finland
stationName = 'Helsinki Kaivopuisto'

# Station latitude and longitude - Latitude is north, longitude is east
stationLat = 60.15
stationLong = 24.96

# Print station name and location to the screen
print("The", stationName, "station is located at", stationLat, "N,", stationLong, "E")
```
<!-- #endregion -->

<!-- #region -->
## Use a docstring


A documentation string, or a *docstring* a block of text that describes what a spesific method or module does and how to use it. Surprise surprise, PEP 8 contains more guidance about [documentation strings](https://www.python.org/dev/peps/pep-0008/#documentation-strings), and docstrings even have their own guide page: [PEP 257](https://www.python.org/dev/peps/pep-0257/).

A docstring is always the first statement in a module or a function. Docstrings are written using `"""triple double quotation marks"""`. We already discussed docstrings when defining functions earlier in lesson 4, and here is an example of using a **multi-line docstring** at the start of a script file.

When adding docstrings at the start of a script file, you can also include your name, and also licensing information.



```python
"""Prints information about an FMI observation station to the screen.

Usage:
    ./stationinfo.py

Author:
    David Whipp - 23.9.2020
"""

# Finnish Meterological Institute observation station name and location data

# Station name for the station in Kaivopuisto, Helsinki, Finland
stationName = 'Helsinki Kaivopuisto'

# Station latitude and longitude - Latitude is north, longitude is east
stationLat = 60.15
stationLong = 24.96

# Print station name and location to the screen
print("The", stationName, "station is located at", stationLat, "N,", stationLong, "E")
```

In this example the script is simple, but many Python programs have optional values that can be used by the code when it is run, making the **usage** statement crucial.

Note that the closing quotes are on a line by themselves. It is also possible to write [one-line docstrings](https://www.python.org/dev/peps/pep-0257/#one-line-docstrings), for example with very simple functions, in which case the starting and closing quotation marks are on the same line.
<!-- #endregion -->

<!-- #region -->
## Advanced topics

### Adding a license

Depending on what you aim to do with your script, you may want to include a formal software license in the docstring to state the conditions under which the code can be used or modified.
There are many helpful web resources to [teach you about software licenses](https://tldrlegal.com/) and [how to choose a license](http://choosealicense.com/).
In most cases my preference is the [MIT License](https://opensource.org/licenses/MIT), which is simple and allows software use by anyone. An example is below.

```python
"""Prints information about an FMI observation station to the screen.

Usage:
    ./stationinfo.py

License:
    MIT License

    Copyright (c) 2020 David Whipp

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

# Finnish Meterological Institute observation station name and location data

# Station name for the station in Kaivopuisto, Helsinki, Finland
stationName = 'Helsinki Kaivopuisto'

# Station latitude and longitude - Latitude is north, longitude is east
stationLat = 60.15
stationLong = 24.96

# Print station name and location to the screen
print("The", stationName, "station is located at", stationLat, "N,", stationLong, "E")
```

Here the license is embedded in the docstring, so anyone using this part of the script will clearly see the license.
Another possibility would be to include a separate `LICENSE` text file in a software repository that could cover one or more source code files.

In this example I have taken the license information directly from an [online software license template](http://choosealicense.com/licenses/mit/).
Software licensing is an important consideration when posting your software in online repositories such as GitHub.
It is one way to protect your intellectual property from being used in ways you do not wish.
<!-- #endregion -->

<!-- #region -->
### Starting with a shebang

Starting with a shebang is another thing to consider doing with your scripts.
Why?
Well, without going into too much detail, it makes it easier for users to run your script directly from a terminal, rather than needing to use a Jupyter notebook or open an Python console first.
If this doesn’t make a great deal of sense, you can get a bit more information on [Wikipedia](https://en.wikipedia.org/wiki/Shebang_(Unix)).

Starting with a shebang means that the first line of your program starts with the characters `#!` followed by the location of a program that will run the Python software installed on the computer.
An example is below.

```python
#!/usr/bin/env python3
'''Prints information about an FMI observation station to the screen.

Usage:
    ./stationinfo.py

Author:
    David Whipp - 10.9.2017
'''

# Finnish Meterological Institute observation station name and location data

# Station name for the station in Kaivopuisto, Helsinki, Finland
stationName = 'Helsinki Kaivopuisto'

# Station latitude and longitude - Latitude is north, longitude is east
stationLat = 60.15
stationLong = 24.96

# Print station name and location to the screen
print("The", stationName, "station is located at", stationLat, "N,", stationLong, "E")
```

We’ll leave it at that for now, but if you have questions let us know.
<!-- #endregion -->

<!-- #region jp-MarkdownHeadingCollapsed=true -->
## Page summary

As we continue in the course we will mostly be working in Jupyter notebooks rather than writing scripts.
That said, we can still create simple docstrings for functions that provide short statements about how the function works, the parameters that are input, and the value that is returned.
In the event you end up writing scripts for other courses or your thesis research, don't forget to include inline comments, blank lines, and a docstring!
<!-- #endregion -->
