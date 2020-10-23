---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region -->
# Writing script files

Up to this point we have been keeping our Python code and Markdown comments in a single Jupyter notebook document.
This is great, but there are some cases, like when you have long Python code blocks or a set of functions used in many notebooks, in which you may want to have Python code in a separate document to make sure your Jupyter notebook is easy to read (and use).
An alternative to typing in all of the commands you would like to run is the list them in a Python *{term}`script`* file.
A Python script file is simply a file containing a list of the commands you would like to run, normally with one command per line, and formatted in the same way as if you were to type them in.
Python script files traditionally use the `.py` file extension in their names.

## The general concept of a script file

Because a Python script file is simply a list of commands that you might otherwise type into a Python cell in a Jupyter notebook or a Python console, we can quite easily create a basic script file and test things out.

### Getting started

First, we need to create a new text file by clicking on **File** -> **New** -> **Text File** in the JupyterLab menu bar.

![Creating a new text file in JupyterLab.](../img/new-text-file-400.png)

This will create a new tab in your JupyterLab window that should look something like that below, a blank slate.

![Our new text file in JupyterLab.](../img/new-text-tab-800.png)

Start by copying and pasting the text below into your new text file editor panel.

```python
def celsius_to_fahr(temp_celsius):
    return 9/5 * temp_celsius + 32
```
<!-- #endregion -->

### Saving a text file as a Python file

As it turns out, Python scripts are just regular text files with a certain file extension to identify them as source code for Python.
In order for our new text file to be detected as a Python source file in JupyterLab we need to rename it to have a `.py` file extension.
You can rename the file by right clicking on the tab titled `untitled.txt` and renaming it as `temp_converter.py`.

```{note}
Be sure you change the `.txt` file extension to `.py`.
```

![Renaming a text file in JupyterLab.](../img/rename-file-part-1-600.png)

![Changing the file name in JupyterLab.](../img/rename-file-part-2-300.png)

If all goes well, you should now see the Python syntax is highlighted in different colors in the JupyterLab editor panel.

```{note}
Be sure to save your `temp_converter.py` file after making your changes.
```

We'll return later to some best practices for writing script files, but for now let's continue with how to use our functions saved in the Python file we just created.

<!-- #region -->
## Saving and loading functions

Functions such as the ones we just created can also be saved in a script file and called from Jupyter notebooks.
In fact, quite often it is useful to create a dedicated function library for functions that you use frequently, when doing data analysis, for example.
Basically this is done by listing useful functions in a single `.py` file from which you can then import and use them whenever needed.

### Saving functions in a script file

Basically, we've just seen how to save some functions to a script file.
Let's now add the other functions we had been using to our script.
Simply copy and paste the text below into your `temp_converter.py` file leaving one blank line between each function.

```python
def kelvins_to_celsius(temp_kelvins):
    return temp_kelvins - 273.15
```

```python
def kelvins_to_fahr(temp_kelvins):
    temp_celsius = kelvins_to_celsius(temp_kelvins)
    temp_fahr = celsius_to_fahr(temp_celsius)
    return temp_fahr
```

Don't forget to save your changes!
<!-- #endregion -->

## Calling functions from a script file

Now that we have saved our temperature conversion functions into a script file we can start using them.

### Making sure we're in the right working directory

Hopefully you have saved you `temp_converter.py` file in the same location as this Jupyter notebook (`functions.ipynb`).
If so, that's good, but we need to do one more thing to be able to start working with it.
We need to change the working directory in JupyterLab to be the one where the `temp_converter.py` exists.

First, we can check where we are working currently using an IPython magic command called `%ls`.

```python
%ls
```

<!-- #region -->
Your output from `%ls` probably looks different than that above, but don't worry.
`%ls` allows us to see the files located in the directory where we are currently working.

#### Binder users

If you are using Binder, you may see

```bash
functions.ipynb  img/  modules.ipynb  temp_converter.py  writing-scripts.ipynb
```

