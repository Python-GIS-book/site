---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Data wrangling, grouping and aggregation

Next, we will continue working with weather data, but expand our analysis to cover longer periods of data from Finland. In the following, you will learn various useful techniques in pandas to manipulate, group and aggregate the data in different ways that are useful when extracting insights from your data. In the end, you will learn how to create an automated data analysis workflow that can be repeated with multiple input files having a similar structure. As a case study, we will investigate whether January 2020 was the warmest month on record also in Finland, as the month was the warmest one on record globally [^noaanews]. 


## Cleaning data while reading

In this section we are using weather observation data from Finland that was downloaded from NOAA (see `Datasets` chapter for further details). The input data is separated with varying number of spaces (i.e., fixed width). The first lines and columns of the data look like following:

``` 
  USAF  WBAN YR--MODAHRMN DIR SPD GUS CLG SKC L M H  VSB MW MW MW MW AW  ...
029440 99999 190601010600 090   7 *** *** OVC * * *  0.0 ** ** ** ** **  ...
029440 99999 190601011300 ***   0 *** *** OVC * * *  0.0 ** ** ** ** **  ...
029440 99999 190601012000 ***   0 *** *** OVC * * *  0.0 ** ** ** ** **  ...
029440 99999 190601020600 ***   0 *** *** CLR * * *  0.0 ** ** ** ** **  ...
```

By looking at the data, we can notice a few things that we need to consider when reading the data:

1. **Delimiter:** The columns are separated with a varying amount of spaces which requires using some special tricks when reading the data with pandas `read_csv()` function
2. **NoData values:** NaN values in the NOAA data are coded with varying number of `*` characters, hence, we need to be able to instruct pandas to interpret those as NaNs. 
3. **Many columns**: The input data contains many columns (altogether 33). Many of those do not contain any meaningful data for our needs. Hence, we should probably ignore the unnecessary columns already at this stage. 

Handling and cleaning heterogeneous input data (such as our example here) can be done after reading in the data. However, in many cases, it is actually useful to do some cleaning and preprocessing already when reading the data. In fact, that is often much easier to do. In our case, we can read the data with varying number of spaces between the columns (1) by using a parameter `delim_whitespace=True` (alternatively, specifying `sep='\s+'` would work). For handling the NoData values (2), we can tell pandas to consider the `*` characters as NaNs by using a paramater `na_values` and specifying a list of characters that should be converted to NaNs. Hence, in this case we can specify `na_values=['*', '**', '***', '****', '*****', '******']` which will then convert the varying number of `*` characters into NaN values. Finally, we can limit the number of columns that we read (3) by using the `usecols` parameter, which we already used previously. In our case, we are interested in columns that might be somehow useful to our analysis (or at least meaningful to us), including e.g. the station name, timestamp, and data about the wind and temperature: `'USAF','YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN'`. Achieving all these things is pretty straightforward using the `read_csv()` function: 

```python
import pandas as pd

# Define relative path to the file
fp = "data/029820.txt"

# Read data using varying amount of spaces as separator,
# specifying '*' characters as NoData values,
# and selecting only specific columns from the data
data = pd.read_csv(
    fp,
    delim_whitespace=True,
    na_values=["*", "**", "***", "****", "*****", "******"],
    usecols=["USAF", "YR--MODAHRMN", "DIR", "SPD", "GUS", "TEMP", "MAX", "MIN"],
)
```

Let's see now how the data looks by printing the first five rows with the `head()` function:

```python jupyter={"outputs_hidden": false}
data.head()
```

Perfect, looks good. We have skipped a bunch of unnecessary columns and also the asterisk (\*) characters have been correctly converted to NaN values.  


## Renaming columns

Let's take a closer look at the column names of our DataFrame: 

```python jupyter={"outputs_hidden": false}
data.columns
```

As we see, some of the column names are a bit awkward and difficult to interpret (a description for the columns is available in the metadata [data/3505doc.txt](data/3505doc.txt)). Luckily, it is easy to alter labels in a pandas DataFrame using the `rename()` function. In order to change the column names, we need to tell pandas how we want to rename the columns using a dictionary that converts the old names to new ones. As you probably remember from Chapter 1, a `dictionary` is a specific data structure in Python for storing key-value pairs. We can define the new column names using a dictionary where we list "`key: value`" pairs in following manner:
   
