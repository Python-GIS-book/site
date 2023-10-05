---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.15.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} -->
# Common geometric operations
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Geometric operations refer to a set of methods that can be used to process and analyze geometric features, like points, lines and polygons. In the context of geographic data analysis, these operations allow us, for instance, to ask questions about how two or more geographic objects relate to each other: Do they intersect, touch, or overlap? Are they adjacent to one another? How far apart are they? With the tools bundled in geopandas, it is easy to perform these kind of operations. As we delve into geometric operations, you'll discover they form the foundation of many geospatial analyses, enabling insights that are often difficult to discern from non-spatial data alone.

In the following, we demonstrate some of the most common geometric manipulation functions available in geopandas. We will do this by continuing to explore the census tract data from Austin, Texas. Geometric manipulations are often useful e.g. when working with data related to administrative boundaries, as we often might need to transform or manipulate the geographic data in one way or another for further analysis and visualization purposes. Next, we will learn how to generate centroids, different outlines and buffer zones for the polygons. Let's start by reading the census tract data into `GeoDataFrame`. In this case, we use data that we already manipulated a bit in the previous section (by calculating the area and population density):
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
import geopandas as gpd
from pathlib import Path

# Define path do the data
data_folder = Path("data/Austin")
fp = data_folder / "austin_pop_density_2019.gpkg"

# Read in the data and check the contents
data = gpd.read_file(fp)
data.head()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
For the purposes of geometric manipulations, we are mainly interested in the geometry column which contains the polygon geometries. Remember, that the data type of the geometry-column is `GeoSeries`. As we have mentioned earlier, the individual geometries are ultimately shapely geometric objects (e.g. `Point`, `LineString`, `Polygon`), and we can use all of shapely's tools for geometric manipulations directly via geopandas. The following shows that the geometries in the `GeoSeries` are stored as `MultiPolygon` objects:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data["geometry"].head()
```

```python editable=true slideshow={"slide_type": ""}
# Check data type of the geometry column
type(data["geometry"])
```

```python editable=true slideshow={"slide_type": ""}
# Check data type of a value in the geometry column
type(data["geometry"].values[0])
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's first plot the original geometries. We can use the built-in `.plot()` function in geopandas to plot the geometries, and `matplotlib.pyplot` to turn off axis lines and labels:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
import matplotlib.pyplot as plt

data.plot(facecolor="none", linewidth=0.2)

plt.axis("off")
plt.show()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 6.13**. Basic plot of the census tracts._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Centroid

The centroid of a geometry is the geometric center of a given geometry (line, polygon or a geometry collection). Extracting the centroid of geometric features is useful in many cases. Geometric centroid can, for example, be used for locating text labels in visualizations. We can extract the center point of each polygon via the `centroid` attribute of the `geometry` column. The data should be in a projected coordinate reference system when calculating the centroids. If trying to calculate centroids based on latitude and longitude information, geopandas will warn us that the results are likely (slightly) incorrect. Our `GeoDataFrame` is in WGS 84 / UTM zone 14N (EPSG:32614) coordinate reference system (CRS) which is a projected one (we will learn more about these in the next section). Thus, we can directly proceed to calculating the centroids:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data.crs.name
```

```python editable=true slideshow={"slide_type": ""}
data["geometry"].centroid.head()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
We can also apply the method directly to the `GeoDataFrame` to achieve the same result using the syntax `data.centroid`. At the same time, we can also  plot the centroids for a visual check:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data.centroid.plot(markersize=1)

plt.axis("off")
plt.show()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 6.14**. Basic plot of census tract centroids._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Updating the source for geometries in a GeoDataFrame

Before diving into other examples of geometric operations, let's discuss briefly about different ways to update the source column which is used to represent the geometries in your `GeoDataFrame`. In some cases, such as when calculating the centroids as we did earlier, you might actually want to save the centroids into your `GeoDataFrame` and continue processing or analysing the data based on these centroids. This can be done easily with geopandas, and there are a couple of approaches how to do this:

1. Overwrite the existing geometries in the `geometry` column by storing the centroids into it.
2. Create a new column (e.g. `centroid`) and store the centroid into this one. Then activate the column as the "source" for geometries in your `GeoDataFrame`. This means that you can have multiple simultaneous columns containing geometries in a `GeoDataFrame` which can be very handy!

Some important remarks about these approaches: The option 1 is very easy to do, but the downside of it is the fact that you do not have access to the original geometries (e.g. polygons) anymore. The option 2 requires a couple of steps, but the good side of it, is that you can easily swap between the original geometries and the centroids in your data. However, when saving the geographic data into disk, you can only include one column with geometries. Hence, latest at this stage, you need to decide which column is used for representing the geometric features in your data. In the following, we demonstrate how to do both of these. Let's start by showing how you can overwrite the existing geometries with centroids:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Make a copy
option_1 = data.copy()

option_1["geometry"].head(2)
```

```python editable=true slideshow={"slide_type": ""}
# Update the geometry column with centroids
option_1["geometry"] = option_1.centroid

option_1.head(2)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As we can see, now the geometries in the `geometry` column were replaced and populated with `Point` objects that represent the centroids of the polygons. With this approach, you cannot anymore access the original polygon geometries.

The second option is to create a new column for storing the centroids and then use this column as the source for representing geometries of the given `GeoDataFrame`:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Make a copy
option_2 = data.copy()

# Step 1: Create a column with centroids
option_2["centroid"] = data.centroid
option_2.head(2)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now we have two columns in our `GeoDataFrame` that contain geometries. By default, geopandas always uses the `geometry` column as a source for representing the geometries. However, we can easily change this with `.set_geometry()` method which can be used to tell geopandas to use another column with geometries as the geometry-source:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Use centroids as the GeoDataFrame geometries
option2 = option_2.set_geometry("centroid")
option2.head(2)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Nothing seem to have changed in the data itself, which is good because we did not want to modify any data. However, when we take a look at the `.geometry.name` attribute of the `GeoDataFrame`, we can see that the name of the column used for representing geometries has actually changed:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
option2.geometry.name
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
We can still confirm this by plotting our `GeoDataFrame` which now returns a map with points:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
option2.plot()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
By following this approach, you can easily change the active `geometry` for your `GeoDataFrame`. This can be highly useful when manipulating geometries as you can store the geometries from different computational steps into a same `GeoDataFrame` without a need to make multiple copies of the data. However, we recommend to be a bit careful when storing multiple columns with geometries, as it is possible that you accidentally use a different source for geometries than what you have planned to do, which can cause confusion and problems with your analyses. Always remember the name the columns intuitively which can help avoiding issues and confusion in your analyses!
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Unary union

We can generate a joint outline for the administrative areas through creating a geometric union among all geometries. This could be useful, for example, for visualizing the outlines of a study area. The `unary_union` returns a single geometry object, which is automatically visualized when running the code in a Jupyter Notebook.
<!-- #endregion -->

```python
data.unary_union
```

_**Figure 6.15**. Union of all of census tract polygon geometries._


## Simplifying geometries

Geometry simplification is a useful process especially when visualizing data that has very detailed geometry. With our sample data, we can generate simplified version of the outline extent. The tolerance parameter controls the level of simplification.

```python
data.unary_union.simplify(tolerance=1000)
```

_**Figure 6.16**. Simplified union of the census tract polygons._


## Bounding polygon

Bounding polygons are useful in many cases for describing the approximate extent of geographic data. A minimum bounding rectangle, also called a bounding box or an envelope is the smallest rectangular polygon surrounding a geometric object. In a `GeoDataFrame`, the `envelope` attribute returns the bounding rectangle for each geometry.

```python
data.envelope.head()
```

In order to get the bounding rectangle for the whole layer, we  first create an union of all geometries using `unary_union`, and then create the bounding rectangle for that polygon.

