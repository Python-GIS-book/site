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

<!-- #region deletable=true editable=true -->
# Getting started with Python

In this section, we will introduce some basic programming concepts in Python.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
## Simple Python math

We will start our Python introduction by learning a bit of the basic operations you can perform. Python can be used as a simple calculator. Let's try it out with some simple math operations such as `1 + 1` or `5 * 7`.  When using a Jupyter Notebook you can press **Shift-Enter** to execute the code cells. 
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
1 + 1
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
5 * 7
```

<!-- #region deletable=true editable=true -->
If you want to edit and re-run some code, simply make changes to the Python cell and press **Shift-Enter** to execute the modified code.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
### Functions

You can use Python for more advanced math by using a *{term}`function`*. Functions are pieces of code that perform a single action such as printing information to the screen (e.g., the `print()` function). Functions exist for a huge number of operations in Python.

Let's try out a few simple examples using functions to find the sine or square root of a value using the `sin()` and `sqrt()` functions.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} tags=["raises-exception"]
sin(3)
```

```python deletable=true editable=true jupyter={"outputs_hidden": false} tags=["raises-exception"]
sqrt(4)
```

<!-- #region deletable=true editable=true -->
Wait, what? Python can’t calculate square roots or do basic trigonometry? Of course it can, but we need one more step.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
### Math operations

The list of basic arithmetic operations that can be done by default in Python are listed in Table 2.1.

: _**Table 2.1**. Basic math operations in Python._

|Operation      | Symbol | Example syntax | Returned value |
|:--------------|:------:|:--------------:|:--------------:|
|Addition       | `+`    | `2 + 2`        | `4`            |
|Subtraction    | `-`    | `4 - 2`        | `2`            |
|Multiplication | `*`    | `2 * 3`        | `6`            | 
|Division       | `/`    | `4 / 2`        | `2`            |
|Exponentiation | `**`   | `2**3`         | `8`            |

For anything more advanced, we need to load a *{term}`module`* or *{term}`library`*. For math operations, this module is called `math` and it can be loaded by typing `import math`.
<!-- #endregion -->

```python deletable=true editable=true
import math
```

Now that we have access to functions in the math module, we can use it by typing the module name, a period (dot), and the the name of the function we want to use. For example, `math.sin(3)`.

```python deletable=true editable=true jupyter={"outputs_hidden": false}
math.sin(3)
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
math.sqrt(4)
```

<!-- #region deletable=true editable=true -->
Let's summarize what we've just seen with modules:

1. A {index}`module` is a group of code items such as functions that are related to one another. Individual modules are often in a group referred to as a library.

2. Modules can be loaded using the `import` statement. Functions that are part of the module `modulename` can then be used by typing `modulename.functionname()`. For example, `sin()` is a function that is part of the `math` module, and used by typing `math.sin()` with some number between the parentheses.

3. In a Jupyter Notebook the variables you define earlier code cells will be available for use in the cells that follow as long as you have already executed the cells.

Note that modules may also contain constants such as `math.pi`. Parentheses are not used when calling constant values.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
math.pi
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.1

Use your Python skills to calculate the sine of pi. What value do you expect for this calculation? Did you get the expected result?
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Note that lines starting with "#" are ignored in Python.
# Use this cell to enter your solution.
```

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

math.sin(math.pi)
```

<!-- #region deletable=true editable=true -->
### Combining functions

