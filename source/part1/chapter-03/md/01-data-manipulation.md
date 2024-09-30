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

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
# Common tabular operations in pandas

We have new learned the basics of `pandas` data structures (i.e., `Series` and `DataFrame`) and you should be familiar with some methods for loading and exploring `pandas` data. Next, we will continue exploring the `pandas` data analysis functionalities, and see how it can be used for data manipulation, conducting simple calculations, and making selections based on specific criteria.
<!-- #endregion -->

## Basic calculations

One of the most common things to do in `pandas` is to create new columns based on calculations between different variables (columns). Next, we will learn how to do this using the same input data (`data/kumpula-summer-2024.txt`) as in the previous section. We will first load it using the `pd.read_csv()` method. Remember, that the first 8 lines contains the metadata which we will skip. This time, let's store the filepath as a separate variable in order to make the code more readable and easier to change afterwards (a good practice).

```python deletable=true editable=true jupyter={"outputs_hidden": false}
import pandas as pd

# Define file path:
fp = "data/kumpula-summer-2024.txt"

# Read in the data from the file (starting at row 9):
data = pd.read_csv(fp, skiprows=8)
```

As a first step, it is always good to remember to check the data after reading it. This way we can be sure that everything looks as it should.

```python
data.head()
```

Everything seems to be OK. Now we can start by creating a new column `DIFF` in our `DataFrame`. This can be done by specifying the name of the column and giving it some default value (in this case the decimal number `0.0`).

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data["DIFF"] = 0.0
data.head()
```

<!-- #region deletable=true editable=true -->
As we can see, now we have a new column `DIFF` in our `DataFrame` that has value `0.0` for all rows. When creating a new column, you can initialize it with any value you want. Typically, the value could be a number (`0.0` as we use here), but it could also be `None` (i.e., nothing), some text (e.g., `"test text"`), or more or less any other value or object that can be represented as a single item. You could even initialize the column by storing a function inside the cells if you like. Let's continue by checking the data type of our new column.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data["DIFF"].dtypes
```

<!-- #region deletable=true editable=true -->
As we can see, `pandas` created a new column and automatically recognized that the data type is `float64` as we passed a `0.0` value to it. Great, but what about making those calculations with `pandas` as promised at the start of this section? Next, we will calculate the difference between the `MAX` and `MIN` columns to get an idea how much the temperatures have been varied on different days. The result will be updated into the column `DIFF` that we created earlier. A typical way of performing calculations such as this is to access the set of `Series` (columns) from the `DataFrame` that interests us and perform the mathematical calculation using the selected columns. Typically you store the result directly into a column in the `DataFrame`, such as shown below.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data["DIFF"] = data["MAX"] - data["MIN"]
data.head()
```

<!-- #region deletable=true editable=true -->
As expected, the output from the calculations was stored into the `DIFF` column. Conducting calculations like this is extremely fast in `pandas` because the math operations happen in a vectorized manner. This means that instead of looping over individual values of the `DataFrame` and comparing them to each other individually, calculating the difference happens simultaneously at all rows. You can also create new columns on the fly when doing the calculation (i.e., the column does not have to exist beforehand). Furthermore, it is possible to use any kind of math algebra (e.g., subtraction, addition, multiplication, division, exponentiation, etc.) when creating new columns. We can, for example, calculate another estimate of the average daily temperature by averaging the values in the `TEMP1` and `TEMP2` columns and storing the result as `TEMP`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data["TEMP"] = (data["TEMP1"] + data["TEMP2"]) / 2
data.head()
```


<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 3.4

Calculate the temperatures in Kelvins using the Celsius values and store the result in a new column called `TEMP_KELVIN` in our `DataFrame`. Zero Kelvins is is -273.15 degrees Celsius as we learned in Chapter 2, and the formula for converting degrees Celsius (C) to Kelvins (K) is thus $T_{K} = T_{C} + 273.15$.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["hide-cell", "remove_book_cell"]
# Solution

