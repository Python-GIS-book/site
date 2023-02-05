---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Geometric data manipulations


Here we demonstrate some of the most common geometry manipulation functions available in `geopandas`. We will continue exploring the census tract data from Austin, Texas. It is often useful to do geometric manipulations on administrative borders for further analysis and visualization purposes. We will learn how to generate centroids, different outlines and buffer zones for the polygons.  

```python tags=["remove_cell"]
import os
os.environ['USE_PYGEOS'] = '0'
```

```python
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
```

```python
# Define path do the data
data_folder = Path("data/Austin")
fp = data_folder / "austin_pop_density_2019.gpkg"

# Read in the data and check the contents
data = gpd.read_file(fp)
data.head()
```

For the purposes of geometric manipulations, we are mainly interested in the geometry column which contains the polygon geometries. Remember, that the data type of the geometry-column is `GeoSeries`. Individual geometries are eventually `shapely` objects and we can use all of `shapely`'s tools for geometry manipulation directly via `geopandas`.

```python
# Check contents of the geometry column
data["geometry"].head()
```

```python
# Check data type of the geometry column
type(data["geometry"])
```

```python
# Check data type of a value in the geometry column
type(data["geometry"].values[0])
```

Let's first plot the original geometries. We can use the in-built plotting function in `geopandas` to plot the geometries, and `matplotlib.pyplot` to turn off axis lines and labels.

```python
data.plot(facecolor="none", linewidth=0.2)

plt.axis("off")
plt.show()
```

_**Figure 6.13**. Basic plot of the census tracts._

<!-- #region tags=[] -->
## Centroid

Extracting the centroid of geometric features is useful in many cases. Geometric centroid can, for example, be used for locating text labels in visualizations. We can extract the center point of each polygon via the `centroid`-attribute of the geometry-column. The data should be in a projected coordinate reference system when calculating the centroids. If trying to calculate centroids based on latitude and longitude information, `geopandas` will warn us that the results are likely incorrect. Our sample data are in WGS 84 / UTM zone 14N (EPSG:32614), which is a projected , and we can proceed to calculating the centroids.
<!-- #endregion -->

```python
data.crs.name
```

```python
data["geometry"].centroid.head()
```

We can also apply the method directly to the `GeoDataFrame` to achieve the same result using the syntax `data.centroid`. At the same time, we can also  plot the centroids for a visual check.

```python
data.centroid.plot(markersize=1)

plt.axis("off")
plt.show()
```

_**Figure 6.14**. Basic plot of census tract centroids._


## Unary union

We can generate a joint outline for the administrative areas through creating a geometric union among all geometries. This could be useful, for example, for visualizing the outlines of a study area. The `unary_union` returns a single geometry object, which is automatically visualized when running the code in a Jupyter Notebook.

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

<!-- #region tags=[] -->
## Dissolving and merging geometries

Spatial data aggregation refers to combining geometries into coarser spatial units based on some attributes. The process may also include the calculation of summary statistics. 

In `pandas`, we learned how to group and aggregate data using the `groupby`method. In `geopandas`, there is a function called `dissolve()` that groups the data based on an anttribute column and unions the geometries for each group in that attribute. At the same time, we can also get summary statistics of the attributes. Read more about the details of the dissolve-function and related aggregation options in the `geopandas` [online documentation](https://geopandas.org/en/stable/docs/user_guide/aggregation_with_dissolve.html) [^gpd_dissolve].
<!-- #endregion -->

To exceplify how dissolve works with our sample data, let's create create a new column to indicate census tracts with above average population density. We can do this by adding a new empty column `dense` and adding values that indicate above and below average population densities per census tract.

```python
# Create a new column and add a constant value
data["dense"] = 0
```

```python
# Filter rows with above average pop density and update the column dense
data.loc[data["pop_density_km2"]> data["pop_density_km2"].mean(), "dense"] = 1
```

```python
# Check number of rows per category
data.dense.value_counts()
```

Now we have a new column with value 1 indicating above average population density which we can use for dissolving the data into two groups using the `.dissolve()` funcition. At the same time, we can sum up the population and area columns valuens using the `aggfunc` parameter. The aggregation requires that we do a selection of the numerical columns we want to include in the output.

```python
# Conduct the aggregation
dissolved = data[["pop2019", "area_km2", 
                  "dense", "geometry"]].dissolve(by="dense", aggfunc="sum")
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
