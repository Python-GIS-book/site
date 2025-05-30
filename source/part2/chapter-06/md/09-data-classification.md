---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Data classification


Data classification is a common task in geospatial data analysis that determines the assignment of values to distinct classes.
Classifying original values into categories may help simplify the data for further analysis or communicating the results. Data classification is central when visualizing geographic information to correctly represent the distribution of the data. 

Here, we will get familiar with classification schemes from the [PySAL](https://pysal.org/) [^pysal] [`mapclassify` library](https://pysal.org/mapclassify/) [^mapclassify] that is intended to be used when visualizing thematic maps. Further details of geographic data visualization will be covered in chapter 8. We will also learn how to classify data values based on pre-defined threshold values and conditional statements directly in `geopandas`. 

Our sample data is an extract from the  Helsinki Region Travel Time Matrix ({cite}`Tenkanen2020`) that represents travel times to the central railway station across 250 m x 250 m statistical grid squares covering the Helsinki region. Let's read in the data and check the first rows of data: 

```python
from pathlib import Path
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

data_dir = Path("data")
grid_fp = data_dir / "Helsinki" / "TravelTimes_to_5975375_RailwayStation.shp"

# Read files
grid = gpd.read_file(grid_fp)
grid.head()
```

Detailed column descriptions are available in Table 3, {cite}`Tenkanen2020`. We will use column `'pt_r_t'` which contains information about travel time in minutes to the central railway station by public transportation in rush hour traffic. Missing data are presented with value -1. Let's set the missing values as `NaN` to exclude no data from further analysis:

```python
grid = grid.replace(-1, np.nan)
```

## Classification schemes

We will now learn how to use `mapclassify`to assing the data vaules into distinct classes. `Mapclassify` allows applying various classification schemes on our data that partition the attribute values into mutually exclusive groups. Choosing an adequate classification scheme and number of classes depends on the message we want to convey with our map and the underlying distribution of the data. Available classification schemes include: 

- box_plot
- equal_interval
- fisher_jenks
- fisher_jenks_sampled
- headtail_breaks
- jenks_caspall
- jenks_caspall_forced
- jenks_caspall_sampled
- max_p_classifier
- maximum_breaks
- natural_breaks
- quantiles
- percentiles
- std_mean
- user_defined
  
See {cite}`Rey_et_al_2023` for a thorough introduction on the mathematics behind each classification scheme. These classification schemes can be used directly when plotting data in `geopandas` as long as `mapclassify` package is also installed.



### Choosing a classification scheme

Let's have a look at the distribution of the public transport travel times through checking the histogram and descriptive statistics. A histogram is a graphic representation of the distribution of the data. Descriptive statistics summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding `NaN` values. While looking at the histogram, remember that each observation is one 250 meter x 250 meter grid square in the Helsinki region and the histogram shows the distribution of travel times to the central railway station across the whole region. 

For exploring the different classification schemes, let's create a `pandas` `Series` without `NaN` values.

```python
# Creating a data Series withouth NaN values
travel_times = grid.loc[grid["pt_r_t"].notnull(), "pt_r_t"]
```



```python
# Plot a histogram
travel_times.plot.hist(bins=50, color="lightgray")
```

_**Figure 6.60**. Histogram of the travel time values. Data source: Tenkanen & Toivonen 2020._

```python
travel_times.describe()
```

The maximum travel time to the central railway station by public transport (including time for walking) is 181 minutes, i.e. over three hours. Most of the travel times range between 38 and 65 minutes with an average travel time of 53 minutes. Looking at the histogram (Figure 8.6), we can tell than only a handful of grid squares have more than two hour travel times to the central railway station. These grid squares are most likely located in rather inaccessible places in terms of public transport accessibility. 

Let's have a closer look at how these `mapclassify` classifiers work and try out different classification schemes for visualizing the public transport traveltimes. In the interactive version of this book, you can try out different numbers of classes and different classification schemes.


#### Natural breaks

First, let's try out natural breaks classifier that tries to split the values into natural clusters. The number of observations per bin may vary according to the distribution of the data.

```python jupyter={"outputs_hidden": false}
import mapclassify

mapclassify.NaturalBreaks(y=travel_times, k=10)
```

It's possible to extract the threshold values into an array:

```python jupyter={"outputs_hidden": false}
mapclassify.NaturalBreaks(y=travel_times, k=10).bins
```

We can further explore the classification on top of the histogram:

```python
import matplotlib.pyplot as plt

# Define classifier
classifier = mapclassify.NaturalBreaks(y=travel_times, k=10)

# Plot histogram for public transport rush hour travel time
grid["pt_r_t"].plot.hist(bins=50, color="lightgray", title="Natural Breaks")

# Add vertical lines for class breaks
for break_point in classifier.bins:
    plt.axvline(break_point, linestyle="dashed", linewidth=1)
```

_**Figure 6.61**. Histogram of the travel time values with natural breaks classification into 10 groups. Data source: Tenkanen & Toivonen 2020._


We can apply the classifier on our data and store the result in a new column.

```python
# Classify the data
grid["pt_r_t_nb"] = grid[["pt_r_t"]].apply(classifier)
grid["pt_r_t_nb"].head()
```

Finally, we can visualize our data using the classification scheme when plotting the data in `geopandas` through adding the `scheme` option, while the parameter `k` defines the number of classess to use. 

```python jupyter={"outputs_hidden": false}
# Plot the data using natural breaks
ax = grid.plot(
    figsize=(6, 4),
    column="pt_r_t",
    linewidth=0,
    scheme="natural_breaks",
    k=10,
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

_**Figure 6.62**. Travel times visualized using the natural breaks classification scheme. Data source: Tenkanen & Toivonen 2020._


#### Quantiles 

Next, let's explore the quantiles classification that splits the data so that each class has an equal number of observations. 

```python jupyter={"outputs_hidden": false}
mapclassify.Quantiles(y=travel_times, k=10)
```

Notice that the numerical range of the groups created using the quantiles classification scheme may vary greatly depending on the distribution of the data. In our example, some classes have more than 30 min interval, while others less than 10 minutes. The default number of classes is five (quintiles), but you can set the desired number of classes using the `k` parameter. In the interactive version of the book, you can try changing the number of classes and see what happens to the class intervals; more classes get added around the central peak of the histogram if increasing the number of classes.

```python
import matplotlib.pyplot as plt

# Define classifier
classifier = mapclassify.Quantiles(y=travel_times, k=10)

# Plot histogram for public transport rush hour travel time
grid["pt_r_t"].plot.hist(bins=50, color="lightgray", title="Quantiles")

# Add vertical lines for class breaks
for break_point in classifier.bins:
    plt.axvline(break_point, linestyle="dashed", linewidth=1)
```

_**Figure 6.63**. Histogram of the travel time values with Quantile classification into 10 groups. Data source: Tenkanen & Toivonen 2020._

If comparing the histograms of natural breaks and quantile classifications, we can observe that natural breaks might work better to display differences in the data values across the whole data range, while quantiles would help distinguishing differences around the central peak of the data distribution. However, neither of the classification schemes display differences in short, less than 25 minute travel times which might be important for making an informative map. Also, we might want to have round numbers for our class values to facilitate quick and intuitive interpretation. 

```python
# Plot the data using quantiles
ax = grid.plot(
    figsize=(6, 4),
    column="pt_r_t",
    linewidth=0,
    scheme="quantiles",
    k=10,
    legend=True,
    legend_kwds={"title": "Travel times (min)", "bbox_to_anchor": (1.4, 1)},
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```


_**Figure 6.64**. Static map of travel times visualized using the quantiles classification scheme. Data source: Tenkanen & Toivonen 2020._

```python
# Store the class index numbers
grid["pt_r_t_q10"] = grid[["pt_r_t"]].apply(classifier)
grid["pt_r_t_q10"].head()
```

The quantile classification allows us to extract, for example the best 10 % of all grid squares in terms of travel times to the central railway station. Now that we divided the data into quintiles, we can get the top 10 % of the data through extracting the first category of our classified values. 

```python
grid[grid["pt_r_t_q10"] == 0].explore()
```

<!-- #raw editable=true raw_mimetype="" slideshow={"slide_type": ""} tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 6.65}. Top 10 % out of all statistical grid squares in the Helsinki Region in terms of public transport travel times to the Helsinki.}}, center, nofloat}{../img/figure_6-65.png}
{ \hspace*{\fill} \\}
<!-- #endraw -->

_**Figure 6.65**. Top 10 % out of all statistical grid squares in the Helsinki Region in terms of public transport travel times to the Helsinki. Data source: Tenkanen & Toivonen 2020._


#### Pretty breaks

The pretty breaks classification shceme rounds the class break values and divides the range equally to create intervals that look nice and that are easy to read. This classification scheme might be tempting to use as it creates intuitive and visually appealing intervals. However, depending on the distribution of the data, the group sizes might vary greatly which might lead to misleading visualizations.

```python
mapclassify.PrettyBreaks(y=travel_times, k=10)
```

```python
import matplotlib.pyplot as plt

# Define classifier
classifier = mapclassify.PrettyBreaks(y=travel_times, k=10)

# Plot histogram for public transport rush hour travel time
grid["pt_r_t"].plot.hist(bins=50, color="lightgray", title="Pretty breaks")

# Add vertical lines for class breaks
for break_point in classifier.bins:
    plt.axvline(break_point, linestyle="dashed", linewidth=1)
```

_**Figure 6.66**. Histogram of the travel time values with 10 pretty breaks. Data source: Tenkanen & Toivonen 2020._

```python
# Plot the data using pretty breaks
ax = grid.plot(
    figsize=(6, 4),
    column="pt_r_t",
    linewidth=0,
    scheme="prettybreaks",
    k=10,
    legend=True,
    legend_kwds={"title": "Travel times (min)", "bbox_to_anchor": (1.4, 1)},
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

_**Figure 6.67**. Static map of travel times visualized using the pretty breaks classification scheme. Data source: Tenkanen & Toivonen 2020._

<!-- #region -->


Regardless of the number of classes, pretty breaks is not ideal for our data as it fails to capture the variation in the data. Compared to this map, the previous two versions using natural breaks and quantiles provide a more informative view of the travel times.
<!-- #endregion -->

### Custom map classification

In case none of the existing classification schemes produce a desired output, we can also create a custom classification scheme using `mapclassify` and select which class interval values to use. Fixed intervals with gradually increasing travel times provide an intuitive way to display travel time data. While the pretty breaks classification scheme follows this approach, it didn’t work perfectly for our data. With our own classification scheme, we can show differences among the typical travel times, but avoid having classes distinguishing between long travel times. We'll create a custom classifier with fixed 10-minute intervals up to 90 minutes to achieve this. 

```python editable=true slideshow={"slide_type": ""}
break_values = [10, 20, 30, 40, 50, 60, 70, 80, 90]
classifier = mapclassify.UserDefined(y=travel_times, bins=break_values)
classifier
```

```python
import matplotlib.pyplot as plt

# Define classifier
classifier = mapclassify.UserDefined(y=travel_times, bins=break_values)

# Plot histogram for public transport rush hour travel time
grid["pt_r_t"].plot.hist(bins=50, title="User defined classes", color="lightgray")

# Add vertical lines for class breaks
for break_point in classifier.bins:
    plt.axvline(break_point, linestyle="dashed", linewidth=1)
```

_**Figure 6.68**. Histogram of the travel time values with user defined class breaks. Data source: Tenkanen & Toivonen 2020._


When plotting the map, we can pass the break values using `classification_kwds`. 

```python
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

grid.plot(
    ax=ax,
    column="pt_r_t",
    linewidth=0,
    scheme="UserDefined",
    classification_kwds={"bins": break_values},
    legend=True,
    legend_kwds={"title": "Travel times (min)", "bbox_to_anchor": (1.4, 1)},
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

_**Figure 6.69**. Static map of travel times by car and public transport using a custom classification scheme. Data source: Tenkanen & Toivonen 2020._

<!-- #region editable=true slideshow={"slide_type": ""} -->
#### Question 6.14

Select another column from the data (for example, travel times by car: `car_r_t`) and visualize a thematic map using our custom classification scheme. 
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""}
# Solution

# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

# Visualize the travel times using a classification scheme and add a legend
grid.plot(
    ax=ax,
    column="car_r_t",
    linewidth=0,
    scheme="UserDefined",
    classification_kwds={"bins": break_values},
    legend=True,
    legend_kwds={"title": "Travel times (min)", "bbox_to_anchor": (1.4, 1)},
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

## Rule-based classification

Sometimes our analysis task benefits from combining multiple criteria for classifying data. For example, we might want to find out locations that are outside the city center within a reasonable public transport travel time. Such a selection could help us classify the statistical grid squares based on the potential for finding apartments with good public transport connections while avoiding the most expensive areas in the city center.

To implement this, we can use conditional statements to find grid squares where public transport travel time (column `pt_r_tt`) is less than a selected threshold value in minutes, and where walking distance (`walk_d`) is more than a selected threshold value in meters. Each rule will give a binary result (`True`/`False`) and we can further combine these rules to find those locations that meet both requirements.

```python editable=true slideshow={"slide_type": ""}
# Threhsold values
pt_maximum = 30
walk_minimum = 2500
```

```python
grid["pt_r_tt"] < pt_maximum
```

```python
grid["walk_d"] > walk_minimum
```

We can then use our `pandas` skills to combine these rules. Notice that you need parentheses around each set of condition.

```python editable=true slideshow={"slide_type": ""}
grid["rule1"] = (grid["pt_r_tt"] < pt_maximum) & (grid["walk_d"] > walk_minimum)
```

Finally, now that we have our rule-based classification stored in one of our `GeoDataFrame`columns, we can use this information to visualize the areas that meet our criteria:

```python editable=true slideshow={"slide_type": ""}
grid.loc[grid["rule1"] == True].explore()
```

<!-- #raw editable=true raw_mimetype="" slideshow={"slide_type": ""} tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 6.70}. Grid squares that meet the selection criteria.}}, center, nofloat}{../img/figure_6-70.png}
{ \hspace*{\fill} \\}
<!-- #endraw -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 6.70**. Grid squares that meet the selection criteria._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
#### Question 6.15

Change the threshold values above and see how the map changes!
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Footnotes

[^pysal]: <https://pysal.org/> 
[^mapclassify]: <https://pysal.org/mapclassify/>

<!-- #endregion -->