data["TEMP_KELVIN"] = data["TEMP"] + 273.15
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
## Selecting and updating data

We often want to make selections from our data and only use specific rows from a `DataFrame` in the analysis. There are multiple ways of selecting subsets from a `pandas` `DataFrame` that can be based on specific index values, for example, or using some predefined criteria to make the selection such as selecting all rows where values in column `X` are larger than `0.0`. Next, we will go through the most useful ways of selecting specific rows, columns, and individual values.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Selecting rows and columns

One common way of selecting only specific rows from a `DataFrame` is done via the concept of slicing. Getting a slice of data in `pandas` can be done in a similar manner as with normal Python lists, by specifying an index range inside square brackets: `DataFrame[start_index:stop_index]`. Let's select the first five rows and assign them to a variable called `selection`. Here, we will first see how selecting the data based on index values works just like with "normal" Python lists.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
selection = data[0:5]
selection
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
Here we have selected the first five rows (index `0`-`4`) using the integer index. Notice that the logic here is similar to how Python's `list` slicing (or `range()` function) works; the value on the right side of the colon (here number `5`) is the stop value, which is excluded from the range selection. Hence, the syntax is `[start_index:stop_index]`. In addition, the parameter `:step` could be added at the end in indicate the step size between values (`1` by default). 
<!-- #endregion -->

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
Selections like the previous example are possible, but there is a better and more flexible way of selecting data using the [`pandas` `.loc[]` label-based indexer](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) [^loc]. As the name suggests, `.loc[]` selects data based on axis labels (row and column labels). This alone does not necessarily tell much to you at this point, but `.loc[]` makes it possible to conduct more specific selections, such as allowing you to choose which columns are chosen when selecting a subset of rows. It also makes possible to benefit from row labels that are not necessarily sequential numbers (as has been the case with all our examples thus far). For instance, you can make selections for rows indexed by dates or timestamps. Hence, `.loc[]` can become very handy when working with time series data (we will learn more about this later). Let's now test out the `.loc[]` label indexer by selecting values from column `TEMP` from rows `0`-`5`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
# Select temp column values on rows 0-5
selection = data.loc[0:5, "TEMP"]
selection
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Notice that in this case, we get six rows of data (index `0`-`5`)! This happens because we are now doing the selection based on axis labels instead of normal Python collection indices. It is important to notice the difference between these two approaches, as mixing the two may cause confusion, incorrect analysis results, or bugs in your code. We recommend to use `.loc[]` whenever possible (there are specific cases when you may want to use other approaches). The basic syntax for using `.loc[]` is:
 
```python
.loc[first_included_label:last_included_label, columns]
```

By looking at the syntax, you might imagine that it is possible to select multiple columns when using `.loc[]`. We can test this by selecting the `TEMP` and `TEMP_KELVIN` columns from a set of rows by passing the selected column names inside a list.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
selection = data.loc[0:5, ["TEMP", "TEMP_KELVIN"]]
selection
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As a result, we now have a new `DataFrame` with two columns and 6 rows (i.e., index labels ranging from `0` to `5`).
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 3.5

Calculate the mean temperature (in Celsius) for the last seven days of August 2024. Do the selection using the row index values.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["hide-cell", "remove_book_cell"]
# Solution

data.loc[85:91, "TEMP"].mean()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Selecting a single row or value

You can also select an individual row from specific position using the `.loc[]` indexing. Here we select all the data values using index `4` (the 5th row).
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
row = data.loc[4]
row
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
`.loc[]` indexing returns the values from that row as a `Series` where the indices are actually the column names of the row variables. Hence, you can access the value of an individual column by referring to its index using following format:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
# Print one attribute from the selected row
row["TEMP"]
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Sometimes it is enough to access a single value in a `DataFrame` directly. In this case, we can use the [`pandas` `.at[]` indexer](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html) [^at] instead of `.loc[]`.
Let's select the temperature (column `TEMP`) on the first row (index `0`) of our `DataFrame`:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
selection.at[0, "TEMP"]
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As an output, we get an individual value `23.7`. `.at[]` works only when accessing a single value, whereas the `.loc[]` can be used to access both single or multiple values at the same time. The end result when fetching a single value with `.loc[]` is exactly the same and the difference between the two approaches is minimal. Hence, we recommend using `.loc[]` in all cases because it is more flexible (`.at[]` is slightly faster but in most cases this does not make a difference).
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
selection.loc[0, "TEMP"]
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Selections based on index positions

