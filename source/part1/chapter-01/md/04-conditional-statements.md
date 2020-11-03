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

# Conditional statements

In this lesson we will learn how to make choices in our code using conditional statements (`if`, `elif`, `else`) and Boolean values (`True`, `False`). 

This section was inspired by the Programming in Python lessons {cite}`Bostroem2016` from the Software Carpentry organization [^swc] and the Python for Data Analysis book {cite}`McKinney2017`.

## Basics of conditional statements

Conditional statements can change the code behaviour based on certain conditions. The idea is simple: **IF** a condition is met, **THEN** a set of actions is performed. 

### A simple conditional statement

**Let’s look at a simple example with temperatures**, and check if temperature 17 (celsius degrees) is hot or not:

```python
temperature = 17

if temperature > 25:
    print('it is hot!')
else:
    print('it is not hot!')
```

What did we do here?
First, we used the `if` and `else` statements to determine what parts of the code to execute.

What do these tests do?
The `if` statement checks to see whether the variable value for `temperature` is greater than 25.
If this condition is met, `'it is hot'` would be written to the screen. 
Since 17 is smaller than 25, the code beneath `else` is executed.
Code under the `else` statement will run whenever the `if` test is `False`.


#### Check your understanding 

Update the value of `temperature` to a "hot" temperature:

```python
# Here's one possible solution
temperature = 30

if temperature > 25:
    print('it is hot!')
else:
    print('it is not hot!')
```

The code indented under the if-statement is not executed if the condition is not True. Instead, code under the else-statement gets executed.


```{admonition} if without else?
The combination of `if` and `else` is very common, but the `else` statement is not strictly required. Python simply does nothing if the `if` statement is False and there is no `else` statement. 
```


Try it out yourself by typing in the previous example without the else-statement:

```python
temperature = 17

if temperature > 25:
    print(temperature,'is greater than 25')
```

Makes sense, right? Conditional statements always check if the conditional expression is **True** or **False**. If True, the codeblock under the conditional statement gets executed.


Nothing is printed to the screen if temperature is smaller than 25.


**Let's look at another example from our daily lives**

As it turns out, we all use logic similar to `if` and `else` conditional statements daily.
Imagine you’re getting ready to leave your home for the day and want to decide what to wear.
You might look outside to check the weather conditions.
If it is raining, you will wear a rain jacket.
Otherwise, you will not.
In Python we could say:

```python
weather = 'rain'

if weather == 'rain':
    print('Wear a raincoat!')
else:
    print('No raincoat needed.')
```

Note here that we use the `==` operator to test if a value is exactly equal to another.


```{admonition} Note the syntax
Similarly as with for loops, Python uses colons (`:`) and whitespace (indentations; often four spaces) to structure conditional statements. If the condition is `True`, the indented code block after the colon (`:`) is executed. The code block may contain several lines of code, but they all must be indented identically You will receive an `IndentationError`, a `SyntaxError`, or unwanted behavior if you haven't indented your code correctly.
```


#### Check your understanding 

We might also need some other rainwear on a rainy day. Let's add another instruction after the `weather == rain` condition so that the code would tell us to:

``` 
Wear a raincoat
Wear rain boots
```

```python
# Here's one possible solution
weather = 'rain'

if weather == 'rain':
    print('Wear a raincoat')
    print('Wear rain boots')
else:
    print('No rainwear needed')
```

### Comparison operators

Comparison operators such as `>` and `==` compare the values on each side of the operator. Here is the full list of operators used for value comparisons in Python: 

| Operator | Description              |
| -------- | ------------------------ |
| <        | Less than                |
| <=       | Less than or equal to    |
| ==       | Equal to                 |
| >=       | Greater than or equal to |
| >        | Greater than             |
| !=       | Not equal to             |

**Table 1.3**. Comparison operators in Python.


### Boolean values
Comparison operations yield boolean values (`True` or `False`). In Python, the words `True` and `False` are reserved for these Boolean values, and can't be used for anything else. 

Let's check the current value of the conditions we used in the previous examples:

```python
temperature > 25
```

```python
weather == 'rain'
```

### if, elif and else

We can link several conditions together using the "else if" -statement `elif`. Python checks the `elif` and `else` statements only if previous conditions were `False`. You can have multiple `elif` statements to check for additional conditions.


Let's create a chain of `if` `elif` and `else` -statements that are able to tell us if the temperature is above freezing, exactly at freezing point or below freezing:

```python
temperature = -3
```

```python
if temperature > 0:
     print(temperature, 'degrees celsius is above freezing')
elif temperature == 0:
     print(temperature, 'degrees celsius is at the freezing point')
else:
     print(temperature, 'degrees celsius is below freezing')
```

<!-- #region -->
### Check your understanding

Let's assume that yesterday it was 14°C, it is 10°C outside today, and tomorrow it will be 13°C.
The following code compares these temperatures and prints something to the screen based on the comparison.

```python
yesterday = 14
today = 10
tomorrow = 13

if yesterday <= today:
    print('A')
elif today != tomorrow:
    print('B')
elif yesterday > tomorrow:
    print('C')
elif today == today:
    print('D')
```

Which of the letters `A`, `B`, `C`, and `D` would be printed to the screen?
Select your answer from the poll options at https://geo-python.github.io/poll/.
<!-- #endregion -->

```python
# Here is the solution
yesterday = 14
today = 10
tomorrow = 13

if yesterday <= today:
    print('A')
elif today != tomorrow:
    print('B')
elif yesterday > tomorrow:
    print('C')
elif today == today:
    print('D')
```

### Combining conditions

We can also use `and` and `or` to combine multiple conditions on boolean values.


| Keyword   |example   | Description                          |
| --------- |--------- |------------------------------------- |
|  and      | a and b  | True if both a and b are True        |
|  or       | a or b   | True if either a or b is True        |

```python
if (1 > 0) and (-1 > 0):
     print('Both parts are true')
else:
     print('At least one part is not true')
```

```python
if (1 < 0) or (-1 < 0):
    print('At least one test is true')
```

```{admonition} Note the syntax
Later on we will also need the bitwise operators `&` for `and`, and `|` for `or`.
```


#### Check your understanding 

**Let's return to our example about making decisions on a rainy day.** Imagine that we consider not only the rain, but also the wind speed. If it is windy or raining, we’ll just stay at home. If it's not windy or raining, we can go out and enjoy the weather! 

8 m/s is the limit for a "fresh breeze" (*navakka tuuli* in Finnish) and we can set that as our comfort limit in the conditional statement. The Finnish Meteorological Institute forecasts strong winds in Helsinki on the day of giving this lesson (https://en.ilmatieteenlaitos.fi/local-weather/helsinki), so let's see what our Python program tells us to do these days:

```python
weather = 'rain'
wind_speed = 9

# If it is windy or raining, print "stay at home", else print "go out and enjoy the weather!"
if (weather == 'rain') or (wind_speed >= 8):
    print('Just stay at home')
else:
    print('Go out and enjoy the weather! :)')
```

As you can see, we better just stay home if it is windy or raining! If you don't agree, you can modify the conditions and print statements accordingly.


## Combining for-loops and conditional statements

Finally, we can also combine for-loops and conditional statements. Let's iterate over a list of temperatures, and check if the temperature is hot or not:

```python
temperatures = [0, 12, 17, 28, 30]

# For each temperature, if the temperature is greater than 25, print "..is hot"
for temperature in temperatures:
    if temperature > 25:
        print(temperature, 'is hot')
    else:
        print(temperature, 'is not hot')
```

## Footnotes

[^swc]: <http://software-carpentry.org>