Functions can also be combined. The `print()` function returns values within the parentheses as text on the screen. Let's print the value of the square root of four.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
print(math.sqrt(4))
```

You can also combine text with other calculated values using the `print()` function. For example, `print('Two plus two is', 2+2)` would generate text reading 'Two plus two is 4'. Let's combine the `print()` function with the `math.sqrt()` function in to produce text that reads `The square root of 4 is 2.0`.

```python deletable=true editable=true jupyter={"outputs_hidden": false}
print("The square root of 4 is", math.sqrt(4))
```

<!-- #region deletable=true editable=true -->
## Variables

A *{term}`variable`* can be used to store values calculated in expressions and used for other calculations.
<!-- #endregion -->

### Variable assignment

Assigning value to variables is straightforward. To assign a value, you simply type `variable_name = value`, where `variable_name` is the name of the variable you wish to define. Let's define a variable called `temp_celsius` and assign it a value of 10.0. Note that when the variable is assigned there is no output to the screen.

```python deletable=true editable=true jupyter={"outputs_hidden": false}
temp_celsius = 10.0
```

In order to see the value that has been assigned to the `temp_celsius` variable you need to either use the `print()` function (e.g., `print(temp_celsius)`) or simply type the name of the variable into the code cell to have its value displayed. This is a convenient way to see calculated values in code cells of Jupyter Notebooks, so for simplicity we will avoid using the `print()` function when possible in this book. In some cases, however, the `print()` function is needed, such as displaying output from multiple lines of a single code cell.

```python
temp_celsius
```

It is also possible to combine text and numbers and even use some math when printing out variable values. The idea is similar to the examples of adding 2+2 or calculating the square root of four from the previous section. Next, we will print out the value of `temp_celsius` in degrees Fahrenheit by multiplying `temp_celsius` by 9/5 and adding 32. This should be done within the `print()` function to produce output that reads 'Temperature in Fahrenheit: 50.0'.

```python deletable=true editable=true jupyter={"outputs_hidden": false}
print("Temperature in Fahrenheit:", 9 / 5 * temp_celsius + 32)
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.2

Define a variable and display its value on the screen. The variable value can be anything you like, and you can even consider defining several variables and printing them out together. Consider using pothole_case_naming for your variable name.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python deletable=true editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

my_variable = "Python is cool!"
my_variable
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
### Updating variables

Values stored in variables can also be updated. Let's redefine the value of `temp_celsius` to be equal to 17.0 and print its value using the `print()` function.
<!-- #endregion -->

```python deletable=true editable=true slideshow={"slide_type": ""}
temp_celsius = 17.0
```

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
print("temperature in Celsius is now:", temp_celsius)
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
Please note that if you try to run some code that accesses a variable that has not yet been defined you will get a `NameError` message.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} tags=["raises-exception"]
print("Temperature in Celsius:", 5 / 9 * (tempFahrenheit - 32))
```

<!-- #region deletable=true editable=true -->
When running the code in a Jupyter Notebook variables get stored in memory only after executing the code cell where the variable is defined. 
<!-- #endregion -->

```python deletable=true editable=true slideshow={"slide_type": ""}
tempFahrenheit = 9 / 5 * temp_celsius + 32
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now that we have defined `tempFahrenheit`, we can run again the print statement without getting a `NameError`. Let's print out the values of `temp_celsius` and `tempFahrenheit` to check their current values.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
print("temperature in Celsius:", temp_celsius, "and in Fahrenheit:", tempFahrenheit)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
The number beside the cell, for example `In [22]`, tells you the order in which the Python cells have been executed. This way you can see a history of the order in which you have run the cells.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
### Variable values

Changing the value of a variable does not affect other variable values. Let's redefine `temp_celsius` to be equal to 20.0, and print out the values of `temp_celsius` and `tempFahrenheit`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
temp_celsius = 20.0
print(
    "temperature in Celsius is now:",
    temp_celsius,
    "and temperature in Fahrenheit is still:",
    tempFahrenheit,
)
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
## Data types

A *{term}`data type`* determines the characteristics of data in a program.
There are 4 basic data types in Python as shown in Table 2.2.

: _**Table 2.2**. Basic data types in Python._

|Data type name |Data type            | Example    |
|:--------------|:--------------------|:----------:|
|`int`          |Whole integer values | `4`        |
|`float`        |Decimal values       | `3.1415`   |
|`str`          |Character strings    | `'Hot'`    |
|`bool`         |True/false values    | `True`     |

