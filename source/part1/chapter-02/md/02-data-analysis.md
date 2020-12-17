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

# Data wrangling, grouping and aggregation

Next, we will continue working with weather data, but expand our analysis to cover longer periods of data from Finland. In the following, you will learn various useful techniques in pandas to manipulate, group and aggregate the data in different ways that are useful when extracting insights from your data. In the end, you will learn how to create an automated data analysis workflow that can be repeated with multiple input files having a similar structure. As a case study, we will investigate whether January 2020 was the warmest month on record also in Finland, as the month was the warmest one on record globally [^noaanews]. 


## Cleaning data while reading

In this section we are using weather observation data from Finland that was downloaded from NOAA (see `Datasets` chapter for further details). The input data is separated with varying number of spaces (i.e., fixed width). The first lines and columns of the data look like following:

``` 
  USAF  WBAN YR--MODAHRMN DIR SPD GUS CLG SKC L M H  VSB MW MW MW MW AW AW AW AW W TEMP DEWP    SLP   ALT    STP MAX MIN PCP01 PCP06 PCP24 PCPXX SD
029440 99999 190601010600 090   7 *** *** OVC * * *  0.0 ** ** ** ** ** ** ** ** *   27 **** 1011.0 ***** ****** *** *** ***** ***** ***** ***** ** 
029440 99999 190601011300 ***   0 *** *** OVC * * *  0.0 ** ** ** ** ** ** ** ** *   27 **** 1015.5 ***** ****** *** *** ***** ***** ***** ***** ** 
029440 99999 190601012000 ***   0 *** *** OVC * * *  0.0 ** ** ** ** ** ** ** ** *   25 **** 1016.2 ***** ****** *** *** ***** ***** ***** ***** ** 
029440 99999 190601020600 ***   0 *** *** CLR * * *  0.0 ** ** ** ** ** ** ** ** *   26 **** 1016.2 ***** ****** *** *** ***** ***** ***** ***** **
```

By looking at the data, we can notice a few things that we need to consider when reading the data:

1. **Delimiter:** The columns are separated with a varying amount of spaces which requires using some special tricks when reading the data with pandas `read_csv`
2. **NoData values:** NaN values in the NOAA data are coded with varying number of `*` characters, hence, we need to be able to instruct pandas to interpret those as NaNs. 
3. **Many columns**: The input data contains altogether 33 columns. Many of those do not contain any meaningful data for our needs. Hence, we should probably ignore the unnecessary columns already at this stage. 

Handling and cleaning heterogeneous input data (such as our example here) could naturally be done after the data has been imported to a DataFrame. However, in many cases, it is actually useful to do some cleaning and preprocessing already when reading the data. In fact, that is often much easier to do. In our case, we can read the data with varying number of spaces between the columns (1) by using a parameter `delim_whitespace=True` (alternatively, specifying `sep='\s+'` would work). For handling the NoData values (2), we can tell pandas to consider the `*` characters as NaNs by using a paramater `na_values` and specifying a list of characters that should be converted to NaNs. Hence, in this case we can specify `na_values=['*', '**', '***', '****', '*****', '******']` which will then convert the varying number of `*` characters into NaN values. Finally, we can limit the number of columns that we read (3) by using the `usecols` parameter, which we already used previously. In our case, we are interested in columns that might be somehow useful to our analysis (or at least meaningful to us), including e.g. the station name, timestamp, and data about the wind and temperature: `'USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN'`

Achieving all these things is pretty straightforward using the `read_csv` function as we can see: 

```python
import pandas as pd

# Define relative path to the file
fp = 'data/029820.txt'

# Read data using varying amount of spaces as separator, 
# specifying '*' characters as NoData values, 
# and selecting only specific columns from the data
data = pd.read_csv(fp, delim_whitespace=True, 
                   na_values=['*', '**', '***', '****', '*****', '******'],
                   usecols=['USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN']
                  )
```

Let's see now how the data looks by printing the first five rows with the `head()` function:

```python jupyter={"outputs_hidden": false}
data.head()
```

Perfect, looks good. We have skipped a bunch of unnecessary columns and also the asterisk (\*) characters have been correctly converted to NaN values.  


### Renaming columns

Let's take a closer look at the column names of our DataFrame. A description for all these columns is available in the metadata file [data/3505doc.txt](data/3505doc.txt). 

```python jupyter={"outputs_hidden": false}
data.columns
```

