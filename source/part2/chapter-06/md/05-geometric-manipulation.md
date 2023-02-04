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


Here we demonstrate some of the most common geometry manipulation functions available in geopandas. We will use country borders from Africa as our example data. It is often useful to do geometric manipulations on administrative borders for further analysis and visualization purposes. We will learn how to generate centroids, different outlines and buffer zones for the country polygons. 

Geopandas comes with some ready-to-use data for country borders from [Natural Earth](https://www.naturalearthdata.com/) which we will use here. 

```python
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
data.head()
```

Let's continue with only the African continent.

```python
data = data.loc[data["continent"]=='Africa'].copy()
```

For the purposes of geometric manipulations, we are mainly interested in the geometry column which contains the polygon geometries. Remember, that the data type of the geometry-column is `GeoSeries`. Individual geometries are eventually shapely objects and we can use all of shapely's tools for geometry manipulation directly via geopandas.

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

Let's first plot the original geometries. We can use the in-built plotting function in geopandas to plot the geometries, and `matplotlib.pyplot` to turn off axis lines and labels.

```python
data.plot(facecolor="none", linewidth=0.2)

plt.axis("off")
plt.show()
```

<!-- #region tags=[] -->
## Centroid

Extracting the centroid of geometric features is useful in many cases. Geometric centroid can, for example, be used for locating text labels in visualizations. We can extract the center point of each polygon via the `centroid`-attribute of the geometry-column. 
<!-- #endregion -->

```python
data["geometry"].centroid.head()
```

We can also apply the method directly to the `GeoDataFrame` to achieve the same result.

```python
data.centroid.head()
```

Notice that geopandas warns us that we are trying to calculate centroids based on a geographic CRS and that our results are likely incorrect. Let's check what is the CRS definition of our data.

```python
data.crs
```

Our data are indeed in a geographic coordinate reference system WGS 84 (EPSG:4326). In order to get valid centroids, we should re-project the data to a projected coordinate reference system.


We can then plot the centroids for a visual check.

```python
data.centroid.plot(markersize=0.1)

plt.axis("off")
plt.show()
```

## Unary union

We can generate a joint outline for African countries represented in the Natural Earth data through creating a geometric union among all geometries. This could be useful, for example, for visualizing the outlines of a study area. The `unary_union` returns a single geometry object, which is automatically visualized when running the code in a Jupyter Notebook.

```python
data.unary_union
```

```python
type(data.unary_union)
```

## Simplifying geometries

Geometry simplification is a useful process especially when visualizing data that has very detailed geometry. With our sample data, we can generate simplified version of the outline extent. The tolerance parameter controls the level of simplification.

```python
data.unary_union.simplify(tolerance=1)
```

```python
data.unary_union.simplify(tolerance=10)
```

## Bounding polygon

Bounding polygons are useful in many cases for describing the approximate extent of geographic data. A minimum bounding rectangle, also called a bounding box or an envelope is the smallest rectangular polygon surrounding a geometric object. In a `GeoDataFrame`, the `envelope` attribute returns the bounding rectangle for each geometry.

```python
data.envelope.head()
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

A bit more detailed delineation of the data extent can be extracted using a convex hull which represents the smalles possible polygon that contains all points in an object. If we apply the convex hull method on the whole `GeoDataFrame`, we will get a GeoSeries containing a convex hull for each polygon separately.

```python
data.convex_hull.head()
```

In order to create a covex hull for the whole extent, we need to first create an union of all polygons. 

```python
data.unary_union.convex_hull
```

## Buffer

Buffering is a common spatial operation that has a multitude of use cases in spatial analyses. For example, in transport network analyses, it is good to fetch the transport network also from outside the study area in order to capture routes that go beyond the study area border. 

The distance parameter in the `buffer` function defines the radius or the buffer (according to the coordinate reference system of the data).

```python
# 5 km buffer for the travel time matrix extent
data.buffer(5).head()
```

<!-- #region tags=[] -->


## Dissolving and merging geometries

Data aggregation refers to a process where we combine data into groups. Spatial data aggregation refers to combining geometries into coarser spatial units based on some attributes. The process may also include the calculation of summary statistics. 

In pandas, we learned how to group and aggregate data using the `groupby`method. In geopandas, there is a function called `dissolve()` that groups the data based on an anttribute column and unions the geometries for each group in that attribute. 

Here we will conduct a simple dissolve operation through combining national borders by continent.
<!-- #endregion -->

```python
# Conduct the aggregation
dissolved = data.dissolve(by="continent")

# Check the result
dissolved
```

The column used for dissolving the data can now be found in the index.

```python
dissolved.index
```

The dissolved data should have as many rows of data as there were unique values in the column - one row for each unique value. Let's compare the number of cells in the layers before and after the aggregation.

```python
print("Rows in original intersection GeoDataFrame:", len(data))
print("Rows in dissolved layer:", len(dissolved))
```

Indeed the number of rows in our data has decreased. For each row, the original polygon geometries have been dissolved. 