As we have learned thus far, `.loc[]` and `.at[]` are based on the axis labels, the names of columns and rows. For positional based indexing, `pandas` has an [`.iloc[]` indexer](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html) [^iloc], which is based on integer value indices. With `.iloc[]` it is also possible to refer to the columns based on their index value (i.e., to a positional number of a column in the `DataFrame`). For example, `data.iloc[0, 0]` would return `20240601` in our example `DataFrame`, which is the value on the first row and first column in the data.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Check the first rows
print(data.head())
print()
print(f"The value at position (0, 0) is {data.iloc[0, 0]}.")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
The syntax for using `.iloc[]` is: 

```python
.iloc[start_row_position:stop_row_position,
      start_column_position:stop_column_position]
```

Using this syntax, we can access the value on the first row and second column (`TEMP`) as follows:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data.iloc[0, 1]
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
It is also possible to get ranges of rows and columns with `.iloc[]`. For example, we could select the `YEARMODA` and `TEMP` columns from the first five rows based on their indices (positions) in the data set. Here, we will select rows from positions 0 to 5 and columns from positions 0 to 2.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
selection = data.iloc[0:5, 0:2]
selection
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As a result we indeed get only two columns and the first five rows. It is important to notice is that the behavior in terms of how many rows are returned differs between `.iloc[]` and `.loc[]`. Here, the `.iloc[0:5]` returns 5 rows (following the Python list slicing behavior), whereas using `.loc[0:5]` would return 6 rows (i.e., also including the row at index `5`). 
    
One handy functionality with `.iloc[]` is the ability to fetch data starting from the end of the `DataFrame`, similar to how values can be selected from the end of a Python `list`. It is possible to retrieve the last row in the `DataFrame` by passing a negative number to `.iloc[]`, where value `-1` corresponds to the last row (or column), -2 corresponds to the second to last, and so on. Following this, it is easy to find the value in the last row and column (the final value in the `TEMP_KELVIN` column in our case).
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data.iloc[-1, -1]
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Selections using listed criteria

Another common way of selecting rows from a `DataFrame` is to provide a list of values that are used for finding matching rows in a specific `DataFrame` column. For example, selecting rows that match specific dates can be done by passing a list of values used as criteria to the [`.isin()` function of `pandas`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html) [^isin]. This will go through each value in the selected column (in this case `YEARMODA`) and check whether there is a match or not. As an output, the `.isin()` function returns a `Series` of Boolean values (True or False) that can be combined with `.loc[]` to do the final selection that returns only rows that meet the selection criteria. 
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# List of values that will be used as basis for selecting the rows
selection_criteria = [20240601, 20240708, 20240809]

# Do the selection based on criteria applied to YEARMODA column
data.loc[data["YEARMODA"].isin(selection_criteria)]
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
### Conditional selections

