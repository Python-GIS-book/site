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

<!-- #region deletable=true editable=true -->
# Data manipulation and analysis

Now you have learned the basics of pandas data structures (i.e. *Series* and *DataFrame*) and you should be familiar with basic methods for loading and exploring data. Next, we will continue exploring the pandas functionalities, and see how it can be used for data manipulation, conducting simple calculations, and making selections based on specific criteria.

## Basic calculations

One of the most common things to do in pandas is to create new columns based on calculations between different variables (columns). Next, we will learn how to do that using the same input data (`'Kumpula-June-2016-w-metadata.txt'`) as in the previous section. We will first load it using the `pd.read_csv()` method. Remember, that the first 8 lines contains the metadata which we will skip. This time, let's store the filepath into a separate variable in order to make the code more readable and easier to change afterwards (a good practice).
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
import pandas as pd

# Define file path:
fp = 'data/Kumpula-June-2016-w-metadata.txt'

# Read in the data from the file (starting at row 9):
data = pd.read_csv(fp, skiprows=8)
```

As a first step, it is always good to remember to check the data after reading it. This way we can be sure that everything looks as it should.

```python
data.head()
```

All good.

Now we can start by creating a new column `DIFF` in our DataFrame. This can be done by specifying the name of the column and giving it some default value (in this case the decimal number `0.0`).

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Define a new column "DIFF"
data['DIFF'] = 0.0

# Check how the dataframe looks like:
data
```

<!-- #region deletable=true editable=true -->
As we can see, now we have a new column (`DIFF`) in our DataFrame that has value 0.0 for all rows. When creating a new column, you can *initialize* it with any value you want. Typically, the value could be a number 0 as in here, but it could also be `None` (i.e. nothing), some text (e.g. `"test text"`), or more or less any other value or object that can be represented as a single item. You could even initiliaze the column by storing a function inside the cells if you like.   

Let's continue by checking the datatype of our new column.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data['DIFF'].dtypes
```

<!-- #region deletable=true editable=true -->
As we can see, pandas created a new column and automatically recognized that the data type is float as we passed a 0.0 value to it.

Okay great, but whatabout making those calculations with pandas as promised in the beginning? Next, we will learn to do that. We will update the column `DIFF` by calculating the difference between `MAX` and `MIN` columns to get an idea how much the temperatures have been varying during different days. A typical way of conducting calculations such as this, is to access the specific Series that interests us from the DataFrame, conduct the mathematical calculations (between two or more series), and store the result into a column in the DataFrame, like following:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Calculate max min difference
data['DIFF'] = data['MAX'] - data['MIN']

# Check the result
data.head()
```

<!-- #region deletable=true editable=true -->
The calculations were stored into the ``DIFF`` column as planned. Conducting calculation like this is extremely fast in pandas because the math operations happen in *vectorized* manner. This means that instead of looping over individual values of the DataFrame and comparing them to each other, calculating the difference happens simultaneously at all rows.

You can also create new columns on-the-fly when doing the calculation (i.e. the column does not have to exist before). Furthermore, it is possible to use any kind of math algebra (e.g. subtracttion, addition, multiplication, division, exponentiation, etc.) when creating new columns.

We can for example convert the Fahrenheit temperatures in the `TEMP` column into Celsius using the formula that we have seen already many times. Let's do that and store it in a new column called `TEMP_CELSIUS`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Create a new column and convert temp fahrenheit to celsius:
data['TEMP_CELSIUS'] = (data['TEMP'] - 32) / (9/5)

# Check output
data.head()
```

**Check your understanding**

**NOTE: THIS IS QUITE COMPLICATED TASK. MAKE AN EASIER ONE THAT DOES NOT REQUIRED GOING BACK TO OTHER MATERIALS.** Calculate the temperatures in Kelvins using the Celsius values **and store the result a new column** calle `TEMP_KELVIN` in our dataframe.
0 Kelvins is is -273.15 degrees Celsius as we learned in Chapter 1.

```python
# Add column "TEMP_KELVIN" and populate it with Kelvin values

```

<!-- #region deletable=true editable=true -->
## Selecting and updating data

We often want to make selections from our data and only use specific rows from a DataFrame in the analysis. There are multiple ways of selecting subsets of a pandas DataFrame than can be based on e.g. specific index values or using some predefined criteria to make the selection, such as "give me all rows where values in column X are larger than zero". Next, we will go through the most useful tricks for selecting specific rows, columns and individual values.


### Selecting rows and columns

One common way of selecting only specific rows from your DataFrame is done via a concept of **slicing**. Slicing in pandas can be done in a similar manner as with normal Python lists, i.e. you specify index range you want to select inside the square brackets: ``dataframe[start_index:stop_index]``.

Let's select the first five rows and assign them to a variable called `selection`. Here, we will first see how selecting the data works like you would do using normal Python list.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select first five rows of dataframe using row index values
selection = data[0:5]
selection
```