- `USAF`: `STATION_NUMBER`
- `YR--MODAHRMN`: `TIME`
- `SPD`: `SPEED`
- `GUS`: `GUST`
- `TEMP`: `TEMP_F`

Hence, the original column name (e.g. `YR--MODAHRMN`) is the dictionary `key` which will be converted to a new column name `TIME` (which is the `value`). The temperature values in our data file is again represented in Fahrenheit. We will soon convert these temperatures to Celsius. Hence, in order to avoid confusion with the columns, let's rename the column `TEMP` to `TEMP_F`. Also the station number `USAF` is much more intuitive if we call it `STATION_NUMBER`. Let's create a dictionary for the new column names:

```python jupyter={"outputs_hidden": false}
new_names = {
    "USAF": "STATION_NUMBER",
    "YR--MODAHRMN": "TIME",
    "SPD": "SPEED",
    "GUS": "GUST",
    "TEMP": "TEMP_F",
}
new_names
```

Our dictionary looks correct, so now we can change the column names by passing that dictionary using the parameter `columns` in the `rename()` function:

```python jupyter={"outputs_hidden": false}
data = data.rename(columns=new_names)
data.columns
```

Perfect, now our column names are easier to understand and use. 


## Using functions with pandas

Now it's time to convert those temperatures from Fahrenheit to Celsius. We have done this many times before, but this time we will learn how to apply our own functions to data in a pandas DataFrame. We will define a function for the temperature conversion, and apply this function for each Celsius value on each row of the DataFrame. Output celsius values should be stored in a new column called `TEMP_C`. But first, it is a good idea to check some basic properties of our new input data before proceeding with data analysis:

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

Nothing suspicous for the first and last rows, but here with `info()` we can see that the number of observations per column seem to be varying if you compare the `Non-Null Count` information to the number of entries in the data (N=198334). Only station number and time seem to have data on each row. All other columns seem to have some missing values. This is not necessarily anything dangerous, but good to keep in mind. Let's still look at the descriptive statistics:

```python
# Descriptive stats
data.describe()
```

By looking at the `TEMP_F` values (Fahrenheit temperatures), we can confirm that our measurements seems more or less valid because the value range of the temperatures makes sense, i.e. there are no outliers such as extremely high `MAX` values or low `MIN` values. It is always a good practice to critically check your data before doing any analysis, as it is possible that your data may include incorrect values, e.g. due to a sensor malfunction or human error. 


### Defining a function

Now we are sure that our data looks okay, and we can start our temperature conversion process by first defining our temperature conversion function from Fahrenheit to Celsius. Pandas can use regular functions, hence you can define functions for pandas exactly in the same way as you would do normally (as we learned in Chapter 1). Hence, let's define a function that converts Fahrenheits to Celsius: 

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

Now we have the function defined and stored in memory. At this point it is good to test the function with some known value:

```python
fahr_to_celsius(32)
```

32 Fahrenheits is indeed 0 Celsius, so our function seem to be working correctly.


### Using a function by iterating over rows

Next we will learn how to use our function with data stored in pandas DataFrame. We will first apply the function row-by-row using a `for` loop and then we will learn a more efficient way of applying the function to all rows at once.

Looping over rows in a DataFrame can be done in a couple of different ways. A common approach is to use a `iterrows()` method which loops over the rows as a index-Series pairs. In other words, we can use the `iterrows()` method together with a `for` loop to repeat a process *for each row in a Pandas DataFrame*. Please note that iterating over rows this way is a rather inefficient approach, but it is still useful to understand the logic behind the iteration (we will learn a more efficient approach later). When using the `iterrows()` method it is important to understand that `iterrows()` accesses not only the values of one row, but also the `index` of the row as we mentioned. Let's start with a simple for loop that goes through each row in our DataFrame:

```python jupyter={"outputs_hidden": false}
# Iterate over the rows
for idx, row in data.iterrows():

    # Print the index value
    print("Index:", idx)

    # Print the temperature from the row
    print("Temp F:", row["TEMP_F"], "\n")

    break
```

We can see that the `idx` variable indeed contains the index value at position 0 (the first row) and the `row` variable contains all the data from that given row stored as a pandas `Series`. Notice, that when developing a for loop, you don't always need to go through the entire loop if you just want to test things out. Using the `break` statement in Python terminates a loop whenever it is placed inside a loop. We used it here just to test check out the values on the first row. With a large data, you might not want to print out thousands of values to the screen!

