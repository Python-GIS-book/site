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

# Working with temporal data

> “Ever since the dawn of civilization, people have not been content to see events as unconnected and inexplicable. They have craved an understanding of the underlying order in the world." - Stephen Hawking (1988)

Time is one of the very fundamental ways how we humans organize things in life and what we use to find understanding of the underlying world as Stephen Hawking (1988) famously put it in his book "A brief history of time". Hence, it is not surprising that the time dimension is very commonly attached to almost all data that we have in the world (the other dimension is naturally space or location, which we will focus in Part II). Hence, being able to handle and work with temporal information is extremely important when doing data analysis. Time information in the data allows us to see patterns through time (trends) as well as to make predictions to the future (at certain level of confidence). In this section, we will introduce some of the core ideas and functionalities how you can work with temporal data in Python and pandas.


## Date and time basics

Before doing any progamming, we need to understand a few details about time conventions themselves. There are a couple of ways how the time information (commonly referred as `timestamp`) is typically represented. The first one is to represent the temporal information as text with specific format such as `"2020-12-24T09:12:45Z"` which follows an international ISO 8601 standard [^isostandard]. In this format, the date components (year, month, day) are separated with dash (`-`) and the time components (hour, minute, second) are separated with colon (`:`). Typically there is a letter `T` separating the date and time components from each other (in some other formats, there could just be a space between them). The letter `Z` at the end of the string relates to time zones and means that the time here is represented as Coordinated Universal Time (UTC). Time zone information around the world are expressed using negative or positive offsets from the UTC. `UTC±00:00` is the same as Greenwhich Mean Time (GMT), and it was chosen after a series of conferences between 1881-1884 (Ogle, 2015) as the worldwide standard for representing the zone 0 to which all other time zones in the world are relative to. For instance, the local time in Finland is two hours ahead of UTC, meaning that the time zone information is expressed as `UTC+2` or `UTC+02:00`, whereas the local time in New York is four hours behind UTC respectively (i.e. `UTC-4`). Another commonly used way to represent time is to use a so called *Unix time* (also known as *Epoch time* or *POSIX time*). Unix time is expressed as number of seconds since *Unix Epoch* that was on the first of January 1970 at midnight in UTC (i.e. `1970-01-01T00:00:00Z`). This system was developed to describe a point in time in numerical format, and it is widely used in computers by different operating systems. Unix time increments every second and e.g. the Unix time of December 22nd 2020 at 15:00:00 (UTC) is represented as a single number `1608649200`. Using this kind of numerical representation of time makes it much easier for computers to store and manipulate the time information compared to having the information in textual format (`2020-12-22T15:00:00Z`). 


## Working with temporal data in Python

Next we will learn how temporal data can be handled in Python in general. The most fundamental Python library for dealing with temporal data is called `datetime` that supplies functionalities to construct and manipulate dates and times. The module is one of the Python's standard libraries, hence you do not need to install it separately. Other useful libraries for dealing with time and dates are `time` and `calendar` which provide some additional functionalities in addition to the functionalities provided by `datetime`. In addition, `pytz` library provides many useful functionalities to deal with time zone information and `dateutil` provides some handy functionalities to automate date parsing. Most often the `datetime` module and `pytz` (in addition to pandas) provide everything you need when doing analysis with temporal data. 


## Constructing datetime objects

A `datetime` object is a representation of time in a way that Python can understand and operate with it. With the `datetime` library it is possible to construct a `datetime` object for example by `parsing` it from text following the ISO 8601 format or from the Unix timestamp (notice that the name of the library and the object are the same). Let's see how we can construct a `datetime` object from text using a function `strptime()`. The `strptime()` function takes the variable `timestamp` as the first argument representing the time in textual format and a second argument ("%Y-%m-%dT%H:%M:%S") which looks quite complicated, but it is the `format code` that instructs the `datetime` how the textual representation of the time should be interpreted:

```python
from datetime import datetime
timestamp = "2020-12-22T15:00:00"
datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
```

