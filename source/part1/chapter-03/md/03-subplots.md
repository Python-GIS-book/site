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

# Creating subplots

At this point you should know the basics of making plots with Matplotlib module.
Now we will expand on our basic plotting skills to learn how to create more advanced plots.
In this part, we will show how to visualize data using Pandas/Matplotlib and create plots such as the one below.

![Subplot example in Matplotlib](./../img/subplots.png)


## Preparing the data for plotting 

Let's start again by reading the data.

```python
import pandas as pd
import matplotlib.pyplot as plt

fp = "data/029740.txt"

data = pd.read_csv(fp, delim_whitespace=True, 
                   na_values=['*', '**', '***', '****', '*****', '******'],
                   usecols=['YR--MODAHRMN', 'TEMP', 'MAX', 'MIN'],
                   parse_dates=['YR--MODAHRMN'], index_col='YR--MODAHRMN')
```

Let's rename the `'TEMP'` column as `TEMP_F`, since we'll later convert our temperatures from Fahrenheit to Celsius:

```python
new_names = {'TEMP':'TEMP_F'}
data = data.rename(columns=new_names)
```

Check again the first rows of data to confirm successful renaming:

```python
data.head()
```

First, we have to deal with no data values. Let's check how many no data values we have:

```python
print('Number of no data values per column: ')
print(data.isna().sum())
```

So, we have 3579 missing values in the TEMP_F column. Let's get rid of those. We need not worry about the no data values in `'MAX'` and `'MIN'` columns since we won't be using them for plotting. We can remove rows from our DataFrame where `'TEMP_F'` is missing values using the `dropna()` method: 

```python
data.dropna(subset=['TEMP_F'], inplace=True)
print("Number of rows after removing no data values:", len(data))
```

**Check your understanding (online)**

What would happen if we removed all rows with any no data values from our data (also considering no data values in the `MAX` and `MIN` columns)?

```python
# After removing all no data values we are left with only a fraction of the original data.
# Note! Here we are not applying .dropna() "inplace" 
#       so we are not making any permanent changes to our dataframe.
len(data.dropna())
```

Now that we have loaded our data, we can convert the values of temperature in Fahrenheit to Celsius, like we have in earlier lessons.

```python
data["TEMP_C"] = (data["TEMP_F"] - 32.0) / 1.8
```

Let's check how our dataframe looks like at this point:

```python
data.head()
```

## Subplots

Let's continue working with the weather data and learn how to use *subplots*. Subplots are figures where you have multiple plots in different panels of the same figure, as was shown at the start of this section.


Let's now select data from different seasons of the year in 2012/2013:

- Winter (December 2012 - February 2013)
- Spring (March 2013 - May 2013)
- Summer (June 2013 - August 2013)
- Autumn (Septempber 2013 - November 2013)

```python
winter = data.loc[(data.index >= '201212010000') & (data.index < '201303010000')]
winter_temps = winter['TEMP_C']

spring = data.loc[(data.index >= '201303010000') & (data.index < '201306010000')]
spring_temps = spring['TEMP_C']

summer = data.loc[(data.index >= '201306010000') & (data.index < '201309010000')]
summer_temps = summer['TEMP_C']

autumn = data.loc[(data.index >= '201309010000') & (data.index < '201312010000')]
autumn_temps = autumn['TEMP_C']
```

Now we can plot our data to see how the different seasons look separately.

```python
ax1 = winter_temps.plot()
```

```python
ax2 = spring_temps.plot()
```

```python
ax3 = summer_temps.plot()
```

```python
ax4 = autumn_temps.plot()
```

OK, so from these plots we can already see that the temperatures in different seasons are quite different, which is rather obvious of course.
It is important to also notice that the scale of the *y*-axis changes in these different plots.
If we would like to compare different seasons to each other we need to make sure that the temperature scale is similar in the plots of the different seasons.

### Finding data bounds

Let's set our *y*-axis limits so that the upper limit is the maximum temperature + 5 degrees in our data (full year), and the lowest is the minimum temperature - 5 degrees.