<!-- #region deletable=true editable=true -->
Here we have selected the first five rows (index 0-4) using the integer index. Notice that the logic here follows how Python's list slicing (or `range` function) works, i.e. the value on the right side of the colon (here number `5`) tells when to stop, but that value is not taken into the final selection. Hence, the syntax is `start_index:stop_index` (also additional parameter `:step` could be added here to the end). 
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Doing selections like in the previous example can be done, but there is also a better and more flexible way of selecting data using so called `.loc` label-indexing. As the name implies, `loc` selects data based on axis labels (row and column labels). This does not necesssarily tell much to you at this point, but `loc` makes it possible to conduct more specific selections, such as allowing you to choose which columns are chosen when selecting a subset of rows. It also makes possible to benefit from row labels that are not necessarily sequantial numbers (as with all our examples thus far), but they can represent other objects as well, such as dates or timestamps. Hence, `loc` can become very handy when working with timeseries data (we will learn more about this later). 

Let's test the `loc` label-indexing by selecting temperature values from column `TEMP` using rows 0-5:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select temp column values on rows 0-5
selection = data.loc[0:5, 'TEMP']
selection
```

Notice that in this case, we get six rows of data (index 0-5)! This happens because we are now doing the selection based on axis labels instead of normal Python-kind of indexing. It is important to notice the difference between these two approaches, as mixing the two may cause confusion,  incorrect analysis results or bugs in your code, if you do not pay attention. We recommend to use `loc` always when possible (there are specific cases when you want to use other approaches, more about this soon). 

Hence, the basic syntax for `loc` is `.loc[first_included_label:last_included_label, columns]`. By looking at the syntax, you might guess that it is also possible to select multiple columns when using `loc`. Next, we will test this by selecting the `TEMP` and `TEMP_CELSIUS` columns from a set of rows by passing them inside a list.

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select columns temp and temp_celsius on rows 0-5
selection = data.loc[0:5, ['TEMP', 'TEMP_CELSIUS']]
selection
```

As a result, we now have a new DataFrame with two columns and 6 rows (i.e. index labels ranging from 0 to 5). A good thing to understand when doing selections, is that the end result after the selection is often something called a ``view``. This means that our selection and the original data may still linked to each other. If you change a value in our ``selection`` DataFrame (i.e. the view from the original DataFrame), this change will also be reflected in the original DataFrame (in this case ``data``). Without going into details why and when this happens, this behavior can nevertheless be confusing having unexpected consequences. To avoid this behavior, a good practice to follow is to always make a copy whenever doing selections (i.e. *unlink* the two DataFrames). You can make a copy easily while doing the selection by adding a `.copy()` at the end of the command:   

```python
# Select columns temp and temp_celsius on rows 0-5 and 
# make a copy out of it to ensure they are not linked to each other
selection_copy = data.loc[0:5, ['TEMP', 'TEMP_CELSIUS']].copy()
selection_copy
```

Now we have the exact same data in our end result, but we have ensured that the selection is not linked to the original data anymore. We will see more examples about this later, when the difference becomes more evident. 


**Test your understanding**

Calculate the mean temperature (in Celsius) for the last seven days of June. Do the selection using the row index values.


### Selecting a single row or value

You can also select an individual row from specific position using the `.loc[]` indexing. Here we select all the data values using index 4 (the 5th row):

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select one row using index
row = data.loc[4]
row
```

<!-- #region deletable=true editable=true -->
``.loc[]`` indexing returns the values from that position as a ``Series`` where the indices are actually the column names of those variables. Hence, you can access the value of an individual column by referring to its index using following format (both should work):
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Print one attribute from the selected row
row['TEMP']
```

Sometimes it is enough to access a single value in a DataFrame directly. In this case, we can use ``.at`` instead of `loc`.
Let's select the temperature (column `TEMP`) on the first row (index `0`) of our DataFrame.

```python
selection.at[0, "TEMP"]
```

As an output, we got the individual value 65.5. `at` works only when accessing a single value, whereas the `loc` can be used to access both a single or multiple values at the same time. The end result when fetching a single value with `loc` is exactly the same. The difference between the two approaches is minimal, hence we recommend using `loc` in all cases because it is more flexible (`at` is slightly faster but in most cases it does not make a difference). 

```python
selection.loc[0, "TEMP"]
```

### Selecting values based on index positions

As we have learned thus far, `.loc` and `.at` are based on the *axis labels* - the names of columns and rows. For positional based indexing, pandas has an `.iloc` which is based on *integer value* indices. With `.iloc`, it is also possible to refer to the columns based on their index value (i.e. to a positional number of a column in the DataFrame). For example,  `data.iloc[0,0]` would return `20160601` in our example DataFrame which is the value on the first row and first column in the data.
    

