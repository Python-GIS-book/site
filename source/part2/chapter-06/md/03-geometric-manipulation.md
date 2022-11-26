---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Geometric data manipulations


Here we demonstrate some of the most common geometry manipulation functions available in geopandas. We will use the Helsinki Region Travel Time Matrix as example data for geometric manipulations. The Travel Time Matrix constist of 13231 statistical grid squares (250m x 250m) from the Helsinki Region in Southern Finland and we will learn how to generate centroids, different outlines and buffer zones for these polygons. 

```python
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

input_folder = Path("../data/Helsinki")
fp = input_folder / "TravelTimes_to_5975375_RailwayStation.shp"

data = gpd.read_file(fp)
data.head(2)
```

The attribute columns contain information about travel times and distances by car, public transport and walking across the region. For now, we are only interested in the geometry column of the data that contains the polygon geometry of the grid squares. Remember, that the data type of the geometry-column a `GeoDataFrame` is `GeoSeries` and individual geometries are eventually shapely objects, we can use all of shapely's tools for geometry manipulation directly via geopandas.

```python
data["geometry"].head()
```

```python
type(data["geometry"])
```

```python
type(data["geometry"].values[0])
```

Let's first plot the original geometry of the grid squares. We use the in-built plotting function in geopandas to plot the geometries, and `matplotlib.pyplot` to turn off axis lines and labels.

```python
data.plot(facecolor="none", linewidth=0.2)

plt.axis("off")
plt.show()
```

<!-- #region tags=[] -->
## Centroid

Extracting the centroid of geometric features is useful in many cases. In this case, the values in the Travel Time Matrix data set have been originally calculated for the grid square centroids, and we can extract these point locations via the `centroid`-attribute of the geometry-column. 
<!-- #endregion -->

```python
data["geometry"].centroid
```

We can also apply the method directly to the `GeoDataFrame` to achieve the same result.

```python
data.centroid
```

We can then plot the centroids for a visual check.

```python
data.centroid.plot(markersize=0.1)

plt.axis("off")
plt.show()
```

## Unary union

We can generate a joint outline for the 13231 grid squares through creating a geometric union among all geometries in the data. This could be useful, for example, for visualizing the outlines of a study area. The `unary_union` returns a single geometry object, which is automatically visualized when running the code in a Jupyter Notebook, so we don't need to use any additional plotting tools in this case.

```python
# Polygon centroids
data.unary_union
```

```python
type(data.unary_union)
```

## Simplifying geometries

Geometry simplification is a useful process especially when visualizing data that has very detailed geometry. With our sample data, we can generate simplified version of the outline extent. The tolerance parameter controls the level of simplification.

```python
data.unary_union.simplify(tolerance=500)
```

## Bounding polygon

Sometimes it is enough to describe the approximate extent of the data using a bounding polygon. A minimum bounding rectangle, also called a bounding box or an envelope is the smallest rectangular polygon surrounding a geometric object. In a `GeoDataFrame`, the `envelope` attribute returns the bounding rectangle for each geometry.

```python
data.envelope
```

In order to get the bounding rectangle for the whole layer, we  first create an union of all geometries using `unary_union`, and then create the bounding rectangle for that polygon.

```python
data.unary_union.envelope
```

Corner coordinates of the bounding box for a `GeoDataFrame` can be fetched via the `total_bounds` attribute. The `bounds` attribute returns the bounding coordinates of each feature.

```python
data.total_bounds
```

```python
data.bounds.head()
```

### Convex hull

A bit more detailed delineation of the data extent can be extracted using a convex hull which represents the smalles possible polygon that contains all points in an object. For a single grid square in our data, the convex hull would be identical to the polygon geometry due to it's square shape. In order to create a covex hull for all grid squares, we need to first create an union of all polygons. 

```python
data.unary_union.convex_hull
```

## Buffer

Buffering is a common spatial operation that has a multitude of use cases in spatial analyses. In the case of the Travel Time Matrix data, the original analysis has been conducted using a buffer zone in order to include routes outside the study area into the analysis to avoid edge-effects. We can extract the original analysis extent by buffering the data extent. The distance parameter in the `buffer` function defines the radius or the buffer in meters (according to the coordinate reference system of the data).

```python
# 5 km buffer for the travel time matrix extent
data.unary_union.buffer(5000)
```

<!-- #region tags=[] -->


## Dissolving and merging geometries

Data aggregation refers to a process where we combine data into groups. Spatial data aggregation refers to combining geometries into coarser spatial units based on some attributes. The process may also include the calculation of summary statistics. A simple example of spatial data aggregation would be to combine national borders by continent.

In pandas, we learned how to group and aggregate data using the `groupby`method. In geopandas, there is a function called `dissolve()` that groups the data based on an anttribute column and unions the geometries for each group in that attribute. 

At this point, we will make use of the attribute columns in the data. We will aggregate our travel time data by car travel times (column `car_r_t`) so that the grid cells that have the same travel time to Railway Station will be merged together.
<!-- #endregion -->

```python
# Conduct the aggregation
dissolved = data.dissolve(by="car_r_t")

# What did we get
dissolved.head()
```

The column used for dissolving the data (`car_r_t`) can now be found in the index and the numbers in this index are the unique travel time values found in that column. Note that `-1` represents `NoData`.

```python
dissolved.index
```

The dissolved data should have as many rows of data as there were unique values in the column - one row for each unique value. Let's compare the number of cells in the layers before and after the aggregation.

```python
print("Rows in original intersection GeoDataFrame:", len(data))
print("Rows in dissolved layer:", len(dissolved))
```

Indeed the number of rows in our data has decreased. For each row, the original polygon geometries have been dissolved.  Let's inspect the regions with exactly 15 minutes travel distance to the railway station.

```python
dissolved.loc[15, "geometry"]
```

The grid squares with `car_r_t` equal to 15 have been dissolved into a signle `MultiPolygon` object.

```python
import geopandas as gpd

# File path
fp = "data/Amazon_river.shp"
data = gpd.read_file(fp)

# Print crs
print(data.crs)

# Plot the river
data.plot()
```

The LineString that is presented here is quite detailed, so let's see how we can generalize them a bit. As we can see from the coordinate reference system, the data is projected in a metric system using [Mercator projection based on SIRGAS datum](http://spatialreference.org/ref/sr-org/7868/). 

- Generalization can be done easily by using a Shapely function called `.simplify()`. The `tolerance` parameter can be used to adjusts how much geometries should be generalized. **The tolerance value is tied to the coordinate system of the geometries**. Hence, the value we pass here is 20 000 **meters** (20 kilometers).

```python
# Generalize geometry
data["geom_gen"] = data.simplify(tolerance=20000)

# Set geometry to be our new simlified geometry
data = data.set_geometry("geom_gen")

# Plot
data.plot()
```

Nice! As a result, now we have simplified our LineString quite significantly as we can see from the map.