Let's now create an empty column `TEMP_C` for the Celsius temperatures and update the values in that column using the `fahr_to_celsius()` function that we defined earlier. For updating the value, we can use `at` which we already used earlier in this chapter. This time, we will use the `itertuples()` method which works in a similar manner, except it only return the row values without the `index`. When using `itertuples()` accessing the row values needs to be done a bit differently, because the row is not a Series, but a `named tuple` (hence the name). A tuple is like a list (but immutable, i.e. you cannot change it) and "named tuple" is a special kind of tuple object that adds the ability to access the values by name instead of position index. Hence, we will access the `TEMP_F` value by using `row.TEMP_F` (compare to how we accessed the value in the prevous code block):

```python
# Create an empty column for the output values
data["TEMP_C"] = 0.0

# Iterate over the rows
for row in data.itertuples():

    # Convert the Fahrenheit to Celsius
    # Notice how we access the row value
    celsius = fahr_to_celsius(row.TEMP_F)

    # Update the value for 'Celsius' column with the converted value
    # Notice how we can access the Index value
    data.at[row.Index, "TEMP_C"] = celsius
```

```python
# Check the result
data.head()
```

```python
# How does our row look like?
row
```

Okay, now we have iterated over our data and updated the temperatures in Celsius to `TEMP_C` column by using our `fahr_to_celsius()` function. The values look correct as 32 Fahrenheits indeed is 0 Celsius degrees, as can be seen on the second row. We also have here the last row of our DataFrame which is a named tuple. As you can see, it is a bit like a weird looking dictionary with values assigned to the names of our columns. Basically, it is an object with attributes that we can access in a similar manner as we have used to access some of the pandas DataFrame attributes, such as `data.shape`. 

A couple of notes about our appoaches. We used `itertuples()` method for looping over the values because it is significantly faster compared to `iterrows()` (can be ~100x faster). We used `.at` to assign the value to the DataFrame because it is designed to access single values more efficiently compared to `.loc`, which can access also groups of rows and columns. That said, you could have used `data.loc[idx, new_column] = celsius` to achieve the same result (it is just slower). 


### Using a function with apply

Although using for loop with `itertuples()` can be fairly efficient, pandas DataFrames and Series have a dedicated method called `apply()` for applying functions on columns (or rows). `apply()` is typically faster than `itertuples()`, especially if you have large number of rows, such as in our case. When using `apply()`, we pass the function that we want to use as an argument. Let's start by applying the function to the `TEMP_F` column that contains the temperature values in Fahrenheit:

```python
data["TEMP_F"].apply(fahr_to_celsius)
```

The results look logical. Notice how we passed the `fahr_to_celsius()` function without using the parentheses `()` after the name of the function. When using `apply`, you should always leave out the parentheses from the function that you use. Meaning that you should use `apply(fahr_to_celsius)` instead of `apply(fahr_to_celsius())`. Why? Because the `apply()` method will execute and use the function itself in the background when it operates with the data. If we would pass our function with the parentheses, the `fahr_to_celsius()` function would actually be executed once before the loop with `apply()` starts (hence becoming unusable), and that is not what we want. Our previous command only returned the Series of temperatures to the screen, but naturally we can also store them permanently into a new column (overwriting the old values):

```python
data["TEMP_C"] = data["TEMP_F"].apply(fahr_to_celsius)
```

A nice thing with `apply()` is that we can also apply the function on several columns at once. Below, we also sort the values in descending order based on values in `MIN` column to see that applying our function really works:

```python
cols = ["TEMP_F", "MIN", "MAX"]
result = data[cols].apply(fahr_to_celsius)
result.sort_values(by="MIN", ascending=False).head()
```

You can also directly store the outputs to new columns `'TEMP_C'`, `'MIN_C'`, `'MAX_C'`:

```python
cols = ["TEMP_F", "MIN", "MAX"]
data[cols] = data[cols].apply(fahr_to_celsius)
data.head()
```

In this section, we showed you a few different ways to iterate over rows in pandas and apply functions. The most important thing is that you understand the logic of how loops work and how you can use your own functions to modify the values in a pandas DataFrame. Whenever you need to loop over your data, we recommend using `.apply()` as it is typically the most efficient one in terms of execution time. However, remember that in most cases you do not actually need to use loops, but you can do calculations in a "vectorized manner" (which is the fastest way) as we learned previously when doing basic calculations in pandas. 