One really useful feature in `pandas` is the ability to easily filter and select rows based on a conditional statement. The following example shows how we can check whether the temperature at each row of the `MAX` column is greater than or equal to 25 degrees.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# This cell sets the number of lines of pandas output to a maximum of 9
# The cell is removed when building the website/book PDF
pd.set_option("display.max_rows", 9)
```

```python editable=true slideshow={"slide_type": ""}
data["MAX"] > 25
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As a result, we get a `Series` of Boolean values, where the value `True` or `False` at each row determines whether or not our condition was met. This kind of `Series` or `numpy.array` of Boolean values based on some predefined criteria is typically called a mask. We can take advantage of this mask when doing selections with `.loc[]` based on specific criteria. In the following example, we use the same criterion as above and store all rows meeting the criterion into the variable `hot_temps` ("hot" temperatures). We can specify the criterion directly inside the square brackets of the `.loc[]` indexer. Let's select rows that have a temperature greater than or equal to 25 degrees.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
hot_temps = data.loc[data["MAX"] >= 25]
hot_temps
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
It is also possible to combine multiple criteria at the same time. Combining multiple criteria can be done using the `&` (and) or the `|` (or) operators. Notice, that it is often useful to separate the different conditional clauses with parentheses `()`. Let's select rows having average daily temperatures above 20 degrees from the second half of the summer of 2024 (July 15th onwards).
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
warm_temps = data.loc[(data["TEMP"] > 20) & (data["YEARMODA"] >= 20240715)]
warm_temps
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
Now we have a subset of our `DataFrame` with only rows where the `TEMP` is above 20 and the dates in `YEARMODA` column start from the 15th of July. Notice, that the index values (numbers on the left) are still showing the index labels from the original `DataFrame`. This indicates that our result is a slice from the original data.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Of course, it is possible to reset the index using the `.reset_index()` function, which makes the index numbering to start from 0 and increases the index values in a sequential manner. This is often a useful operation to do because it makes it easier then to slice the data with `.loc[]` or `.iloc[]`. By default `.reset_index()` would make a new column called `index` to store the previous index, which might be useful in some cases. That is not the case here, so we can omit storing the old index by including the parameter `drop=True`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
warm_temps = warm_temps.reset_index(drop=True)
warm_temps
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As can be seen, now the index values goes from 0 to 47. Resetting the index has now also unlinked the `warm_temps` `DataFrame` from `data`, meaning that it is not a view anymore but an independent `pandas` object. When making selections, it is quite typical that `pandas` might give you warnings if you modify the selected data without first resetting the index or making a copy of the selected data. To demonstrate this, we will make the selection again and create a new column indicating days in which the temperature was "hot" (maximum temperature greater than 25 degrees Celsius).
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
warm_temps = data.loc[(data["TEMP"] > 20) & (data["YEARMODA"] >= 20240715)]
warm_temps["HOT_TEMP"] = warm_temps["MAX"] > 25
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
In this case we have created a new column using the selection, which is a slice from the original data. As a result, `pandas` raises a warning about a possible invalid value assignment. In most cases this warning can be ignored, but it is a good practice to always make a copy when doing selections, especially if you continue working with the selected data and intend modify it further.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Make the selection and make a copy
warm_temps = data.loc[(data["TEMP"] > 20) & (data["YEARMODA"] >= 20240715)].copy()

# Now update the first value of the last column
warm_temps["HOT_TEMP"] = warm_temps["MAX"] > 25
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As we can see, now we did not receive any warnings this time and it would be safe to continue working with this selection without needing to worry that there are some "hidden linkages" between the selection and another `DataFrame` that could cause issues (we discuss this more in the next section).
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 3.6

Calculate the mean temperature (in Celsius) for the last seven days of August 2024 again. This time you should select the rows based on a condition for the `YEARMODA` column.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["hide-cell", "remove_book_cell"]
# Solution
data["TEMP"].loc[data["YEARMODA"] >= 20240825].mean()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### View versus a copy

