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


Finally, we can visualize our data using the classification scheme through adding the `scheme` option, while the parameter `k` defines the number of classess to use. Note that the syntax via `geopandas` differs a bit from `mapclassify`. 

```python jupyter={"outputs_hidden": false}
# Plot the data using natural breaks
ax = grid.plot(
    figsize=(6, 4),
    column="pt_r_t",
    linewidth=0,
    scheme="Natural_Breaks",
    k=9,
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

_**Figure 6.62**. Static map of travel times visualized using the natural breaks classification scheme. Data source: Tenkanen & Toivonen 2020._

In comparison to the previous maps, the differences in travel times are now more pronounced highlighting lower travel times near the central railway station. Notice also that we now have a different type of map legend that shows the associated class bins, now that we used a classification scheme. Here, we set the title and location of the legend using `legend_kwds` at the same time when plotting the map. We use `bbox_to_anchor` to position the legend item so that it does not overlap and cover our map extent.  An alternative way to achieve the same thing would be to add `ax.get_legend().set_bbox_to_anchor((1.4, 1))` after plotting the data via `geopandas`. For further tips on customizing choropleth map legends, have a look at [`geopandas examples gallery`](https://geopandas.org/en/stable/gallery/choro_legends.html) [^geopandas_choro_legends].


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

_**Figure 6.65**. Histogram of the travel time values with 10 pretty breaks. Data source: Tenkanen & Toivonen 2020._

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

_**Figure 6.66**. Static map of travel times visualized using the pretty breaks classification scheme. Data source: Tenkanen & Toivonen 2020._

<!-- #region -->


Regardless of the number of classes, pretty breaks is not ideal for our data as it fails to capture the variation in the data. Compared to this map, the previous two versions using natural breaks and quantiles provide a more informative view of the travel times.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 6.14

Select another column from the data (for example, travel times by car: `car_r_t`) and visualize a thematic map using one of the available classification schemes.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

# Visualize the travel times using a classification scheme and add a legend
grid.plot(
    ax=ax,
    column="car_r_t",
    linewidth=0,
    scheme="FisherJenks",
    k=9,
    legend=True,
    legend_kwds={"title": "Travel times (min)", "bbox_to_anchor": (1.4, 1)},
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

### Custom map classification

In case none of the existing classification schemes produce a desired output, we can also create a custom classification scheme using `mapclassify` and select which class interval values to use. Fixed intervals with gradually increasing travel times provide an intuitive way to display travel time data. While the pretty breaks classification scheme follows this approach, it didn’t work perfectly for our data. With our own classification scheme, we can show differences among the typical travel times, but avoid having classes distinguishing between long travel times. We'll create a custom classifier with fixed 10-minute intervals up to 90 minutes to achieve this. 

```python
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

_**Figure 6.67**. Histogram of the travel time values with user defined class breaks. Data source: Tenkanen & Toivonen 2020._


When plotting the map, we can pass the break values using `classification_kwds`. For a final touch, we can plot two subplots side by side displaying travel times by different modes of transport using our custom classifier. 

We can plot only one legend, as the two maps use an identical classification. We can add interval brackets on our legend to denote open and closed intervals. An open interval is denoted with parentheses and it does not inlcude the endpoint values. A closed interval is denoted with square brackets and it includes both endpoints. Most of the intervals in our classificaion scheme are half-open (for example, `(10, 20]`) so that the lower bound is not included in the interval, but the upper bound is. 

```python
# Create one subplot. Control figure size in here.
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

# Visualize the travel times into 9 classes using "Quantiles" classification scheme
grid.plot(
    ax=axs[0],
    column="car_r_t",
    linewidth=0,
    scheme="UserDefined",
    classification_kwds={"bins": break_values},
)

grid.plot(
    ax=axs[1],
    column="pt_r_t",
    linewidth=0,
    scheme="UserDefined",
    classification_kwds={"bins": break_values},
    legend=True,
    legend_kwds={
        "title": "Travel times (min)",
        "bbox_to_anchor": (1.4, 1),
        "interval": True,
        "frameon": False,
    },
    label="Travel times by public transport",
)

axs[0].set_title("Travel times by car")
axs[1].set_title("Travel times by public transport")

# Set the x and y axis off and adjust padding around the subplot
axs[0].axis("off")
axs[1].axis("off")

plt.tight_layout()
```

_**Figure 6.68**. Static map of travel times by car and public transport using a custom classification scheme. Data source: Tenkanen & Toivonen 2020._


## Rule-based classification

Sometimes our analysis task benefits from combining multiple criteria for classifying data. For example, we might want to find out locations that are located outside the city center within a reasonable public transport travel time.

To implement this, we can use conditional statements to find grid squares where public transport travel time (column `pt_r_tt`) is less than a selected threshold value in minutes, and where walking distance (`walk_d`) is more than a selected threshold value in meters. Each rule will give a binary result (`True`/`False`) and we can further combine these rules to find those locations that meet both requirements.

```python
# Public transport travel time less than 20 minutes
grid["pt_r_tt"] < 20
```

```python
# Walking distance more than 4000 meters.
grid["walk_d"] > 4000
```

We can then use our `pandas` skills to combine these rules. Notice that you need parentheses around each set of condition.

```python
grid["rule1"] = (grid["pt_r_tt"] < 30) & (grid["walk_d"] > 4000)
```

```python
grid.loc[grid["rule1"]==True].explore()
```

_**Figure 6.68**. Grid squares that meet the selection criteria._


## Footnotes
[^geopandas_mappingtools]: <https://geopandas.org/en/stable/docs/user_guide/mapping.html> 
[^matplotlib_pyplot]: <https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html> 
[^contextily]: <https://github.com/darribas/contextily>
[^HSL_opendata]: <https://www.avoindata.fi/data/en_GB/dataset/hsl-n-linjat>
[^matplotlib_colormaps]: <https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html#choosing-colormaps-in-matplotlib>
[^matplotlib_colors]: <https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.colors>
[^matplotlib_colorbar]: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html>
[^matplotlib_legend]: <https://matplotlib.org/tutorials/intermediate/legend_guide.html>
[^geopandas_scalebar_examples] <https://geopandas.org/en/stable/gallery/matplotlib_scalebar.html#Adding-a-scale-bar-to-a-matplotlib-plot>
[^pysal]: <https://pysal.org/> 
[^mapclassify]: <https://pysal.org/mapclassify/>
[^geopandas_choro_legends]: <https://geopandas.org/en/stable/gallery/choro_legends.html>
