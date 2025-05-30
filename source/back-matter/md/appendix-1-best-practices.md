---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Python programming best practices


This book aims to introduce you to programming in Python, but also to good programming practices. These comprise practical tips based on practices used by professional programmers that help them write better programs that are easier to understand and share with others. To say it differently, there are many ways to learn to program and we want to help you learn how to program the right way!

<!-- #region -->
## Best practice 1: Selecting variable names

The selection of variable names might seem insignificant in some ways, but poorly chosen variable names can be confusing, unclear, or even misleading. Thus, we provide some examples of both poorly and well chosen variable names below along with some tips for formatting of your variables.

### Some "not-so-good" variable names

Let's first consider some examples of problematic variable names.

```python
s = "101533"
sid = "101533"
```

Here we have two variable names that are nice and short, but it is not particularly clear what kind of value they are being used to store. The variables `s` and `sid` are simply too short and cannot communicate what they should be used for in the code. You might think you know what they are for at the moment, but imagine not looking at the code for a few months. Would you know then? What about if you share the code with a friend? Would they know? Probably not.

Let's consider another example.

```python
finnishmeteorlogicalinstituteobservationstationidentificationnumber = "101533"
```

Here we have the opposite problem. The variable name `finnishmeteorologicalinstituteobservationstationidentificationnumber` potentially provides more information about what the variable represents (the identification number of a Finnish Meteorological Institute observation station), but it does so in a format that is not easy to read nor something you're likely to want to type more than once. The previous examples were too short, but now we have a variable name that is too long (and hard to read as a result).
<!-- #endregion -->

### Selecting "good" variable names

A good variable name should:

1. Be clear and concise. 

2. Be written in English. A general coding practice is to write code with variable names in English, as that is the most likely common language between programmers. Thus, variable names such as `muuttuja`, the word for "variable" in Finnish should be avoided. Note that `muuttuja` is not a good name for other reasons as well.

