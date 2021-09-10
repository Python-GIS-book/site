---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Basic plotting with pandas and matplotlib


As we're now familiar with some of the features of pandas, we will wade into visualizing our data in Python using the built-in plotting options available directly in pandas. Much like the case of pandas being built upon numpy, plotting in pandas takes advantage of plotting features from the `matplotlib` [^matplotlib] plotting library. Plotting in pandas provides a basic framework for visualizing our data, but as you'll see we will sometimes need to also use features from matplotlib to enhance our plots. In particular, we will use features from the the `pyplot` [^pyplot] module in matplotlib, which provides MATLAB-like plotting. We will also briefly explore creating interactive plots using the `pandas-bokeh` [^pandas_bokeh] plotting backend, which allows us to produce plots similar to those available in the `bokeh` plotting library [^bokeh] using plotting syntax similar to that used normally in pandas.


## Basic x-y plot

Let's start by importing pandas and reading our data file. We will be using a datetime index for our weather observations as we learned in the previous chapter. In this case, however, we'll include a few additional parameters in order to read the data with a *datetime index*. Let's read the data first, then see what happened:

```python
import pandas as pd
fp = 'data/029740.txt'

data = pd.read_csv(fp, delim_whitespace=True, 
                   na_values=['*', '**', '***', '****', '*****', '******'],
                   usecols=['YR--MODAHRMN', 'TEMP', 'MAX', 'MIN'],
                   parse_dates=['YR--MODAHRMN'], index_col='YR--MODAHRMN')
```

So what's different here? Well, we have added two new parameters: `parse_dates` and `index_col`.

- `parse_dates` takes a Python list of column name(s) containing date data that pandas will parse and convert to the *datetime* data type. For many common date formats this parameter will automatically recognize and convert the date data.
- `index_col` is used to state a column that should be used to index the data in the DataFrame. In this case, we end up with our date data as the DataFrame index. This is a very useful feature in pandas as we'll see below.

Having read in the data, let's have a quick look at what we have using `data.head()`.

```python
data.head()
```

As mentioned above, you can now see that the index column for our DataFrame (the first column) contains date values related to each row in the DataFrame. Now we're ready for our first plot. We can start by using the basic line plot in pandas to look at our temperature data.

```python
ax = data.plot()
```

OK, so what happened here? 1) We first created the plot object using the `plot()` method of the `data` DataFrame. Without any parameters given, this makes the plot of all columns in the DataFrame as lines of different color on the y-axis with the index, time in this case, on the x-axis. 2) In case we want to be able to modify the plot or add anything, we assign the plot object to the variable `ax`. We can check its type below. In fact, let's check the type of the `ax` variable:

```python
type(ax)
```

OK, so it looks like we have some kind of plot data type that is part of matplotlib. Clearly, pandas is using matplotlib for generating our plots.

### Selecting data for plotting based on date

Now, let's make a few small changes to our plot and plot the data again. First, let's only plot the observed temperatures in the `data['TEMP']` column, and let's restrict ourselves to observations from the afternoon of October 1, 2019 (the last day in our dataset). We can do this by selecting the desired data column and date range first, then plotting our selection.

```python
oct1_temps = data['TEMP'].loc[data.index >= '201910011200']
ax = oct1_temps.plot()
```

So, what did we change? 1) We selected only the `'TEMP'` column now by using `data['TEMP']` instead of `data`. 2) We've added a restriction to the date range using `loc[]` to select only rows where the index value `data.index` is greater than `'201910011200'`. In that case, the number in the string is in the format `'YYYYMMDDHHMM'`, where `YYYY` is the year, `MM` is the month, `DD` is the day, `HH` is the hour, and `MM` is the minute. Now we have all observations from noon onward on October 1, 2019. 3) By saving this selection to the DataFrame `oct1_temps` we're able to now use `oct1_temps.plot()` to plot only our selection. This is cool, but we can do even better.


## Basic plot formatting

We can make our plot look a bit nicer and provide more information by using a few additional plotting options to pandas/matplotlib:

```python
ax = oct1_temps.plot(style='ro--', title='Helsinki-Vantaa temperatures')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature [°F]')
```

Now we see our temperature data as a red dashed line with circles showing the data points. This comes from the additional `style='ro--'` used with `oct1_temps.plot()`. In this case, `r` tells the `oct1_temps.plot()` function to use red color for the lines and symbols, `o` tells it to show circles at the points, and `--` says to use a dashed line. You can use `help(oct1_temps.plot)` to find out more about formatting plots. We have also added a title using the `title` parameter, but note that axis labels are assigned using the `set_xlabel()` and `set_ylabel()` methods. 


