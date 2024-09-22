---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} -->
# Writing script files

Up to this point we have been keeping our Python code and Markdown comments in a single Jupyter notebook document.
This is great, but there are some cases, like when you have long Python code blocks or a set of functions used in many notebooks, in which you may want to have Python code in a separate document to make sure your Jupyter notebook is easy to read (and use).
An alternative to typing in all of the commands you would like to run is the list them in a Python *{term}`script`* file.
A Python script file is simply a file containing a list of the commands you would like to run, normally with one command per line, and formatted in the same way as if you were to type them in.
Python script files traditionally use the `.py` file extension in their names.
<!-- #endregion -->

## The general concept of a script file

Because a Python script file is simply a list of commands that you might otherwise type into a Python cell in a Jupyter notebook or a Python console, we can quite easily create a basic script file and test things out.

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Getting started

First, we need to create a new text file by clicking on **File** -> **New** -> **Python File** in the JupyterLab menu bar.

![_**Figure 2.5**. Creating a new Python file in JupyterLab._](../img/new-python-file.png)

_**Figure 2.5**. Creating a new Python file in JupyterLab._

This will create a new tab in your JupyterLab window that should look something like that below, a blank slate.

![_**Figure 2.6**. The new empty Python file in JupyterLab._](../img/new-python-tab.png)

_**Figure 2.6**. Creating a new Python file in JupyterLab._

Start by copying and pasting the text below into your new text file editor panel.

```python
def celsius_to_fahr(temp_celsius):
    return 9/5 * temp_celsius + 32
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Saving a text file as a Python file

As it turns out, Python scripts are just regular text files with the `.py` file extension to identify them as source code for Python. By default, new Python files in JupyterLab will have the name `untitled.py`. You can rename the file by right clicking on the `untitled.py` file in the file browser and renaming it `temp_converter.py`.

![_**Figure 2.7**. Renaming a file in JupyterLab._](../img/rename-python-file-part-1.png)

_**Figure 2.7**. Renaming a file in JupyterLab._

![_**Figure 2.8**. File renaming dialog in JupyterLab._](../img/rename-python-file-part-2.png)

_**Figure 2.8**. Renaming a file in JupyterLab._

Be sure to save your `temp_converter.py` file after making your changes. We'll return later to some best practices for writing script files, but for now let's continue with how to use our functions saved in the Python file we just created.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Saving and loading functions

Naturally, after saving functions such as the one above to a script file, it is important to know how to access those functions from within a Juypter notebook. As noted earlier, quite often it is useful to create a dedicated function library for functions that you use frequently when doing data analysis, for example. Basically this is done by listing useful functions in a single `.py` file from which you can then import and use them whenever needed.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Saving functions in a script file

Before we move on to discussing how to use functions in a script file, let's add a few more functions we have been using to our script. Simply copy and paste the text below into your `temp_converter.py` file leaving two blank lines between each function.

```python
def kelvins_to_celsius(temp_kelvins):
    return temp_kelvins - 273.15


def kelvins_to_fahr(temp_kelvins):
    temp_celsius = kelvins_to_celsius(temp_kelvins)
    temp_fahr = celsius_to_fahr(temp_celsius)
    return temp_fahr
```

Don't forget to save your changes!
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Calling functions from a script file

Now that we have saved our temperature conversion functions into a script file we can start using them.
<!-- #endregion -->

### Making sure we're in the right working directory

Hopefully you have saved your `temp_converter.py` file in the same location as this Jupyter notebook (`06-writing-scripts.ipynb`). If so, that's good, but we need to do one more thing to be able to start working with the script file. We need to change the working directory in Jupyter Lab to be the one where the `temp_converter.py` exists.

First, we can see which files are present in the directory where we are currently working using an IPython magic command called `%ls`.

```python editable=true slideshow={"slide_type": ""}
%ls
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
`%ls` allows us to see the files located in the directory where we are currently working. Your output from `%ls` may look different than that above, but don't worry. As long as you see the file `temp_converter.py`, you should be all set to proceed.