As a result we get a `datetime` object in which the date has been converted into a set of numbers, in which the first one is the year, second one is month, third one day, and so on. This structure is always the same, no matter in what format the input data has been. By using the format codes (i.e. the second argument of the function), we can tell the computer that the first component in our string represents year in 4 digits. The `%Y` characters (i.e. a *directive*) is a special way to instruct the computer to do so. In a similar manner, we can instruct the computer to read the month based on numbers with two digits (`12`) using the directive `%m`. As you can see, there is always a `%` character and then some letter after it, which is the way how we determine how the date is formatted in our text. Notice that the date components are separated with dash (`-`) and the time components are separated with colons (`:`). As we can see from our format code, we can add those separator characters between the directives just as they are represented in the timestamp. Following this approach it is possible to parse basically any kind of time information represented as text. A few of the most commonly used datetime format code directives are listed in Table 2.1. 

_**Table 2.1**. Most commonly used datetime directives and their meaning._

| Directive | Description                                              | Examples                          |
|-----------|----------------------------------------------------------|-----------------------------------|
| %y        | Year without century as a zero-padded number.            | 00, 01, 10, 20                    |
| %Y        | Year including century as a zero-padded number.          | 2000, 1900, 1920                  |
| %m        | Month as a zero-padded number.                           | 01,02, ... , 11, 12               |
| %b        | Month as abbreviated name.                               | Jan, Feb, ..., Dec                |
| %B        | Month as full name.                                      | January, February, ..., December  |
| %d        | Day of the month as a zero-padded number.                | 01, 02, ..., 30, 31               |
| %H        | Hour (24-hour clock) as a zero-padded number.            | 00, 01, ..., 22, 23               |
| %I        | Hour (12-hour clock) as a zero-padded number.            | 01, 02, ..., 11, 12               |
| %p        | AM or PM (12-hour clock).                                | am, pm, AM, PM                    |
| %M        | Minute as a zero-padded number.                          | 00, 01, ..., 58, 59               |
| %S        | Second as a zero-padded number.                          | 00, 01, ..., 58, 59               |
| %z        | UTC offset (can be empty).                               | +0000, +2000, -4000               |
| %Z        | Time zone name (can be empty).                           | UTC, GMT                          |
| %a        | Weekday as abbreviated name.                             | Mon, Tue, Sat, Sun                |
| %A        | Weekday as full name.                                    | Monday, Tuesday, Saturday, Sunday |
| %w        | Weekday as a number where 0 is Sunday and 6 is Saturday. | 0, 1, 2 ..., 6                    |




To crystallize the understanding how the timestamps can be parsed, let's look at a few more examples where we also include time zone information and parse the date information based on a format how we typically write dates as humans (without time component). Let's start by adding `+0200` to the end of the timestamp to express the UTC+2 time zone:    

```python
timestamp_with_tz = "2020-12-22T15:00:00 +0200"
dtz = datetime.strptime(timestamp_with_tz, "%Y-%m-%dT%H:%M:%S %z")
dtz
```

As we can see, now we produced the `datetime` object having time zone information attached into the `tzinfo` attribute showing the offset (i.e. *timedelta*) from UTC represented in seconds. Having the timezone information attached can be very useful if doing analysis with temporal data that has been collected from different parts of the world (under different time zones). Let's still take a look at an example in which we parse the `datetime` object from a textual representation that is written in a way how we humans normally write dates:

```python
date_written = "22 December 2020"
datetime.strptime(date_written, "%d %B %Y")
```

Here, we used a bit different format for instructing the computer how to read the text by using `%B` to denote a written month name, also we changed the order of the directives and used an empty space between them. Writing the exact form of how the timestamp information is written can be quite devious work, especially if working with handwritten data where stucture of the time information can vary a lot. Luckily, Python provides a handy library `dateutil` that automates most of this work. We can use a function called `parse()` that can automatically construct the `datetime` object from various formats:

```python
from dateutil.parser import parse
timestamp_with_tz = "2020-12-22T15:00:00 +0200"
date_written = "22 December 2020"
dt1 = parse(timestamp_with_tz)
dt2 = parse(date_written)
print(dt1, "\n", dt2)
```