3. Not contain special characters. Python supports use of special characters by way of various encoding options that can be given in a program. That said, it is better to avoid variables such as `lämpötila` (the Finnish word for temperature) because encoding issues can arise in some cases. It is recommended to stick to the [standard printable ASCII character set](https://en.wikipedia.org/wiki/ASCII#Printable_characters) [^ascii] to be safe.

4. Not conflict with any [Python keywords](https://www.geeksforgeeks.org/python-keywords/) [^keywords], such as `for`, `True`, `False`, `and`, `if`, or `else`. These are reserved for special operations in Python and cannot be used as variable names.

With this in mind, let's now consider two formats commonly used for formatting Python variables.

<!-- #region -->
### Recommended variable format 1: pothole_case naming

*{term}`pothole_case naming <Pothole case>`* uses lowercase words separated by underscores `_`. This is our suggested format as the underscores make it easy to read the variable and do not add much to the length of the variable name. As an example, consider the variable `temp_celsius`. Considering our earlier examples of poor variable names, we could instead write the following.

```python
fmi_station_id = "101533"
```

Here, our variable name conveys all of the essential information we need, while remaining easy to read.

### Recommended variable format 2: camelCase naming

*{term}`camelCase or CamelCase naming <Camel case>`* uses capitalization of the first letter of words in a variable name to make it easier to read. In some cases the first letter of the variable may be capitalized. The variable `tempFahrenheit` is one example of camelCase. Considering the earlier examples, we could use camelCase to write the following.

```python
fmiStationID = "101533"
stationID = "101533"
```

Again, this variable name is clear and easy to read.

### General recommendation

The choice from the formatting options above is yours, but as you may have seen, we tend to utilize pothole_case naming most often in this book. This is because we feel it is the easiest to read and seems to be most common amongst Python programmers. You are welcome to use either option, as long as you are consistent in the use. It might take an extra second of thought, but selecting and formatting your variables can make a big difference in the ease of use of your Python programs!
<!-- #endregion -->

## Best practice 2: Describing your code

You code ultimately decides what will be executed by a program, but providing some descriptive text is important for helping users (including you) understand what the code is used for and how certain sections work. In a Jupyter notebook, this text can take two basic forms:

- Code comments: Text within your Python programs that does not get executed when the software is run. This text is mixed within the code and often used to describe how some or all of the code works. There are several styles of code comments in Python, which are described in more detail later in this appendix.
- Markdown text: Text written as plain text with a simple syntax that can be rendered with rich formatting (bold, italics, different font sizes, colors, etc.). In Jupyter notebooks this text is written in Markdown cells and displayed as rich text when the cells are executed. In contrast to code comments, this text is generally intended to provide a broader description of the code or other things needed to understand what you code does.

Below you can find some examples of both below code comments and Markdown text, along with some tips.


### Do I need to describe my code?

Absolutely! Providing comments or Markdown text to describe your code is essential for a number of reasons:

1. Code descriptions make it easier to understand your code. Although good variable names can help you and other users better understand what you code does, your Jupyter notebooks and/or script files are seldom short enough for you to be able to read over the entire code at once and fully understand what is going on. For this reason, comments and Markdown text are essential parts of making sure your notebooks are easy to use and understand section by section.
2. Code descriptions make it easier for other users to use your code. Even when writing simple software it is worthwhile to take the time to include some extra documentation about how it works. Everyone has their own tendencies in how they write their software and by including a few comments and/or Markdown text you can make it much easier for people to understand and use your work.
3. Writing code descriptions can help you debug your code. Over time you will gain more experience with understanding why some piece of code does not work the way it should. One way to help fix (or debug) your code is to add comments stating what each line does. By taking things step by step, you may find that your code actually does not do what you thought, and this can help you be able to find and fix issues.
4. Code descriptions are a big part of why Jupyter notebooks are so powerful. Code comments are quite helpful in general, but one of the biggest features of a Jupyter notebook is the ability to mix rich text with your code. With this platform you can even write scientific texts with embedded code cells to be able to perform calculations, analyze data, and visualize your results. This powerful platform is an excellent open science tool that provides a clear means to reproduce your results on demand.

Below we review the main forms of code descriptions we recommend using in your Jupyter notebooks and Python script files.


### But the Internet says I should not comment my code...

Some programmers advocate that people should not need to comment their code if it is easily understood. In essence, the argument is that if you need comments to understand what the code does, it is not good code. The advice is not that you should never comment in your code, but rather that comments are really only needed to describe why something is done a given way (not what is done). While this is true to a degree, this advice does not apply to most of us.

Most of us are only just getting started with programming, and our comments serve a bit different purpose. For new programmers, comments make sure we understand what each line of our code does and helps others who you share your code with understand as well. In addition, writing comments can make you pause, look at your code, and then come up with a way to describe what you have done. For new programmers, this makes for excellent practice!

<!-- #region -->
### Code comments - single-line comments

Single-line comments begin with the `#` character, typically as the first character on the line, and everything to the right of that character will be ignored by the Python interpreter. These comments are most frequently used to describe individual lines of code or a small group of related lines. Let's have a look at an example.

```python
# This is a line comment. It will be ignored when this cell is run
```

If you were to run the cell above, nothing would happen. The `#` character indicates the line contains a comment and the Python interpreter simply skips over this line (the only line in that cell).

Let's have a look at a few more examples.

```python
# This list has the names of FMI observation stations in Helsinki
station_names = [
    "Helsinki Harmaja",
    "Helsinki Kaisaniemi",
    "Helsinki Kaivopuisto",
    "Helsinki Kumpula",
]
```

```python
# Print the last station name
print(station_names[-1])  
```

In the examples above you can see some of the ways in which single-line comments can be used in Python. We encourage you to add line comments within your Python cells to help explain what your code does, especially if there are several lines within a given code cell.
<!-- #endregion -->

<!-- #region -->
### Code comments - block comments

Block comments are somewhat similar to single line comments in format, but comprise several lines of consecutive comments rather than just one. These can be useful in situations where a single line comment is not sufficient to describe the code below it or when commenting out several lines of code during debugging, for example. Let's have a look at a few examples of block comments below.

```python
# This doesn't work, so I'm commenting it out for now
# my_life.append(lots_of_money)
```

```python
# Produce a set of subplots showing data from the:
# - Helsinki Harmaja station
# - Helsinki Kaisaniemi station
# - Helsinki Kaivopuisto station
# - Helsinki Kumpula station
fig, ax = plt.subplots(2, 2)
...
```

As you can see, the syntax is familiar for block comments and using them can make sense for helping make your code easier to understand. However, it can become quite tedious to write many lines of block comments, so we'll consider another option below.
<!-- #endregion -->

<!-- #region -->
### Code comments - inline comments

Finally, it is also possible to have inline comments in Python that are formatted similarly to single-line comments but located on the same line as some Python code (typically with at least two spaces after the code). We can see some examples below, but note that inline comments should be used sparingly as single-line comments are generally preferable.

```python
# NO: Unnecessary inline comment example below
print(f"station_names[0]"  # Print the name of the first station
```

```python
# OK: This is a case where an inline comment could be OK
ax2.axis([xmin, xmax, -max_depth / 1000, 0])  # Plot depth in km rather than meters
```
<!-- #endregion -->

<!-- #region -->
### Code comments - multi-line comments

Multi-line comments are similar to both the single line and block comments described earlier; they are embedded within your code and are not executed when a code cell is run. You can begin a multi-line comment with three quotation marks `"""` and end it with the same thing, three quotation marks `"""`. Although it is possible to also create multi-line comments using single quotes (`'''`), use of double quotes (`"""`) is recommended [to be consistent with PEP 257](https://peps.python.org/pep-0257/) [^pep257] about {term}`docstrings <Docstring>`. Everything between the groups of quotation marks will be ignored. Let's see some examples.

```python
"""This text will also be ignored.
Even if it is spread across multiple lines.
Cool! 
"""
```

```python
"""The list below contains names of FMI observation stations in Helsinki.
More information and a complete list of stations can be found at 
https://en.ilmatieteenlaitos.fi/observation-stations.
"""
station_names = [
    "Helsinki Harmaja",
    "Helsinki Kaisaniemi",
    "Helsinki Kaivopuisto",
    "Helsinki Kumpula",
]
```

```python
"""None of the code below works, commenting this out for now.
step_one = learn_to_code()
step_two = become_programmer()
step_three = ???
step_four = profit()
"""
```

As you may recognize, multi-line comments are recommended to be formatted similarly to docstrings and can be a convenient way to have longer code descriptions or comment out larger numbers of lines of code.
<!-- #endregion -->

<!-- #region -->
### Markdown text

Finally, as noted at the start of this best practice topic, we can also use Markdown text cells to provide information about how our code works. The Markdown text is not a replacement for line or block comments in the code cells, but rather a place to provide a broader description of the code. Let's see an example of the use of a Markdown cell below under the heading "Data source". We can first see the Markdown syntax, then the rich-text rendered result. The Markdown syntax is below.

```markdown
#### Data source

Data used in this example comprises observation station:

- names
- locations
- types
- identification codes

These data are sourced from the [Finnish Meterological Institute website](https://en.ilmatieteenlaitos.fi/observation-stations) and are freely available.
The data be easily merged into Python lists manually for further analysis.
An example Python cell with select observation station names in Helsinki is below.
**NOTE**: These are only some of the observation stations in Helsinki.
```
<!-- #endregion -->

And when that Markdown code is executed, the resulting rich text is shown below.

#### Data source

Data used in this example comprises observation station:

- names
- locations
- types
- identification codes

These data are sourced from the [Finnish Meterological Institute website](https://en.ilmatieteenlaitos.fi/observation-stations) and are freely available.
The data be easily merged into Python lists manually for further analysis.
An example Python cell with select observation station names in Helsinki is below.
**NOTE**: These are only some of the observation stations in Helsinki.


In the example above, you clearly see the benefit of the Markdown cells for providing nicely formatted text to support the code block beneath it. We can also embed images and other features that make the Jupyter notebook document a powerful tool for studying and learning. You can find more about the capabilities of Markdown on the [Markdown Guide Basic Syntax](https://www.markdownguide.org/basic-syntax/) [^markdown_basic] and [Extended Syntax](https://www.markdownguide.org/extended-syntax/) [^markdown_extended] guides.


## Best practice 3: Writing readable code

This best practice focuses on writing code that is easy to read. The basic idea here is that well formatted Python code is easier to read and understand.


### Working code vs readable code

As you may have noticed, Python forces you to indent your code when writing loops and conditional statements. Without the indentation the code simply will not work and you will likely see an `IndentationError`.

However, there are many cases in which you are able to write code that runs without errors, but you (or others!) might have a difficult time reading it and understanding what the code actually does. 

Ideally, our Python code would be understandable both for the computer and for humans reading it. [Coding conventions](https://en.wikipedia.org/wiki/Coding_conventions) [^coding_conventions] are a set of generally agreed guidelines for writing code in a specific programming language. Coding conventions help programmers to write code with formatting that is consistent and easy to read. Consistency and readability are important for sharing your code with others, and also for helping your own brain to follow along!

![_**Figure A.X**. The dangers of coding without coding conventions. Source: <https://xkcd.com/1513/>._](../img/code_quality.png)

_**Figure A.X**. The dangers of coding without coding conventions. Source: <https://xkcd.com/1513/>._


### The PEP 8 Style Guide

[The PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/) [^pep8] gives coding conventions that help us write code that is readable (by humans!) and consistent with code written by others.

PEP 8 goes far beyond the scope of what you might learn in this book, so we recommend that you re-visit the guidelines every now and then when learning new things. Here, we will summarize some of the most relevant highlights that you can start applying to your code right away!


### Maximum line length

The PEP 8 guide states all lines should be limited to [79 characters max](https://peps.python.org/pep-0008/#maximum-line-length). Comments (single-line, block, or multi-line) should be limited to 72 characters. Note that we use a line length limit of 88 characters on the online version of this book and 74 characters for the printed book. The character limit according to PEP 8 is 79 characters, but often a slightly longer line (up to 90 characters) helps with readability (and sometimes formats, such as the printed book only allow so many characters to fit on a given line).

One of the guiding principles of Python is that ["Simple is better than complex"](https://peps.python.org/pep-0020/#the-zen-of-python), but sometimes you might end up having a line of code that exceeds 79 characters, for example, when defining lists. 

Fortunately, Python is able to interpret the code correctly from multiple lines within parentheses, brackets and braces, allowing you to avoid excessively long lines in many cases.

```python
# Implicit line continuation inside brackets
us_cities = [
    "Detroit",
    "Chicago",
    "Denver",
    "Boston",
    "Portland",
    "San Francisco",
    "Houston",
    "Orlando",
]
```

Note that the backslash character `\` might be required to break a line when using more complicated statements such as the `with` statement. You can find more examples of how to handle such situations in the [PEP 8 documentation](https://peps.python.org/pep-0008/#maximum-line-length) [^pep8_length].


### Indentation

Indentation is an essential part of the Python code layout. As you may have seen with `for` loops and conditional statements, some things in Python will not work correctly without consistent indentation. PEP 8 recommends using [4 spaces per indentation level](https://peps.python.org/pep-0008/#indentation). 

Let's have a look at an example with `if` statements. The indented line tells Python what to do if the condition is `True`. Notice the 4 spaces for the indentation.

```python
weather = "Rain"
wind = "Windy"

if (weather == "Rain") and (wind == "Windy"):
    print("Just stay at home")
```

Following PEP 8, it is also possible to break the conditional expression into multiple lines if needed. Notice the extra parentheses in this case.

```python
if (weather == "Rain") and (wind == "Windy"):
    print("Just stay at home")
```

To increase readability of this `if` statement, we could add extra indentation to the continuation line of the conditional statement. This is valid Python syntax in line with PEP 8. As you might expect, it is recommended that the additional indendation be 4 spaces.

```python
if (weather == "Rain") and (wind == "Windy"):
    print("Just stay at home")
```

In the cases above, the first option with the conditional expression on a single line is probably best, as it is not that long after all.

In addition, indentation is needed when breaking one command onto multiple lines, such as in our example with the list `us_cities` in the section about maximum line length. In that case we used the implied line continuation inside the brackets. Following the PEP 8 indentation guidelines, we can define `us_cities` also using a [hanging indent](https://peps.python.org/pep-0008/#fn-hi). Note that there is no value on the first line of a list formatted this way.

```python
# Hanging indentation:
us_cities = [
    "Detroit",
    "Chicago",
    "Denver",
    "Boston",
    "Portland",
    "San Francisco",
    "Houston",
    "Orlando",
]
```

You can find more examples of indentation in the [PEP 8 documentation](https://peps.python.org/pep-0008/#indentation) [^pep8_indentation].


### Whitespace and binary operators

PEP 8 states that binary operators should be [surrounded by a single space on either side](https://peps.python.org/pep-0008/#other-recommendations).

We should always do this with:

- assignment (`=`)
- augmented assignment (`+=`, `-=`, etc.)
- comparisons (`==`, `<`, `>`, `!=`, `<>`, `<=`, `>=`, `in`, `not in`, `is`, `is not`)
- Booleans (`and`, `or`, `not`)

```python
# yes
i = 1
i = i + 1
i += 1
```

```python
# no
i = 1
i = i + 1
i += 1
```

If using operators with different priorities you can also do this.

```python
# yes
a = 1
b = 2
c = (a + b) * (a - b)
```

### Avoid extraneous whitespace

PEP 8 also recommends avoiding [having a space between the function name and parentheses when calling a function](https://peps.python.org/pep-0008/#whitespace-in-expressions-and-statements).

```python
# yes
print("Hello")
```

```python
# no
print("Hello")
```

### Write one statement per line    

For readability, it is advised in PEP 8 to [avoid writing multiple statements on the same line](https://peps.python.org/pep-0008/#other-recommendations).

```python
# yes
print("Hello")
print("world")
```

```python
# no
print("Hello")
print("world")
```

```python
# yes
temperature = 17
if temperature > 25:
    print(f"{temperature} is greater than 25")
```

```python
# no
temperature = 17
if temperature > 25:
    print(f"{temperature} is greater than 25")
```

### Code readability versus code length?

You often have to find a balance between code readability and code length when writing efficient and readable code. [Compound statements](https://docs.python.org/3/reference/compound_stmts.html#compound-statements) [^compound_statements] are a way of writing multiple statements on the same line to make the code shorter but they can be more difficult to read, especially for less experienced programmers. Thus, [PEP 8 recommends avoiding compound statements in general](https://peps.python.org/pep-0008/#other-recommendations). However, sometimes squeezing multiple statements might your best option. You you just have to judge for yourself which option makes the code most readable and use that.


### List comprehensions

One puzzling example regarding the number of statements per line is the use of list comprehensions when defining lists. [List comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) [^list_comprehensions] are a useful approach for creating lists in a concise way. We do not cover list comprehensions in this book, but below is a short example from the [Python documentation](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions). In some cases, list comprehensions might make your code more readable and concise. In other cases, you might end up writing an excessively long statement that is difficult to read. Below we can compare two options that both produce the same output.

The first option iterates over a `range` using a `for` loop, squares all values, and appends them to a `list`.

```python
squares = []
for x in range(10):
    squares.append(x**2)
```

The second option does the same thing using a list comprehension.

```python
squares = [x**2 for x in range(10)]
```

Both approaches are fine and you are free to choose the option that you think makes your code more readable.

<!-- #region -->
## Best practice 4: Using modules

**What should be added here???**



The use of modules is introduced in Chapter 2.8 including some essential  

### Import modules at the start of your files

According to the good coding practices described in [PEP 8](https://peps.python.org/pep-0008/#imports) [^pep8_imports], we should always import modules at the top of a file. In this section, we have demonstrated how to import different modules along the way, but in general it is better to import required modules as the very first thing. PEP 8 refers more to traditional script files, but we can apply the guideline to Jupyter Notebook files as well by placing `import` statements in the first code cell of the notebook.

### Avoid importing functions using wildcards

It is best not to import many functions from a module using the form `from X import *`, where `X` is a Python module. `from X import *` will import all of the functions in module X, and though you might think this is helpful, it is much better to simply `import X` or `import X as Y` to maintain the connection between the functions and their module. In addition to losing the connection between the module and the function, it is much more likely you will encounter conflicting function names when using `from X import *`.

### Choose logical names when renaming on import

Do not use confusing names when renaming on import. Be smart when you import modules, and follow generally used conventions (`import pandas as pd` is a good way to do things!). If you want to make the module name shorter on import, pick a reasonable abbreviation. For instance, `import matplotlib as m` could be confusing, especially if we used `import math as m` above and might do so in other Jupyter notebooks or script files. Similarly, `import matplotlib as math` is perfectly OK syntax in Python, but bound to cause trouble. Remember, people need to be able to read and understand the code you write. Keep it simple and logical.
<!-- #endregion -->

## Best practice 5: Using assertions

[Defensive programming](https://en.wikipedia.org/wiki/Defensive_programming) aims to maximize the reliability and overall quality of a piece of software. For us, this means that we should take steps to handle unexpected input values in our code, and to provide helpful error messages that provide meaningful guidance to the user when a program raises an exception. We can take steps toward writing more reliable software by utilizing a helpful features in Python: Assertions.

### Assertions

{term}`Assertions <Assertion>` are a way to assert, or ensure, that the values being used in your scripts are going to be suitable for what the code does. Let's start by considering the function `convert_kph_ms()` that converts wind speeds from kilometers per hour to meters per second. We can define and use the function in the cell below.

```python
def convert_kph_ms(speed):
    """Converts velocity (speed) in km/hr to m/s"""
    return speed * 1000 / 3600


wind_speed_km = 9
wind_speed_ms = convert_kph_ms(wind_speed_km)

print(f"A wind speed of {wind_speed_km} km/hr is {wind_speed_ms} m/s.")
```

This all seems fine but you might want to ensure that the values for the wind speed are not negative numbers, since speed is the magnitude of the wind velocity and should always be positive or zero. An assertion can be used to enforce this condition by adding an `assert` statement to the function.

```python
def convert_kph_ms(speed):
    """Converts velocity (speed) in km/hr to m/s"""
    assert speed >= 0.0
    return speed * 1000 / 3600


wind_speed_km = 9
wind_speed_ms = convert_kph_ms(wind_speed_km)

print(f"A wind speed of {wind_speed_km} km/hr is {wind_speed_ms} m/s.")
```

OK, so everything still works when using a positive value for `speed` but what happens if a negative value is given for the wind speed?

```python
wind_speed_km = -27
wind_speed_ms = convert_kph_ms(wind_speed_km)

print(f"A wind speed of {wind_speed_km} km/hr is {wind_speed_ms} m/s.")
```

Now we get an `AssertionError` when a negative value is provided. This `AssertionError` is produced because of the `assert` statement in the function definition. If the condition listed after `assert` is `False`, an `AssertionError` will be raised when the code is executed.

This is a definite improvement compared to the first example using the `convert_kph_ms()` function, however it would be much better to provide the user with some information about why this assertion exists. Fortunately, we can do this simply by adding some text after the condition in the assertion.

```python
def convert_kph_ms(speed):
    """Converts velocity (speed) in km/hr to m/s"""
    assert speed >= 0.0, "Wind speed values must be positive or zero"
    return speed * 1000 / 3600


wind_speed_km = -27
wind_speed_ms = convert_kph_ms(wind_speed_km)

print(f"A wind speed of {wind_speed_km} km/hr is {wind_speed_ms} m/s.")
```

<!-- #region -->
Nice! Now we see that when the `AssertionError` is raised, the message informs us about why it happened without having to interpret the code. The message also makes it easy to fix our value for `wind_speed_km` to work with the `convert_kph_ms()` function.

In general, assertions take the following form:

```python
assert <some condition>, "Error message to display"
```

So they start with an `assert` statement, then list a logical test for some condition, and optionally have a text string that follows the condition, separated by a comma. If the test evaluates as `True` then nothing happens and the code continues. Otherwise, the code stops, an `AssertionError` is displayed, and any included text is written to the screen.
<!-- #endregion -->

### Multiple assertions - a bad example

Of course, you may want to have several assertions in a function in order to ensure it works as expected and provides meaningful output. In our case, we might first want to check that the value provided for conversion from km/hr to m/s is a number. If it is not, we would not be able to convert the units properly. Let's add a second assertion to make sure our function is "safe".

```python
def convert_kph_ms(speed):
    """Converts velocity (speed) in km/hr to m/s"""
    assert (
        type(speed) == int or type(speed) == float
    ), "Wind speed values must be numbers"
    assert speed >= 0.0, "Wind speed values must be positive or zero"
    return speed * 1000 / 3600


wind_speed_km = "dog"
wind_speed_ms = convert_kph_ms(wind_speed_km)

print(f"A wind speed of {wind_speed_km} km/hr is {wind_speed_ms} m/s.")
```

OK, so that works. Now, if the user attempts to give a data type that is not `int` or `float`, the function will raise an `AssertionError` indicating a number is expected for the function to work. This is fine, but there are reasons why you may not want to include assertions of this type in a function.

You might think that it would be useful to use an assertion to check the type of `speed` in our function in order to avoid getting a `TypeError` if an incompatible data type is provided. However, this is not really a good idea. The reason is that a `TypeError` is designed to indicate you have incompatible data types. Thus is makes no sense to raise an `AssertionError` that does the same thing. Thus, it is better to allow the code to fail with a `TypeError` in such cases and reserve the assertions for testing values that should be used or produced by the code.


### Multiple assertions - a better example

So we might not want to check our data type compatibility using assertions, but we can include a second assertion to ensure the input wind speed is a reasonable number. In this case, we can assume that the wind speed being converted was measured on Earth, and thus should be lower than [the fastest wind speed ever measured](https://en.wikipedia.org/wiki/Wind_speed#Highest_speed), 408 km/hr. Let's add that condition.

```python
def convert_kph_ms(speed):
    """Converts velocity (speed) in km/hr to m/s"""
    assert speed >= 0.0, "Wind speed values must be positive or zero"
    assert speed <= 408.0, "Wind speed exceeds fastest winds ever measured"
    return speed * 1000 / 3600


wind_speed_km = "409"
wind_speed_ms = convert_kph_ms(wind_speed_km)

print(f"A wind speed of {wind_speed_km} km/hr is {wind_speed_ms} m/s.")
```

This is a better example for two reasons:

1. We now allow a `TypeError` when incompatible data types are used in our function, which is a clear and familiar error message.
2. We use assertions to check the values used in the function make sense for its intended use. If we want to help users convert wind speeds on Earth, we provide bounds that make sure they are using reasonable input values. Thus, we help them use our function the correct way.

Combined, these assertions ensure our function handles common mistakes and provide the user with helpful feedback to be able to use the function properly.

### A final note about assertions

One thing that is important to note about assertions is that although we use them here to check that our function input values are reasonable, this is not generally the suggested use. Instead, more advanced programmers recommend using assertions only to test that your code is working properly internally. For example, you would use assertions to check for things that should not happen, such as functions that duplicate values in lists when they should not. The reason it is not recommended to use assertions for testing user input values or the existence of files is that assertions can be disabled using flags when running a Python program. Thus, it is possible they could be ignored entirely. This is fine when debugging code, but obviously not desired when users are running your programs. If you're interested in more details, you can find more in [an article on using assertions in the Python wiki](https://wiki.python.org/moin/UsingAssertionsEffectively) [^wiki_assertions] or on the [Software Carpentry website](https://swcarpentry.github.io/python-novice-inflammation/10-defensive.html) [^swc_assertions].


## Footnotes

[^ascii]: <https://en.wikipedia.org/wiki/ASCII#Printable_character_table>
[^coding_conventions]: <https://en.wikipedia.org/wiki/Coding_conventions>
[^compound_statements]: <https://docs.python.org/3/reference/compound_stmts.html#compound-statements>
[^keywords]: <https://www.geeksforgeeks.org/python-keywords/>
[^list_comprehensions]: <https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions>
[^markdown_basic]: <https://www.markdownguide.org/basic-syntax/>
[^markdown_extended]: <https://www.markdownguide.org/extended-syntax/>
[^pep8]: <https://peps.python.org/pep-0008/>
[^pep8_imports]: <https://peps.python.org/pep-0008/#imports>
[^pep8_indentation]: <https://peps.python.org/pep-0008/#indentation>
[^pep8_length]: <https://peps.python.org/pep-0008/#maximum-line-length>
[^pep257]: <https://peps.python.org/pep-0257/>
[^swc_assertions]: <https://swcarpentry.github.io/python-novice-inflammation/10-defensive.html>
[^wiki_assertions]: <https://wiki.python.org/moin/UsingAssertionsEffectively>