## String slicing

We will eventually want to group our data based on month in order to see if the January temperatures in 2020 were higher than on average (which is the goal in our analysis as you might recall). Currently, the date and time information is stored in the column `TIME` that has a structure `yyyyMMddhhmm`. This is a typical timestamp format in which `yyyy` equals to year in four digit format, `MM` to month (two digits), `dd` days, `hh` hours and `mm` minutes. Let's have a closer look at the date and time information we have by checking the values in that column, and their data type:

```python
data["TIME"].head()
```

```python
data["TIME"].tail()
```

The `TIME` column contains several observations per day (and even several observations per hour). The timestamp for the first observation is `190601010600`, i.e. from 1st of January 1906 (way back!), and the timestamp for the latest observation is `201910012350`. As we can see, the data type (`dtype`) of our column seems to be `int64`, i.e. the information is stored as integer values. 


We want to aggregate this data on a monthly level. In order to do so, we need to "label" each row of data based on the month when the record was observed. Hence, we need to somehow separate information about the year and month for each row. In practice, we can create a new column (or an index) containing information about the month (including the year, but excluding days, hours and minutes). There are different ways of achieving this, but here we will take advantage of `string slicing` which means that we convert the date and time information into character strings and "cut" the needed information from the string objects. The other option would be to convert the timestamp values into something called `datetime` objects, but we will learn about those a bit later. Before further processing, we first want to convert the `TIME` column as character strings for convenience, stored into a new column `TIME_STR`:

```python jupyter={"outputs_hidden": false}
data["TIME_STR"] = data["TIME"].astype(str)
```

If we look at the latest time stamp in the data (`201910012350`), you can see that there is a systematic pattern `YEAR-MONTH-DAY-HOUR-MINUTE`. Four first characters represent the year, and the following two characters represent month. Because we are interested in understanding monthly averages for different years, we want to slice the year and month values from the timestamp (the first 6 characters), like this:

```python
date = "201910012350"
date[0:6]
```

Based on this information, we can slice the correct range of characters from the `TIME_STR` column using a specific pandas function designed for Series, called `.str.slice()`. As parameters, the function has `start` and `stop` which you can use to specify the positions where the slicing should start and end:

```python
data["YEAR_MONTH"] = data["TIME_STR"].str.slice(start=0, stop=6)
data.head()
```

Nice! Now we have "labeled" the rows based on information about day of the year and hour of the day.



#### Question 3.5

Create a new column `'MONTH'` with information about the month without the year.

```python
# Use this cell to enter your solution.
```

```python tags=["hide-cell"]
# Solution

data["MONTH"] = data["TIME_STR"].str.slice(start=4, stop=6)
```

## Grouping and aggregating data


### Basic logic of grouping a DataFrame using `.groupby()`

In the following sections, we want to calculate the average temperature for each month in our dataset. Here, we will learn how to use a `.groupby()` method which is a handy tool for compressing large amounts of data and computing statistics for subgroups. We will use the groupby method to calculate the average temperatures for each month trough these three main steps:

  1. group the data based on year and month using `groupby()`
  2. calculate the average temperature for each month (i.e. each group) 
  3. store the resulting rows into a DataFrame called `monthly_data`
  
We have quite a few rows of weather data (N=198334), and several observations per day. Our goal is to create an aggreated DataFrame that would have only one row per month. The `.groupby()` takes as a parameter the name of the column (or a list of columns) that you want to use as basis for doing the grouping.  Let's start by grouping our data based on unique year and month combination:

```python
grouped = data.groupby("YEAR_MONTH")
```

Notice, thas it would also be possible to create combinations of years and months "on-the-fly" if you have them in separate columns. In such case, grouping the data could be done as `grouped = data.groupby(['YEAR', 'MONTH'])`. Let's explore the new variable `grouped`:

```python
print(type(grouped))
print(len(grouped))
```

We have a new object with type `DataFrameGroupBy` with 826 groups. In order to understand what just happened, let's also check the number of unique year and month combinations in our data:

```python
data["YEAR_MONTH"].nunique()
```

Length of the grouped object should be the same as the number of unique values in the column we used for grouping (`YEAR_MONTH`). For each unique value, there is a group of data. Let's explore our grouped data further by check the "names" of the groups (five first ones). Here, we access the `keys` of the groups and convert them to a `list` so that we can slice and print only a few of those to the sceen:

```python
list(grouped.groups.keys())[:5]
```

Let's check the contents for a group representing January 1906. We can get the values for that month from the grouped object using the `get_group()` method:

```python jupyter={"outputs_hidden": false}
# Specify a month (as character string)
month = "190601"

# Select the group
group1 = grouped.get_group(month)
group1
```

As we can see, a single group contains a DataFrame with values only for that specific month. Let's check the DataType of this group:

```python
type(group1)
```

So, one group is a pandas DataFrame which is really useful, because it allows us to use all the familiar DataFrame methods for calculating statistics etc. for this specific group which we will see shortly. It is also possible to iterate over the groups in our `DataFrameGroupBy` object which can be useful if you need to conduct and apply some more complicated subtasks for each group. When doing so, it is important to understand that a single group in our `DataFrameGroupBy` actually contains not only the actual values, but also information about the `key` that was used to do the grouping. Hence, when iterating we need to assign the `key` and the values (i.e. the group) into separate variables. Let's see how we can iterate over the groups and print the key and the data from a single group (again using `break` to only see what is happening):

```python jupyter={"outputs_hidden": false}
# Iterate over groups
for key, group in grouped:
    # Print key and group
    print("Key:\n", key)
    print("\nFirst rows of data in this group:\n", group.head())

    # Stop iteration with break command
    break
```

Here, we can see that the `key` contains the name of the group (i.e. the unique value from `YEAR_MONTH`). 


### Aggregating data with `groupby()`

We can, for example, calculate the average values for all variables using the statistical functions that we have seen already (e.g. mean, std, min, max, median). To calculate the average temperature for each month, we can use the `mean()` function. Let's calculate the mean for all the weather related data attributes in our group at once:

```python jupyter={"outputs_hidden": false}
# Specify the columns that will be part of the calculation
mean_cols = ["DIR", "SPEED", "GUST", "TEMP_F", "TEMP_C"]

# Calculate the mean values all at one go
mean_values = group1[mean_cols].mean()
mean_values
```

As a result, we get a pandas Series with mean values calculated for all columns in the group. Notice that if you want to convert this Series back into a DataFrame (which can be useful if you e.g. want to merge multiple groups), you can use command `.to_frame().T` which first converts the Series into a DataFrame and then transposes the order of the axes (the label names becomes the column names):

```python
# Convert to DataFrame
mean_values.to_frame().T
```

To do a similar aggregation with all the groups in our data, we can actually combine the `groupby()` function with the aggregation step (such as taking the mean, median etc. of given columns), and finally restructure the resulting DataFrame a bit. This can be at first a bit harder to understand, but this is how you would do the grouping and aggregating the values as follows:

```python
# The columns that we want to aggregate
mean_cols = ["DIR", "SPEED", "GUST", "TEMP_F", "TEMP_C"]

# Group and aggregate the data with one line
monthly_data = data.groupby("YEAR_MONTH")[mean_cols].mean().reset_index()
monthly_data
```

As we can see, aggregating the data in this way is fairly straightforward and fast process requiring merely a single command. So what did we actually do here? We i) grouped the data, ii) selected specific columns from the result (`mean_cols`), iii) calculated the mean for all of the selected columns of the groups, and finally 4) reset the index. Resetting the index at the end is not necessary, but by doing it, we turn the `YEAR_MONTH` values into a dedicated column in our data (which would be otherwise store as `index`) .

What might not be obvious from this example is the fact that hidden in the background, each group is actually iterated over and the aggregation step is repeated for each group. For you to better understand what happens, we will next repeat the same process by iterating over groups and eventually creating a DataFrame that will contain the mean values for all those weather attributes that we were interested in. In this approach, we will first iterate over the groups, then calculate the mean values,  store the result into a list, and finally merge the aggregated data into a DataFrame called `monthly_data`.

```python
# Create an empty list for storing the aggregated rows/DataFrames
data_container = []

# The columns that we want to aggregate
mean_cols = ["DIR", "SPEED", "GUST", "TEMP_F", "TEMP_C"]

# Iterate over the groups
for key, group in grouped:

    # Calculate mean
    mean_values = group[mean_cols].mean()

    # Add the ´key´ (i.e. the date+time information) into the Series
    mean_values["YEAR_MONTH"] = key

    # Convert the pd.Series into DataFrame and
    # append the aggregated values into a list as a DataFrame
    data_container.append(mean_values.to_frame().T)

# After iterating all groups, merge the list of DataFrames
monthly_data = pd.concat(data_container)
monthly_data
```