As we see, some of the column names are a bit awkward and difficult to interpret. Luckily, it is easy to alter labels in a pandas DataFrame using the `rename` function. In order to change the column names, we need to tell pandas how we want to rename the columns using a dictionary that converts the old names to new ones. As you probably remember from Chapter 1, a `dictionary` is a specific data structure in Python for storing key-value pairs.

We can define the new column names using a dictionary where we list "`key: value`" pairs in following manner:
   
- `USAF`: `STATION_NUMBER`
- `YR--MODAHRMN`: `TIME`
- `SPD`: `SPEED`
- `GUS`: `GUST`
- `TEMP`: `TEMP_F`

Hence, the original column name (e.g. `YR--MODAHRMN`) is the dictionary `key` which will be converted to a new column name `TIME` (which is the `value`). The temperature values in our data file is again represented in Fahrenheit. We will soon convert these temperatures to Celsius. Hence, in order to avoid confusion with the columns, let's rename the column `TEMP` to `TEMP_F`. Also the station number `USAF` is much more intuitive if we call it `STATION_NUMBER`.

```python jupyter={"outputs_hidden": false}
# Create the dictionary with old and new names
new_names = {'USAF':'STATION_NUMBER', 'YR--MODAHRMN': 'TIME', 
             'SPD': 'SPEED', 'GUS': 'GUST', 
             'TEMP': 'TEMP_F'
            }
new_names
```

Our dictionary looks correct, so now we can change the column names by passing that dictionary using the parameter `columns` in the `rename()` function:

```python jupyter={"outputs_hidden": false}
# Rename the columns
data = data.rename(columns=new_names)
data.columns
```

Perfect, now our column names are easier to understand and use. 

## Apply: How to use functions with Series

Now it's time to convert those temperatures from Fahrenheit to Celsius. We have done this many times before, but this time we will learn how to apply our own functions to data in a pandas DataFrame. We will define a function for the temperature conversion, and apply this function for each Celsius value on each row of the DataFrame. Output celsius values should be stored in a new column called `TEMP_C`.

But first, it is a good idea to check some basic properties of our new input data before proceeding with data analysis.

```python
# First rows
data.head(2)
```

```python
# Last rows
data.tail(2)
```

```python
# Data types
data.info()
```

Nothing suspicous for the first and last rows, but here with `info()` we can see that the number of observations per column seem to be varying if you compare the `Non-Null Count` information to the number of entries in the data (N=198334). Only station number and time seem to have data on each row. All other columns seem to have some missing values. This is not necessarily anything dangerous, but good to keep in mind. 

```python
# Descriptive stats
data.describe()
```

By looking at the `TEMP_F` values (Fahrenheit temperatures), we can confirm that our measurements seems more or less valid because the value range of the temperatures makes sense, i.e. there are no outliers such as extremely high `MAX` values or low `MIN` values. It is always a good practice to critically check your data before doing any analysis, as it is possible that your data may include incorrect values, e.g. due to a sensor malfunction or human error. 


### Defining function for pandas

Now we are sure that our data looks okay, and we can start our temperature conversion process by first defining our temperature conversion function from Fahrenheit to Celsius. When using functions with pandas, you can define them exactly in a similar manner as you would do normally. Hence, let's define a function that converts Fahrenheits to Celsius: 

```python
def fahr_to_celsius(temp_fahrenheit):
    """Function to convert Fahrenheit temperature into Celsius.

    Parameters
    ----------

    temp_fahrenheit: int | float
        Input temperature in Fahrenheit (should be a number)
        
    Returns
    -------
    
    Temperature in Celsius (float)
    """

    # Convert the Fahrenheit into Celsius
    converted_temp = (temp_fahrenheit - 32) / 1.8
    
    return converted_temp
```

Now we have the function defined and stored in memory. At this point it is good to test the function with some known value.

```python
fahr_to_celsius(32)
```

32 Fahrenheits is indeed 0 Celsius, so our function seem to be working correctly.


### Using the function by iterating over rows

Next we will learn how to use our function with data stored in pandas DataFrame. We will first apply the function row-by-row using a `for` loop and then we will learn a more efficient way of applying the function to all rows at once.

Looping over rows in a DataFrame can be done in a couple of different ways. A common approach is to use a `iterrows()` method which loops over the rows as a index-Series pairs. In other words, we can use the `iterrows()` method together with a `for` loop to repeat a process *for each row in a Pandas DataFrame*. Please note that iterating over rows this way is a rather inefficient approach, but it is still useful to understand the logic behind the iteration. Other commonly used and faster way to iterate over rows is to use `itertuples()` method. Next, we will see examples from both of them.