```python
# Find lower limit for y-axis
min_temp = min(winter_temps.min(), spring_temps.min(), summer_temps.min(), autumn_temps.min())
min_temp = min_temp - 5.0

# Find upper limit for y-axis
max_temp = max(winter_temps.max(), spring_temps.max(), summer_temps.max(), autumn_temps.max())
max_temp = max_temp + 5.0

# Print y-axis min, max
print("Min:", min_temp, "Max:", max_temp)
```

We can now use this temperature range to standardize the y-axis scale of our plot.

### Visualizing multiple subplots in a single figure

Let's now continue and see how we can plot all these different plots into the same figure.
We can create a 2x2 panel for our visualization using Matplotlib’s `subplots()` function where we specify how many rows and columns we want to have in our figure.
We can also specify the size of our figure with `figsize()` parameter that takes the `width` and `height` values (in inches) as input.

```python
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,8));
axs
```

We can see that as a result we have now a list containing two nested lists where the first one contains the axis for column 1 and 2 on **row 1** and the second list contains the axis for columns 1 and 2 for **row 2**.

We can parse these axes into own variables so it is easier to work with them.

```python
ax11 = axs[0][0]
ax12 = axs[0][1]
ax21 = axs[1][0]
ax22 = axs[1][1]
```

Now we have four different axis variables for different panels in our figure.
Next we can use them to plot the seasonal data into them.
Let's first plot the seasons and give different colors for the lines, and specify the *y*-scale limits to be the same with all subplots.
- `c` parameter changes the color of the line.You can find an extensive list of possible colors and RGB-color codes from [this link](http://www.rapidtables.com/web/color/RGB_Color.htm).
- `lw` parameter controls the width of the line.
- `ylim` parameter controls the y-axis limits

```python
# Set plot line width
line_width = 1.5

# Plot data
winter_temps.plot(ax=ax11, c='blue', lw=line_width, ylim=[min_temp, max_temp])
spring_temps.plot(ax=ax12, c='orange', lw=line_width, ylim=[min_temp, max_temp])
summer_temps.plot(ax=ax21, c='green', lw=line_width, ylim=[min_temp, max_temp])
autumn_temps.plot(ax=ax22, c='brown', lw=line_width, ylim=[min_temp, max_temp])

# Display figure
fig
```

Great, now we have all the plots in same figure! However, we can see that there are some problems with our *x*-axis labels and a few missing items we can add. Let's do that below.

```python
# Create the new figure and subplots
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,8))

# Rename the axes for ease of use
ax11 = axs[0][0]
ax12 = axs[0][1]
ax21 = axs[1][0]
ax22 = axs[1][1]
```

Now, we'll add our seasonal temperatures to the plot commands for each time period.

```python
# Set plot line width
line_width = 1.5

# Plot data
winter_temps.plot(ax=ax11, c='blue', lw=line_width, 
                  ylim=[min_temp, max_temp], grid=True)
spring_temps.plot(ax=ax12, c='orange', lw=line_width,
                  ylim=[min_temp, max_temp], grid=True)
summer_temps.plot(ax=ax21, c='green', lw=line_width,
                  ylim=[min_temp, max_temp], grid=True)
autumn_temps.plot(ax=ax22, c='brown', lw=line_width,
                  ylim=[min_temp, max_temp], grid=True)

# Set figure title
fig.suptitle('2012-2013 Seasonal temperature observations - Helsinki-Vantaa airport')

# Rotate the x-axis labels so they don't overlap
plt.setp(ax11.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax12.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax21.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax22.xaxis.get_majorticklabels(), rotation=20)

# Axis labels
ax21.set_xlabel('Date')
ax22.set_xlabel('Date')
ax11.set_ylabel('Temperature [°C]')
ax21.set_ylabel('Temperature [°C]')

# Season label text
ax11.text(pd.to_datetime('20130215'), -25, 'Winter')
ax12.text(pd.to_datetime('20130515'), -25, 'Spring')
ax21.text(pd.to_datetime('20130815'), -25, 'Summer')
ax22.text(pd.to_datetime('20131115'), -25, 'Autumn')

# Display plot
fig
```

Not bad.


**Check your understading (online)**

Visualize winter and summer temperatures in a 1x2 panel figure. Save the figure as a .png file.

```python
# Two subplots side-by-side:
```
