---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Exercises


## Exercise 2.1 - Getting started with Python

The goal of this exercise is to print text like that below to the screen based on variable values you define.

```
My name is Dave and I give eating ice cream a score of 9 out of 10!
My sleeping enjoyment rating is 8 / 10!
Based on the factors above, my happiness rating is 8.5 out of 10 or 85.0 %!
```
For this exercise you should:

- Create three variables: one integer value (whole number) for your ice cream rating, another integer for your sleeping rating, and a character string for your first name. 
- Calculate the average of the two ratings. Store the result in a variable for your happiness.
- Find the data type of each of the variables you have defined. Are there any surprises?
- Reproduce your version of the example text using the `print()` function and the variables you have defined. Note that you may need to be careful combining text and numbers!


## Exercise 2.2 - Creating and changing lists

![_**Tables 2.5 and 2.6**. [FMI observation stations](http://en.ilmatieteenlaitos.fi/observation-stations) and the years in which they began operating_.](../img/exercise-2.2-tables.png)

_**Tables 2.5 and 2.6**. [FMI observation stations](http://en.ilmatieteenlaitos.fi/observation-stations) and the years in which they began operating_.

For this exercise you should use the data in Tables 2.5 and 2.6 to:

- Create two lists for the station names and first years of operation for the values in Table 2.5 (on the left) only. Be sure to list the values in the order they appear in the table.
- Modify the lists you just created to add the values from Table 2.6 (on the right), again keeping them in the same order.
- Sort the two lists, sorting the first in alphabetical order and the second so that the most recent starting year is first
    - Do you see any problems with how the lists have been sorted?
    - Python has a function called `zip()` that might be helpful in solving the sorting issue. Search online to see whether you can find a way to use `zip()` to solve the problem with the two lists.


## Exercise 2.3 - Lists and index values

![_**Table 2.7**. [Monthly average temperatures recorded at the Helsinki Malmi airport](https://www.timeanddate.com/weather/finland/helsinki/climate)_.](../img/exercise-2.3-table.png)

_**Table 2.7**. [Monthly average temperatures recorded at the Helsinki Malmi airport](https://www.timeanddate.com/weather/finland/helsinki/climate)._

For this exercise you should use the data in Table 2.7 to:

- Create two lists with the months and their average temperatures.
- Use a print statement to produce output like that below, where the months and temperatures are selected using index values in the corresponding lists.

```
The average temperature in Helsinki in March is -1.0
```


## Exercise 2.4 - Batch processing files with a `for` loop

Batch processing is a common task in Python, where a set of data and/or files are analyzed one after another using the same script or program. In this exercise your goal is to produce a Python list of filenames that could be used to batch process the data they contain.

For this exercise you should:

- Use a `for` loop to create a Python list that produces the output below when you print the list:

    ```
    ['Station_0.txt', 'Station_1.txt', 'Station_2.txt', 'Station_3.txt',
     'Station_4.txt', 'Station_5.txt', 'Station_6.txt', 'Station_7.txt',
     'Station_8.txt', 'Station_9.txt', 'Station_10.txt', 'Station_11.txt',
     'Station_12.txt', 'Station_13.txt', 'Station_14.txt', 'Station_15.txt',
     'Station_16.txt', 'Station_17.txt', 'Station_18.txt', 'Station_19.txt',
     'Station_20.txt']
    ```

<!-- #region -->
## Exercise 2.5 - Classifying temperatures

Data classification is another useful data analysis concept, where data values are sorted into different groups that help you to interpret the data. Your goal in this exercise is to sort a list of temperatures into four categories using a Python list for each category:

|Category    |Temperature range                  |List name     |
|:-----------|:----------------------------------|:-------------|
|Cold        |Less than -2 deg. C                |`cold`        |
|Slippery    |Greater than or equal to -2 deg. C |`slippery`    |
|            |and less than +2 deg. C            |              |
|Comfortable |Greater than or equal to +2 deg. C |`comfortable` |
|            |and less than +15 deg. C           |              |
|Warm        |Greater than or equal to +2 deg. C |`warm`        |

: _**Table 2.8**. Temperature categories and ranges for Exercise 2.5 and 2.7._

The list of temperatures below were measured at the Helsinki Malmi Airport in April 2013 with night, day, and evening temperatures recorded for each day.

```python
temperatures = [-5.4, 1.0, -1.3, -4.8, 3.9, 0.1, -4.4, 4.0, -2.2, -3.9, 4.4,
                -2.5, -4.6, 5.1, 2.1, -2.4, 1.9, -3.3, -4.8, 1.0, -0.8, -2.8,
                -0.1, -4.7, -5.6, 2.6, -2.7, -4.6, 3.4, -0.4, -0.9, 3.1, 2.4,
                1.6, 4.2, 3.5, 2.6, 3.1, 2.2, 1.8, 3.3, 1.6, 1.5, 4.7, 4.0,
                3.6, 4.9, 4.8, 5.3, 5.6, 4.1, 3.7, 7.6, 6.9, 5.1, 6.4, 3.8,
                4.0, 8.6, 4.1, 1.4, 8.9, 3.0, 1.6, 8.5, 4.7, 6.6, 8.1, 4.5,
                4.8, 11.3, 4.7, 5.2, 11.5, 6.2, 2.9, 4.3, 2.8, 2.8, 6.3, 2.6,
                -0.0, 7.3, 3.4, 4.7, 9.3, 6.4, 5.4, 7.6, 5.2]
```

For this exercise you should:

- Use a `for` loop and conditional statments (e.g., `if`, `elif`, and `else`) to sort the temperatures in the list into the lists associated with each category.
    - *Hint*: Create the empty lists before the start of the `for` loop.
- Answer the following questions:
    - How many times was it cold in Helsinki in April 2013?
    - How many times was it comfortable?
    - Was it ever warm?
<!-- #endregion -->

## Exercise 2.6 - A temperature conversion function

Functions are commonly used for small calculations that occur frequently within a program, such as converting between units.

For this problem you should:

- Create a function to converts temperature in degrees Fahrenheit to degrees Celsius.
    - Be sure to include a docstring in the function definition.
- Use the new function to convert the temperatures below to Celsius:
    - 32 °F
    - 68 °F
    - 91 °F
    - -17 °F


## Exercise 2.7 - A temperature classifier function

This exercise uses the same logic presented in Exercise 2.5 to classify temperatures, but now using a function.

In this exercise you should:

- Create a function that classifies temperatures based on Table 2.8.
    - The function should return the following values for the different categories
        - Cold: `0`
        - Slippery: `1`
        - Comfortable: `2`
        - Warm: `3`
- Use the function to calculate the returned value the following temperatures:
    - +17 °C
    - +2 °C
    - +1.9 °C
    - -2 °C
