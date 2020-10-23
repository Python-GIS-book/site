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

# Functions

In this lesson we introduce functions as a way of making blocks of code for a specific task that are easy to use and re-use in your programs.

This section was partly based on the Programming in Python lessons {cite}`Bostroem2016` from the Software Carpentry organization [^swc].


## What is a function?

A *{term}`function`* is a block of organized, reusable code that can make your programs more effective, easier to read, and simple to manage. You can think functions as little self-contained programs that can perform a specific task that you can use repeatedly in your code. One of the basic principles in good programming is "do not to repeat yourself". In other words, you should avoid having duplicate lines of code in your scripts. Functions are a good way to avoid such situations and they can save you a lot of time and effort as you don't need to tell the computer repeatedly what to do every time it does a common task, such as converting temperatures from Fahrenheit to Celsius. During the course we have already used some functions such as the `print()` command which is actually a built-in function in Python.


## Anatomy of a function

Let's consider the task from the first lesson when we converted temperatures from Celsius to Fahrenheit.
Such an operation is a fairly common task when dealing with temperature data.
Thus we might need to repeat such calculations quite often when analysing or comparing weather or climate data between the US and Europe, for example.

### Our first function

Let's define our first function called `celsius_to_fahr`.

```python
def celsius_to_fahr(temp):
    return 9/5 * temp + 32
```

![Anatomy of a function.](../img/Function_anatomy-400.png)

The function definition opens with the keyword `def` followed by the name of the function and a list of parameter names in parentheses.
The body of the function — the statements that are executed when it runs — is indented below the definition line.

When we call the function, the values we pass to it are assigned to the corresponding parameter variables so that we can use them inside the function (e.g., the variable `temp` in this function example).
Inside the function, we use a `return` statement to define the value that should be given back when the function is used, or called.


## Calling functions

### Using our new function

Now let's try using our function.
Calling our self-defined function is no different from calling any other function such as `print()`.
You need to call it with its name and provide your value(s) as the required parameter(s) inside the parentheses.
Here, we can define a variable `freezing_point` that is the temperature in degrees Fahrenheit we get when using our function with the temperature 0°C (the temperature at which water freezes). We can then print that value to confirm. We should get a temperature of 32°F.

```python
freezing_point =  celsius_to_fahr(0)
```

```python
print('The freezing point of water in Fahrenheit is:', freezing_point)
```

We can do the same thing with the boiling point of water in degrees Celsius (100°C). Just like with other functions, we can use our new function directly within something like the `print()` function to print out the boiling point of water in degrees Fahrenheit.

```python
print('The boiling point of water in Fahrenheit is:', celsius_to_fahr(100))
```

### Let's make another function

Now that we know how to create a function to convert Celsius to Fahrenheit, let’s create another function called `kelvins_to_celsius`. We can define this just like we did with our `celsius_to_fahr()` function, noting that the Celsius temperature is just the temperature in Kelvins minus 273.15. Just to avoid confusion this time, let's call the temperature variable used in the function `temp_kelvins`.

```python
def kelvins_to_celsius(temp_kelvins):
    return temp_kelvins - 273.15
```

### Using our second function

Let's use it in the same way as the earlier one by defining a new variable `absolute_zero` that is the Celsius temperature of 0 Kelvins. Note that we can also use the parameter name `temp_kelvins` when calling the function to explicitly state which variable values is being used. Again, let's print the result to confirm everything works.

```python
absolute_zero = kelvins_to_celsius(temp_kelvins=0)
```

```python
print('Absolute zero in Celsius is:', absolute_zero)
```

<!-- #region -->
#### Check your understanding

Let's see how things are going so far with functions. In the Python cell below, please:

- Create a new function called `hello` with 2 parameters
    - Parameter 1 should be called `name` and you should assign some text to this parameter this when using the function
    - Parameter 2 should be called `age` and you should provide a number value for this parameter when using the function

When using your function, the value that is returned should be a character string stating the `name` and `age` that were provided, which you can assign to a variable called `output`.
Printing out `output` should produce something like the following:

```python
print(output)
'Hello, my name is Dave. I am 39 years old.'
```
<!-- #endregion -->

```python
def hello(name, age):
    return 'Hello, my name is ' + name + '. I am ' + str(age) + ' years old.'

output = hello(name='Dave', age=39)
print(output)
```

### Functions within a function

What about converting Kelvins to Fahrenheit?
We could write out a new formula for it, but we don’t need to.
Instead, we can do the conversion using the two functions we have already created and calling those from the function we are now creating. Let's create a new function `kelvins_to_fahr` that takes the temperature in Kelvins as the parameter value `temp_kelvins` and uses our `kelvins_to_celsius` and `celsius_to_fahr` functions within the new function to convert temperatures from Kelvins to degrees Fahrenheit.

```python
def kelvins_to_fahr(temp_kelvins):
    temp_celsius = kelvins_to_celsius(temp_kelvins)
    temp_fahr = celsius_to_fahr(temp_celsius)
    return temp_fahr
```

### Using our combined functions

Now let's use the function to calculate the temperature of absolute zero in degrees Fahrenheit. We can then print that value to the screen again.

```python
absolute_zero_fahr = kelvins_to_fahr(temp_kelvins=0)
```

```python
print('Absolute zero in Fahrenheit is:', absolute_zero_fahr)
```

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




## Footnotes

[^swc]: <http://software-carpentry.org>