for example. If this is the case, you are all set to continue!

If you see something else, such as 

```bash
L1/  L2/  L3/  L4/  README.md  requirements.txt
```

you will need to change directories.
To do this you should type the following to change into the directory containing the `temp_converter.py` file.

```ipython
%cd L4/
```

#### CSC notebooks users

Those using the CSC notebooks might see something like

```bash
exercises/  installations.sh*  notebooks/
```

In this case you will need to change directories to the one containing the `temp_converter.py` file.
You can do this by typing 

```ipython
%cd notebooks/L4/
```
<!-- #endregion -->

### Confirming we are in the correct directory

If all has gone well you should now see `temp_converter.py` among the files when you type `%ls` in a Python cell.
Try that out below.

```python
%ls
```

If you see `temp_converter.py` in the list of files above you are all set to continue.


### Importing our script functions

Let's now import our `celsius_to_fahr()` function from the other script by adding a specific `import` statement in the Python cell below: `from temp_converter import celsius_to_fahr`

```python
# DO NOT RUN THIS CELL
# This cell is only needed for generating the course web page
%cd ../../_static/L4/
```

```python tags=["raises-exception"]
from temp_converter import celsius_to_fahr
```

### Using our script functions

Let's also use the function so that we can see that it is working. We can print the temperature in Fahrenheit at which water freezes using our `celsius_to_fahr()` function in the cell below.

```python
print("The freezing point of water in Fahrenheit is:", celsius_to_fahr(0))
```

<!-- #region -->
You should get following output:

```
The freezing point of water in Fahrenheit is: 32.0
```

#### Importing multiple functions

It is also possible to import more functions at the same time by listing and separating them with a comma.

```python
from my_script import func1, func2, func3
```

### Importing all functions from a script

Sometimes it is useful to import the whole script and all of its functions at once. Let's use a different `import` statement and test that all functions work. This time we can type `import temp_converter as tc`.
<!-- #endregion -->

```python tags=["raises-exception"]
import temp_converter as tc
```

Just like the examples we have seen earlier with the `math` library, such as using `math.sin()`, we can now use our functions such as `tc.celsius_to_fahr()`. In the cells below, test our functions as they were used above by printing the freezing point of water in Fahrenheit, absolute zero in Celsius, and absolute zero in Fahrenheit.

```python tags=["raises-exception"]
print("The freezing point of water in Fahrenheit is:", tc.celsius_to_fahr(0))
```

```python tags=["raises-exception"]
print('Absolute zero in Celsius is:', tc.kelvins_to_celsius(temp_kelvins=0))
```

```python tags=["raises-exception"]
print('Absolute zero in Fahrenheit is:', tc.kelvins_to_fahr(temp_kelvins=0))
```

<!-- #region -->
## Temperature calculator (*optional, advanced topic*)

So far our functions have had only one parameter, but it is also possible to define a function with multiple parameters.
Let's now make a simple `temp_calculator` function that accepts temperatures in Kelvins and returns either Celsius or Fahrenheit.
The new function will have two parameters:

- `temp_k` = The parameter for passing temperature in Kelvins
- `convert_to` = The parameter that determines whether to output should be in Celsius or in Fahrenheit (using letters `C` or `F` accordingly)

### Defining the function

Let's start defining our function by giving it a name and setting the parameters.

```python
def temp_calculator(temp_k, convert_to):
```
<!-- #endregion -->

<!-- #region -->
### Adding some conditional statements

Next, we need to add conditional statements that check whether the desired output temperature should be in Celsius or Fahrenheit, and then call the corresponding function that was imported from the `temp_converter.py` file.

```python
def temp_calculator(temp_k, convert_to):
    # Check if user wants the temperature in Celsius
    if convert_to == "C":
        # Convert the value to Celsius using the dedicated function for the task that we imported from another script
        converted_temp = kelvins_to_celsius(temp_kelvins=temp_k)
    elif convert_to == "F":
        # Convert the value to Fahrenheit using the dedicated function for the task that we imported from another script
        converted_temp = kelvins_to_fahr(temp_kelvins=temp_k)
```
<!-- #endregion -->

