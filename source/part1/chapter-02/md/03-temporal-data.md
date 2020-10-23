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

## TODO: READ IN SOME SAMPLE DATA

if we have datetimes as a separate section.


## Datetime 

In pandas, we can convert dates and times into a new data type [datetime](https://docs.python.org/3.7/library/datetime.html) using [pandas.to_datetime](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html) function.

```python
# Convert character strings to datetime
data['DATE'] = pd.to_datetime(data['TIME_STR'])
```

```python
# Check the output
data['DATE'].head()
```

```{admonition} Pandas Series datetime properties
There are several methods available for accessing information about the properties of datetime values. Read more from the pandas documentation about [datetime properties](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#datetime-properties).
```


Now, we can extract different time units based on the datetime-column using the [pandas.Series.dt](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html) accessor:

```python
data['DATE'].dt.year
```

```python
data['DATE'].dt.month
```

We can also combine the datetime functionalities with other methods from pandas. For example, we can check the number of unique years in our input data: 

```python
data['DATE'].dt.year.nunique()
```

For the final analysis, we need combined information of the year and month. One way to achieve this is to use the  `format` parameter to define the output datetime format according to [strftime(format)](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) method:

```python
# Convert to datetime and keep only year and month
data['YEAR_MONTH_DT'] = pd.to_datetime(data['TIME_STR'], format='%Y%m', exact=False)
```

`exact=False` finds the characters matching the specified format and drops out the rest (days, hours and minutes are excluded in the output).

```python
data['YEAR_MONTH_DT']
```

Now we have a unique label for each month as a datetime object.
