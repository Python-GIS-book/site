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
# Data wrangling, grouping and aggregation

Next, we will continue working with weather data but expand our analysis to cover longer periods of data from Finland. In this section, you will learn various useful techniques in `pandas` to manipulate, group, and aggregate the data in different ways that are useful when extracting information from your data. At the end of this section, you will learn how to create an automated data analysis workflow that can be repeated with multiple input files that have a similar structure. As a case study, we will investigate the claim that [the summer of 2021 was exceptionally warm in Finland](https://yle.fi/a/3-12082062) [^ylenews].
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Cleaning data while reading

In this section we are using weather observation data from Finland that was downloaded from NOAA (check the {doc}`data overview </data/index>` section for more details). The input data are separated by varying number of spaces (i.e., fixed column widths). The first lines of the data look like following:

``` 
STATION           ELEVATION  LATITUDE   LONGITUDE  DATE     PRCP     TMAX...
----------------- ---------- ---------- ---------- -------- -------- ----...
GHCND:FIE00142226         24    60.2028    24.9642 20051213 -9999    40  ...
GHCND:FIE00142226         24    60.2028    24.9642 20051214 -9999    35  ...
GHCND:FIE00142226         24    60.2028    24.9642 20051215 -9999    38  ...
```

By looking at the file contents above, we can see a few things that we need to consider when reading the data:

1. The delimiter: The columns are separated with a varying amount of spaces which requires using some special tricks when reading the data with the `pandas` `.read_csv()` function.
2. The line of dashes: The second line of the data file contains characters separating the column headings from the data.
3. NoData values: `NaN` values in the data file are coded as `-9999` and hence we need to be able to instruct `pandas` to interpret those values as `NaN`. 
4. Unnecessary columns: The input data contains eight columns, and several of those do not contain data we need. Thus, we should probably ignore the unnecessary columns when reading in the data file.

Handling and cleaning heterogeneous input data (such as in our example here) can be done after reading in the data. However, in many cases it is preferable to do some cleaning and preprocessing when reading in the data. In fact, it is often much easier to do things this way. Let's see how we can handle each point above when reading in the data file.

1. For our data file, we can read the data with varying number of spaces between the columns by using the parameter `sep=r"\s+"`. In this case, we use a raw text string with the `sep` parameter, which is indicated by the `r` before the first quotation mark and ensures the escape character `\` is handled properly in the `sep` string.
2. The second line of the data file can be skipped using the `skiprows` parameter, as we have seen earlier. However, this time we will give a list of rows to skip (by index value) so that the header line is read, the second line is skipped, and the rest of the file is read. In this case, we can use `skiprows=[1]`.
3. For handling the NoData values (point 2 above), we can tell `pandas` to consider `-9999` as `NaN` by using the `na_values` parameter and specifying the character string `-9999` should be converted to `NaN`. For this data file we can specify `na_values=["-9999"]`, which will then convert the `-9999` values into `NaN` values.
4. Finally, we can limit the number of columns that we read (point 3 above) by using the `usecols` parameter, which we have already used previously. In our case, we are interested in columns that might be somehow useful to our analysis, including the station ID, date, and data about temperatures: `'STATION', 'DATE', 'TMAX', 'TMIN'`. Achieving all these things is pretty straightforward using the `.read_csv()` function, as demonstrated below.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
import pandas as pd

# Define relative path to the file
fp = "data/helsinki-kumpula.txt"

# Read data using varying amount of spaces as separator,
# specifying '*' characters as NoData values,
# and selecting only specific columns from the data
data = pd.read_csv(
    fp,
    sep=r"\s+",
    skiprows=[1],
    na_values=["-9999"],
    usecols=["STATION", "DATE", "TMAX", "TMIN"],
)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's now check the data by printing the first five rows with the `.head()` function.
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
data.head()
```

Perfect, looks good. We have excluded some unnecessary columns, skipped the row of dashes, and converted the `-9999` values to `NaN` values (we will confirm this later in this section).


## Renaming columns

Let's take a closer look at the column names of our `DataFrame`.

```python jupyter={"outputs_hidden": false}
print(data.columns)
```

As we see, some of the column names could be unclear with only their names. Luckily, it is easy to change labels in a `pandas` `DataFrame` using the `.rename()` function. In order to change the column names, we need to tell `pandas` how we want to rename the columns using a *{term}`dictionary`* that converts the old names to new ones. A dictionary is a specific data structure in Python for storing key-value pairs. We can define the new column names using a dictionary where we list `key: value` pairs in following manner:
   
- `STATION`: `STATION_ID`
- `TMAX`: `TMAX_F`
- `TMIN`: `TMIN_F`

Hence, the original column name (e.g., `STATION`) is the dictionary `key` which will be converted to a new column name `STATION_ID` (which is the `value`). In addition, the temperature values in this data file are represented in degrees Fahrenheit. We will soon convert those temperatures to degrees Celsius. Thus, in order to avoid confusion with the columns, let's rename the columns `TMAX` to `TMAX_F`, and `TMIN` to `TMIN_F`. Below we can create a dictionary for the new column names.

```python jupyter={"outputs_hidden": false}
new_names = {
    "STATION": "STATION_ID",
    "TMAX": "TMAX_F",
    "TMIN": "TMIN_F",
}
new_names
```

Our dictionary format looks correct, so now we can change the column names by passing that dictionary with the parameter `columns` in the `.rename()` function.

```python jupyter={"outputs_hidden": false}
data = data.rename(columns=new_names)
data.columns
```

Perfect, now our column names are easier to understand and use. 


## Using functions with pandas

Now it's time to convert those temperatures from degrees Fahrenheit to degrees Celsius. We have done this many times before, but this time we will learn how to apply our own functions to data in a `pandas` `DataFrame`. We will define a function for the temperature conversion and then apply this function for each Fahrenheit value on each row of the `DataFrame`. The output Celsius values will be stored in a new column called `TMAX_C`, for example. But first, it is a good idea to check some basic properties of our input data before proceeding with data analysis.

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

Nothing suspicious in the first and last rows, but here the `.info()` function indicates that the number of observations per column varies if you compare the `Non-Null Count` information to the number of entries in the data (n = 6821). Only the station number and date seem to have data for each row. The other columns appear to have a few missing values. This is not necessarily anything dangerous, but good to keep in mind. Let's now check the descriptive statistics.

```python
# Descriptive stats
data.describe()
```

Looking at the `TMAX_F` values (maximum daily temperatures in Fahrenheit), we can confirm that our measurements seems more or less valid because the value range of the temperatures makes sense (i.e., there are no outliers such as extremely high or low values) and there are not any `-9999` values that were not converted to `NaN`. It is always a good practice to critically inspect your data before doing any analysis, as it is possible that your data may include incorrect values (e.g., due to a sensor malfunction or human error).


### Defining a function

Now that we are sure that our data looks correct, and we can start our temperature conversion process by first defining our function to convert from Fahrenheit to Celsius. `pandas` can use regular functions, so you can simply define functions for `pandas` exactly the same way as you would do normally (as we learned in Chapter 2, for instance). Let's define a function that converts from degrees Fahrenheit to Celsius.

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

Now we have the function defined and stored in memory. At this point it is good to test the function with a known value to make sure it works properly.

```python
fahr_to_celsius(32)
```

32 degrees Fahrenheit is indeed 0 degrees Celsius, so our function seem to be working correctly.


### Using a function by iterating over rows

Next we will learn how to use our function with data stored in a `pandas` `DataFrame`. We will first apply the function row by row using a `for` loop and then we will learn a more efficient way of applying the function to all rows at once.

Looping over rows in a `DataFrame` can be done in a few different ways. A common approach is to use the `.iterrows()` method which loops over the rows as index-Series pairs. In other words, we can use the `.iterrows()` method together with a `for` loop to repeat a process for each row in a `pandas` `DataFrame`. Please note that iterating over rows this way is a rather inefficient approach, but it is still useful to understand the logic behind how this works. When using the `.iterrows()` method it is important to understand that `.iterrows()` accesses not only the values of one row, but also the `index` of the row. Let's start with a simple example `for` loop that goes through each row in our `DataFrame`.

```python jupyter={"outputs_hidden": false}
# Iterate over the rows
for idx, row in data.iterrows():
    # Print the index value
    print(f"Index: {idx}")

    # Print the temperature from the row
    print(f"TMIN F: {row["TMIN_F"]}\n")

    break
```

We can see that the `idx` variable indeed contains the index value `0` (the first row) and the `row` variable contains all the data from that row stored as a `pandas` `Series`. Also, notice that when developing a `for` loop you do not always need to iterate through the entire loop if you just want to test things out. Using the `break` statement in Python terminates a loop wherever it is placed inside the loop. In our case we used it to check out the values on the first row of the `DataFrame`. This saves time and allows us to test the code logic without printing thousands of values to the screen!

Next, let's create an empty column `TMIN_C` for the Celsius temperatures and update the values in that column using the `fahr_to_celsius()` function that we defined earlier. For updating the value in the `DataFrame`, we can use the `.at[]` indexer that we used earlier in this chapter. This time, however, we will use the `.itertuples()` method to access the rows in the `DataFrame`. The `.itertuples()` method works similarly to `.iterrows()`, except it returns only the row values without the `index`. In addition,  the returned values are not a `pandas` `Series`, but instead `.itertuples()` returns a named tuple data type. As a result, when using `.itertuples()` accessing the row values needs to be done a bit differently. Remember, a {term}`tuple` is like a list but {term}`immutable` and a "named tuple" is a special kind of tuple object that adds the ability to access the values by name instead of position index. Thus, we can access the `TMIN_F` value in a given row using `row.TMIN_F` (in contrast to how we accessed the value in the example above). We will not work with named tuples in the rest of the book, but more information can be found in the [Python documentation for named tuples](https://docs.python.org/3/library/collections.html#collections.namedtuple) [^namedtuple].

Let's see an example of how to use the `.itertuples()` method.

```python
# Create an empty column for the output values
data["TMIN_C"] = 0.0

# Iterate over the rows
for row in data.itertuples():
    # Convert the Fahrenheit to Celsius
    # Notice how we access the row value
    celsius = fahr_to_celsius(row.TMIN_F)

    # Update the value for 'Celsius' column with the converted value
    # Notice how we can access the Index value
    data.at[row.Index, "TMIN_C"] = celsius
```

```python
# Check the result
data.head()
```

```python
# What does our row look like?
row._asdict()
```

Okay, now we have iterated over our data, converted the temperatures to degrees Celsius using our `fahr_to_celsius()` function, and stored the results in the `TMIN_C` column. The values look correct as 32 degrees Fahrenheit is 0 degrees Celsius, which can be seen on the first row. We also have the last row of our `DataFrame` stored in the variable `row` from the code above, which is a named tuple that has been converted to the dictionary data type using the `._asdict()` method for named tuples.

Before moving to other more efficient ways to use functions with a `pandas` `DataFrame`, we should note a few things about the approaches above. We demonstrated use of the `.itertuples()` method for looping over the values because it is significantly faster than `.iterrows()` (can be around 100 times faster). We also used `.at[]` to assign the value in the `DataFrame` because it is designed to access single values more efficiently than the `.loc[]` indexer, which can access groups of rows and columns. That said, you could have also simply used `data.loc[idx, new_column] = celsius` to achieve the same result as both examples above. It is simply slower.


### Using a function with the apply method

Although using a `for` loop with `.itertuples()` can be fairly efficient, the `pandas` `DataFrame` and `Series` data structures have a dedicated method called `.apply()` for applying functions in columns (or rows). `.apply()` is typically faster than `.itertuples()`, especially if you have a large number of rows. When using `.apply()`, we pass the function that we want to use as an argument. Let's start by applying our `fahr_to_celsius()` function to the `TMIN_F` column with the temperature values in Fahrenheit.

```python
data["TMIN_F"].apply(fahr_to_celsius)
```

The results again look logical. Notice how we passed the `fahr_to_celsius()` function without using the parentheses `()` after the name of the function. When using `.apply()`, you should always leave out the parentheses from the function that you use. In other words, you should use `.apply(fahr_to_celsius)` not `.apply(fahr_to_celsius())`. Why? Because the `.apply()` method will execute and use the function itself in the background when it operates with the data. If we would pass our function including the parentheses, the `fahr_to_celsius()` function would actually be executed once before the loop with `.apply()` starts (thus becoming unusable) and that is not what we want.

Our previous command only returned the `Series` of temperatures to the screen, but naturally we can also store them permanently in a column of our `DataFrame` (overwriting the old values).

```python
data["TMIN_C"] = data["TMIN_F"].apply(fahr_to_celsius)
```

A nice thing with `.apply()` is that we can also apply the function on several columns at once. Below, we also sort the values in descending order based on values in the `TMIN_F` column to confirm that applying our function really works.

```python
cols = ["TMAX_F", "TMIN_F"]
result = data[cols].apply(fahr_to_celsius)
result.sort_values(by="TMIN_F", ascending=False).head()
```

You can also directly store the outputs to the `DataFrame` columns `TMAX_C` and `TMIN_C`.

```python
cols = ["TMAX_F", "TMIN_F"]
newcols = ["TMAX_C", "TMIN_C"]
data[newcols] = data[cols].apply(fahr_to_celsius)
data.head()
```

In this section, we showed you a few different ways to iterate over rows in `pandas` and apply functions. The most important thing is that you understand the logic of how loops work and how you can use your own functions to modify the values in a `pandas` `DataFrame`. Whenever you need to loop over your data, we recommend using `.apply()` as it is typically the most efficient one in terms of execution time. Remember that in most cases you do not need to use loops. Instead you can do calculations in a "vectorized manner" (which is the fastest way) as we learned previously when doing basic calculations in `pandas`.


## String slicing

We will eventually want to group our data based on month in order to see if the temperatures in June of 2021 were higher than on average (which is the goal in our analysis as you might recall). Currently, the date and time information is stored in the column `DATE` that has a structure `yyyyMMdd`. This is a typical timestamp format in which `yyyy` represents the year in a four digit format, `MM` is for the month (two digits), and `dd` is for the day. Let's have a closer look at the date and time information we have by checking the values in that column and their data type.

```python
data["DATE"].head()
```

```python
data["DATE"].tail()
```

The `DATE` column contains dates for the range of observations in our data set. The timestamp for the first observation is `20051213` (December 13th, 2005) and the timestamp for the latest observation is `20240831` (August 31st, 2024). As we can see, the data type (`dtype`) of our column seems to be `int64` (i.e., the information is stored as integer values).


To proceed with our analysis, we want to aggregate this data on a monthly level. In order to do so, we need to "label" each row of data based on the month when the record was observed. Hence, we need to somehow separate information about the year and month for each row. In practice, we can create a new column (or an index) containing information about the month (including the year but excluding days). There are different ways of achieving this, but here we will take advantage of `string slicing` which means that we convert the date information into character strings and "cut" the needed information from the string objects. The other option would be to convert the timestamp values into something called `datetime` objects, but we will learn about those a bit later. Before further processing, we first want to convert the `DATE` column to character strings for convenience and store those values in a new column called `DATE_STR`.

```python jupyter={"outputs_hidden": false}
data["DATE_STR"] = data["DATE"].astype(str)
```

If we look at the latest time stamp in the data (`20240831`), you can see that there is a systematic pattern: `YEAR-MONTH-DAY`. The first four characters always represent the year and the following two characters represent the month. Because we are interested in understanding monthly averages for different years, we want to slice the year and month values from the timestamp (the first 6 characters) like this:

```python
date = "20240831"
date[0:6]
```

Using this approach, we can slice the correct range of characters from the `DATE_STR` column using a specific `pandas` function designed for a `Series` called `.str.slice()`. The function has the parameters `start` and `stop`, which you can use to specify the positions where the slicing should start and end.

```python
data["YEAR_MONTH"] = data["DATE_STR"].str.slice(start=0, stop=6)
data.head()
```

Nice! Now we have "labeled" the rows based on information about the year and month.

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 3.7

Create a new column `MONTH` with information about the month without the year.
<!-- #endregion -->

```python tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["hide-cell", "remove_book_cell"]
# Solution

data["MONTH"] = data["DATE_STR"].str.slice(start=4, stop=6)
```

## Grouping and aggregating data


### Basic logic of grouping a `DataFrame` using `.groupby()`

In the following sections, we want to calculate the average temperature for each month in our data set. Here, we will learn how to use the `.groupby()` method, which is a handy tool for combining large amounts of data and computing statistics for subgroups. We will use the `.groupby()` method to calculate the average temperatures for each month in three main steps:

1. Group the data based on year and month using `.groupby()`
2. Calculate the average temperature for each month (i.e., each group) 
3. Store the resulting row into a `DataFrame` called `monthly_data`
  
We have many rows of weather data (n = 6821) to process and our goal is to create an aggregated `DataFrame` that has only one row per month. We can group the data by month using the `.groupby()` function by providing the name of the column (or a list of columns) that we want to use as basis for doing the grouping. Let's group our data based on the unique year and month combinations.

```python
grouped = data.groupby("YEAR_MONTH")
```

Notice, that it would also be possible to create combinations of years and months "on the fly" if you have them in separate columns. In such case, grouping the data could be done as `grouped = data.groupby(['YEAR', 'MONTH'])`. Let's explore the new variable `grouped`.

```python
print(type(grouped))
print(len(grouped))
```

We have a new object with type `DataFrameGroupBy` with 225 groups. In order to understand what just happened, let's also check the number of unique year and month combinations in our data.

```python
data["YEAR_MONTH"].nunique()
```

Length of the grouped object should be the same as the number of unique values in the column we used for grouping (`YEAR_MONTH`). For each unique `YEAR_MONTH` value, there is a group of data. Let's explore our grouped data further by checking the "names" of the first five groups. Here, we access the `keys` of the groups and convert them to a `list` so that we can slice and print only a few of those to the screen.

```python
list(grouped.groups.keys())[:5]
```

Let's check the contents for a group representing December 2005. We can get the values for that month from the grouped object using the `.get_group()` method.

```python jupyter={"outputs_hidden": false}
# Specify a month (as character string)
month = "200512"

# Select the group
group1 = grouped.get_group(month)
group1
```

As we can see, a single group contains a `DataFrame` with values only for that specific month. Let's check the data type of this group.

```python
type(group1)
```

So, one group is a `pandas` `DataFrame`, which is really useful because it allows us to use all the familiar `DataFrame` methods for calculating statistics, etc. for this specific group. It is also possible to iterate over the groups in our `DataFrameGroupBy` object which can be useful if you need to conduct and apply some more complicated sub-tasks for each group. When doing so, it is important to understand that a single group in our `DataFrameGroupBy` object actually contains not only the actual values but also information about the `key` that was used to do the grouping. Hence, when iterating we need to assign the `key` and the values (i.e., the group) to separate variables. Let's see how we can iterate over the groups and print the key and the data from a single group (again using `break` to only see the first group).

```python jupyter={"outputs_hidden": false}
# Iterate over groups
for key, group in grouped:
    # Print key and group
    print(f"Key:\n{key}")
    print(f"\nFirst rows of data in this group:\n {group.head()}")

    # Stop iteration with break command
    break
```

Here, we can see that the `key` contains the name of the group (i.e., the unique value from `YEAR_MONTH`). 


### Aggregating data with `.groupby()`

We can, for example, calculate the average values for all variables using the statistical functions that we have seen already (e.g., `.mean()`, `.std()`, `.min()`, etc.). To calculate the average temperature for each month, we can use the `.mean()` function. Let's calculate the mean for all the weather related data attributes in our group at once.

```python jupyter={"outputs_hidden": false}
# Specify the columns that will be part of the calculation
mean_cols = ["TMAX_F", "TMIN_F", "TMAX_C", "TMIN_C"]

# Calculate the mean values all at one go
mean_values = group1[mean_cols].mean()
mean_values
```

As a result, we get a `pandas` `Series` with mean values calculated for all columns in the group. Notice that if you want to convert this `Series` back into a `DataFrame` (which can be useful if you want to merge multiple groups, for example), you can use the command `.to_frame().T`, which first converts the Series into a `DataFrame` and then transposes the order of the axes (the label names become the column names).

```python
# Convert to DataFrame
mean_values.to_frame().T
```

To do a similar aggregation with all the groups in our data set, we can combine the `.groupby()` function with the aggregation step (such as taking the mean of the given columns), and finally restructure the resulting `DataFrame` a bit. This might be a bit harder to understand at first, but this is how you would group and aggregate the values.

```python
# The columns that we want to aggregate
mean_cols = ["TMAX_F", "TMIN_F", "TMAX_C", "TMIN_C"]

# Group and aggregate the data with one line
monthly_data = data.groupby("YEAR_MONTH")[mean_cols].mean().reset_index()
monthly_data
```

As we can see, aggregating the data in this way is a fairly straightforward and fast process requiring merely a single command. So what did we actually do here? We (1) grouped the data, (2) selected specific columns from the result (`mean_cols`), (3) calculated the mean for all of the selected columns of the groups, and finally (4) reset the index. Resetting the index at the end is not necessary, but by doing it we turn the `YEAR_MONTH` values into a dedicated column in our data (which would be otherwise be stored as `index`).

What might not be obvious from this example is the fact that each group is actually iterated over and the aggregation step is repeated for each group. For you to better understand what happens, we will next repeat the same process by iterating over the groups and eventually creating a `DataFrame` that contains the mean values for all of the weather attributes that we are interested in. In this approach, we will iterate over the groups, calculate the mean values, store the result in a list, and finally merge the aggregated data into a `DataFrame` called `monthly_data`.

```python
# Create an empty list for storing the aggregated rows/DataFrames
data_container = []

# The columns that we want to aggregate
mean_cols = ["TMAX_F", "TMIN_F", "TMAX_C", "TMIN_C"]

# Iterate over the groups
for key, group in grouped:
    # Calculate mean
    mean_values = group[mean_cols].mean()

    # Add the "key" (i.e., the date+time information) into the Series
    mean_values["YEAR_MONTH"] = key

    # Convert the Series into a DataFrame and
    # append the aggregated values into a list as a DataFrame
    data_container.append(mean_values.to_frame().T)

# After iterating over all groups, merge the list of DataFrames
monthly_data = pd.concat(data_container)
monthly_data
```

As a result, we get identical results to those produced by the approach that was done earlier with a single line of code (except for the position of the `YEAR_MONTH` column).

So which approach should you use? From the performance point of view, we recommend using the first approach (i.e., chaining), which does not require you to use a separate `for` loop, and is highly efficient. However, this approach might be a bit more difficult to read and comprehend (the loop might be easier). Also, sometimes you want to include additional processing steps within the loop that can be hard accomplish by chaining everything into a single command. Hence, it is useful to know both of these approaches for doing aggregations of the data.


## Case study: Detecting warm months

Now that we have aggregated our data on monthly level, all we need to do is to check which years had the warmest June temperatures. A simple approach is to select all June values from the data and check which group(s) have the highest mean value. Before doing this, let's separate the month information from our timestamp following the same approach as previously we did when slicing the year-month combination.

```python
monthly_data["MONTH"] = monthly_data["YEAR_MONTH"].str.slice(start=4, stop=6)
monthly_data.head()
```

Let's also make an estimate of the mean monthly temperature `TAVG_C` as the average of `TMIN_C` and `TMAX_C`.

```python
monthly_data["TAVG_C"] = (monthly_data["TMAX_C"] + monthly_data["TMIN_C"]) / 2.0
```

Now we can select the values for June from our data and store it into a new variable `june_data`. Then we can check the highest temperature values by sorting the `DataFrame` by the `TAVG_C` column in descending order.

```python
june_data = monthly_data.loc[monthly_data["MONTH"] == "06"]
june_data.sort_values(by="TAVG_C", ascending=False).head()
```

By looking at the order of `YEAR_MONTH` column, we can see that June 2021 is indeed the warmest June on record for the Helsinki Kumpula weather station (as of 2024) based on the estimated average monthly temperatures. Let's now explore similar temperature data from other weather stations in Finland and see whether June of 2021 has been exceptionally warm in other locations.


## Automating the analysis

Above, we learned how to aggregate data using `pandas` to calculate average monthly temperatures based on daily weather observations. With these skills, we can now take advantage of one of the most useful aspects of programming: automating processes and repeating analyses for any number of similar data files (assuming the data structure is the same). 

Let's now see how we can repeat the previous data analysis steps for 15 weather stations located in different parts of Finland containing data for up to 116 years (1908-2024). The idea is that we will repeat the process for each input file using a (rather long) `for` loop. We will use the most efficient alternatives of the previously represented approaches, and finally will store the results in a single `DataFrame` for all stations. We will learn how to manipulate file paths in Python using the `pathlib` module and see how we can list our input files in the data directory `data/finnish-stations`. We will store those paths in the variable `file_list` so that we can use the file paths easily in the later steps.


### Managing and listing filesystem paths

In Python there are two commonly used approaches to manage and manipulate file paths, namely the `os.path` sub-module and the newer `pathlib` module (available since Python 3.4), which we will demonstrate here. The built-in module `pathlib` provides many useful functions for interacting and manipulating file paths in your operating system. In the following example, we have data in different files in a sub-folder and will learn how to use the `Path` class from the `pathlib` library to construct file paths. To start, we will import and use the `Path` class and see how we can construct a file path by joining a folder path and a file name.

```python
from pathlib import Path

# Initialize the Path
input_folder = Path("data/finnish-stations")

# Join folder path and filename
fp = input_folder / "enontekio-kilpisjarvi.txt"
fp
```

Above, we first initialized the `Path` object and stored it in the variable `input_folder` by passing a relative path as a string indicating the directory where all our files are located. Then we created a complete file path to the file `enontekio-kilpisjarvi.txt` by adding a forward slash (`/`) character between the folder and the filename which joins them together (easy!). In this case, our end result is something called a `PosixPath`, which is a file system path to a given file in the Linux or macOS operating systems. If you would run the same commands on a computer using the Windows operating system, the end result would be a `WindowsPath` object. Thus, the output depends on which operating system you are using. However, you do not need to worry about this because both types of Paths work exactly the same no matter which operating system you use.

Both the `Path` object that we stored in the `input_folder` variable and the `PosixPath` object that we stored in variable `fp` are actually quite versatile creatures, and we can do many useful things with them. For instance, we can find the parent folder where the file is located, extract the filename from the full path, test whether the file or directory actually exists, find various properties of the file (such as size of the file or creation time), and so on. Let's see a few examples below.

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
print(
    f"Size (bytes): {size_in_bytes}\nCreated (seconds since Epoch): {creation_time}\nModified (seconds since Epoch): {modified_time}"
)
```

There are also various other methods that you can use from the `pathlib` module, such as for renaming files (`.rename()`) or creating directories (`.mkdir()`). You can see all available methods from the [`pathlib` documentation](https://docs.python.org/3/library/pathlib.html) [^pathlib]. One of the most useful tools in `pathlib` is the ability to list all of the files within a given directory using the `.glob()` method, which also allows you to add specific search criteria for listing only specific files from a directory.

```python
file_list = list(input_folder.glob("*txt"))
```

Here, the result is stored in the variable `file_list` as a list. By default, the `.glob()` function produces something called a `generator` which is a "lazy iterator" (a special kind of function that allows you to iterate over items like a list, but without actually storing the data in memory). By enclosing the `.glob()` search functionality in the `list()` function, we convert this generator into a normal Python list. Note that we're using the \* character as a wildcard, so any filename that ends with `txt` will be added to the list of files. Let's take a look what we produced as a result.

```python
print(f"Number of files in the list: {len(file_list)}")
file_list
```

### Iterate over input files and repeat the analysis

At this point we should have all the relevant file paths in the `file_list` variable, and we can loop over the list using a `for` loop (again we will break the loop after the first iteration).

```python
for fp in file_list:
    print(fp)
    break
```

The data we have in the data files are formatted just like the example file we have used in this section (in fact, it is one of the files in our data directory). Thus, we can easily the file data using the `pd.read_csv()` function with the same parameter values specified earlier.

```python
data = pd.read_csv(
    fp,
    sep=r"\s+",
    skiprows=[1],
    na_values=["-9999"],
    usecols=["STATION", "DATE", "TMAX", "TMIN"],
)
data.head()
```

Now that we have all the file paths for our weather observation data sets in a list, we can start iterating over them and repeat the analysis steps for each file separately. We will keep all the analytical steps inside a loop so that all of them are repeated for the different stations. Finally, we will store the warmest June for each station in a list called `results` using a regular Python list's `.append()` method and merge the list of `DataFrames` into one using the `pd.concat()` function.

```python jupyter={"outputs_hidden": false}
# A list for storing the result
results = []

# Repeat the analysis steps for each input file:
for fp in file_list:
    # Read the data from text file
    data = pd.read_csv(
        fp,
        sep=r"\s+",
        skiprows=[1],
        na_values=["-9999"],
        usecols=["STATION", "DATE", "TMAX", "TMIN"],
    )

    # Rename the columns
    new_names = {
        "STATION": "STATION_ID",
        "TMAX": "TMAX_F",
        "TMIN": "TMIN_F",
    }
    data = data.rename(columns=new_names)

    # Print info about the current input file
    # This is useful to understand how the process proceeds
    print(
        f"STATION NUMBER: {data.at[0,'STATION_ID']}\tNUMBER OF OBSERVATIONS: {len(data)}"
    )

    # Estimate daily average temperature as average of TMAX and TMIN
    data["TAVG_F"] = (data["TMAX_F"] + data["TMIN_F"]) / 2.0

    # Create column
    data["TAVG_C"] = None

    # Convert temperatures from Fahrenheit to Celsius
    data["TAVG_C"] = data["TAVG_F"].apply(fahr_to_celsius)

    # Convert DATE to string
    data["DATE_STR"] = data["DATE"].astype(str)

    # Parse year and month and convert them to numbers
    data["MONTH"] = data["DATE_STR"].str.slice(start=5, stop=6).astype(int)
    data["YEAR"] = data["DATE_STR"].str.slice(start=0, stop=4).astype(int)

    # Extract observations for the months of June
    june = data[data["MONTH"] == 6]

    # Aggregate the data and get mean values
    columns = ["TAVG_F", "TAVG_C"]
    monthly_mean = june.groupby(by=["YEAR", "MONTH"])[columns].mean().reset_index()

    # Sort the values and take the warmest June
    warmest = monthly_mean.sort_values(by="TAVG_C", ascending=False).head(1)

    # Save data file name in DataFrame
    warmest["FILE"] = fp.name

    # Add to results
    results.append(warmest)

# Merge all the results into a single DataFrame
results = pd.concat(results)
```

Awesome! Now we have conducted the same analysis for 15 weather stations in Finland and it did not take many lines of code! We were able to follow how the process in real time via the information printed as the data were analyzed (i.e., we did some simple "logging" of the operations). Let's finally investigate our results.

```python
results
```

Each row in the results represents the warmest June at given station starting between 1908-2005 and ending in 2024. Based on the `YEAR` column, the warmest June in the majority of weather stations we have used was indeed in 2021. We can confirm this by checking the value counts for the `YEAR` column.

```python
results["YEAR"].value_counts()
```

It seems at least the start of summer in 2021 was abnormally warm in Finland!


## Footnotes

[^namedtuple]: <https://docs.python.org/3/library/collections.html#collections.namedtuple>
[^ylenews]: <https://yle.fi/a/3-12082062>
[^pathlib]: <https://docs.python.org/3/library/pathlib.html>