When using the `iterrows()` method it is important to understand that `iterrows()` accesses not only the values of one row, but also the `index` of the row as we mentioned. Let's start with a simple for loop that goes through each row in our DataFrame:

```python jupyter={"outputs_hidden": false}
# Iterate over the rows
for idx, row in data.iterrows():
    
    # Print the index value
    print('Index:', idx)
    
    # Print the temperature from the row
    print('Temp F:', row['TEMP_F'], "\n")
    
    break
```

We can see that the `idx` variable indeed contains the index value at position 0 (the first row) and the `row` variable contains all the data from that given row stored as a pandas `Series`. Notice, that when developing a for loop, you don't always need to go through the entire loop if you just want to test things out. Using the `break` statement in Python terminates a loop whenever it is placed inside a loop. We used it here just to test check out the values on the first row. With a large data, you might not want to print out thousands of values to the screen!

Let's now create an empty column `TEMP_C` for the Celsius temperatures and update the values in that column using the `fahr_to_celsius` function that we defined earlier. For updating the value, we can use `at` which we already used earlier in this chapter. This time, we will use the `itertuples()` method which works in a similar manner, except it only return the row values without the `index`. When using `itertuples` accessing the row values needs to be done a bit differently, because the row is not a Series, but a `named tuple` (hence the name). A tuple is like a list (but immutable, i.e. you cannot change it) and "named tuple" is a special kind of tuple object that adds the ability to access the values by name instead of position index. Hence, below we will access the `TEMP_F` value by using `row.TEMP_F` (compare to how we accessed the value in the prevous code block). 

```python
# Create an empty column for the output values
data['TEMP_C'] = 0.0

# Iterate over the rows 
for row in data.itertuples():
    
    # Convert the Fahrenheit to Celsius
    # Notice how we access the row value
    celsius = fahr_to_celsius(row.TEMP_F)
    
    # Update the value for 'Celsius' column with the converted value
    # Notice how we can access the Index value
    data.at[row.Index, 'TEMP_C'] = celsius

# Print the last row to show how it looks like
row
```

Here we can see how our row (i.e. named tuple) looks like. It is like a weird looking dictionary with values assigned to the names of our columns. Before explaining more, let's see how our DataFrame looks like now.

```python
data.head()
```

Okay, now we have iterated over our data and updated the temperatures in Celsius to `TEMP_C` column by using our `fahr_to_celsius` function. The values look correct as 32 Fahrenheits indeed is 0 Celsius degrees, as can be seen on the second row. 