```python
# Check the first rows
print(data.head())
print()
print("Value at position (0,0) is", data.iloc[0,0])
```

Hence, the syntax for `iloc` is `iloc[start_row_position:stop_row_position, start_column_position:stop_column_position]`.

By following this syntax, we can access the value on the first row and second column (`TEMP`) by calling:

```python
data.iloc[0,1]
```

It is also possible to get ranges of rows and columns with `iloc`. For example, we could select `YEARMODA` and `TEMP` columns from the first five rows based on their indices (positions) in the data:

```python
# Select rows from positions 0 to 5
# and columns from positions 0 to 2 
data.iloc[0:5:,0:2]
```

A good thing to notice, is that with `iloc`, the behavior in terms of how many rows are returned differs from `loc`. Here, the `0:5` returns 5 rows (following the Python list slicing behavarior), whereas using `loc` would return 6 rows (i.e. also including the row at index 5). 
    
One handy functionality with `iloc` is the ability to fetch data starting from the end of the DataFrame. Hence, it is possible to retrieve the last row in the DataFrame by passing a negative number to the `iloc`, where value -1 corresponds to the last row (or column), -2 corresponds to the second last, and so on. Following this, it is easy to see e.g. what is the ``TEMP_CELSIUS`` value (the last column) of the last row of data.

```python
# Check the value on the last row and last column in the data
data.iloc[-1, -1]
```

<!-- #region deletable=true editable=true -->
### Conditional selections

One really useful feature in pandas is the ability to easily filter and select rows based on a conditional statement.
The following example shows how to select rows when the Celsius temperature has been higher than 15 degrees into variable `warm_temps` (warm temperatures). Pandas checks if the condition is `True` or `False` for each row, and returns those rows where the condition is `True`:
<!-- #endregion -->

```python
# Check the condition
data['TEMP_CELSIUS'] > 15
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select rows with temp celsius higher than 15 degrees
warm_temps = data.loc[data['TEMP_CELSIUS'] > 15]
warm_temps
```

<!-- #region deletable=true editable=true -->
It is also possible to combine multiple criteria at the same time. Here, we select temperatures above 15 degrees that were recorded on the second half of June in 2016 (i.e. `YEARMODA >= 20160615`).
Combining multiple criteria can be done with the `&` operator (AND) or the `|` operator (OR). Notice, that it is often useful to separate the different clauses inside the parentheses `()`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select rows with temp celsius higher than 15 degrees from late June 2016
warm_temps = data.loc[(data['TEMP_CELSIUS'] > 15) & (data['YEARMODA'] >= 20160615)]
warm_temps
```

<!-- #region deletable=true editable=true -->
Now we have a subset of our DataFrame with only rows where the `TEMP_CELSIUS` is above 15 and the dates in `YEARMODA` column start from 15th of June.

Notice, that the index values (numbers on the left) are still showing the positions from the original DataFrame. It is possible to **reset** the index using `reset_index()` function that
might be useful in some cases to be able to slice the data in a similar manner as above. By default the `reset_index()` would make a new column called `index` to keep track on the previous
index which might be useful in some cases but here not, so we can omit that by passing parameter `drop=True`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Reset index
warm_temps = warm_temps.reset_index(drop=True)
warm_temps
```

As can be seen, now the index values goes from 0 to 12.


#### Check your understanding

Find the mean temperatures (in Celsius) for the last seven days of June again. This time you should select the rows based on a condition for the `YEARMODA` column!

```python
# Mean temperature for the last seven days of June (use a conditional statement to select the correct rows):
data['TEMP_CELSIUS'].loc[data['YEARMODA'] >= 20160624].mean()
```

```{admonition} Deep copy
In this lesson, we have stored subsets of a DataFrame as a new variable. In some cases, we are still referring to the original data and any modifications made to the new variable might influence the original DataFrame.
    
If you want to be extra careful to not modify the original DataFrame, then you should take a proper copy of the data before proceeding using the `.copy()` method. You can read more about indexing, selecting data and deep and shallow copies in [pandas documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html) and in [this excellent blog post](https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-part-4-c4216f84d388).
```

<!-- #region deletable=true editable=true -->
## Dealing with missing data

As you may have noticed by now, we have several missing values for the temperature minimum, maximum, and difference columns (`MIN`, `MAX`, `DIFF`, and `DIFF_MIN`). These missing values are indicated as `NaN` (not-a-number). Having missing data in your datafile is really common situation and typically you want to deal with it somehow. Common procedures to deal with `NaN` values are to either **remove** them from
the DataFrame or **fill** them with some value. In Pandas both of these options are really easy to do.