## Formatting the appearance of the figure

While the plot sizes we're working with are OK, it would be nice to have them displayed a bit larger. Fortunately, there is an easy way to make the plots larger in Jupyter notebooks. First, we need to import the `matplotlib pyplot library` [^pyplot], then we can make the default plot size larger by running the Python cell below.

```python
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 6]
```

The cell above sets the default plot size to be 12 inches wide by 6 inches tall. Adding text to plots can be done using `ax.text()`:

```python
import datetime
ax = oct1_temps.plot(style='ro--', title='Helsinki-Vantaa temperatures')
x, y = '201910011400', 38
ax.text(x, y, 'This is my text.')
```

No we added "This is my text" at the location of *x*, *y* on the plot. Notice that we passed the `x` coordinate as a text following the formatting in the original data. It is also possible to to change the axis ranges. Changing the plot axes can be done using the `xlim` and `ylim` parameters of the `plot()` function, where the `xmin` should be the minimum bound of the x-axis, and the `xmax` should be the maximum bound, and the same goes for the y-axis with `ymin` and `ymax`. Next, we will take advantage of the `datetime` library to determine the time range for the x-axis, as it is easier to read and understand than having a long text:

```python
from datetime import datetime

xmin, xmax = datetime(2019, 10, 1, 15), datetime(2019, 10, 1, 22) 
ymin, ymax = 38, 44
oct1_temps.plot(xlim=[xmin, xmax], ylim=[ymin, ymax])
```

As we can see, now we "zoomed" our plot based on the x and y axis-ranges that we defined. Notice that the underlying data did not disappear anywhere, we just specified which parts of the plot we want to show in the figure. 


## Dealing with datetime axes

One issue we will encounter with both placing text on the plot and changing the axis ranges is our datetime index for our DataFrame. In order to do either thing, we need to define x-values using a datetime object. The easiest way to do this is to use the pandas `pd.to_datetime()` function, which converts a character string date to a datetime object. For example, we can convert 13:00 on October 1, 2019 from the character string `'201910011300'` to a datetime equivalent by typing

```python
pd.to_datetime('201910011300')
```

With this datetime issue in mind, let's now consider a modified version of the plot above, we can

1. Limit our time range to 12:00 to 15:00 on October 1, 2019
2. Only look at temperatures between 40-46° Fahrenheit
3. Add text to note the coldest part of the early afternoon.

```python
start_time = pd.to_datetime('201910011200')
end_time = pd.to_datetime('201910011500')
cold_time = pd.to_datetime('201910011205')

ax = oct1_temps.plot(style='ro--', title='Helsinki-Vantaa temperatures',
                     xlim=[start_time, end_time], ylim=[40.0, 46.0])
ax.set_xlabel('Date')
ax.set_ylabel('Temperature [°F]')
ax.text(cold_time, 42.0, '<- Coldest temperature in early afternoon')
```

**Check your understanding (online)**

Create a line plot similar to our examples above with the following attributes:
    
- Temperature data from 18:00-24:00 on October 1, 2019
- A dotted black line connecting the observations (do not show the data points)
- A title that reads "Evening temperatures on October 1, Helsinki-Vantaa"
- A text label indicating the warmest temperature in the evening

```python
# Define start, end, and cold times

```

## Bar plots in pandas

In addition to line plots, there are many other options for plotting in pandas.
Bar plots are one option, which can be used quite similarly to line plots with the addition of the `kind=bar` parameter.
Note that it is easiest to plot our selected time range for a bar plot by selecting the dates in our data series first, rather than adjusting the plot limits. Pandas sees bar plot data as categorical, so the date range is more difficult to define for x-axis limits. For the y-axis, we can still define its range using the `ylim=[ymin, ymax]` parameter. Similarly, text placement on a bar plot is more difficult, and most easily done using the index value of the bar where the text should be placed.

```python
oct1_afternoon = oct1_temps.loc[oct1_temps.index <= '201910011500']
ax = oct1_afternoon.plot(kind='bar', title='Helsinki-Vantaa temperatures',
                         ylim=[40, 46])
ax.set_xlabel('Date')
ax.set_ylabel('Temperature [°F]')
ax.text(0, 42.1, 'Coldest \ntemp \nv')
```

You can find more about how to format bar charts on the [pandas documentation website](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.bar.html).


## Saving your plots as image files

Saving plots created using pandas can be done in several ways.
The recommendation for use outside of Jupyter notebooks is to use Matplotlib's `plt.savefig()` function.
When using `plt.savefig()`, you simply give a list of commands to generate a plot and include `plt.savefig()` with some parameters as the last command in the Python cell.
The file name is required, and the image format will be determined based on the listed file extension.

