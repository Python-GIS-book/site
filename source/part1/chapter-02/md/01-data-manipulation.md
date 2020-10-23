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

During the first part of this lesson you learned the basics of pandas data structures (*Series* and *DataFrame*) and got familiar with basic methods loading and exploring data.
Here, we will continue with basic data manipulation and analysis methods such calculations and selections.

We are now working in a new notebook file and we need to import pandas again. 
<!-- #endregion -->

```python
import pandas as pd
```

Let's work with the same input data `'Kumpula-June-2016-w-metadata.txt'` and load it using the `pd.read_csv()` method. Remember, that the first 8 lines contain metadata so we can skip those. This time, let's store the filepath into a separate variable in order to make the code more readable and easier to change afterwards: 

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Define file path:
fp = '../../data/NOAA/Kumpula-June-2016-w-metadata.txt'


# Read in the data from the file (starting at row 9):
data = pd.read_csv(fp, skiprows=8)
```

Remember to always check the data after reading it in:

```python
data.head()
```

<!-- #region deletable=true editable=true -->
## Basic calculations

One of the most common things to do in pandas is to create new columns based on calculations between different variables (columns).

We can create a new column `DIFF` in our DataFrame by specifying the name of the column and giving it some default value (in this case the decimal number `0.0`).
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Define a new column "DIFF"
data['DIFF'] = 0.0

# Check how the dataframe looks like:
data
```

<!-- #region deletable=true editable=true -->
Let's check the datatype of our new column:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data['DIFF'].dtypes
```

<!-- #region deletable=true editable=true -->
Okey, so we see that Pandas created a new column and recognized automatically that the data type is float as we passed a 0.0 value to it.

Let's update the column `DIFF` by calculating the difference between `MAX` and `MIN` columns to get an idea how much the temperatures have
been varying during different days:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
#Calculate max min difference
data['DIFF'] = data['MAX'] - data['MIN']

# Check the result
data.head()
```

<!-- #region deletable=true editable=true -->
The calculations were stored into the ``DIFF`` column as planned. 

You can also create new columns on-the-fly at the same time when doing the calculation (the column does not have to exist before). Furthermore, it is possible to use any kind of math
algebra (e.g. subtracttion, addition, multiplication, division, exponentiation, etc.) when creating new columns.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
We can for example convert the Fahrenheit temperatures in the `TEMP` column into Celsius using the formula that we have seen already many times. Let's do that and store it in a new column called `TEMP_CELSIUS`.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Create a new column and convert temp fahrenheit to celsius:
data['TEMP_CELSIUS'] = (data['TEMP'] - 32) / (9/5)

#Check output
data.head()
```

#### Check your understanding

Calculate the temperatures in Kelvins using the Celsius values **and store the result a new column** calle `TEMP_KELVIN` in our dataframe.
    
0 Kelvins is is -273.15 degrees Celsius as we learned during [Lesson 4](https://geo-python-site.readthedocs.io/en/latest/notebooks/L4/functions.html#let-s-make-another-function).

```python
# Add column "TEMP_KELVIN" and populate it with Kelvin values

```

<!-- #region deletable=true editable=true -->
## Selecting and updating data

We often want to select only specific rows from a DataFrame for further analysis. There are multiple ways of selecting subsets of a pandas DataFrame. In this section we will go through most useful tricks for selecting specific rows, columns and individual values.

### Accessing rows and columns

#### Selecting rows

One common way of selecting only specific rows from your DataFrame is done via **index slicing** to extract part of the DataFrame. Slicing in pandas can be done in a similar manner as with normal Python lists, i.e. you specify index range you want to select inside the square brackets: ``dataframe[start_index:stop_index]``.

Let's select the first five rows and assign them to a variable called `selection`:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select first five rows of dataframe using row index values
selection = data[0:5]
selection
```

<!-- #region deletable=true editable=true -->
```{note}
Here we have selected the first five rows (index 0-4) using the integer index.
```
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
#### Selecting several rows and columns

It is also possible to control which columns are chosen when selecting a subset of rows. In this case we will use [pandas.DataFrame.loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) which selects data based on axis labels (row labels and column labels). 

Let's select temperature values (column `TEMP`) from rows 0-5:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select temp column values on rows 0-5
selection = data.loc[0:5, 'TEMP']
selection
```

```{note}
In this case, we get six rows of data (index 0-5)! We are now doing the selection based on axis labels instead of the integer index.
```

<!-- #region deletable=true editable=true -->
It is also possible to select multiple columns when using `loc`. Here, we select the `TEMP` and `TEMP_CELSIUS` columns from a set of rows by passing them inside a list (`.loc[start_index:stop_index, list_of_columns]`):
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select columns temp and temp_celsius on rows 0-5
selection = data.loc[0:5, ['TEMP', 'TEMP_CELSIUS']]
selection
```

#### Check your understanding

Find the mean temperatures (in Celsius) for the last seven days of June. Do the selection using the row index values.

```python
# Mean temperature for the last seven days of June (use loc indexing to select the correct rows):
data.loc[23:29, 'TEMP_CELSIUS'].mean()
```

#### Selecting a single row

You can also select an individual row from specific position using the `.loc[]` indexing. Here we select all the data values using index 4 (the 5th row):

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select one row using index
row = data.loc[4]
row
```

<!-- #region deletable=true editable=true -->
``.loc[]`` indexing returns the values from that position as a ``pd.Series`` where the indices are actually the column names of those variables. Hence, you can access the value of an individual column by referring to its index using following format (both should work):

<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
#Print one attribute from the selected row
row['TEMP']
```

#### Selecting a single value

Sometimes it is enough to access a single value in a DataFrame. In this case, we can use [DataFrame.at](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html#pandas-dataframe-at) instead of `Data.Frame.loc`.

Let's select the temperature (column `TEMP`) on the first row (index `0`) of our DataFrame.

```python
selection.at[0, "TEMP"]
```

<!-- #region -->
### EXTRA: Selections by integer position


`.loc` and `.at` are based on the *axis labels* - the names of columns and rows. Axis labels can be also something else than "traditional" index values. For example, datetime is commonly used as the row index. `.iloc` is another indexing operator which is based on *integer value* indices. Using `.iloc`, it is possible to refer also to the columns based on their index value. For example,  `data.iloc[0,0]` would return `20160601` in our example data frame.
    
See the pandas documentation for more information about [indexing and selecting data](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-and-selecting-data).

For example, we could select select `TEMP` and the `TEMP_CELSIUS` columns from a set of rows based on their index.
<!-- #endregion -->

```python
data.iloc[0:5:,0:2]
```

To access the value on the first row and second column (`TEMP`), the syntax for `iloc` would be:
    

```python
data.iloc[0,1]
```

We can also access individual rows using `iloc`. Let's check out the last row of data:

```python
data.iloc[-1]
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
