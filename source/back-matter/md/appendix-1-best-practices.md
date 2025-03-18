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
## Selecting variable names

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

### Recommended variable format 1: camelCase naming

*{term}`camelCase or CamelCase naming <Camel case>`* uses capitalization of the first letter of words in a variable name to make it easier to read. In some cases the first letter of the variable may be capitalized. The variable `tempFahrenheit` is one example of camelCase. Considering the earlier examples, we could use camelCase to write the following.

```python
fmiStationID = "101533"
stationID = "101533"
```

Again, this variable name is clear and easy to read.

### General recommendation

The choice from the formatting options above is yours, but as you may have seen, we tend to utilize pothole_case naming most often in this book. This is because we feel it is the easiest to read and seems to be most common amongst Python programmers. You are welcome to use either option, as long as you are consistent in the use. It might take an extra second of thought, but selecting and formatting your variables can make a big difference in the ease of use of your Python programs!
<!-- #endregion -->

## Using modules

### Import modules at the start of your files

According to the good coding practices described in [PEP 8](https://peps.python.org/pep-0008/#imports) [^pep8], we should always import modules at the top of a file. In this section, we have demonstrated how to import different modules along the way, but in general it is better to import required modules as the very first thing. PEP 8 refers more to traditional script files, but we can apply the guideline to Jupyter Notebook files as well by placing `import` statements in the first code cell of the notebook.

### Avoid importing functions using wildcards

It is best not to import many functions from a module using the form `from X import *`, where `X` is a Python module. `from X import *` will import all of the functions in module X, and though you might think this is helpful, it is much better to simply `import X` or `import X as Y` to maintain the connection between the functions and their module. In addition to losing the connection between the module and the function, it is much more likely you will encounter conflicting function names when using `from X import *`.

### Choose logical names when renaming on import

Do not use confusing names when renaming on import. Be smart when you import modules, and follow generally used conventions (`import pandas as pd` is a good way to do things!). If you want to make the module name shorter on import, pick a reasonable abbreviation. For instance, `import matplotlib as m` could be confusing, especially if we used `import math as m` above and might do so in other Jupyter notebooks or script files. Similarly, `import matplotlib as math` is perfectly OK syntax in Python, but bound to cause trouble. Remember, people need to be able to read and understand the code you write. Keep it simple and logical.


## Footnotes

[^ascii]: <https://en.wikipedia.org/wiki/ASCII#Printable_character_table>
[^keywords]: <https://www.geeksforgeeks.org/python-keywords/>
[^pep8]: <https://peps.python.org/pep-0008/#imports>