All of the previous examples focused on using textual representation of time as input. Naturally it is also possible to construct a datetime object using Unix time representation. Because Unix time is a simple number, it is much more straightforward to parse a datetime object based on them. This is how would convert a Unix time `1608649200` into a `datetime` using `fromtimestamp()` function:

```python
unix_time = 1608649200
datetime.fromtimestamp(unix_time)
```

Wait, what? In the beginning of this chapter, we said that Unix time `1608649200` should be "December 22nd 2020 at 15:00:00 (UTC)", but here we have the result as five o'clock (i.e. 17, 0). This is due to the fact that the computer that this code is written with is located at a Finnish time zone (UTC+02), and as the Unix time is always passed as UTC time (GMT), the computer automatically returns the timestamp in local timezone (i.e. in Finnish time or whatever the local time has been specified in your computer's settings). This is a good thing to understand because it can be rather confusing sometimes when working with temporal data. Finally, it is naturally possible to initialize the `datetime` object also directly by passing integer numbers into the object itself. Here we use the same date and time as before but add `30` seconds to the end:  

```python
dt = datetime(2020, 12, 22, 17, 0, 30)
dt
```

## Parsing temporal components from datetime object

There are few useful tricks that you can do with the `datetime` objects. It is for example possible to parse specific temporal components directly from the `datetime` object. You can for example access the `.year`, `.month`, `.day`, `.hour`, `.minute` and `.second` attributes very easily that will return the value of the temporal element as an integer number:

```python
dt = datetime(2020, 12, 22, 17, 0, 30)
print(dt.year)
print(dt.month)
print(dt.day)
print(dt.hour)
```

In addition, you can parse for example the day of week by using `weekday()` function or parse only the date components from the `datetime` object by using `date()` function:

```python
print(dt.weekday())
print(dt.date())
```

By using `strftime()` function, you can use the same directives from Table 2.1 to construct and convert the `datetime` object to any text representation of the date and time. Next, we will see how this function can be used quite nicely for creating an easily understandable text based on our date and time information:

```python
custom_format = "%d %B %Y is %A. The time is %I:%M %p."
datetime.strftime(dt, custom_format)
```

## Working with temporal data in pandas

After learning the basics of how the temporal data can be represented as `datetime` objects, we can continue and see how temporal data can be manipulated in pandas. Pandas is extremely powerful and flexible what comes to working with temporal data. For instance, all the simple tricks that we saw earlier with `datetime` can be done also with pandas. When doing data analysis with pandas, it is typical that instead of dealing with single observations in time, you actually work with time series data, such as the hourly temperature values that we analyzed in the previous chapter. Pandas supports many useful functionalities related to parsing, manipulating and aggregating time series data. Let's start exploring the temporal capabilities of pandas by reading the hourly temperature observations from the same CSV file in a similar manner as we did previously. As a reminder, this is how the data look like:

``` 
  USAF  WBAN YR--MODAHRMN DIR SPD GUS CLG SKC L M H  VSB MW MW MW MW AW  ...
029440 99999 190601010600 090   7 *** *** OVC * * *  0.0 ** ** ** ** **  ...
029440 99999 190601011300 ***   0 *** *** OVC * * *  0.0 ** ** ** ** **  ...
029440 99999 190601012000 ***   0 *** *** OVC * * *  0.0 ** ** ** ** **  ...
029440 99999 190601020600 ***   0 *** *** CLR * * *  0.0 ** ** ** ** **  ...
```

The timestamps stored in the column `YR--MODAHRMN` can be automatically converted to `datetime` objects when reading the data by using `parse_dates` parameter and providing a list of column names that should be parsed to `datetime`:

```python
import pandas as pd

# Read the data and parse dates
fp = 'data/029820.txt'
data = pd.read_csv(fp, delim_whitespace=True, 
                   na_values=['*', '**', '***', '****', '*****', '******'],
                   usecols=['USAF','YR--MODAHRMN', 'DIR', 'SPD', 
                            'GUS','TEMP', 'MAX', 'MIN'],
                   parse_dates=["YR--MODAHRMN"]
                  )
# Rename the columns
new_cols = ['STATION_NUMBER', 'TIME', 'DIR', 'SPEED', 'GUST', 'TEMP_F', 'MAX', 'MIN']
data.columns = new_cols
data.head()
```

As we can see, the values in `TIME` column were automatically parsed into a format that are much easier to read than the original ones. When using pandas datetime parsing functionalities, the timestamps can be represented in different formats such as text in ISO 8601 format or Unix times (seconds since 1.1.1970). Let's take a look how the values in our `TIME` column look like:

```python
data["TIME"].head()
```

As we can see, pandas actually converted the timestamp values into a time series having specific data type called `datetime64`. The individual value of the time series is a specific pandas object called `Timestamp` that is a similar object as the Python's regular `datetime` object that we saw previously: 

```python
data.loc[0, "TIME"]
```

The `TimeStamp` object contains all the same attributes as the `datetime` object, but in addition, it has many useful attributes and functions that can be used in a vectorized manner. For instance, you can parse different temporal components from the time series stored in a column very efficiently. Let's parse the temporal components from `TIME` into columns `YEAR`, `MONTH`, `DAY` and `HOUR`: 

```python
data["YEAR"] = data["TIME"].dt.year
data["MONTH"] = data["TIME"].dt.month
data["DAY"] = data["TIME"].dt.day
data["HOUR"] = data["TIME"].dt.hour
data.head()
```

Now the new columns have corresponding integer values for each temporal component. We were able to access all the temporal attributes by using the `.dt` accessor that is available for all `Series` having `datetime64` data type. 

```python
data.head()
```

We can also combine the datetime functionalities with other methods from pandas. For example, we can check the number of unique years in our input data: 

```python
data['TIME'].dt.year.nunique()
```

As a result, we can see that we have data from 69 years. Similarly as with `datetime` library, we can construct custom formatted texts using the `strftime()` function that can be applied to the time series. Let's create a new column `DATE_TZ` using a format that will add time zone information for the values:

```python
# Convert to datetime and keep only year and month
data['DATE_TZ'] = data["TIME"].dt.strftime("%Y-%m-%dT%H:%M:%S +02:00")
data.head()
```

Now we have a column `DATE_TZ` with timestamps as texts including additional information about the time zone (UTC+02:00). To understand how timezone information can be used in pandas, let's parse the information from `DATE_TZ` into a new column `TIME_TZ`. We can convert timestamps stored as text in a column by using `pd.to_datetime()` function. It basically does the same thing as using the `parse_dates` parameter during reading:  

```python
data['TIME_TZ'] = pd.to_datetime(data["DATE_TZ"])
data["TIME_TZ"].head()
```

As we can see, now we have the time series as `datetime64` having additional information about the time zone stored as an offset of 120 minutes from UTC (i.e. +02 hours). If you for example, would like to understand what the time was in New York when these weather observations were recorded, you could convert the time information with `.dt.tz_convert()` function: 

```python
data["TIME_TZ"].dt.tz_convert("US/Eastern")
```

Now we can see, that the timestamps were converted to represent the times in US/Eastern time zone. It's good to notice, that for example the first observation in our data that was recorded at 6 AM 1st of January in 1906 was correctly converted to a value from the last day of previous year at 11 PM (`1905-12-31 23:00`). This functionality can be very useful when working with temporal data from different parts of the world. Quite often the data collected from different global services (such as tweets collected from Twitter) store the information as UTC0 values. Hence, it is up to the user to parse the correct local time for tweets posted in different parts of the world. Using pandas for doing these kind of manipulation with the temporal data is extremely handy and efficient.    


## Selecting data based on DateTimeIndex

Add materials.


## Resampling, shifting and calculating rolling statistics

Add materials.


## Exercises

Add exercises.


## Footnotes

[^isostandard]: <https://en.wikipedia.org/wiki/ISO_8601>