<!-- #region -->
### Returning the result

Next, we need to add a return statement so that our function sends back the value that we are interested in.

```python
def temp_calculator(temp_k, convert_to):
    # Check if user wants the temperature in Celsius
    if convert_to == "C":
        # Convert the value to Celsius using the dedicated function for the task that we imported from another script
        converted_temp = kelvins_to_celsius(temp_kelvins=temp_k)
    elif convert_to == "F":
        # Convert the value to Fahrenheit using the dedicated function for the task that we imported from another script
        converted_temp = kelvins_to_fahr(temp_kelvins=temp_k)
    # Return the result
    return converted_temp
```
<!-- #endregion -->

<!-- #region -->
### Adding a docstring

Finally, since we want to be good programmers, we should add a short docstring at the beginning of our function that tells what the function does and how the parameters work.

```python
def temp_calculator(temp_k, convert_to):
    """
    Function for converting temperature in Kelvins to Celsius or Fahrenheit.

    Parameters
    ----------
    temp_k: <numerical>
        Temperature in Kelvins
    convert_to: <str>
        Target temperature that can be either Celsius ('C') or Fahrenheit ('F'). Supported values: 'C' | 'F'

    Returns
    -------
    <float>
        Converted temperature.
    """

    # Check if user wants the temperature in Celsius
    if convert_to == "C":
        # Convert the value to Celsius using the dedicated function for the task that we imported from another script
        converted_temp = kelvins_to_celsius(temp_kelvins=temp_k)
    elif convert_to == "F":
        # Convert the value to Fahrenheit using the dedicated function for the task that we imported from another script
        converted_temp = kelvins_to_fahr(temp_kelvins=temp_k)
    # Return the result
    return converted_temp
```
<!-- #endregion -->

### Testing the new function

That's it!
Now we have a temperature calculator that has a simple control for the user where they can change the output using the `convert_to` parameter.
Now as we added the short docstring in the beginning of the function we can use the `help()` function in Python to find out how our function should be used.
Run the Python cell below and then try running `help(temp_calculator)`.

```{attention}
Reloading modules from within a Jupyter notebook is a bit of a pain.
The easiest option is to restart the IPython kernel by going to **Kernel** -> **Restart kernel...**.
Note that this will delete all variables currently stored in memory in the Jupyter notebook you're using, so you may need to re-run some cells.
```

```python tags=["raises-exception"]
help(tc.temp_calculator)
```

### Using the tempCalculator

Let's use it.

```python
temp_kelvin = 30
```

```python tags=["raises-exception"]
temperature_c = tc.temp_calculator(temp_k=temp_kelvin, convert_to="C")
```

```python tags=["raises-exception"]
print("Temperature", temp_kelvin, "in Kelvins is", temperature_c, "in Celsius")
```

## Footnotes

[^swc]: <http://software-carpentry.org>


# Good coding practices - Writing our scripts the "right" way

The script example for functions we have seen so far works, but one of the big advantages of using scripts is including features that make the code easier to read and understand.
These include comments in the code, which explain what the code does, but are not executed when the code is run.
As your scripts get longer and more complicated, features such as comments will become essential.
Below are some suggestions to make sure your code is formatted nicely and easy to understand.

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
    David Whipp - 26.9.2018
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

    Copyright (c) 2017 David Whipp

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

In this case I have taken the license information directly from an [online software license template](http://choosealicense.com/licenses/mit/).
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

## Page summary

As we continue in the course we will be creating more advanced Python scripts that include more complex code logic and other features we’ve not yet learned.
With these, we'll also learn a few tips for incorporating them in our scripts.
However, an expectation in this course is that you stick to the general template described above when writing your script files, which means including appropriate use of inline comments, blank lines, and a docstring.
