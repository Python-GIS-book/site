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

# Creating a repeatable analysis workflow

In this section, we will create a data analysis workflow that we can repeat with multiple input files with a similar structure. 

![Finland April 2019](./../img/Finland-April-2019.png)
*Source: [https://weather.com/news/climate/news/2019-05-20-april-2019-global-temperatures-nasa-noaa](https://weather.com/news/climate/news/2019-05-20-april-2019-global-temperatures-nasa-noaa)*

April 2019 was the [second warmest April on record globally](https://weather.com/news/climate/news/2019-05-20-april-2019-global-temperatures-nasa-noaa), and the warmest on record at 13 weather stations in Finland. 
In this lesson, we will use our data manipulation and analysis skills to analyze weather data from Finland, and investigate the claim that April 2019 was the warmest on record across Finland.

Along the way we will cover a number of useful techniques in pandas including:

- renaming columns
- iterating data frame rows and applying functions
- data aggregation
- repeating the analysis task for several input files


## Preparations

### Input data

In this section we are using weather observation data from Finland [downloaded from NOAA](https://www7.ncdc.noaa.gov/CDO/cdopoemain.cmd?datasetabbv=DS3505&countryabbv=&georegionabbv=&resolution=40).

### Downloading the data

INSERT DATA DOWNLOAD INSTRUCTIONS IF NEEDED (OR PROVIDE SMALL ENOUGH FILE THAT CAN BE HOSTED WITH THE BOOK)



As part of the download there are a number of files that describe the weather data. These *metadata* files include:

- A list of stations\*: [data/6367598020644stn.txt](metadata/6367598020644stn.txt)
- Details about weather observations at each station: [data/6367598020644inv.txt](metadata/6367598020644inv.txt)
- A data description (i.e., column names): [data/3505doc.txt](metadata/3505doc.txt)

\*Note that the list of stations is for all 15 stations, even if you're working with only the 4 stations on the CSC Notebooks platform.

The input data for this week are separated with varying number of spaces (i.e., fixed width). The first lines and columns of the data look like following:

``` 
  USAF  WBAN YR--MODAHRMN DIR SPD GUS CLG SKC L M H  VSB MW MW MW MW AW AW AW AW W TEMP DEWP    SLP   ALT    STP MAX MIN PCP01 PCP06 PCP24 PCPXX SD
029440 99999 190601010600 090   7 *** *** OVC * * *  0.0 ** ** ** ** ** ** ** ** *   27 **** 1011.0 ***** ****** *** *** ***** ***** ***** ***** ** 
029440 99999 190601011300 ***   0 *** *** OVC * * *  0.0 ** ** ** ** ** ** ** ** *   27 **** 1015.5 ***** ****** *** *** ***** ***** ***** ***** ** 
029440 99999 190601012000 ***   0 *** *** OVC * * *  0.0 ** ** ** ** ** ** ** ** *   25 **** 1016.2 ***** ****** *** *** ***** ***** ***** ***** ** 
029440 99999 190601020600 ***   0 *** *** CLR * * *  0.0 ** ** ** ** ** ** ** ** *   26 **** 1016.2 ***** ****** *** *** ***** ***** ***** ***** **
```

We will develop our analysis workflow using data for a single station. Then, we will repeat the same process for all the stations.


### Reading the data

In order to get started, let's import pandas: 

```python
import pandas as pd
```

At this point, you can already have a quick look at the input file `029440.txt` for Tampere Pirkkala and how it is structured. We can notice at least two things we need to consider when reading in the data:

```{admonition} Input data structure
- **Delimiter:** The data are **separated with a varying amount of spaces**. If you check out the documentation for the [read_csv() method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html), you can see that there are two different ways of doing this. We can use either `sep='\s+'` or `delim_whitespace=True` (but not both at the same time). In this case, we prefer to use `delim_whitespace` parameter.

- **No Data values:** No data values in the NOAA data are coded with varying number of `*`. We can tell pandas to consider those characters as NaNs by specifying `na_values=['*', '**', '***', '****', '*****', '******']`.
```

```python
# Define relative path to the file
fp = r'./../../data/NOAA/hourly/statistics/029440.txt'

# Read data using varying amount of spaces as separator and specifying * characters as NoData values
data = pd.read_csv(fp, delim_whitespace=True, na_values=['*', '**', '***', '****', '*****', '******'])
```

Let's see how the data looks by printing the first five rows with the `head()` function:

```python jupyter={"outputs_hidden": false}
data.head()
```

All seems ok. However, we won't be needing all of the 33 columns for detecting warm temperatures in April. We can check all column names by running `data.columns`:

```python jupyter={"outputs_hidden": false}
data.columns
```

A description for all these columns is available in the metadata file [data/3505doc.txt](metadata/3505doc.txt). 

**Let's read in the data one more time.** This time, we will read in only some of the columns using the `usecols` parameter. Let's read in columns that might be somehow useful to our analysis, or at least that contain some values that are meaningful to us, including the station name, timestamp, and data about wind and temperature: `'USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN'`

```python
# Read in only selected columns
data = pd.read_csv(fp, delim_whitespace=True, 
                   usecols=['USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN'], 
                   na_values=['*', '**', '***', '****', '*****', '******'])

# Check the dataframe
data.head()
```

Okay so we can see that the data was successfully read to the DataFrame and we also seemed to be able to convert the asterisk (\*) characters into `NaN` values. 


### Renaming columns

As we saw above some of the column names are a bit awkward and difficult to interpret. Luckily, it is easy to alter labels in a pandas DataFrame using the [rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html)-function. In order to change the column names, we need to tell pandas how we want to rename the columns using a dictionary that lists old and new column names

Let's first check again the current column names in our DataFrame:

```python
data.columns
```

```{admonition} Dictionaries
A [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) is a specific data structure in Python for storing key-value pairs. During this course, we will use dictionaries mainly when renaming columns in a pandas series, but dictionaries are useful for many different purposes! For more information about Python dictionaries, check out [this tutorial](https://realpython.com/python-dicts/).
```


We can define the new column names using a [dictionary](https://www.tutorialspoint.com/python/python_dictionary.htm) where we list "`key: value`" pairs, in which the original column name (the one which will be replaced) is the key and the new column name is the value.

- Let's change the following:
   
   - `YR--MODAHRMN` to `TIME`
   - `SPD` to `SPEED`
   - `GUS` to `GUST`

```python jupyter={"outputs_hidden": false}
# Create the dictionary with old and new names
new_names = {'YR--MODAHRMN': 'TIME', 'SPD': 'SPEED', 'GUS': 'GUST'}

# Let's see what the variable new_names look like
new_names
```

```python
# Check the data type of the new_names variable
type(new_names)
```

From above we can see that we have successfully created a new dictionary. 

Now we can change the column names by passing that dictionary using the parameter `columns` in the `rename()` function:

```python jupyter={"outputs_hidden": false}
# Rename the columns
data = data.rename(columns=new_names)

# Print the new columns
print(data.columns)
```

Perfect, now our column names are easier to understand and use. 


### Check your understanding

The temperature values in our data files are again in Fahrenheit. As you might guess, we will soon convert these temperatures in to Celsius. In order to avoid confusion with the columns, let's rename the column `TEMP` to `TEMP_F`. Let's also rename `USAF` to `STATION_NUMBER`.

```python
# Create the dictionary with old and new names
new_names = {'USAF':'STATION_NUMBER', 'TEMP': 'TEMP_F'}

# Rename the columns
data = data.rename(columns=new_names)

# Check the output
data.head()
```

### Data properties

As we learned last week, it's always a good idea to check basic properties of the input data before proceeding with data analysis. Let's check the:

- Number of rows and columns:

```python
data.shape
```

- Top and bottom rows: 

```python
data.head()
```

```python
data.tail()
```

- Data types of the columns: 

```python
data.dtypes
```

- Descriptive statistics:

```python jupyter={"outputs_hidden": false}
data.describe()
```

Here we can see that there are varying number of observations per column (see the `count` information), because some of the columns have missing values.


## Applying a function

Now it's again time to convert temperatures from Fahrenheit to Celsius! Yes, we have already done this many times before, but this time we will learn how to apply our own functions to data in a pandas DataFrame.

**We will define a function for the temperature conversion, and apply this function for each Celsius value on each row of the DataFrame. Output celsius values should be stored in a new column called** `TEMP_C`.

We will first see how we can apply the function row-by-row using a `for` loop and then we will learn how to apply the method to all rows more efficiently all at once.

### Defining the function

For both of these approaches, we first need to define our temperature conversion function from Fahrenheit to Celsius:

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

Let's test the function with some known value:

```python
fahr_to_celsius(32)
```

Let's also print out the first rows of our data frame to see our input data before further processing: 

```python
data.head()
```

### Iterating over rows

We can apply the function one row at a time using a `for` loop and the [iterrows()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html) method. In other words, we can use the `iterrows()` method and a `for` loop to repeat a process *for each row in a Pandas DataFrame* . Please note that iterating over rows is a rather inefficient approach, but it is still useful to understand the logic behind the iteration.

When using the `iterrows()` method it is important to understand that `iterrows()` accesses not only the values of one row, but also the `index` of the row as well. 

Let's start with a simple for loop that goes through each row in our DataFrame:

```python jupyter={"outputs_hidden": false}
# Iterate over the rows
for idx, row in data.iterrows():
    
    # Print the index value
    print('Index:', idx)
    
    # Print the row
    print('Temp F:', row['TEMP_F'], "\n")
    
    break
```

```{admonition} Breaking a loop
When developing a for loop, you don't always need to go through the entire loop if you just want to test things out. 
The [break](https://www.tutorialspoint.com/python/python_break_statement.htm) statement in Python terminates the current loop whereever it is placed and we used it here just to test check out the values on the first row.
With a large data, you might not want to print out thousands of values to the screen!
```


We can see that the `idx` variable indeed contains the index value at position 0 (the first row) and the `row` variable contains all the data from that given row stored as a pandas `Series`.

- Let's now create an empty column `TEMP_C` for the Celsius temperatures and update the values in that column using the `fahr_to_celsius` function we defined earlier:

```python
# Create an empty float column for the output values
data['TEMP_C'] = 0.0

# Iterate over the rows 
for idx, row in data.iterrows():
    
    # Convert the Fahrenheit to Celsius
    celsius = fahr_to_celsius(row['TEMP_F'])
    
    # Update the value of 'Celsius' column with the converted value
    data.at[idx, 'TEMP_C'] = celsius
```

```{admonition} Reminder: .at or .loc?
Here, you could also use `data.loc[idx, new_column] = celsius` to achieve the same result. 
    
If you only need to access a single value in a DataFrame, [DataFrame.at](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html) is faster compared to [DataFrame.loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html), which is designed for accessing groups of rows and columns. 
```


Finally, let's see how our dataframe looks like now:

```python
data.head()
```

### Applying the function

Pandas DataFrames and Series have a dedicated method `.apply()` for applying functions on columns (or rows!). When using `.apply()`, we pass the function name (without parenthesis!) as an argument to the `apply()` method. Let's start by applying the function to the `TEMP_F` column that contains the temperature values in Fahrenheit:

```python
data['TEMP_F'].apply(fahr_to_celsius)
```

The results look logical and we can store them permanently into a new column (overwriting the old values): 

```python
data['TEMP_C'] = data['TEMP_F'].apply(fahr_to_celsius)
```

We can also apply the function on several columns at once. We can re-order the dataframe at the same time in order to see something else than `NaN` from the `MIN` and `MAX` columns

```python
data[['TEMP_F', 'MIN', 'MAX']].apply(fahr_to_celsius)
```

#### Check your understanding

Convert `'TEMP_F'`, `'MIN'`, `'MAX'` to Celsius by applying the function like we did above and store the outputs to  new columns `'TEMP_C'`, `'MIN_C'`, `'MAX_C'`.

```python
data[['TEMP_C', 'MIN_C', 'MAX_C']]  = data[['TEMP_F', 'MIN', 'MAX']].apply(fahr_to_celsius)
```

Applying the function on all columns `data.apply(fahr_to_celsius)` would not give an error in our case, but the results also don't make much sense for columns where input data was other than Fahrenheit temperatures.


You might also notice that our conversion function would also allow us to 
pass one column or the entire dataframe as a parameter. For example, like this: `fahr_to_celsius(data["TEMP_F"])`. However, the code is perhaps easier to follow when using the apply method.


Let's check the output:

```python jupyter={"outputs_hidden": false}
data.head(10)
```

```{admonition} Should I use .iterrows() or .apply()?
We are teaching the `.iterrows()` method because it helps to understand the structure of a DataFrame and the process of looping through DataFrame rows. However, using `.apply()` is often more efficient in terms of execution time. 

At this point, the most important thing is that you understand what happens when you are modifying the values in a pandas DataFrame. When doing the course exercises, either of these approaches is ok!
```


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