A couple of notes about our appoaches. We used `itertuples()` method for looping over the values because it is significantly faster compared to `iterrows()` (can be ~100x faster). We used `at` to assign the value to the DataFrame because it is designed to access single values more efficiently compared to `.loc`, which can access also groups of rows and columns. That said, you could have used `data.loc[idx, new_column] = celsius` to achieve the same result (it's just slightly slower). 


### Using the function with `apply`

Although using for loop with `itertuples` can be fairly efficient, pandas DataFrames and Series have a dedicated method called `apply` for applying functions on columns (or rows). `apply` can be even faster than `itertuples` especially if you have large number of rows, such as in our case. When using `apply`, we pass the function as an argument to the `apply` method. Let's start by applying the function to the `TEMP_F` column that contains the temperature values in Fahrenheit:

```python
data['TEMP_F'].apply(fahr_to_celsius)
```

The results look logical. Notice how we passed the `fahr_to_celsius` function without using the typical parentheses `()` after the name of the function. When using `apply`, you should always leave out the parentheses from the function that you use. Meaning that you should use `apply(fahr_to_celsius)` instead of `apply(fahr_to_celsius())`. 

Our command above only returns the Series of temperatures to the screen, but naturally we can also store them permanently into a new column (overwriting the old values). 

```python
data['TEMP_C'] = data['TEMP_F'].apply(fahr_to_celsius)
```

A nice thing with `apply` is that we can also apply the function on several columns at once. Below, we also sort the values in descending order based on values in `MIN` column to see that applying our function really works.  

```python
multiple_columns_at_once = data[['TEMP_F', 'MIN', 'MAX']].apply(fahr_to_celsius)
multiple_columns_at_once.sort_values(by="MIN", ascending=False).head()
```

You can also directly store the outputs to new columns `'TEMP_C'`, `'MIN_C'`, `'MAX_C'`.

```python
data[['TEMP_C', 'MIN_C', 'MAX_C']]  = data[['TEMP_F', 'MIN', 'MAX']].apply(fahr_to_celsius)
data.head()
```

<!-- #region -->


We are teaching the `.iterrows()` method because it helps to understand the structure of a DataFrame and the process of looping through DataFrame rows. However, using `.apply()` is often more efficient in terms of execution time. 

At this point, you have seen a couple of different ways to apply functions over rows of data. The most important thing is that you understand the logic of how loops work and how you can use your own functions to modify the values in a pandas DataFrame. 
<!-- #endregion -->

## String slicing

We will eventually want to group our data based on month in order to see if April temperatures in 2019 were higher than average. Currently, the date and time information is stored in the column `TIME` (which was originally titled `YR--MODAHRMN`:

`YR--MODAHRMN = YEAR-MONTH-DAY-HOUR-MINUTE IN GREENWICH MEAN TIME (GMT)`


Let's have a closer look at the date and time information we have by checking the values in that column, and their data type:

```python
data['TIME'].head(10)
```

```python
data['TIME'].tail(10)
```

The `TIME` column contains several observations per day (and even several observations per hour). The timestamp for the first observation is `190601010600`, i.e. from 1st of January 1906 (way back!), and the timestamp for the latest observation is `201910012350`.

```python
data['TIME'].dtypes
```

The information is stored as integer values.


We would want to **aggregate the data on a monthly level**, and in order to do so we need to "label" each row of data based on the month when the record was observed. In order to do this, we need to somehow separate information about the year and month for each row.

In practice, we can create a new column (or an index) containing information about the month (including the year, but excluding days, hours and minutes).

Before further processing, we want to convert the `TIME` column as character strings for convenience:

```python jupyter={"outputs_hidden": false}
# Convert to string
data['TIME_STR'] = data['TIME'].astype(str)
```

It is possible to convert the date and time information into character strings and "cut" the needed information from the [string objects](https://docs.python.org/3/tutorial/introduction.html#strings). If we look at the latest time stamp in the data (`201910012350`), you can see that there is a systematic pattern `YEAR-MONTH-DAY-HOUR-MINUTE`. Four first characters represent the year, and six first characters are year + month!

```python
date = "201910012350"
date[0:6]
```

Based on this information, we can slice the correct range of characters from the `TIME_STR` column using [pandas.Series.str.slice()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html)


```python
# SLice the string
data['YEAR_MONTH'] = data['TIME_STR'].str.slice(start=0, stop=6)

# Let's see what we have
data.head()
```

Nice! Now we have "labeled" the rows based on information about day of the year and hour of the day.


#### Check your understanding

Create a new column `'MONTH'` with information about the month without the year.

```python
# Extract information about month from the TIME_STR column into a new column 'MONTH':
data['MONTH'] = data['TIME_STR'].str.slice(start=4, stop=6)
```

```python
# Check the result:
data[['YEAR_MONTH', 'MONTH']]
```

## Grouping and aggregating data

Here, we will learn how to use [pandas.DataFrame.groupby](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html) which is a handy method for compressing large amounts of data and computing statistics for subgroups.

We will use the groupby method to calculate the average temperatures for each month trough these main steps:

  1. **grouping the data** based on year and month
  2. Calculating the average for each month (each group) 
  3. Storing those values into **a new DataFrame** `monthly_data`


Before we start grouping the data, let's once more check how our input data looks like:

```python
print("number of rows:", len(data))
```

```python
data.head()
```

We have quite a few rows of weather data, and several observations per day. Our goal is to create an aggreated data frame that would have only one row per month.


Let's **group** our data based on unique year and month combinations

```python
grouped = data.groupby('YEAR_MONTH')
```

````{note}
It would be also possible to create combinations of years and months on-the-fly when grouping the data:
    
```
# Group the data 
grouped = data.groupby(['YEAR', 'MONTH'])
```
````


Let's explore the new variable `grouped`:

```python
type(grouped)
```

```python
len(grouped)
```

We have a new object with type `DataFrameGroupBy` with 82 groups. In order to understand what just happened, let's also check the number of unique year and month combinations in our data:

```python
data['YEAR_MONTH'].nunique()
```

Length of the grouped object should be the same as the number of unique values in the column we used for grouping. For each unique value, there is a group of data.


Let's explore our grouped data further. 

Check the "names" of each group

```python
# Next line will print out all 82 group "keys"
#grouped.groups.keys()
```

**Accessing data for one group:**

- Let's check the contents for a group representing August 2019 (name of that group is `(2019, 4)` if you grouped the data based on datetime columns `YEAR` and `MONTH`). We can get the values of that hour from the grouped object using the `get_group()` method:

```python jupyter={"outputs_hidden": false}
# Specify a month (as character string)
month = "190601"

# Select the group
group1 = grouped.get_group(month)
```

```python
# Let's see what we have
group1
```

Ahaa! As we can see, a single group contains a **DataFrame** with values only for that specific month. Let's check the DataType of this group:

```python
type(group1)
```

So, one group is a pandas DataFrame! This is really useful, because we can now use all the familiar DataFrame methods for calculating statistics etc for this specific group. 
We can, for example, calculate the average values for all variables using the statistical functions that we have seen already (e.g. mean, std, min, max, median, etc.).

We can do that by using the `mean()` function that we already used during Lesson 5. 

- Let's calculate the mean for following attributes all at once:
   - `DIR`, 
   - `SPEED`, 
   - `GUST`, 
   - `TEMP`, 
   - `TEMP_C`
   - `MONTH` 

```python jupyter={"outputs_hidden": false}
# Specify the columns that will be part of the calculation
mean_cols = ['DIR', 'SPEED', 'GUST', 'TEMP_F', 'TEMP_C']

# Calculate the mean values all at one go
mean_values = group1[mean_cols].mean()

# Let's see what we have
print(mean_values)
```

Here we saw how you can access data from a single group. For getting information about all groups (all months) we can use a `for` loop or methods available in the grouped object.

**For loops and grouped objects:**

When iterating over the groups in our `DataFrameGroupBy`  object it is important to understand that a single group in our `DataFrameGroupBy` actually contains not only the actual values, but also information about the `key` that was used to do the grouping. Hence, when iterating over the data we need to assign the `key` and the values into separate variables.

- Let's see how we can iterate over the groups and print the key and the data from a single group (again using `break` to only see what is happening).

```python jupyter={"outputs_hidden": false}
# Iterate over groups
for key, group in grouped:
    # Print key and group
    print("Key:\n", key)
    print("\nFirst rows of data in this group:\n", group.head())
    
    # Stop iteration with break command
    break
```

Okey so from here we can see that the `key` contains the name of the group (year, month).

- Let's see how we can create a DataFrame where we calculate the mean values for all those weather attributes that we were interested in. I will repeat slightly the earlier steps so that you can see and better understand what is happening.

```python
# Create an empty DataFrame for the aggregated values
monthly_data = pd.DataFrame()

# The columns that we want to aggregate
mean_cols = ['DIR', 'SPEED', 'GUST', 'TEMP_F', 'TEMP_C']

# Iterate over the groups
for key, group in grouped:
    
   # Calculate mean
   mean_values = group[mean_cols].mean()

   # Add the ´key´ (i.e. the date+time information) into the aggregated values
   mean_values['YEAR_MONTH'] = key

   # Append the aggregated values into the DataFrame
   monthly_data = monthly_data.append(mean_values, ignore_index=True)
```

- Let's see what we have now:

```python jupyter={"outputs_hidden": false}
print(monthly_data)
```

Awesome! Now we have aggregated our data and we have a new DataFrame called `monthly_data` where we have mean values for each month in the data set.


**Mean for all groups at once**

We can also achieve the same result by computing the mean of all columns for all groups in the grouped object:

```python
grouped.mean()
```

### Detecting warm months

Now, we have aggregated our data on monthly level and all we need to do is to check which years had the warmest April temperatures. A simple approach is to select all Aprils from the data, group the data and check which group(s) have the highest mean value:

- select all records that are from April (regardless of the year):

```python
aprils = data[data['MONTH']=="04"]
```

- take a subset of columns that might contain interesting information:

```python
aprils = aprils[['STATION_NUMBER','TEMP_F', 'TEMP_C','YEAR_MONTH']]
```

- group by year and month:

```python
grouped = aprils.groupby(by='YEAR_MONTH')
```

- calculate mean for each group:

```python
monthly_mean = grouped.mean()
```

```python
monthly_mean.head()
```

- check the highest temperature values (sort the data frame in a descending order):

```python
monthly_mean.sort_values(by='TEMP_C', ascending=False).head(10)
```

How did April 2019 rank at the Tampere Pirkkala observation station? 


## Automating the analysis

Finally, let's repeat the data analysis steps above for all the available data we have (!!). First, confirm the path to the **folder** where all the input data are located. 
The idea is, that we will repeat the analysis process for each input file using a (rather long) for loop! Here we have all the main analysis steps with some additional output info - all in one long code cell:

```python
# Read selected columns of  data using varying amount of spaces as separator and specifying * characters as NoData values
data = pd.read_csv(fp, delim_whitespace=True, 
                   usecols=['USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN'], 
                   na_values=['*', '**', '***', '****', '*****', '******'])

# Rename the columns
new_names = {'USAF':'STATION_NUMBER','YR--MODAHRMN': 'TIME', 'SPD': 'SPEED', 'GUS': 'GUST', 'TEMP':'TEMP_F'}
data = data.rename(columns=new_names)

#Print info about the current input file:
print("STATION NUMBER:", data.at[0,"STATION_NUMBER"])
print("NUMBER OF OBSERVATIONS:", len(data))

# Create column
col_name = 'TEMP_C'
data[col_name] = None

# Convert tempetarues from Fahrenheits to Celsius
data['TEMP_C'] = data['TEMP_F'].apply(fahr_to_celsius)

# Convert TIME to string 
data['TIME_STR'] = data['TIME'].astype(str)

# Parse year and month
data['MONTH'] = data['TIME_STR'].str.slice(start=5, stop=6).astype(int)
data['YEAR'] = data['TIME_STR'].str.slice(start=0, stop=4).astype(int)

# Extract observations for the months of April 
aprils = data[data['MONTH']==4]

# Take a subset of columns
aprils = aprils[['STATION_NUMBER','TEMP_F', 'TEMP_C', 'YEAR', 'MONTH']]

# Group by year and month
grouped = aprils.groupby(by=['YEAR', 'MONTH'])

# Get mean values for each group
monthly_mean = grouped.mean()

# Print info
print(monthly_mean.sort_values(by='TEMP_C', ascending=False).head(5))
print("\n")
```

We will use the `glob()` function from the module `glob` to list our input files. 

```python
import glob
```

```python
file_list = glob.glob(r'data/0*txt')
```

```{note}
Note that we're using the \* character as a wildcard, so any file that starts with `data/0` and ends with `txt` will be added to the list of files we will iterate over. We specifically use `data/0` as the starting part of the file names to avoid having our metadata files included in the list!
```

```python
print("Number of files in the list", len(file_list))
print(file_list)
```

Now, you should have all the relevant file names in a list, and we can loop over the list using a for-loop:

```python
for fp in file_list:
    print(fp)
```

```python jupyter={"outputs_hidden": false}
# Repeat the analysis steps for each input file:
for fp in file_list:

    # Read selected columns of  data using varying amount of spaces as separator and specifying * characters as NoData values
    data = pd.read_csv(fp, delim_whitespace=True, usecols=['USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN'], na_values=['*', '**', '***', '****', '*****', '******'])

    # Rename the columns
    new_names = {'USAF':'STATION_NUMBER','YR--MODAHRMN': 'TIME', 'SPD': 'SPEED', 'GUS': 'GUST', 'TEMP':'TEMP_F'}
    data = data.rename(columns=new_names)

    #Print info about the current input file:
    print("STATION NUMBER:", data.at[0,"STATION_NUMBER"])
    print("NUMBER OF OBSERVATIONS:", len(data))

    # Create column
    col_name = 'TEMP_C'
    data[col_name] = None

    # Convert tempetarues from Fahrenheits to Celsius
    data['TEMP_C'] = data['TEMP_F'].apply(fahr_to_celsius)

    # Convert TIME to string 
    data['TIME_STR'] = data['TIME'].astype(str)

    # Parse year and month
    data['MONTH'] = data['TIME_STR'].str.slice(start=5, stop=6).astype(int)
    data['YEAR'] = data['TIME_STR'].str.slice(start=0, stop=4).astype(int)

    # Extract observations for the months of April 
    aprils = data[data['MONTH']==4]

    # Take a subset of columns
    aprils = aprils[['STATION_NUMBER','TEMP_F', 'TEMP_C', 'YEAR', 'MONTH']]

    # Group by year and month
    grouped = aprils.groupby(by=['YEAR', 'MONTH'])

    # Get mean values for each group
    monthly_mean = grouped.mean()

    # Print info
    print(monthly_mean.sort_values(by='TEMP_C', ascending=False).head(5))
    print("\n")
```

How about now, how did April 2019 rank across different stations?


## Footnotes

[^noaanews]: <https://www.noaa.gov/news/january-2020-was-earth-s-hottest-january-on-record>