If you do not see the `temp_converter.py` file in the list of files from `%ls`, then you will need to take an additional few steps, which differ depending on what files you see.

- If you see the list of notebooks above (e.g., `00-motivation.ipynb`, `01-computers-and-programs.ipynb`, ...) but do note see the `temp_converter.py` file, then you should make sure you have saved the `temp_converter.py` file in the notebooks directory for Chapter 2. The easiest way to do this would be to use the file browser in JupyterLab, find the `temp_converter.py` file, right click on it and select **Copy**, navigate to the `part1/chapter-02/nb` directory in the file browser, and right click again in the space beneath the list of files to paste a copy of the `temp_converter.py` file in that location.
- If you do not see the list of notebooks above, you may need to change directories to be in the Chapter 2 notebooks directory. For example, if you see

    ```bash
    _static          conf.py          index.rst        requirements.txt
    authors.rst      data             part1
    back-matter      environment.rst  part2
    bibtex.json      front-matter     part3
    ```

    you are working in the base `source` directory. You can change directories to the notebooks directory for Chapter 2 by typing

    ```ipython
    %cd part1/chapter-02/nb
    ```


### Confirming we are in the correct directory

If all has gone well you should now see `temp_converter.py` among the files when you type `%ls` in a Python cell. Try that out below.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
%ls
```

If you see `temp_converter.py` in the list of files above you are all set to continue.

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Importing our script functions

Let's now import our `celsius_to_fahr()` function from the `temp_converter.py` script file by adding a specific `import` statement in the Python cell below: `from temp_converter import celsius_to_fahr`
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# DO NOT RUN THIS CELL
# This cell is only needed for generating the web page and book documents
%cd ../../../_static/part1/chapter-02/
```

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
from temp_converter import celsius_to_fahr
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Using our script functions

Let's now use the function so that we can see that it is working. We can print the temperature in Fahrenheit at which water freezes using our `celsius_to_fahr()` function in the cell below.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
print(f"The freezing point of water in Fahrenheit is: {celsius_to_fahr(0)}")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
You should get following output:

```code
The freezing point of water in Fahrenheit is: 32.0
```
<!-- #endregion -->

<!-- #region -->
### Other ways of importing functions

It is also possible to import more than one function at a time by listing and separating them with a comma.

```python
from my_script import func1, func2, func3
```

Additionally, it is sometimes useful to import the whole script and all of its functions at once. This can be done using a different `import` statement, which we can use and then test that all of the imported functions work. This time we can type `import temp_converter as tc`.
<!-- #endregion -->

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
import temp_converter as tc
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Just like the examples we have seen earlier with the `math` library, such as using `math.sin()`, we can now use our functions such as `tc.celsius_to_fahr()`. In the cells below, test our functions as they were used above by printing the freezing point of water in Fahrenheit, absolute zero in Celsius, and absolute zero in Fahrenheit.
<!-- #endregion -->

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
print(f"The freezing point of water in Fahrenheit is: {tc.celsius_to_fahr(0)}")
```

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
print(f"Absolute zero in Celsius is: {tc.kelvins_to_celsius(temp_kelvins=0)}")
```

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
print(f"Absolute zero in Fahrenheit is: {tc.kelvins_to_fahr(temp_kelvins=0)}")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Creating a temperature calculator

The functions above have had only one parameter, but now we will add another function with multiple parameters. In this case we will create a simple `temp_calculator()` function that accepts temperatures in Kelvins and returns either Celsius or Fahrenheit. The new function will have two parameters:

- `temp_k` = The parameter for passing temperature in Kelvins
- `convert_to` = The parameter that determines whether the output should be in degrees Celsius or Fahrenheit (using the letters `C` or `F`)
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Defining the function