As a result, we get identical results as with the earlier approach that was done with a single line of code (except for the position of the `YEAR_MONTH` column).

So which approach should you use? From the performance point of view, we recommend using the first approach (i.e. chaining) which does not require you to create a separate for loop, and is highly performant. However, this approach might be a bit more difficult to read and comprehend (the loop might be easier). Also sometimes you want to include additional processing steps inside the loop which can be hard accomplish by chaining everything into a single command. Hence, it is useful to know both of these approaches for doing aggregations with the data.  


## Case study: Detecting warm months

Now, we have aggregated our data on monthly level and all we need to do is to check which years had the warmest January temperatures. A simple approach is to select all January values from the data and check which group(s) have the highest mean value. Before doing this, let's separate the month information from our timestamp following the same approach as previously we did when slicing the year-month combination:

```python
monthly_data["MONTH"] = monthly_data["YEAR_MONTH"].str.slice(start=4, stop=6)
monthly_data.head()
```

Now we can select the values for January from our data and store it into a new variable `january_data`. We will also check the highest temperature values by sorting the DataFrame in a descending order:

```python
january_data = monthly_data.loc[monthly_data["MONTH"] == "01"]
january_data.sort_values(by="TEMP_C", ascending=False).head()
```

By looking at the order of `YEAR_MONTH` column, we can see that January 2020 indeed was on average the warmest month on record based on weather observations from Finland.


## Automating the analysis

Now we have learned how to aggregate data using pandas. average temperatures for each month based on hourly weather observations. One of the most useful aspects of programming, is the ability to automate processes and repeat analyses such as these for any number of weather stations (assuming the data structure is the same). 

Hence, let's now see how we can repeat the previous data analysis steps for 15 weather stations located in different parts of Finland containing data for five years (2015-2019). The idea is that we will repeat the process for each input file using a (rather long) for loop. We will use the most efficient alternatives of the previously represented approaches, and finally will store the results in a single DataFrame for all stations. We will learn how to manipulate filepaths in Python using the `pathlib` module and see how we can list our input files in the data directory `data/finnish_stations`. We will store those paths to a variable `file_list`, so that we can use the file paths easily in the later steps.


### Managing and listing filesystem paths

In Python there are two commonly used approaches to manage and manipulate filepaths, namely `os.path` sub-module and a newer `pathlib` module (available since Python 3.4) which we will demonstrate here.  The built-in module `pathlib` provides many useful functions for interacting and manipulating filepaths on your operating system. On the following, we have data in different sub-folders and we will learn how to use the `Path` class from the `pathlib` library to construct filepaths. Next, we will import and use the `Path` class and see how we can construct a filepath by joining a folder path and file name:

```python
from pathlib import Path 

# Initialize the Path
input_folder = Path("data/finnish_stations")

# Join folder path and filename
fp = input_folder / "028360.txt"
fp
```

Here, we first initialized the `Path` object and stored it in variable `input_folder` by passing a relative path as a string to directory where all our files are located. Then we created a full filepath to file `028360.txt` by adding a forward slash (`/`) character between the folder and the filename which joins them together (easy!). In this case, our end result is something called a *`PosixPath`* which is a filesystem path to a given file on Linux or Mac operating systems. If you would run the same commands on Windows machine, the end result would be a *`WindowsPath`*. Hence, the output depends on which operating system you are using. However, you do not need to worry about this, because both types of Paths work exactly the same, no matter which operating system you use.

Both the `Path` object that we stored in `input_folder` variable and the `PosixPath` object that we stored in variable `fp` are actually quite versatile creatures, and we can do many useful things with them. For instance, we can find the parent folder where the file is located, extract the filename from the full path, test whether the file or directory actually exists, find various properties of the file (such as size of the file or creation time), and so on:

```python
fp.parent
```

```python
fp.name
```

```python
fp.exists()
```

```python
# File properties
size_in_bytes = fp.stat().st_size
creation_time = fp.stat().st_ctime
modified_time = fp.stat().st_mtime
print(f"Size (bytes): {size_in_bytes}\nCreated (seconds since Epoch): {creation_time}\nModified (seconds since Epoch): {modified_time}")
```