As we have seen above, making a selection can sometimes result to something called a view. In such cases, the selection and the original data may still linked to each other. This happens, for example, if you make a selection like above but return only a single column from the original source data. In a situation where you have a view, a change in the original data for that specific column can also change the value in the selection. This behavior can be confusing and yield unexpected consequences, so a good practice to follow is to always make a copy whenever doing selections to unlink the source `DataFrame` from the selection. You can make a copy easily while doing the selection by adding `.copy()` at the end of the selection command.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
selection = data.loc[0:5, ["TEMP", "TEMP_KELVIN"]].copy()
selection
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now we have the exact same data in our end result, but we have ensured that the selection is not linked to the original data anymore. To demonstrate what can happen with the view, let's make a selection of a single column from the selection data (which will be a view), and modify the data a bit to demonstrate the consequences if we are not careful.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
temp = selection["TEMP"]
temp
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now if we make a change to our original data `selection` it will also influence our values in `temp`.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
selection.iloc[0, 0] = 30.0
selection.head()
```

```python editable=true slideshow={"slide_type": ""}
# Check the values in temp (which we did not modify)
temp
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As we can see, the value in our `temp` `Series` has changed from `23.70` to `30.00` although we did not make any change to it directly. The change happened because the data objects were still linked to each other.
<!-- #endregion -->

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
## Dealing with missing data

As you may have noticed by now, we have several missing values for the temperature minimum, maximum, and average columns (`MIN`, `MAX`, and `TEMP`). These missing values appear as `NaN` (not-a-number). Having missing data in your data file is quite common and typically you want to deal with these values somehow. Common procedures to deal with `NaN` values are to either remove them from the `DataFrame` or replace (fill) them with some other value. In `pandas`, both of these options are easy to do. Let's first start by checking whether the data we are using has and `NaN` values.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
warm_temps
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As we can see, the `MIN` and `TEMP` columns are clearly missing values at index `82`. It is also possible to confirm this with `pandas` by accessing a specific `Series` attribute called `.hasnans`, which can be a handy tool when automating a data analysis pipeline. Each `Series` (or column) in the `DataFrame` has this attribute. Let's check whether the `MIN` column contains any `NaN` values.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
warm_temps["MIN"].hasnans
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
The `.hasnans` attribute will be either `True` or `False` depending on whether or not the `Series` contains any `NaN` values. Let's now see how we can remove the missing data values (i.e., clean the data) using the `.dropna()` function. Inside the `.dropna()` function you can pass a list of column(s) in which the `NaN` values should be processed by using the `subset` parameter.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
cols_to_check = ["MIN"]
warm_temps_clean = warm_temps.dropna(subset=cols_to_check)
warm_temps_clean
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
As you can see by looking at the output above, we now have a `DataFrame` without `NaN` values in the `MIN` column (we have only 23 rows compared to 27 before cleaning). However, you might recall that there may also have been `NaN` values in the `MAX` column. In order to drop all rows containing `NaN` values, we could instead to the following:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
warm_temps_clean = warm_temps.dropna()
warm_temps_clean
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
In this case we can see an additional 2 rows have been dropped due to the `NaN` values that were in the `MAX` column. However, it is using `.dropna()` without the `subset` parameter is not recommended as sometimes it can result in dropping data you may not want to remove. Thus, we generally recommend always using the `subset` parameter with the list of columns from which to remove `NaN` values.

Of course, by dropping rows using `.dropna()` you naturally lose data (rows), which might not be an optimal solution for all cases. Because of this, `pandas` also provides an option to fill the `NaN` values with some other value using the `.fillna()` function. Let's instead fill the missing values in our data set the with value `-9999`. Note that we are not giving the `subset` parameter this time.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
warm_temps.fillna(-9999)
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
As a result we now have a `DataFrame` where all `NaN` values in the DataFrame are filled with the value `-9999`. As was the case for the `.dropna()` function, you can fill values in select columns by directing the `.fillna()` function to a specific column (or set of columns).
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
warm_temps["MIN"] = warm_temps["MIN"].fillna(-9999)
warm_temps
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Notice that now the `NaN` value at index `82` of the `MIN` has been replaced, while the `NaN` value in the `DIFF` column remains.  

