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

# Pandas basics

## What is Pandas?

Pandas [^urlpandas]  is a modern, powerful and feature rich library that is designed for doing
data analysis in Python. It is a mature data analytics framework that is widely used among different fields of science, thus there exists a lot of good examples and documentation that can help you get going with your data analysis tasks. Pandas development started in 2008 and it is now maintained by an active developer community. The book Python for Data Analysis (First published in 2012 and updated in 2017) by  Wes McKinney (main developer of Pandas) provides a comprehensive overview of wrangling data using Pandas.

Pandas is a "high-level" package, which means that it makes use of several other packages in the background.
Pandas combines the performance of powerful Python libraries such as [NumP](http://www.numpy.org/),
(matplotlib)[https://matplotlib.org/] and (scipy)[https://www.scipy.org/]. Thus, you can use many of the features included in those packages even without importing them separately. This book focuses primarily on Pandas because it is easy-to-use, efficient and intuitive.

One of the most useful features of Pandas is its ability to write and read data to and from numerous data formats.
Pandas supports reading and writing data e.g. from/to:

- CSV
- JSON
- HTML
- MS Excel
- HDF5
- Stata
- SAS
- Python Pickle format
- SQL (Postgresql, MySQL, Oracle, MariaDB, etc.)

See full list from (Pandas docs)[http://pandas.pydata.org/pandas-docs/version/0.20/io.html].

<!-- #region deletable=true editable=true -->
## Pandas data structures

In Pandas, table-like data are stored in two-dimensional DataFrames with labeled rows and columns. You can think of the pandas DataFrame as a programmable spreadsheet. The Pandas DataFrame was originally inspired by dataframes that are in-built in the R programming language. One-dimensional sequences of values are stored in pandas Series. One row or one column in a Pandas DataFrame is actually a Pandas Series. You can think of a pandas Series as a clever list. 

![Pandas data structures](./../img/pandas-structures.png)

*Pandas DataFrame is a 2-dimensional data structure used for storing and mainpulating table-like data (data with rows and columns). Pandas Series is a 1-dimensional data structure used for storing and manipulating an sequence of values.*

These Pandas structures incorporate a number of things we've already encountered, such as indices, data stored in a collection, and data types. Let's have another look at the Pandas data structures below with some additional annotation.

![Pandas data structures annotated](./../img/pandas-structures-annotated.png)

As you can see, both DataFrames and Series in pandas have an index that can be used to select values, but they also have column labels to identify columns in DataFrames. In the lesson this week we'll use many of these features to explore real-world data and learn some useful data analysis procedures.

For a comprehensive overview of Pandas data structures you can have a look at Chapter 5 in {cite}`MacKinney2017` and Pandas online documentation about data structures [^urlds].
<!-- #endregion -->

## Reading tabular data 

### Input data: weather statistics

Our input data is a text file containing weather observations from Kumpula, Helsinki, Finland retrieved from NOAA [^noaa] climate database:

- File name: [Kumpula-June-2016-w-metadata.txt](Kumpula-June-2016-w-metadata.txt) (have a look at the file before reading it in using pandas!)
- The data file contains observed daily mean, minimum, and maximum temperatures from June 2016 recorded from the Kumpula weather observation station in Helsinki.
- There are 30 rows of data in this sample data set.
- The data has been derived from a data file of daily temperature measurments downloaded from NOAA [^urlnoaa1]

### Reading a csv file

Now we're ready to read in our temperature data file. First, we need to import the Pandas module. It is customary to import pandas as `pd`:

```python deletable=true editable=true
import pandas as pd
```

<!-- #region deletable=true editable=true -->
Next, we will read the input data file and store the contents of that file into a variable called `data` Using the `read_csv()` function:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data = pd.read_csv('../../data/NOAA/Kumpula-June-2016-w-metadata.txt')
```


Our input file is a comma-delimited file; columns in the data are separted by commas (`,`) on each row. The `read_csv()` function has the comma as the default delimiter so we don't need to specify it separately. 

The `sep` parameter can be used to specify whether the input data uses some other character, such as semicolon (`;`) as a delimiter. For a full list of available parameters, please refer to the pandas documentation for pandas.read_csv [^urlreadcsv], or run `help(pd.read_csv)`.



```{note}

**Reading different file formats:**`read_csv()` in pandas is a general function for reading data files separated by commas, spaces, or other common separators. 

Pandas has several functions for parsing input data from different formats. There is, for example, a separate function for reading Excel files .read_excel()`. Another useful function is `read_pickle()` for reading data stored in the Python pickle format.. Check out the pandas documentation about input and output functions [^urlpandasiotools] and Chapter 6 in {cite}`MacKinney2017` for more details about reading data.
```


If all goes as planned, you should now have a new variable `data` in memory that contains the input data. 

Let's check the the contents of this variable by calling `data` or `print(data)`:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
print(data)
```

<!-- #region deletable=true editable=true -->
This looks OK, but there are some strange values present such as `NaN`, and the first lines of the dataframe look a bit weird.

`NaN` stands for "not a number", and might indicate some problem with reading in the contents of the file. Plus, we expected about 30 lines of data, but the index values go up to 36 when we print the contents of the `data` variable. Looks like we need to investigate this further.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
As we can observe, there are some metadata at the top of the file giving basic information about its contents and source. This isn't data we want to process, so we need to skip over that part of the file when we load it.

Here are the 8 first rows of data in the text file (note that the 8th row is blank):
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
```
# Data file contents: Daily temperatures (mean, min, max) for Kumpula, Helsinki
#                     for June 1-30, 2016
# Data source: https://www.ncdc.noaa.gov/cdo-web/search?datasetid=GHCND
# Data processing: Extracted temperatures from raw data file, converted to
#                  comma-separated format
#
# David Whipp - 02.10.2017

```
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Fortunately, skipping over rows is easy to do when reading in data using pandas. We just need to add the `skiprows` parameter when we read the file, listing the number of rows to skip (8 in this case).

Let's try reading the datafile again, and this time defining the `skiprows` parameter.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data = pd.read_csv('../../data/NOAA/Kumpula-June-2016-w-metadata.txt', skiprows=8)
```

<!-- #region deletable=true editable=true -->
Let's now print the dataframe and see what changed:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
print(data)
```

<!-- #region deletable=true editable=true -->
After reading in the data, it is always good to check that everything went well by printing out the data as we did here. However, often it is enough to have a look at the top few rows of the data. 

We can use the `head()` function of the pandas DataFrame object to quickly check the top rows. By default, the `head()` function returns the first 5 rows of the DataFrame:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data.head()
```

We can also check the last rows of the data using `data.tail()`:

```python
data.tail()
```

<!-- #region deletable=true editable=true -->
Note that Pandas that DataFrames have **labelled axes (rows and columns)**.  In our sample data, the rows labeled with an index value (`0` to `29`), and columns labelled `YEARMODA`, `TEMP`, `MAX`, and `MIN`. Later on, we will learn how to use these labels for selecting and updating subsets of the data.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Let's also confirm the data type of our data variable:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
type(data)
```

<!-- #region deletable=true editable=true -->
No surprises here, our data variable is a Pandas DataFrame.
<!-- #endregion -->

**Check your understanding**

Read the file `Kumpula-June-2016-w-metadata.txt` in again and store its contents in a new variable called `temp_data`. In this case you should only read in the columns `YEARMODA` and `TEMP`, so the new variable `temp_data` should have 30 rows and 2 columns. You can achieve this using the `usecols` parameter when reading in the file. Feel free to check for more help in the [pandas.read_csv documentation](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html).

```python
temp_data = pd.read_csv('../../data/NOAA/Kumpula-June-2016-w-metadata.txt', skiprows=8, usecols=["YEARMODA", "TEMP"])
```

```python
temp_data.head()
```

<!-- #region deletable=true editable=true -->
## Basic data exploration
### DataFrame properties

Let's continue with the full data set that we have stored in the variable `data` and explore it's contents further. 
A normal first step when you load new data is to explore the dataset a bit to understand how the data is structured, and what kind of values are stored in there.
<!-- #endregion -->

Let's start by checking the size of our data frame. We can use the `len()` function similar to the use with lists to check how many rows we have:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Check the number of rows 
len(data)
```

<!-- #region deletable=true editable=true -->
We can also get a quick sense of the size of the dataset using the `shape` attribute.

<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Check dataframe shape (number of rows, number of columns)
data.shape
```

<!-- #region deletable=true editable=true -->
Here we see that our dataset has 30 rows and 4 columns, just as we saw above when printing out the entire DataFrame.
<!-- #endregion -->

```{note}
`shape` is one of the several attributes related to a pandas DataFrame object [^urlpandasattributes]. Pay attention that do not use parentheses in the syntax when accessing attributes.
```


Let's also check the column names we have in our DataFrame. We already saw the column names when we checked the 5 first rows using `data.head()`, but often it is useful to access the column names directly. You can check the column names by calling `data.columns` (returns an index object that contains the column labels) or `data.columns.values`:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
#Print column names
data.columns.values
```

<!-- #region deletable=true editable=true -->
We can also find information about the row identifiers using the `index` attribute:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
#Print index
data.index
```

<!-- #region deletable=true editable=true -->
Here we see how the data is indexed, starting at 0, ending at 30, and with an increment of 1 between each value. This is basically the same way in which Python lists are indexed, however, pandas allows also other ways of identifying the rows. DataFrame indices could, for example, be character strings, or date objects. We will learn more about resetting the index later.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
What about the data types of each column in our dataFrame? We can check the data type of all columns at once using `pandas.DataFrame.dtypes`:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Print data types
data.dtypes
```

<!-- #region deletable=true editable=true -->
Here we see that `YEARMODA` is an integer value (with 64-bit precision; ``int64``), while the other values are all decimal values with 64-bit precision (float64).
<!-- #endregion -->

**Check your understanding**

See if you can find a way to print out the number of columns in our DataFrame.

```python
len(data.columns)
```

### Selecting columns


We can select specific columns based on the column values. The basic syntax is `dataframe[value]`, where value can be a single column name, or a list of column names. Let's start by selecting two columns, `'YEARMODA'` and `'TEMP'`:

```python
selection = data[['YEARMODA','TEMP']]
```

```python
selection
```

Let's also check the data type of this selection:

```python
type(selection)
```

The subset is still a pandas DataFrame, and we are able to use all the methods and attributes related to a pandas DataFrame also with this subset. For example, we can check the shape:

```python
selection.shape
```

<!-- #region deletable=true editable=true -->
We can also access a single column of the data based on the column name:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data['TEMP']
```

What about the type of the column itself?

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Check datatype of the column
type(data['TEMP'])
```

<!-- #region deletable=true editable=true -->
Each column (and each row) in a pandas data frame is indeed a pandas Series.
<!-- #endregion -->

````{note}
You can also retreive a column using a different syntax:
    
``` 
data.TEMP
```

This syntax works only if the column name is a valid name for a Python variable (e.g. the column name should not contain whitespace). The syntax `data["column"]` works for all kinds of column names, so we recommend using this approach.
````

<!-- #region editable=true -->
### Unique values
<!-- #endregion -->

<!-- #region editable=true -->
Sometimes it is useful to extract the unique values that you have in your column.
We can do that by using `unique()` method:
<!-- #endregion -->

```python editable=true jupyter={"outputs_hidden": false}
# Get unique celsius values
data['TEMP'].unique()
```

<!-- #region editable=true -->
As a result we get an array of unique values in that column. We can also directly access the number of unique values using the `nunique()` method:
<!-- #endregion -->

```python editable=true jupyter={"outputs_hidden": false}
# Number of unique values
print("There were", data['TEMP'].nunique(), "days with unique mean temperatures in June 2016.")
```

### Descriptive statistics

<!-- #region deletable=true editable=true -->
Pandas DataFrames and Series contain useful methods for getting summary statistics. Available methods include `mean()`, `median()`, `min()`, `max()`, and `std()` (the standard deviation).
<!-- #endregion -->

We could, for example, check the mean temperature in our input data. We check the mean for a single column (*Series*): 

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Check mean value of a column
data['TEMP'].mean()
```

and for all columns (in the *DataFrame*):

```python
# Check mean value for all columns
data.mean()
```

<!-- #region deletable=true editable=true -->
For an overview of the basic statistics for all attributes in the data, we can use the `describe()` method:

<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Get descriptive statistics
data.describe()
```

<!-- #region deletable=true editable=true -->
## From lists to Pandas objects (DEL OR MOVE?)

Most often we create pandas objects by reading in data from an external source, such as a text file. Here, we will briefly see how you can create pandas objects from Python lists. If you have long lists of numbers, for instance, creating a Pandas Series will allow you to interact with these values more efficiently in terms of computing time.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Create Pandas Series from a list
number_series = pd.Series([ 4, 5, 6, 7.0])
print(number_series)
```

<!-- #region deletable=true editable=true -->
Note that Pandas is smart about the conversion, detecting a single floating point value (`7.0`) and assigning all values in the Series the data type float64.
<!-- #endregion -->

If needed, you can also set a custom index when creating the object:

```python
number_series = pd.Series([ 4, 5, 6, 7.0], index=['a','b','c','d'])
print(number_series)
```

```python
type(number_series)
```

How about combining several lists as a DataFrame? Let's take a subset of the lists we used in Exercise 3, problem 3 and see how we could combine those as a pandas DataFrame:

```python
# Station names
stations = ['Hanko Russarö', 'Heinola Asemantaus', 'Helsinki Kaisaniemi', 'Helsinki Malmi airfield']

# Latitude coordinates of Weather stations  
lats = [59.77, 61.2, 60.18, 60.25]

# Longitude coordinates of Weather stations 
lons = [22.95, 26.05, 24.94, 25.05]
```

Often we indeed create pandas DataFrames by reading in data (e.g. using `pd.read_csv(filename.csv)`), but sometimes your might also combine lists into a DataFrame inside the script using the `pandas.DataFrame` constructor. Here, we are using a *Python dictionary* `{"column_1": list_1, "column_2": list_2, ...}` to indicate the structure of our data. 

```python
new_data = pd.DataFrame(data = {"station_name" : stations, "lat" : lats, "lon" : lons})
new_data
```

```python
type(new_data)
```

Often, you might start working with an empty data frame in stead of existing lists:

```python
df = pd.DataFrame()
```

```python
print(df)
```

Check more details about available paramenters and methods from [the pandas.DataFrame documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas-dataframe).


### Footnotes
[^urlpandas] http://pandas.pydata.org/
[^urlpandas]: https://pandas.pydata.org/pandas-docs/stable/
[^urlds]: https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html
[^urlnoaa1]: US National Oceanographic and Atmospheric Administration's National Centers for Environmental Information: https://www.ncdc.noaa.gov/
[^urnlnoaa2]: https://www.ncdc.noaa.gov/cdo-web/
[^urlreadcsv]: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
[^urlpandasiotools]: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-tools-text-csv-hdf5
[^urlpandasattributes]: https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#attributes-and-underlying-data