There are also various other methods that you can do with `pathlib`, such as rename the files (`.rename()`) or create folders (`.mkdir()`). You can see all available methods from `pathlib` documentation [^pathlib]. One of the most useful tools in `pathlib` is the ability to list all files within a given folder by using the method `.glob()` which also allows you to add specific search criteria for listing only specific files from the directory:

```python
file_list = list(input_folder.glob("0*txt"))
```

Here, the result is stored into variable `file_list` as a list. By default, the `.glob()` produces something called a `generator` which is a "lazy iterator", i.e. a special kind of function that allows you to iterate over items like a list, but without actually storing the data in memory. By enclosing the `.glob()` search functionality with `list()` we convert this generator into a normal Python list. Note that we're using the \* character as a wildcard, so any filename that starts with `0` and ends with `txt` will be added to the list of files. We specifically use the number `0` as the starting part for the search criteria to avoid having metadata files included in the list. Let's take a look what we got as a result:

```python
print("Number of files in the list:", len(file_list))
file_list
```

### Iterate over input files and repeat the analysis

Now, we should have all the relevant file paths in the `file_list`, and we can loop over the list using a for loop (again we break the loop after first iteration):

```python
for fp in file_list:
    print(fp)
    break
```

The data that we have sampled is in regular CSV format which we can read easily with `pd.read_csv()` function: 

```python
data = pd.read_csv(fp)
data.head()
```

Now we have all the file paths to our weather observation datasets in a list, and we can start iterating over them and repeat the analysis steps for each file separately. We keep all the analytical steps inside a loop so that all of them are repeated to different stations. Finally, we will store the warmest January for each station in a list called `results` using a regular Python's `append()` method and merge the list of DataFrames into one by using `pd.concat()` function:

```python jupyter={"outputs_hidden": false}
# A list for storing the result
results = []

# Repeat the analysis steps for each input file:
for fp in file_list:

    # Read the data from CSV file
    data = pd.read_csv(fp)

    # Rename the columns
    new_names = {
        "USAF": "STATION_NUMBER",
        "YR--MODAHRMN": "TIME",
        "SPD": "SPEED",
        "GUS": "GUST",
        "TEMP": "TEMP_F",
    }
    data = data.rename(columns=new_names)

    # Print info about the current input file (useful to understand how the process advances):
    print(
        f"STATION NUMBER: {data.at[0,'STATION_NUMBER']}\tNUMBER OF OBSERVATIONS: {len(data)}"
    )

    # Create column
    col_name = "TEMP_C"
    data[col_name] = None

    # Convert tempetarues from Fahrenheits to Celsius
    data["TEMP_C"] = data["TEMP_F"].apply(fahr_to_celsius)

    # Convert TIME to string
    data["TIME_STR"] = data["TIME"].astype(str)

    # Parse year and month and convert them to numbers
    data["MONTH"] = data["TIME_STR"].str.slice(start=5, stop=6).astype(int)
    data["YEAR"] = data["TIME_STR"].str.slice(start=0, stop=4).astype(int)

    # Extract observations for the months of January
    january = data[data["MONTH"] == 1]

    # Aggregate the data and get mean values
    columns = ["TEMP_F", "TEMP_C", "STATION_NUMBER"]
    monthly_mean = january.groupby(by=["YEAR", "MONTH"])[columns].mean().reset_index()

    # Sort the values and take the warmest January
    warmest = monthly_mean.sort_values(by="TEMP_C", ascending=False).head(1)

    # Add to results
    results.append(warmest)

# Merge all the results into a single DataFrame
results = pd.concat(results)
```

Awesome! Now we have conducted the same analysis for 15 weather stations in Finland and it did not took too many lines of code! We were able to follow how the process advances with the printed lines of information, i.e. we did some simple `logging` of the operations. Let's finally investigate our results:

```python
results
```

Each row in the results represents the warmest January at given `STATION_NUMBER` between the years 2015 and 2019. Based on the `YEAR` column, the warmest January in most of Finland's weather stations during this five-year period was in 2015. We can confirm this by checking the value counts of the `YEAR` column:

```python
results["YEAR"].value_counts()
```

## Footnotes

[^noaanews]: <https://www.noaa.gov/news/january-2020-was-earth-s-hottest-january-on-record>
[^pathlib]: <https://docs.python.org/3/library/pathlib.html>