The data type can be found using the `type()` function. As you will see, the data types are important because some are not compatible with one another. Let's define a variable `weatherForecast` and assign it the value "Hot". After this, we can check its data type using the `type()` function.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
weatherForecast = "Hot"
type(weatherForecast)
```

Let's also check the type of `tempFahrenheit`. What happens if you try to combine `tempFahrenheit` and `weatherForecast` in a single math equation such as `tempFahrenheit = tempFahrenheit + weatherForecast`?

```python deletable=true editable=true jupyter={"outputs_hidden": false} tags=["raises-exception"]
type(tempFahrenheit)
tempFahrenheit = tempFahrenheit + weatherForecast
```

<!-- #region deletable=true editable=true -->
In this case we get at `TypeError` because we are trying to execute a math operation with data types that are not compatible. It is not possible to add a number directly to a character string in Python. In order for addition to work, the data types need to be compatible with one another.
<!-- #endregion -->

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.3

As it turns out, it is possible some math with character strings in Python. Define two variables and assign them character string values. What happens if you try to add two character strings together? Can you subtract them? Which other math operations work for character strings?
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python deletable=true editable=true slideshow={"slide_type": ""} tags=["raises-exception", "remove_book_cell", "hide-cell"]
# Solution

first_variable = "Python"
second_variable = " is cool!"

print(first_variable + second_variable)
print(5 * first_variable)
print(first_variable - second_variable)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Making different data types work together

In the previous section we saw that not all Python data types are directly compatible with others, which may result in a `TypeError` being raised. This means that (1) it is important to be aware of the data type of variables and (2) some additional steps may be needed to make different data compatible. Let's consider an example where we try to combine `tempFahrenheit` (type `float`) with another temperature value. In this case, the other temperature is stored in a character string `forecastHighStr` (type `str`) with a value of `"77.0"`. As we know, data of type `float` and type `str` are not compatible for math operations. Let's start by defining `forecastHighStr` and then see how we can we address this issue to make these data work together.
<!-- #endregion -->

```python
forecastHighStr = "77.0"
forecastHighStr
```

```python
type(forecastHighStr)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Converting data from one type to another

It is not the case that things like the `tempFahrenheit` and `forecastHighStr` cannot be combined at all, but in order to combine a character string with a number we need to perform a *{term}`type conversion`* to make them compatible. Let's convert `forecastHighStr` to a floating point number using the `float()` function. We can store the converted variable as `forecastHigh`.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
forecastHigh = float(forecastHighStr)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
We can confirm the type has changed by checking the type of `forecastHigh` or by checking the output of a code cell with the variable.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
type(forecastHigh)
```

```python editable=true slideshow={"slide_type": ""}
forecastHigh
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As you can see, `float()` converts a character string to a decimal value representing the number stored in the string. As a result, we can now easily calculate the difference between the forecast high temperature `forecastHigh` and `tempFahrenheit` as the data are now compatible.
<!-- #endregion -->

```python
forecastHigh - tempFahrenheit
```

`float()` can be used to convert strings or integers to floating point numbers, however it is important to note that `float()` can only convert strings that represent numerical values. For example, `float("Cold")` will raise a `ValueError` because `"Cold"` cannot be converted to a number directly. Similar to `float()`, `str()` can convert numbers to character strings, and `int()` can be used to convert strings or floating point numbers to integers. For example, we could convert `tempFahrenheit` to an integer as follows.

```python editable=true slideshow={"slide_type": ""}
tempFahrenheitInt = int(tempFahrenheit)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Again, we can confirm the data type and value of `tempFahrenheitInt` in below. Do you notice any issues?
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
type(tempFahrenheitInt)
```

```python editable=true slideshow={"slide_type": ""}
tempFahrenheitInt
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Here we see that the data type conversion has occurred properly, but notice that the value of `tempFahrenheitInt` is `62`. This occurs because the type conversion truncates the decimal part of the number rather than rounding to the nearest whole number (for this we need the `round()` function). Thus, one must be careful when converting data types as conversion may result in unexpected results!
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.4

What output would you expect to see when you execute `print(tempFahrenheitInt + temp_celsius)`?
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

print(tempFahrenheitInt + temp_celsius)
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.5

What output would you expect to see when you execute `float(weatherForecast)`?
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell", "raises-exception"]
# Solution

float(weatherForecast)
```
