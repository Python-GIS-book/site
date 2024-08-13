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

# Exercises


### Exercise 3.1

In this exercise your task is to open and explore a NOAA weather data file using Pandas. The data file name is 6153237444115dat.csv and it is located in the data folder (*add link*). An overview of the tasks in this exercise:

- Import the Pandas module
- Read the data using Pandas into a variable called data
- Calculate a number of basic statistics from the data

#### Problem 1 - Read the file and clean it

Import the pandas module and read the weather data into a variable called `data`. Print the first five rows of the data file.

#### Problem 2 - Basic characteristics of the data

Based on the `data` DataFrame from Problem 1, answer to following questions:

1. How many rows is there in the data?
2. What are the column names?
3. What are the datatypes of the columns?

#### Problem 3 - Descriptive statistics

Based on the `data` DataFrame from Problem 1, answer to following questions:

- What is the mean Fahrenheit temperature in the data (use the `TEMP` column)?
- What is the standard deviation of the Maximum temperature (use the `MAX` column)?
- How many unique stations exists in the data (use the `USAF` column)?


### Exercise 3.2

In this exercise, you will clean the data from our data file by removing no-data values, convert temperature values in Fahrenheit to Celsius, and split the data into separate datasets using the weather station identification code. We will start this problem by cleaning and converting our temperature data. An overview of the tasks in this exercise:

- Create a new dataframe called `selected` that contains selected columns from the data file
- Clean the new DataFrame by removing no-data values
- Create a new column for temperatures converted from Fahrenheit to Celsius
- Divide the data into separate DataFrames for the Helsinki Kumpula and Rovaniemi stations
- Save the new DataFrames to CSV files

#### Problem 1 - Read the data and remove NaN values

The first step for this problem is to read the data file 6153237444115dat.csv into a variable `data` using pandas and cleaning it a bit:

- Select the columns `USAF, YR--MODAHRMN, TEMP, MAX, MIN` from the `data` DataFrame and assign them to a variable `selected`
- Remove all rows from `selected` that have NoData in the column `TEMP` using the `dropna()` function

#### Problem 2 - Convert temperatures to Celsius

Convert the temperature values from Fahrenheits to Celsius:

- Create a new column to `selected` called `Celsius`.
- Convert the Fahrenheit temperatures from `TEMP` using the conversion formula below and store the results in the new `Celsius` column:
   - TempCelsius = (TempFahrenheit - 32) / 1.8
- Round the values in the `Celsius` column to have 0 decimals (do not create a new column, update the current one)
- Convert the `Celsius` values into integers (do not create a new column, update the current one)

#### Problem 3 - Select data and save to disk

Divide the data in `selected` into two separate DataFrames:

- Select all rows from the selected DataFrame with the `USAF` code `29980` into a variable called `kumpula`.
- Select all rows from the selected DataFrame with the `USAF` code `28450` into a variable called `rovaniemi`.
- Save the `kumpula` DataFrame into a file `Kumpula_temps_May_Aug_2017.csv` in CSV format:
  - Separate the columns with commas (,)
  - Use only 2 decimals for the floating point numbers
- Repeat the same procedures and save the `rovaniemi` DataFrame into a file `Rovaniemi_temps_May_Aug_2017.csv`.


### Exercise 3.3

In this Exercise, we will explore our temperature data by comparing spring temperatures between Kumpula and Rovaniemi. To do this we'll use some conditions to extract subsets of our data and then analyse these subsets using basic pandas functions. Notice that in this exercise, we will use data saved from the previous Exercise (2.2.6), hence you should finish that Exercise before this one. An overview of the tasks in this exercise:

- Calculate the median temperatures for Kumpula and Rovaniemi for the summer of 2017
- Select temperatures for May and June 2017 in separate DataFrames for each location
- Calculate descriptive statistics for each month (May, June) and location (Kumpula, Rovaniemi)

#### Problem 1 - Read the data and calculate basic statistics

Read in the CSV files generated in Exercise 2.2.6 to the variables `kumpula` and `rovaniemi` and answer to following questions:

- What was the median Celsius temperature during the observed period in Helsinki Kumpula? Store the answer in a variable `kumpula_median`.
- What was the median Celsius temperature during the observed period in Rovaniemi? Store the answer in a variable `rovaniemi_median`.

#### Problem 2 - Select data and compare temperatures between months

The median temperatures above consider data from the entire summer (May-Aug), hence the differences might not be so clear. Let's now find out the mean temperatures from May and June 2017 in Kumpula and Rovaniemi:

- From the `kumpula` and `rovaniemi` DataFrames, select the rows where values of the `YR--MODAHRMN` column are from May 2017. Assign these selected rows into the variables `kumpula_may` and `rovaniemi_may` 
- Repeat the procedure for the month of June and assign those values into variables to `kumpula_june` and `rovaniemi_june`
- Calculate and print the mean, min and max Celsius temperatures for both places in May and June using the new subset dataframes (kumpula_may, rovaniemi_may, kumpula_june, and rovaniemi_june). Answer to following questions:
    - Does there seem to be a large difference in temperatures between the months?
    - Is Rovaniemi a much colder place than Kumpula?

#### Problem 3 - Parse daily temperatures by aggregating data 

In this problem, the aim is to aggregate the hourly temperature data for Kumpula and Rovaniemi weather stations to a daily level. Currently, there are at most three measurements per hour in the data, as you can see from the YR--MODAHRMN column:

```
    USAF  YR--MODAHRMN  TEMP  MAX  MIN  Celsius
0  28450  201705010000  31.0  NaN  NaN       -1
1  28450  201705010020  30.0  NaN  NaN       -1
2  28450  201705010050  30.0  NaN  NaN       -1
3  28450  201705010100  31.0  NaN  NaN       -1
4  28450  201705010120  30.0  NaN  NaN       -1
```

In this problem you should:

- Summarize the information for each day by aggregating (grouping) the DataFrame using the `groupby()` function.
- The output should be a new DataFrame where you have calculated mean, max and min Celsius temperatures for each day separately based on hourly values.
- Repeat the task for the two data sets you created in Problem 2 (May-August temperatures from Rovaniemi and Kumpula).