Matplotlib plots can be saved in a number of useful file formats, including PNG, PDF, and EPS.
PNG is a nice format for raster images, and EPS is probably easiest to use for vector graphics.
Let's check out an example and save our lovely bar plot.

```python
ax = oct1_afternoon.plot(kind='bar', title='Helsinki-Vantaa temperatures',
                         ylim=[40, 46])
ax.set_xlabel('Date')
ax.set_ylabel('Temperature [°F]')
ax.text(0, 42.1, 'Coldest \ntemp \nv')

plt.savefig('bar-plot.png')
```

If you refresh your **Files** tab on the left side of the JupyterLab window you should now see `bar-plot.png` listed.
We could try to save another version in higher resolution with a minor change to our plot commands above.

```python
ax = oct1_afternoon.plot(kind='bar', title='Helsinki-Vantaa temperatures',
                         ylim=[40, 46])
ax.set_xlabel('Date')
ax.set_ylabel('Temperature [°F]')
ax.text(0, 42.1, 'Coldest \ntemp \nv')

plt.savefig('bar-plot-hi-res.pdf', dpi=600)
```

## Interactive plotting with pandas-bokeh

When using Jupyter Notebooks, we don't need to stick to static visualizations. We can easily create plots that are interactive, allowing us to view data values by mousing over them, or click to enable/disable plotting of some data. There are several ways we can do this, but we'll utilize the [pandas-bokeh plotting backend](https://github.com/PatrikHlobil/Pandas-Bokeh) [^pandas_bokeh], which allows us to create interactive plots with little additional effort.

To get started, we need to import pandas-bokeh and make some configurations:

1. We want to change the settings so that output will be displayed on this page rather than in a separate window
2. we set pandas plotting backend to use pandas-bokeh rather than matplotlib for plotting

```python
import pandas_bokeh

pandas_bokeh.output_notebook()
pd.set_option('plotting.backend', 'pandas_bokeh')
```

Now, we can consider an example plot similar to the one we started with, but with data for three days (September 29-October 1, 2019). Pandas-bokeh expects a DataFrame as the source for the plot data, so we'll need to create a time slice of the `data` DataFrame containing the desired date range before making the plot. Let's generate the pandas-bokeh plot and the see what is different.

```python
sept29_oct1_df = data.loc[data.index >= '201909290000']

start_time = pd.to_datetime('201909290000')
end_time = pd.to_datetime('201910020000')

ax = sept29_oct1_df.plot(title='Helsinki-Vantaa temperatures',
                         xlabel='Date', ylabel='Temperature [°F]',
                         xlim=[start_time, end_time], ylim=[35.0, 60.0])
```

So now we have a similar plot to those generated previously, but when you move the mouse along the curve you can see the temperature values at each time. We can also hide any of the lines by clicking on them in the legend, as well as use the scroll wheel/trackpad to zoom.

But we did also have to make a few small changes to generate this plot:

1. We need to use a DataFrame as the data source for the plot, rather than a pandas Series. Thus, `data['TEMP'].plot()` will not work with pandas-bokeh.
2. The x- and y-axis labels are specified using the `xlabel` and `ylabel` parameters, rather than using `ax.set_xlabel()` or `ax.set_ylabel()`.
3. The line color and plotting of points are not specified using the `style` keyword. Instead, the line colors could be specified using the `color` or `colormap` parameters. Plotting of the points is enabled using the `plot_data_points` parameter (see below). More information about formatting the lines can be found on the [pandas-bokeh website](https://github.com/PatrikHlobil/Pandas-Bokeh) [^pandas_bokeh].
4. We have not included a text label on the plot, as it may not be possible to do so with pandas-bokeh.

But otherwise, we are able to produce these cool interactive plots with minimal effort, and directly within our notebooks!

```python
ax = sept29_oct1_df.plot(title='Helsinki-Vantaa temperatures',
                         xlabel='Date', ylabel='Temperature [°F]',
                         xlim=[start_time, end_time], ylim=[35.0, 60.0],
                         plot_data_points=True)
```

## Exercises

Add exercises.


## Footnotes

[^matplotlib]: <https://matplotlib.org/>
[^pyplot]: <https://matplotlib.org/api/pyplot_api.html>
[^matlab]: <https://www.mathworks.com/products/matlab.html>
[^pandas_bokeh]: <https://github.com/PatrikHlobil/Pandas-Bokeh>
[^bokeh]: <https://docs.bokeh.org/en/latest/index.html>