Let's start defining our function by giving it a name and listing the parameters.

```python
def temp_calculator(temp_k, convert_to):
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Adding some conditional statements

Next, we need to add conditional statements that check whether the desired output temperature should be in degrees Celsius or Fahrenheit, and then call the corresponding function from the `temp_converter.py` script file.

```python
def temp_calculator(temp_k, convert_to):
    # Check if the user wants temperatures in Celsius
    if convert_to == "C":
        # Convert the value to Celsius using the dedicated function for
        # the task from the temp_converter.py script file
        converted_temp = kelvins_to_celsius(temp_kelvins=temp_k)
    elif convert_to == "F":
        # Convert the value to Fahrenheit using the dedicated function
        # for the task from the temp_converter.py script file
        converted_temp = kelvins_to_fahr(temp_kelvins=temp_k)
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Returning the result

Next, we need to add a `return` statement so that our function sends back the value that we are interested in.

```python
def temp_calculator(temp_k, convert_to):
    # Check if the user wants temperatures in Celsius
    if convert_to == "C":
        # Convert the value to Celsius using the dedicated function for
        # the task from the temp_converter.py script file
        converted_temp = kelvins_to_celsius(temp_kelvins=temp_k)
    elif convert_to == "F":
        # Convert the value to Fahrenheit using the dedicated function
        # for the task from the temp_converter.py script file
        converted_temp = kelvins_to_fahr(temp_kelvins=temp_k)
    # Return the result
    return converted_temp
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Adding a docstring

Finally, since we want to be good programmers, we should add a short docstring at the beginning of our function that explains what the function does and how the parameters work.

```python
def temp_calculator(temp_k, convert_to):
    """
    Converts temperature in Kelvins to Celsius or Fahrenheit.

    Parameters
    ----------
    temp_k: <numerical>
        Temperature in Kelvins
    convert_to: <str>
        Target temperature that can be either Celsius ('C') or
        Fahrenheit ('F'). Supported values: 'C' | 'F'

    Returns
    -------
    <float>
        Converted temperature.
    """

    # Check if the user wants temperatures in Celsius
    if convert_to == "C":
        # Convert the value to Celsius using the dedicated function for
        # the task from the temp_converter.py script file
        converted_temp = kelvins_to_celsius(temp_kelvins=temp_k)
    elif convert_to == "F":
        # Convert the value to Fahrenheit using the dedicated function
        # for the task from the temp_converter.py script file
        converted_temp = kelvins_to_fahr(temp_kelvins=temp_k)
    # Return the result
    return converted_temp
```

At this point, we can copy and paste the function into the `temp_converter.py` script file and proceed to testing things out.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Testing the new function

Now we have a temperature calculator that has a simple option that allows the user to select the temperature unit for output using the `convert_to` parameter. 

At this point we need to re-import the functions from the `temp_calculator.py` script file. However, when working in a Jupyter Notebook, reloading modules can be a bit challenging. The easiest option is to restart the IPython kernel by going to **Kernel** -> **Restart kernel...** in the menu bar. Note that this will delete all variables currently stored in memory in the Jupyter notebook you're using, so you may need to re-run some cells. After restarting the kernel, you can re-import the functions from the `temp_converter.py` script file by typing:

```python
import temp_converter as tc
```

We can check that this step worked as expected by using the `help()` function in Python to see how our function should be used (since we added a short docstring at the beginning of the function). Try running `help(temp_calculator)` in the cell below to see the docstring.
<!-- #endregion -->

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
help(tc.temp_calculator)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Using the temp calculator function

Finally, let's see how our function works!
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temp_kelvin = 30
```

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
temperature_c = tc.temp_calculator(temp_k=temp_kelvin, convert_to="C")
```

```python tags=["raises-exception"] editable=true slideshow={"slide_type": ""}
print(f"{temp_kelvin} Kelvins is {temperature_c:.2f} degrees Celsius.")
```