Let's first see how we can remove the NoData values (i.e. clean the data) using the [.dropna()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html) function. Inside the function you can pass a list of column(s) from which the `NaN` values should found using the `subset` parameter.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Drop no data values based on the MIN column
warm_temps_clean = warm_temps.dropna(subset=['MIN'])
warm_temps_clean
```

<!-- #region deletable=true editable=true -->
As you can see by looking at the table above (and the change in index values), we now have a DataFrame without the NoData values.

````{note}
Note that we replaced the original `warm_temps` variable with version where no data are removed. The `.dropna()` function, among other pandas functions can also be applied "inplace" which means that the function updates the DataFrame object and returns `None`:
    
```python
warm_temps.dropna(subset=['MIN'], inplace=True)
```
````

Another option is to fill the NoData with some value using the `fillna()` function. Here we can fill the missing values in the with value -9999. Note that we are not giving the `subset` parameter this time.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Fill na values
warm_temps.fillna(-9999)
```

<!-- #region deletable=true editable=true -->
As a result we now have a DataFrame where NoData values are filled with the value -9999.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
```{warning}
In many cases filling the data with a specific value is dangerous because you end up modifying the actual data, which might affect the results of your analysis. For example, in the case above we would have dramatically changed the temperature difference columns because the -9999 values not an actual temperature difference! Hence, use caution when filling missing values. 
    
You might have to fill in no data values for the purposes of saving the data to file in a spesific format. For example, some GIS software don't accept missing values.  Always pay attention to potential no data values when reading in data files and doing further analysis!
```
<!-- #endregion -->

## Data type conversions

<!-- #region editable=true -->
There are occasions where you'll need to convert data stored within a Series to another data type, for example, from floating point to integer.
<!-- #endregion -->

Remember, that we already did data type conversions using the [built-in Python functions](https://docs.python.org/3/library/functions.html#built-in-functions) such as `int()` or `str()`.


For values in pandas DataFrames and Series, we can use the `astype()` method.

<!-- #region editable=true -->
```{admonition} Truncating versus rounding up
**Be careful with type conversions from floating point values to integers.** The conversion simply drops the stuff to the right of the decimal point, so all values are rounded down to the nearest whole number. For example, 99.99 will be truncated to 99 as an integer, when it should be rounded up to 100.

Chaining the round and type conversion functions solves this issue as the `.round(0).astype(int)` command first rounds the values with zero decimals and then converts those values into integers.
```
<!-- #endregion -->

```python
print("Original values:")
data['TEMP'].head()
```

```python
print("Truncated integer values:")
data['TEMP'].astype(int).head()
```

```python editable=true jupyter={"outputs_hidden": false}
print("Rounded integer values:")
data['TEMP'].round(0).astype(int).head()
```

Looks correct now.


## Sorting data

Quite often it is useful to be able to sort your data (descending/ascending) based on values in some column
This can be easily done with Pandas using `sort_values(by='YourColumnName')` -function.

Let's first sort the values on ascending order based on the `TEMP` column:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Sort dataframe, ascending
data.sort_values(by='TEMP').head()
```

<!-- #region deletable=true editable=true -->
Of course, it is also possible to sort them in descending order with ``ascending=False`` parameter:

<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Sort dataframe, descending
data.sort_values(by='TEMP', ascending=False).head()
```

<!-- #region deletable=true editable=true -->
## Writing data to a file

Lastly, it is of course important to be able to write the data that you have analyzed into your computer. This is really handy in Pandas as it [supports many different data formats
by default](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html).

**The most typical output format by far is CSV file.** Function `to_csv()` can be used to easily save your data in CSV format.
Let's first save the data from our `data` DataFrame into a file called `Kumpula_temp_results_June_2016.csv`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# define output filename
output_fp = "Kumpula_temps_June_2016.csv"

# Save dataframe to csv
data.to_csv(output_fp, sep=',')
```

<!-- #region deletable=true editable=true -->
Now we have the data from our DataFrame saved to a file:
![Text file output1](img/pandas-save-file-1.png)

As you can see, the first value in the datafile contains now the index value of the rows. There are also quite many decimals present in the new columns
that we created. Let's deal with these and save the temperature values from `warm_temps` DataFrame without the index and with only 1 decimal in the floating point numbers.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# define output filename
output_fp2 = "Kumpula_temps_above15_June_2016.csv"

# Save dataframe to csv
warm_temps.to_csv(output_fp2, sep=',', index=False, float_format="%.1f")
```

<!-- #region deletable=true editable=true -->
Omitting the index can be with `index=False` parameter. Specifying how many decimals should be written can be done with `float_format` parameter where text `%.1f` defines Pandas to use 1 decimals
in all columns when writing the data to a file (changing the value 1 to 2 would write 2 decimals etc.)

![Output after float fomatting](img/pandas-save-file-2.png)

As a results you have a "cleaner" output file without the index column, and with only 1 decimal for floating point numbers.
<!-- #endregion -->
