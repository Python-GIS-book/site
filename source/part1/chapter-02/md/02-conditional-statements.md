---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.15.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} -->
# Conditional statements

Next, we will learn how to make choices in our code using conditional statements (`if`, `elif`, `else`) and Boolean values (`True`, `False`). 

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Basics of conditional statements

Conditional statements can change the code behaviour based on certain conditions. The idea is simple: If a condition is met, then a set of actions is performed. 
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### A simple conditional statement

Let’s look at a simple example with temperatures, and check if temperature 17 (celsius degrees) is hot or not:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temperature = 17

if temperature > 25:
    print(f"{temperature} is hot!")
else:
    print(f"{temperature} is not hot!")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
What did we do here? First, we used the `if` and `else` statements to determine what parts of the code to execute. The `if` statement checks to see whether the variable value for `temperature` is greater than 25. If this condition were true, `'17 is hot'` would be written to the screen. Since 17 is smaller than 25, the `if` condition is false and thus the code beneath `else` is executed. The code under the `else` statement will run whenever the `if` condition is false.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's update `temperature` to a "hot" temperature and repeat the same process:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temperature = 30

if temperature > 25:
    print(f"{temperature} is hot!")
else:
    print(f"{temperature} is not hot!")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
In this case, the `if` statement is true, and thus `'30 is hot'` is printed.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
How about `if` without `else`? The combination of `if` and `else` is very common, but the `else` statement is not strictly required. Python simply does nothing if the `if` statement is false and there is no `else` statement. 
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temperature = 17

if temperature > 25:
    print(f"{temperature} is greater than 25")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Makes sense, right? Conditional statements always check if the conditional expression evaluates as `True` or `False`. If true, the codeblock under the conditional statement gets executed. Nothing is printed to the screen if temperature is smaller than 25.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's look at another example from our daily lives. As it turns out, we all use logic similar to `if` and `else` conditional statements daily. Imagine you’re getting ready to leave your home for the day and want to decide what to wear. You might look outside to check the weather conditions. If it is raining, you will wear a rain jacket.
Otherwise, you will not. Remember that Python uses the `==` operator to test if a value is exactly equal to another.
<!-- #endregion -->

```python
weather = "rain"

if weather == "rain":
    print("Wear a raincoat!")
else:
    print("No raincoat needed.")
```

Similarly as with for loops, Python uses colons (`:`) and whitespace (indentations; often four spaces) to structure conditional statements. If the condition is `True`, the indented code block after the colon (`:`) is executed. The code block may contain several lines of code, but they all must be indented identically You will receive an `IndentationError`, a `SyntaxError`, or unwanted behavior if you haven't indented your code correctly.

Note also that the case of the text being compared (uppercase or lowercase) is important. For instance, in the example above, if we define `weather = 'Rain'`, the comparsion `weather == 'rain'` would be false. One possible solution to this problem is to use the `.lower()` method for strings, which would convert the text to which it is applied to lowercase. In the example here, if we define `weather = Rain`, the comparison `weather.lower() == 'rain'` would be true!

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.9

We might also need some other rainwear on a rainy day. Think about how you could add another instruction after the `weather == rain` condition so that the code would tell us to:

``` 
Wear a raincoat
Wear rain boots
```
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["hide-cell", "remove_book_cell"]
# Solution

weather = "rain"

if weather == "rain":
    print("Wear a raincoat")
    print("Wear rain boots")
else:
    print("No rainwear needed")
```

### Comparison operators

Comparison operators such as `>` and `==` compare the values on each side of the operator. Table 2.3 lists operators used for value comparisons in Python: 

: _**Table 2.3**. Comparison operators in Python._

|Operator |Description              |
|:--------|:------------------------|
|`<`      |Less than                |
|`<=`     |Less than or equal to    |
|`==`     |Equal to                 |
|`>=`     |Greater than or equal to |
|`>`      |Greater than             |
|`!=`     |Not equal to             |


### Boolean values
Comparison operations yield boolean values (`True` or `False`). In Python, the words `True` and `False` are reserved for these Boolean values, and can't be used for anything else. 

Let's check the current value of the conditions we used in the previous examples:

```python
temperature > 25
```

```python
weather == "rain"
```

### if, elif and else

We can link several conditions together using the "else if" -statement `elif`. Python checks the `elif` and `else` statements only if previous conditions were `False`. You can have multiple `elif` statements to check for additional conditions. Let's create a chain of `if` `elif` and `else` -statements that are able to tell us if the temperature is above freezing, exactly at freezing point or below freezing:

```python
temperature = -3
```

```python
if temperature > 0:
    print(temperature, "degrees celsius is above freezing")
elif temperature == 0:
    print(temperature, "degrees celsius is at the freezing point")
else:
    print(temperature, "degrees celsius is below freezing")
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.10

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

Which of the letters `A`, `B`, `C`, and `D` would be printed out?
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["hide-cell", "remove_book_cell"]
# Solution

"B"
```

### Combining conditions

We can also use `and` and `or` to combine multiple conditions on boolean values (Table 2.4).


: _**Table 2.4**. Logic for the `and` and `or` keywords in Python._

|Keyword   | Example   |Description                          |
|:---------|:---------:|:------------------------------------|
|`and`     | `a and b` |True if both `a` and `b` are True    |
|`or`      | `a or b`  |True if either `a` or `b` is True    |

```python editable=true slideshow={"slide_type": ""}
hot_temperature = 35.0
warm_temperature = 24.0
cold_temperature = -4.0

if (hot_temperature > warm_temperature) and (cold_temperature > warm_temperature):
    print("Both parts are true")
else:
    print("At least one part is not true")
```

```python editable=true slideshow={"slide_type": ""}
if (hot_temperature < warm_temperature) or (cold_temperature < warm_temperature):
    print("At least one test is true")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Later in this book we will also see how to use the bitwise operators `&` for `and`, and `|` for `or`.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.11

Let's return to our example about making decisions on a rainy day. Imagine that we consider not only the rain, but also the wind speed (in meters per second). If it is windy or raining, we’ll just stay at home. If it's not windy or raining, we can go out and enjoy the weather! 

Let's set 10 m/s as our comfort limit in the conditional statement and see what our Python program tells us to do in these conditions:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["hide-cell", "remove_book_cell"]
# Solution

weather = "rain"
wind_speed = 14
comfort_limit = 10

# If it is windy or raining, print "stay at home",
# otherwise (else) print "go out and enjoy the weather!"
if (weather == "rain") or (wind_speed >= comfort_limit):
    print("Just stay at home")
else:
    print("Go out and enjoy the weather! :)")
```

As you can see, we better just stay home if it is windy or raining! If you don't agree, you can modify the conditions and print statements accordingly.

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Combining for loops and conditional statements

Finally, we can also combine for-loops and conditional statements. Let's iterate over a list of temperatures, and check if the temperature is hot or not:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temperatures = [0, 28, 12, 17, 30]

# Loop over each temperature
# If the temperature is greater than 25, print "...is hot"
for temperature in temperatures:
    if temperature > 25:
        print(f"{temperature} is hot")
    else:
        print(f"{temperature} is not hot")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Footnotes

<!-- #endregion -->
