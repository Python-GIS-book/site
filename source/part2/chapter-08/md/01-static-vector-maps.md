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

# Static maps


Static visualizations of geographic information are useful for many purposes during a data analysis process and for communicating the end result. Static maps can be exported to various image formats and integrated, for example, in reports and scientific articles. In this section, we will practice plotting static maps using sample data from Helsinki, Finland. 

[Mapping tools in `geopandas`](https://geopandas.org/en/stable/docs/user_guide/mapping.html) [^geopandas_mappingtools] allow creating simple static maps easily. In the background, `geopandas` uses `matplotlib` for creating the plots and we can use [`matplotlib.pyplot`](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html) [^matplotlib_pyplot] tools for further customizing our figures. We covered basic `matplotlib` plotting techniques already in Part I chapter 4 and will apply some of them for plotting our static maps. Additionally, we will explore how to enhance our maps by adding basemaps with `contextily`.

## Creating a simple multi-layer map

We will visualize information about travel times across the region from the Helsinki Region Travel Time Matrix dataset ({cite}`Tenkanen2020`). 
We will also incorporate [transport network data from Helsinki Region Transport](https://www.avoindata.fi/data/en_GB/dataset/hsl-n-linjat) [^HSL_opendata] to add spatial context. Let's start by importing the required modules and defining our data sources.

```python
from pathlib import Path
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

data_dir = Path("../data")
grid_fp = data_dir / "TravelTimes_to_5975375_RailwayStation.shp"
transport_fp = data_dir / "HSL%3An_linjat.zip"

# Read files
grid = gpd.read_file(grid_fp)
transport = gpd.read_file(transport_fp)

# Filtering out some useful transport features for our map
metro = transport.loc[transport["JL_LAJI"] == "06"]
train = transport.loc[transport["JL_LAJI"] == "12"]
```

The travel time data contains multiple columns with information about travel times and distances from each statistical grid square to the central railway station in Helsinki. 

```python
grid.columns
```

See Table 3 in {cite}`Tenkanen2020` for detailed description of each column. Here, we will use the column `'pt_r_t'` which contains information about travel time in minutes to the central railway station by public transportation in rush hour traffic. Missing data are presented with value -1. Let's set the missing values as `NaN` before proceeding:

```python
grid = grid.replace(-1, np.nan)
```

Now we can use `geopandas` for visualizing a simple map representing the rush hour public transport travel times (`'pt_r_t'`).
With the `column` parameter in the `plot()` method, we can specify the column which we want to visualize creating a color gradient of the  values:

```python
grid.plot(column="pt_r_t")
```

_**Figure 8.1**. Simple static map plotted using `geopandas`. The color gradient represents travel times by public transport to the central railway station in Helsinki, Finland from across the region. Data source: Tenkanen & Toivonen 2020._

What we have here is a `choropleth map` where the colors of each grid square polygon are based on values from the column `pt_r_t`. We will see later how to change the classification scheme that determines the assignment of values to each class for the visualization. 

### Re-projecting data (if needed)

The power of geographic information often relies on overlaying multiple features and exploring their spatial relations. Here, we can visualize the transport network data on top of the travel time information to add spatial context in our map. In order to plot multiple layers in the same figure, the first thing is to check the coordinate reference system (CRS) of each layer and check that they match:

```python jupyter={"outputs_hidden": false}
# Check the crs of each layer
print(grid.crs)
print(metro.crs)
print(train.crs)
```

All layers have a defined CRS, but we can see that the coordinate reference system definitions don't match, which is a problem for plotting our map. The grid is in ETRS89 / TM35FIN (EPSG:3067), which is an appropriate map projection for visualizing data from Finland. Roads and the metro are in WGS 84 (EPSG:4326) meaning that the coordinates are in latitudes and longitudes. Let's see what happens if trying to plot all three layers in the same figure without re-projecting the data:

```python
ax = grid.plot(column="pt_r_t")
train.plot(ax=ax)
metro.plot(ax=ax)
```

_**Figure 8.2**. Failed attempt to plot a static map with multiple layers._

We need to re-project the data in order to get the layers in the same coordinate space. Here, we can re-project the linear features (train and metro) from WGS 84 to ETRS89 / TM35FIN (EPSG:3067). While doing this, we can get the crs definition based on the grid layer ensuring that the crs definitions will be identical.

```python jupyter={"outputs_hidden": false}
# Reproject geometries to ETRS89 / TM35FIN based on the grid crs:
train = train.to_crs(crs=grid.crs)
metro = metro.to_crs(crs=grid.crs)
```

Now the layers should be in the same coordinate reference system:

```python jupyter={"outputs_hidden": false}
# Check the crs of each layer
print(grid.crs)
print(metro.crs)
print(train.crs)
```

Once the data are in the same projection, we can plot them on a map. First, we plot one of the layers and store that plot object in the variable `ax` (referring to the subplot object) and use this for plotting the other layers in the same subplot:

```python
ax = grid.plot(column="pt_r_t")
train.plot(ax=ax)
metro.plot(ax=ax)
```

_**Figure 8.3**. Static map with multiple layers displaying the original data extent. Data source: Tenkanen & Toivonen 2020; Helsinki Region Transport 2024._

### Customizing our map
Now our layers are nicely aligned, but the map needs some further improvement. Some map elements such as color and linewidth are still easy to configure directly via `geopandas`, but we need `matplotlib.pyplot` for controlling other features related to the layout. Let's apply the following changes to our plot: 

- Changing the colors of the choropleth map using the `cmap` parameter. See available [colormap options from matplotlib documentation](https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html#choosing-colormaps-in-matplotlib) [^matplotlib_colormaps].
- Changing line colors using the `color` parameter. See [color options from matplotlib pyplot documentation](https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.colors) [^matplotlib_colors].
- Changing the `linewidth` of line features.
- Adding transparency using the `alpha` parameter (this parameter ranges from 0 to 1 where 0 is fully transparent).
- Cropping the figure by adjusting the view limit of each axis. We can get the desired plot extent from the `total_bounds` of the grid layer. This way we don't need to separately crop the train line that goes outside the extent of the grid data.
- Using a `tight_layout`to adjust the subplot to fit in the figure area via `matplotlib`.
- Removing the frame and and axis labels through setting x- and y- axis on or off via `matplotlib`.

Finally, we can save the figure as PNG image.

```python
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

# Visualize the travel times
grid.plot(ax=ax, 
          column="car_r_t", 
          cmap="Spectral"
          )

# Add roads and change the color, linewidth and and transparency
train.plot(ax=ax, color="grey", linewidth=1, alpha=0.1)

# Add metro and change the color, linewidth and and transparency
metro.plot(ax=ax, color="red", linewidth=2, alpha=0.1)

# Set axis view limits based on the total bounds of the grid layer
ax.set_xlim(grid.total_bounds[0], grid.total_bounds[2])
ax.set_ylim(grid.total_bounds[1], grid.total_bounds[3])

# Set the x and y axis off 
plt.axis("off")

# Adjust padding around the subplot
plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = "static_map.png"
plt.savefig(outfp, dpi=300)
```

_**Figure 8.4**. Static map with multiple layers with adjusted extent and colors. Data source: Tenkanen & Toivonen 2020; Helsinki Region Transport 2024._


## Adding a legend


Our map is currently lacking information about the values being presented. We can add a map legend directly when plotting the `GeoDataFrame` through setting `legend=True`.  Additional keywords can be added through `legend_kwds`. For additional options, have a look at [`geopandas` mapping tools](https://geopandas.org/en/stable/docs/user_guide/mapping.html) [^geopandas_mappingtools] and [`matplotlib` legend guide](https://matplotlib.org/tutorials/intermediate/legend_guide.html) [^matplotlib_legend].

```python
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

# Visualize the travel times
grid.plot(ax=ax, 
          column="car_r_t", 
          cmap="Spectral",
          legend=True,
          legend_kwds={"label": "Travel times by public transport (min)"},
          )

# Set axis view limits based on the total bounds of the grid layer
ax.set_xlim(grid.total_bounds[0], grid.total_bounds[2])
ax.set_ylim(grid.total_bounds[1], grid.total_bounds[3])

# Set the x and y axis off 
plt.axis("off")

# Adjust padding around the subplot
plt.tight_layout()
```

_**Figure 8.5**. Static map with multiple layers and a scale bar. Data source: Tenkanen & Toivonen 2020; Helsinki Region Transport 2024._

Here, our legend is a [colorbar object](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html) [^matplotlib_colorbar] and the legend keyword arguments will control how the colorbar looks. Next, we will see how we can further control the way in which the travel time values and the associated scalebar are displayed using classification schemes.


## Classification schemes

With choropleth maps, it is essential to pay attention to the classification scheme that is used to display the values. We will now learn how to use classification schemes from the [PySAL](https://pysal.org/) [mapclassify library](https://pysal.org/mapclassify/) [^mapclassify] to classify quantitative data into multiple classes for visualization purposes. These classification schemes can be used directly when plotting data in `geopandas` as long as `mapclassify` package is also installed.  Available classification schemes include: 

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
  
Each classification scheme partitions the data into mutually exclusive groups that define how the values are displayed on the map. See {cite}`Rey_et_al_2023` for a thorough introduction on the mathematics behind each classification scheme. Choosing an adequate classification scheme and number of classes depends on the message we want to convey with our map and the underlying distribution of the data. 

### Explore the classifiers

For exploring the different classification schemes, let's create a `pandas` `Series` without `NaN` values.

```python
# Getting a data Series withouth NaN values
travel_times = grid.loc[grid["pt_r_t"].notnull(), "pt_r_t"]
```

When visualizing travel times we want our map to show regional differences in the travel times in an intuitive way while avoiding excess detail. We might want to, e.g., highlight more the differences in relatively short travel times versus very long travel times. Let's have a look at the distribution of the public transport travel times through checking the histogram and descriptive statistics. A histogram is a graphic representation of the distribution of the data. Descriptive statistics summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding `NaN` values. While looking at the histogram, remember that each observation is one 250 m x 250 m grid square in the Helsinki region and the histogram shows the distribution of travel times to the central railway station across the whole region. 

```python
travel_times.plot.hist(bins=50, color="lightgray")
```

_**Figure 8.6**. Histogram of the travel time values. Data source: Tenkanen & Toivonen 2020._

```python
travel_times.describe()
```

The maximum travel time to the central railway station by public transport (including time for walking) is 181 minutes, i.e. over three hours. Most of the travel times range between 38 and 65 minutes with an average travel time of 53 minutes. Looking at the histogram (Figure 8.5), we can tell than only a handful of grid squares have more than two hour travel times to the central railway station. These grid squares are most likely located in rather inaccessible places in terms of public transport accessibility. 

Let's have a closer look at how these `mapclassify` classifiers work and try out different classification schemes for visualizing the public transport traveltimes. In the interactive version of this book, you can try out different numbers of classes and different classification schemes.

```python
import mapclassify
```

#### Natural breaks

Natural Breaks tries to split the values into natural clusters. The number of observations per bin may vary according to the distribution of the data.

```python jupyter={"outputs_hidden": false}
mapclassify.NaturalBreaks(y=travel_times, k=6)
```

It's possible to extract the threshold values into an array:

```python jupyter={"outputs_hidden": false}
mapclassify.Quantiles(y=travel_times, k=9).bins
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
    plt.axvline(break_point,  linestyle="dashed", linewidth=1)
```

_**Figure 8.7**. Histogram of the travel time values with natural breaks classification into 10 groups. Data source: Tenkanen & Toivonen 2020._


#### Quantiles 

Quantiles classification splits the data so that each class as an equal number of observations. 

```python jupyter={"outputs_hidden": false}
mapclassify.Quantiles(y=travel_times, k=5)
```

Notice that the numerical range of the groups created using the quantiles classification scheme may vary greatly depending on the distribution of the data. In our example, some classes have more than 30 min interval, while others less than 10 minutes. The default number of classes is five (quintiles), but you can set the desired number of classes using the `k` parameter. In the interactive version of the book, you can try increasing the number of classes and see what happens. 

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

<!-- #region -->
_**Figure 8.8**. Histogram of the travel time values with Quantile classification into 10 groups. Data source: Tenkanen & Toivonen 2020._

If comparing the histograms of natural breaks and quantile classifications, we can observe that natural breaks might work better to display differences in the data values across the whole data range, while quantiles would help distinguishing differences around the central peak of the data distribution. However, neither of the classification schemes display differences in short, less than 25 minute travel times which might be important for making an informative map. Also, we might want to have round numbers for our class values to facilitate quick and intuitive interpretation. 


#### Pretty breaks

The pretty breaks classification shceme rounds the class break values and divides the range equally to creat nice and pretty intervals.
<!-- #endregion -->

```python
mapclassify.PrettyBreaks(y=travel_times, k=8)
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

### Using the classification schemes via geopandas

We can continue exploring the available classification schemes on a map through adding the `scheme` option, while the parameter `k` defines the number of classess to use. Note that the syntax via `geopandas` differs a bit from `mapclassify`. We can control the position and title of the legend using `matplotlib` tools trough changing the properties of the legend object. It is easy to add a label for the legend using `legend_kwds`. You can read more about creating a legend via geopandas [in here](https://geopandas.org/mapping.html#creating-a-legend).

```python jupyter={"outputs_hidden": false}
# Plot using 9 classes and classify the values using "Natural Breaks" classification
ax = grid.plot(
    figsize=(6, 4),
    column="pt_r_t",
    cmap="RdYlBu",
    linewidth=0,
    scheme="Natural_Breaks",
    k=9,
    legend=True,
)

# Re-position the legend and set a title
ax.get_legend().set_bbox_to_anchor((1.4, 1))
ax.get_legend().set_title("Travel time (min)")

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

_**Figure 8.9**. Static map of travel times visualized using the natural breaks classification scheme. Data source: Tenkanen & Toivonen 2020._

In comparison to the previous maps, the differences in travel times are now more pronounced highlighting lower travel times near the central railway station. Notice also that we now have a different type of map legend that shows the associated class bins.  

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 8.1

Select another column from the data (for example, travel times by car: `car_r_t`) and visualize a thematic map using one of the available classification schemes and save it as a PNG image file.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

# Visualize the travel times into 9 classes using "Quantiles" classification scheme
grid.plot(
    ax=ax,
    column="car_r_t",
    cmap="RdYlBu",
    linewidth=0,
    scheme="Quantiles",
    k=9,
    legend=True,
)

# Re-position the legend and set a title
ax.get_legend().set_bbox_to_anchor((1.4, 1))
ax.get_legend().set_title("Travel time by car (min)")

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = "static_map2.png"
plt.savefig(outfp, dpi=300)
```

### Defining our own intervals

For our travel time data, one intuitive way to display the values is to  is to visualize the increasing travel time in fixed intervals, for example changing the color at each 10 minute interval.
We can acheive something like this susing the pretty breaks classifier and a large number of classes, or we can create our own intervals using `mapclassify`for better contro. We can, for example choose to display differences until 1,h hours (90 minutes), after which all values will be categorized in the highest interval.

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

_**Figure 8.10**. Histogram of the travel time values with user defined class breaks. Data source: Tenkanen & Toivonen 2020._

```python
# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))


# Visualize the travel times into 9 classes using "Quantiles" classification scheme
grid.plot(
    ax=ax,
    column="car_r_t",
    cmap="RdYlBu",
    linewidth=0,
    scheme="UserDefined",
    classification_kwds={'bins': break_values},
    legend=True,
    legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "interval": True}
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()
```

_**Figure 8.11**. Static map of travel times visualized using our own classification scheme. Data source: Tenkanen & Toivonen 2020._


## Adding a basemap

Let's now forget about separate transport network layers we used previously and add spatial context using basemaps from online sources. Basemaps might feature satellite imagery or a readily visualized bacground maps displaying various essential features such as streets, administrative boundaries, water bodies and so on.  We can use [contextily](https://github.com/darribas/contextily) together with `geopandas` and `matplotlib` to fetch map tiles as basemaps for our static maps. Bacground maps are available via `contextily` from various providers: 

```python jupyter={"outputs_hidden": false}
print(list(ctx.providers))
```

For most of the providers, there are multiple style options available. Here is an example for available OpenStreetMap visualizations: 


```python jupyter={"outputs_hidden": false}
ctx.providers.OpenStreetMap.keys()
```

Map tiles are typically distributed in [Web Mercator projection (EPSG:3857)](http://spatialreference.org/ref/sr-org/epsg3857-wgs84-web-mercator-auxiliary-sphere/). We either need to re-project our data before plotting, or set the desired coordinate reference system directly when adding the basemap using contextily. Let's plot our data using `geopandas` and add a default basemap for our plot using `contextily` using in the local EPSG:3067 projection:

```python jupyter={"outputs_hidden": false}
# Control figure size in here
fig, ax = plt.subplots(figsize=(6, 4))

# Plot the data
grid.plot(
    ax=ax,
    column="pt_r_t",
    cmap="RdYlBu",
    linewidth=0,
    scheme="Natural_Breaks",
    k=9,
    alpha=0.6,
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Add basemap and set crs
ctx.add_basemap(ax, crs=grid.crs)
```

_**Figure 8.11**. Static map of travel times visualized on top of a basemap. Data source: Tenkanen & Toivonen 2020; OpenStreetMap contributors 2025._

We can change the background map easily using the `source` -parameter when adding the basemap:

As you can see, `contextily` automatically adds credits for the bacground map. We can modify the credits text and add attribution also to the travel time data (Tenkanen & Toivonen 2020) in addition to the credits to OpenStreetMap contributors.

```python jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}
credits = "Travel time data by Tenkanen & Toivonen (2020), Map Data © OpenStreetMap contributors"
```

```python jupyter={"outputs_hidden": false}
# Control figure size in here
fig, ax = plt.subplots(figsize=(6, 4))

# Plot the data
grid.plot(
    ax=ax,
    column="pt_r_t",
    cmap="RdYlBu",
    linewidth=0,
    scheme="Natural_Breaks",
    k=9,
    alpha=0.6,
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Add basemap with basic OpenStreetMap visualization
ctx.add_basemap(ax, attribution=credits, source=ctx.providers.OpenStreetMap.Mapnik, crs=grid.crs)
```

_**Figure 8.13**. Static map of travel times visualized on top of a basemap. Data source: Tenkanen & Toivonen 2020; OpenStreetMap contributors 2025._


 Let's take a subset of our data to see a bit better the background map characteristics. We can, for example, visualize grid squares from where the central railway station can be reached in less than 15 minutes to get a zoomed-in view of the map:

```python

```

```python jupyter={"outputs_hidden": false}
# Control figure size in here
fig, ax = plt.subplots(figsize=(6, 4))

#  Plot only a subset of the data
grid.loc[(grid["pt_r_t"] < 20)].plot(ax=ax,
                                    column="pt_r_t",
                                    cmap="RdYlBu",
                                    linewidth=0,
                                    scheme="Quantiles",
                                    k=5,
                                    alpha=0.6
                                    )

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Add basemap with `OSM_A` style
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=grid.crs)
```

_**Figure 8.14**. Static map of travel times visualized on top of a basemap. Data source: Tenkanen & Toivonen 2020; OpenStreetMap contributors 2025._


Now our map has much more details as the zoom level of the background map is larger. `Contextily` sets the zoom level automatically but it is also possible to control the zoom level manually. The zoom level is by default specified as `auto` and it can be changed by passing in a specified [zoom level](https://wiki.openstreetmap.org/wiki/Zoom_levels) as numbers ranging typically from 1 to 19 (the larger the number, the more details your basemap will have). Let's try reducing the level of detail from our map by passing `zoom=11`:


```python jupyter={"outputs_hidden": false}
# Control figure size in here
fig, ax = plt.subplots(figsize=(6, 4))

#  Plot only a subset of the data
grid.loc[(grid["pt_r_t"] < 20)].plot(ax=ax,
                                    column="pt_r_t",
                                    cmap="RdYlBu",
                                    linewidth=0,
                                    scheme="Quantiles",
                                    k=5,
                                    alpha=0.6
                                    )

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Add basemap with `OSM_A` style
ctx.add_basemap(ax, zoom=11, source=ctx.providers.OpenStreetMap.Mapnik, crs=grid.crs)
```

_**Figure 8.14**. Static map of travel times visualized on top of a basemap. Data source: Tenkanen & Toivonen 2020; OpenStreetMap contributors 2025._

With this zoom setting, the map has now less detail. For example, there are less place names visible which makes the map easier to read. 



<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 8.2

Explore different background map options and make a final visualization of our travel time data with a basemap.

<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# Control figure size in here
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the data
grid.plot(
    ax=ax,
    column="pt_r_t",
    cmap="RdYlBu",
    linewidth=0,
    scheme="Natural_Breaks",
    k=9,
    alpha=0.6,
)

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Add basemap with basic OpenStreetMap visualization
ctx.add_basemap(ax, attribution=credits, source=ctx.providers.OpenStreetMap.Mapnik, crs=grid.crs)
```

## Footnotes
[^geopandas_mappingtools]: <https://geopandas.org/en/stable/docs/user_guide/mapping.html> 
[^matplotlib_pyplot]: <https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html> 
[^HSL_opendata]: <https://www.avoindata.fi/data/en_GB/dataset/hsl-n-linjat>
[^matplotlib_colormaps]: <https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html#choosing-colormaps-in-matplotlib>
[^matplotlib_legend]: <https://matplotlib.org/tutorials/intermediate/legend_guide.html>
[^matplotlib_colors]: <https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.colors>
[^matplotlib_colorbar]: <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html>
[^mapclassify]: <https://pysal.org/mapclassify/>

```python

```
