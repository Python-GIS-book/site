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
# Conditional statements

In this section, we will learn how to make choices in our code using conditional statements (`if`, `elif`, `else`) and Boolean values (`True`, `False`). 

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Basics of conditional statements

Conditional statements can change the code behaviour based on certain conditions. The idea is simple: If a condition is met, then a set of actions will be performed. 
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### A simple conditional statement

Let’s look at a simple example with temperatures, and check if a temperature of 17 degrees Celsius is hot or not.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temperature = 17

if temperature > 25:
    print(f"{temperature} is hot!")
else:
    print(f"{temperature} is not hot!")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
What did we do here? First, we used the `if` and `else` statements to determine what parts of the code to execute. The `if` statement checks to see whether the variable value for `temperature` is greater than 25 (hot by northern European standards). If this condition is true, `'17 is hot'` will be written to the screen. Since 17 is smaller than 25, the `if` condition is false and thus the code beneath the `else` statement is executed. The code under the `else` statement will run whenever the `if` condition is false.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's update `temperature` to a "hot" temperature and repeat the same process.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temperature = 30

if temperature > 25:
    print(f"{temperature} is hot!")
else:
    print(f"{temperature} is not hot!")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
In this case, the `if` statement is true and thus `'30 is hot'` is printed.
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
Makes sense, right? Conditional statements always check if the conditional expression evaluates as `True` or `False`. If true, the codeblock under the conditional statement gets executed. In this example, nothing is printed to the screen if temperature is smaller than 25.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's look at another example from our daily lives. As it turns out, we all use logic similar to `if` and `else` conditional statements daily. Imagine you’re getting ready to leave your home for the day and want to decide what to wear. You might look outside to check the weather conditions. If it is raining, you will wear a rain jacket.
Otherwise, you will not. Python uses the `==` operator to test if a value is exactly equal to another.
<!-- #endregion -->

```python
weather = "rain"

if weather == "rain":
    print("Wear a raincoat!")
else:
    print("No raincoat needed.")
```

As with `for` loops, Python uses colons (`:`) and white space (indentations) to structure conditional statements. If the condition is `True`, the indented code block after the colon (`:`) is executed. The code block may contain several lines of code, but they all must be indented equally. You will receive an `IndentationError`, a `SyntaxError`, or unwanted behavior if you haven't indented your code correctly.

Note also that the case of the text being compared (uppercase or lowercase) is important. For instance, in the example above, if we define `weather = "Rain"`, the comparison `weather == "rain"` would be false. One possible solution to this problem is to use the `.lower()` method for strings, which would convert the text to which it is applied to lowercase. In the example here, if we define `weather = "Rain"`, the comparison `weather.lower() == "rain"` would be true!

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.9

We might also need some other rain gear on a rainy day. Think about how you could add another instruction after the `weather == "rain"` condition so that the code would tell us to:

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

| Operator | Description              | Comparison example | Result  |
|:--------:|:-------------------------|:------------------:|:-------:|
| `==`     | Equal to                 | `"cat" == "dog"`   | `False` |
| `!=`     | Not equal to             | `"cat" != "dog"`   | `True`  |
| `<`      | Less than                | `2 < 1`            | `False` |
| `>`      | Greater than             | `2 > 1`            | `True`  |
| `<=`     | Less than or equal to    | `2 <= 2`           | `True`  |
| `>=`     | Greater than or equal to | `2 >= 4`           | `False` |


### Boolean values

As shown in Table 2.3, comparison operations yield Boolean values (`True` or `False`). In Python, the words `True` and `False` are reserved for these Boolean values and cannot be used for other purposes.

To demonstrate this, let's check the current value of the conditions we used in the previous examples:

```python
temperature > 25
```

```python
weather == "rain"
```

### if, elif and else

We can link several conditions together using the "else if" statement `elif`. Python checks the `elif` and `else` statements only if previous conditions were `False`. You can have multiple `elif` statements to check for additional conditions. Let's create a chain of `if`, `elif`, and `else` statements that are able to tell us if the temperature is above freezing, exactly at the freezing point, or below freezing.

```python
temperature = -3
```

```python
if temperature > 0:
    print(f"{temperature} degrees Celsius is above freezing")
elif temperature == 0:
    print(f"{temperature} degrees Celsius is at the freezing point")
else:
    print(f"{temperature} degrees Celsius is below freezing")
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 2.10

Let's assume that yesterday it was 14 °C, it is 10 °C outside today, and tomorrow it will be 13 °C.
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

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Combining conditions

We can also use the `and` and `or` operators to combine multiple conditions that use Boolean values (Table 2.4).
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["remove_book_cell"] -->
<!-- WARNING: If you update the contents of this cell, you must also update the LaTeX table in the following cell! -->
: _**Table 2.4**. Logic for the `and`, `or`, and `not` operators in Python._

| Operator | Description                                | Comparison example | Result  |
|:--------:|:-------------------------------------------|:------------------:|:-------:|
| `and`    | True only if both comparisons are true     | `2 > 1 and 1 < 0`  | `False` |
| `or`     | True if either comparison is true          | `2 > 1 or 1 < 0`   | `True`  |
| `not`    | False if comparison is true and vice versa | `not 2 > 1`        | `False` |
<!-- #endregion -->

<!-- #raw editable=true slideshow={"slide_type": ""} tags=["hide-cell"] raw_mimetype="" -->
\begin{longtable}[]{@{}clcc@{}}
\caption{\emph{\textbf{Table 2.4}. Logic for the \texttt{and},
\texttt{or}, and \texttt{not} operators in Python.}}\tabularnewline
\toprule\noalign{}
Operator & Description & Comparison example & Result \\
\midrule\noalign{}
\endfirsthead
\toprule\noalign{}
Operator & Description & Comparison example & Result \\
\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
~\texttt{and} & True only if both &
\texttt{2\ \textgreater{}\ 1\ and\ 1\ \textless{}\ 0} &
\texttt{False} \\
& comparisons are true & & \\
~\texttt{or} & True if either &
\texttt{2\ \textgreater{}\ 1\ or\ 1\ \textless{}\ 0} & \texttt{True} \\
& comparison is true & & \\
~\texttt{not} & False if comparison is &
\texttt{not\ 2\ \textgreater{}\ 1} & \texttt{False} \\
& true and vice versa & & \\
\end{longtable}
<!-- #endraw -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
With Table 2.4 in mind, let's consider a few examples.
<!-- #endregion -->

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

Let's return to our example about making decisions on a rainy day. Imagine that we consider not only the rain but also the wind speed (in meters per second). If it is windy or raining, we’ll just stay at home. If it's not windy or raining, we can go out and enjoy the weather! 

Let's set 10 m/s as our comfort limit for wind speed in the conditional statement and see what our Python program tells us to do in these conditions.
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

Finally, we can also combine `for` loops and conditional statements. Let's use a `for` loop to iterate over a list of temperatures and check whether the temperature is hot or not.
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