It is important to be aware, that in many cases filling the data with a specific value is dangerous because you end up modifying the actual data, which might affect the results of your analysis. For example, in the case above we would have dramatically changed the temperature difference columns because the `-9999` values not an actual temperature! Hence, use caution when filling missing values. In some cases, you might have to fill in missing data values for the purpose of saving the data file in a specific format. For example, some GIS software cannot handle missing values. Always pay attention to potential missing data values when reading in data files and performing your data analysis.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Data type conversions
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
When doing data analysis, another quite typical operation that needs to be done is to convert values in a column from one data type to another, such as from floating point values to integers. Remember, that we have already performed data type conversions in Chapter 2 using built-in Python functions such as `int()` or `str()`. For values stored in a `pandas` `Series`, we can use the `.astype()` method for converting data types. Let's explore this by converting the temperature values (type `float64`) in the column `TEMP` to be integers (type `int64`). Let's first have a look at the existing data.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data["TEMP"].head()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now we can easily convert those decimal values to integers using `.astype(int)`.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data["TEMP"].astype(int).head()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Great! As we can see the values were converted to integers. However, this example demonstrates the importance of being careful with type conversions from floating point values to integers. This type conversion simply drops the stuff to the right of the decimal point, so all values are effectively rounded down to the nearest whole number. For example, the first value in our `Series` (`23.7`) was truncated to `23` as an integer when it clearly should be rounded up to `24`. This issue can be resolved by chaining together the `.round()` function with the `.astype()` function. For example, `.round(0).astype(int)` will first round the values to have zero decimal places and then converts those values into integers.
<!-- #endregion -->