```python
data.unary_union.envelope
```

_**Figure 6.17**. Minimum bounding box for the census tracts._

Corner coordinates of the bounding box for a `GeoDataFrame` can be fetched via the `total_bounds` attribute. 

```python
data.total_bounds
```

The `bounds` attribute returns the bounding coordinates of each feature.

```python
data.bounds.head()
```

### Convex hull

A bit more detailed delineation of the data extent can be extracted using a convex hull which represents the smalles possible polygon that contains all points in an object. If we apply the convex hull method on the whole `GeoDataFrame`, we will get a GeoSeries containing a convex hull for each polygon separately.

```python
data.convex_hull.head()
```

In order to create a covex hull for the whole extent, we need to first create an union of all polygons. 

```python
data.unary_union.convex_hull
```

_**Figure 6.18**. Smallest convex polygon for the census tracts._


## Buffer

Buffering is a common spatial operation that has a multitude of use cases in spatial analyses. For example, in transport network analyses, it is good to fetch the transport network also from outside the study area in order to capture routes that go beyond the study area border. The distance parameter in the `buffer` function defines the radius or the buffer (according to the coordinate reference system of the data). Applying the buffer function on the entire data frame will produce separate buffers for each census tract.

```python
# 1000 m buffer for each polygon
data.buffer(1000).plot(edgecolor="white")

plt.axis("off")
plt.show()
```

_**Figure 6.19**. 1km buffer for each census tract._


If we want one buffer for the whole area, we first need to combine the geometries into one object before the buffer analysis. 

```python
# 1000 m buffer for each polygon
data.unary_union.buffer(1000)
```

_**Figure 6.20**. 1km buffer for each census tract._


## Dissolving and merging geometries

Spatial data aggregation refers to combining geometries into coarser spatial units based on some attributes. The process may also include the calculation of summary statistics. 

In `pandas`, we learned how to group and aggregate data using the `groupby`method. In `geopandas`, there is a function called `dissolve()` that groups the data based on an anttribute column and unions the geometries for each group in that attribute. At the same time, we can also get summary statistics of the attributes. Read more about the details of the dissolve-function and related aggregation options in the `geopandas` [online documentation](https://geopandas.org/en/stable/docs/user_guide/aggregation_with_dissolve.html) [^gpd_dissolve].


To exceplify how dissolve works with our sample data, let's create create a new column to indicate census tracts with above average population density. We can do this by adding a new empty column `dense` and adding values that indicate above and below average population densities per census tract.

```python
# Create a new column and add a constant value
data["dense"] = 0
```

```python
# Filter rows with above average pop density and update the column dense
data.loc[data["pop_density_km2"] > data["pop_density_km2"].mean(), "dense"] = 1
```

```python
# Check number of rows per category
data.dense.value_counts()
```

Now we have a new column with value 1 indicating above average population density which we can use for dissolving the data into two groups using the `.dissolve()` funcition. At the same time, we can sum up the population and area columns valuens using the `aggfunc` parameter. The aggregation requires that we do a selection of the numerical columns we want to include in the output.

```python
# Conduct the aggregation
dissolved = data[["pop2019", "area_km2", "dense", "geometry"]].dissolve(
    by="dense", aggfunc="sum"
)
```

```python
# Check the result
dissolved
```

The dissolved data should have as many rows of data as there were unique values in the column - one row for each unique value. Our data have been compressed into two geometric objects and the column used for dissolving the data can now be found in the index. Attribute columns represent the sum of the values per group. We can reset the index and insert the categorical information into a new column after which we can do a quick visualization of the result.

```python
dissolved = dissolved.reset_index()
```

```python
dissolved.plot(column="dense")

plt.axis("off")
plt.show()
```

_**Figure 6.21**. Dissolved census tract geometries._


## Footnotes

[^gpd_dissolve]: <https://geopandas.org/en/stable/docs/user_guide/aggregation_with_dissolve.html>