```python editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
data["TEMP"].round(0).astype(int).head()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As we can see, now the integer values are correctly rounded. 

The `.astype()` method supports converting between all basic Python data types (`int`, `float`, `str`), but it also knows how to convert between more specific `numpy` data types such as `int64`, `int32`, `float64`, `float32` (a full list can be found in the [NumPy documentation](https://numpy.org/doc/stable/user/basics.types.html) [^numpydtypes]). Using the `numpy` data type can useful if you need to be more specific about how many bits should be reserved for storing the values, for example. For instance, `int64` (i.e., a 64-bit integer) can store integer values ranging between -9223372036854775808 and 9223372036854775807, whereas `int16` can only store values from -32768 to 32767. If passing the "normal" `int` or `float` to the `astype()` function, `pandas` will automatically store 64-bit numeric values. However, higher the number precision (i.e., the larger number of bits you use), the more physical memory is required to store the data. Hence, in some specific cases dealing with extremely large datasets, it may be useful to be able to specify that the values in specific columns should be stored with lower precision to save memory.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Sorting data

Quite often it is useful to be able to sort your data (descending/ascending) based on values in some column. This can be done easily with `pandas` using the `.sort_values(by='YourColumnName')` function. Let's first sort the values in ascending order using the `TEMP` column.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
# Sort DataFrame, ascending
data.sort_values(by="TEMP")
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
Of course, it is also possible to sort them in descending order by including the `ascending=False` parameter.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
# Sort DataFrame, descending
data.sort_values(by="TEMP", ascending=False)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
In some situations, you might need to sort values based on multiple columns simultaneously, which is sometimes referred to as multi-level sorting. This can be done by passing a list of column names to the `by` parameter. When you sort the data based on multiple columns, sometimes you also might want to sort your data in a way that the first-level sorting happens in ascending order and the second-level sorting happens in descending order. An example situation for this kind of sorting could be when sorting the temperatures first by weekday (Monday, Tuesday, etc.) and then ordering the values for each weekday in descending order. This would always show the warmest temperature for a given day of the week first. Let's modify our data a bit to demonstrate this. We will add a new column that has information about the weekday. The 1st of June, 2024 was a Saturday, so we start from that.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Create a list of weekdays that matches with our data
# The data covers 13 weeks + 1 day (altogether 92 days)
week_days = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
day_list = 13 * week_days + week_days[:1]

# Add the weekdays to our DataFrame
data["WEEKDAY"] = day_list
data
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now we have a new column with information about the weekday of each row. Next, we can test how to sort the values, so that we order the data by weekday and within each weekday the temperatures are in descending order. You can adjust how the ordering works by passing a list of Boolean values to the `ascending` parameter.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data.sort_values(by=["WEEKDAY", "TEMP"], ascending=[True, False])
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As a result the data are now ordered first by weekday (i.e., the same weekday values are grouped) and the within these weekdays the temperature values are sorted in descending order showing the warmest day first. Ordering data in this manner based on multiple criteria can sometimes be very useful when analyzing your data.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Table joins: Combining DataFrames based on a common key
<!-- #endregion -->

### The basic logic of a table join

Joining data between two or several DataFrames is a common task when doing data anaysis. The minimum requirement for being able to combine data between two (or more) DataFrames (i.e. *tables*), is to have at least one common attribute (called *key*) that has identical values in both DataFrames. Figure 3.4 illustrates this logic: we want to merge the precipitation data from Kumpula weather station to the temperature data that we worked earlier. The common `key` in this case is the time information which is in column `YEARMODA` in the left DataFrame and `DATE` column in the right DataFrame accordingly. The column names of the keys can be different (as in our case), but the actual values stored in these columns should correspond to each other, so that it is possible to match the records between tables. The attribute values of the key can contain data in any format (dates, text, numbers, etc.). Hence, the data is not limited to dates or integers as demonstrated in this example. 

![_**Figure 3.4**. Joining precipitation data from the right DataFrame to the left based on common key._](../img/Table_join_logic.png)

_**Figure 3.4**. Joining precipitation data from the right DataFrame to the left based on common key._


### Table join using pandas `.merge()`

In the following, we first read the precipitation data from Kumpula, and then join this data with the DataFrame containing the average temperature data. Merging two DataFrames together based on a common key (or multiple keys) can be done easily with pandas using the `.merge()` -function. The column which represents the key can be specified with parameter `on`, if the key column is identical in both DataFrames. In our case, the columns containing the common values between the DataFrames are named differently. Hence, we need to specify separately the key for the left DataFrame using parameter `left_on`, and parameter `right_on` for the right DataFrame accordingly. 

```python
# Read precipitation data and show first rows
rainfall = pd.read_csv("data/2902781.csv")
rainfall.head()
```

```python
# Make a table join
join = data.merge(rainfall, left_on="YEARMODA", right_on="DATE")
join.head()
```

Now we have merged all the information from the right DataFrame into the left one and stored the result into variable `join`. By doing this, we can e.g. analyze the relationship between the daily average temperature and precipitation, to understand whether the temperature is lower when it rains. Currently, the `join` DataFrame contains many variables that are not necessarily useful for us. To make the output more concise, a useful trick to do when joining is to limit the number of columns that will be kept from the right DataFrame. This can be done by chaining a simple column selection while doing the merge as shown next. When doing this, it is important to remember that the `key` column on the right DataFrame needs to be part of the selection for the table join to work.  

```python
# Make another join but only keep the attribute of interest
join2 = data.merge(rainfall[["DATE", "PRCP"]], left_on="YEARMODA", right_on="DATE")
join2.head()
```

As can be seen, now only the column `DATE` and the attribute of interest `PRCP` were joined and kept in the output from the right DataFrame. Similar trick can also be applied to the left DataFrame by adding the selection before the `.merge()` call if you want to reduce the number of columns on the result. 

In our case, doing the table join was fairly straightforward because we had only one unique record per day in both DataFrames. However, in some cases you might have multiple records on either one of the DataFrames (e.g. hourly observations vs daily observations). This can in specific cases cause issues (not always!), incorrect analysis results, and other undesired consequences if not taken into account properly. This kind of mismatch in number of records per table can be handled e.g. by aggregating the hourly data to a daily average. You can learn more about these aggregation techniques in the following sections. 

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Footnotes

[^at]: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html>
[^iloc]: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html>
[^isin]: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html>
[^loc]: <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html>
[^numpydtypes]: <https://numpy.org/doc/stable/user/basics.types.html>
<!-- #endregion -->
