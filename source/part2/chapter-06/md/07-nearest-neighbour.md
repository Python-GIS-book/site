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

# Nearest neighbour analysis


The idea of neighbourhood is one of the fundamental concepts in geographic data analysis and modelling. Being able to understand how close geographic objects are to each other, or which features are neighboring a specific location is fundamental to various spatial analysis techniques, such as spatial interpolation (which we cover in Chapter 10) or understanding whether there exist spatial autocorrelation (i.e. clustering) in the data (see Chapters [6](https://geographicdata.science/book/notebooks/06_spatial_autocorrelation.html) and [7](https://geographicdata.science/book/notebooks/07_local_autocorrelation.html) in {cite}`Rey_et_al_2023`). Many of these techniques rely on the idea that proximity in geographic space typically indicates also similarity in attribute space. For example, it is quite typical that a neighborhood with high population density is next to another neighborhood that also has high concentration of residents (i.e. the population density tend to cluster). One of the most famous notions related to this is the *First law of geography* which states that "everything is related to everything, but near things are more related than distant things" ({cite}`Tobler1970`). Thus, being able to understand how close neighboring geographic features are, or which objects are the closest ones to specific location is an important task in GIS. 

**Figure 6.43** illustrates two common ways to find nearest neighbors to specific locations. In these examples, we have two Point datasets visualized with blue circles and red rectangles that are used for doing the nearest neighbor analysis. In the first example (top row), the idea is to find the closest geometry (rectangles) for all the points in the area. Here, the nearest neighbor is determined based on distance between the points and rectangles, and the nearest neighbors are visualized with a line from every point to the closest rectangle (on the right). The bottom row shows an example in which we aim to find the closest point for each rectangle, but in this case we also apply a maximum search distance that limits the search area. Only those points that are within the search area are considered when finding the nearest neighbor, while the points outside of this area are simply ignored. As a result, the point closest to a given rectangle is visualized with a connected line (on the right). In these examples, the geographic objects are simple point like features, but similar approach can be used with any geographic features, for example by finding closest LineString or Polygon geometry to a given Point, or by finding the closest Polygon to another Polygon. In these cases, the calculations are a bit more complicated, but the basic idea is the same. 

Quite often with very large datasets, we might want to limit the search area up to a specific maximum distance. This can be due to practical reasons as it can significantly speed up the computation time, or because we have specific reasoning that makes it sensible to limit the search area. For example, if we would aim to understand how easily accessible public transportation is to citizens living in a city, it would make sense to limit the search area e.g. up to 2 km from the homes of people, because people are not willing to walk for very long distances to get into a bus stop. It's important to notice that the distances in the calculations are commonly based on the Euclidian distance, i.e. we calculate the distances based on coordinates on a Cartesian plain, meaning that the distances do not consider changes in height (i.e. third dimension is omitted). It is of course possible also to consider 3D distances, but the most typical Python tools ignore the height information. 


![_**Figure 6.43**. The basic idea of finding a nearest neighbour based on geographic distance.](../img/nearest-neighbour.png)

_**Figure 6.43**. The basic idea of finding a nearest neighbour based on geographic distance._


## Nearest neighbour analysis with Python

In Python, there are various libraries that can be used to find nearest neighbors for given set of geometries, including `shapely`, `geopandas`, `scikit-learn`, and `pysal` among others. Here, we focus on first introducing how `shapely` can be used to find the nearest neighbor for a given Point geometry, and then we show how to find nearest neighbors for all geometries in a given GeoDataFrame based on geometries in another GeoDataFrame. 

In `shapely`, we can do a simple nearest neighbour analysis between Point observations using a function called `nearest_points()` which returns a tuple of the nearest points in the input geometries.
Let's start by creating a "source" Point object and a few "destination" Points and find out which of the points in "destination" set of geometries is the closest:

```python
from shapely import Point, MultiPoint
from shapely.ops import nearest_points

# Source point
orig = Point(1, 1.67)

# Destination points
dest1 = Point(0, 1.45)
dest2 = Point(2, 2)
dest3 = Point(0, 2.5)
```

Now we have one source point and three destination points. To be able to find out the closest destination point from the source, we need to create a MultiPoint object from the destination points:

```python
destinations = MultiPoint([dest1, dest2, dest3])
print(destinations)
```

```python
destinations
```

_**Figure 6.44**. A set of geometries represented as MultiPoint object which are used in nearest neighbor computation._

As we can see from Figure 6.44, all the destination points are represented as a single MultiPoint object. Now we can find the nearest point from the `destination` variable by using the `nearest_points()` function:

```python
nearest_geometries = nearest_points(orig, destinations)
type(nearest_geometries)
```

As we can see, the `nearest_points()` function returns a tuple. Let's take a look at the contents of this variable: 

```python
print(nearest_geoms)
```

```python
print(nearest_geoms[0])
print(nearest_geoms[1])
```

In the tuple, the first item (at index 0) is the geometry of our source point and the second item (at index 1) is the actual nearest geometry from the destination points. Hence, the closest destination point seems to be the one located at coordinates (0, 1.45). This is the basic logic how we can find the nearest point from a set of points using `shapely`. While Shapely's `nearest_points` function provides a nice way to conduct the nearest neighbor analysis, it can be quite slow. Using it also requires taking the `unary union` of the point dataset where all the Points are merged into a single layer. This can be a really memory hungry and slow operation, that can cause problems with large point datasets. Luckily, we can do nearest neighbor analysis much more efficiently using geopandas. 


## Nearest neighbor analysis between GeoDataFrames

In the following, we go through a very practical example that relates to our daily commute: Where is the closest public transport stop from my place of living? Hence, our aim is to search for each building in the Helsinki Region the closest public transport stop. In geopandas, we can find nearest neighbors for all geometries in a given GeoDataFrame based on another GeoDataFrame very easily by using a method called `.sjoin_nearest()`. To show how to use this method, let's start by reading the datasets into GeoDataFrames and visualize them to understand a bit better what we have. 

```python
import geopandas as gpd
import matplotlib.pyplot as plt

stops = gpd.read_file("data/Helsinki/pt_stops_helsinki.gpkg")
buildings = gpd.read_file("data/Helsinki/building_points_helsinki.zip")

print("Number of stops:", len(stops))
stops.head(2)
```

```python
print("Number of buildings:", len(buildings))
buildings.head(2)
```

As we can see, both GeoDataFrames contain Point geometries. There seems to be approximately 8400 stops and almost 159 thousand buildings in our data. Hence, we have already a fair amount of data and calculations to do, to find the nearest neighbor for each building. Let's still visualize the GeoDataFrames next to each other so that we can see them on a map:

```python
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 10))

# Plot buildings
buildings.plot(ax=ax1, markersize=0.2, alpha=0.5)
ax1.set_title("Buildings")

# Plot stops
stops.plot(ax=ax2, markersize=0.2, alpha=0.5, color="red")
ax2.set_title("Stops");
```

_**Figure 6.45**. Maps representing the buildings and public transport stops which we use to find the closest stop for each building._

As mentioned earlier, finding the nearest geometries between two GeoDataFrames (here building and stop points) can be done easily using the `.sjoin_nearest()` method in geopandas. As the name implies, this method is actually designed to merge data between GeoDataFrames in a similar manner as with regular `.sjoin()` method that we saw earlier in Chapter 6.7. However, in this case the method is actually searching for the closest geometries instead of relying on spatial predicates, such as *within*. The `sjoin_nearest()` can be used for different geometry types, so the input geometries do not necessarily need to be Point objects as in our example. For the method to work properly, it is recommended to ensure that the both GeoDataFrames are having the same coordinate reference system (CRS), and preferably having a projected (metric) CRS because that ensures that the reported distances are meaningful (in meters) and correct. Hence, let's start by reprojecting our latitude and longitude values into a metric system using the national EUREF-FIN coordinate reference system (EPSG code 3067) for Finland:

```python
stops = stops.to_crs(epsg=3067)
buildings = buildings.to_crs(epsg=3067)

stops.head(2)
```

Now the GeoDataFrames are surely in the same coordinate system and we can see that the coordinates in the `geometry` column have changed representing meters. Next, we will use the `buildings.sjoin_nearest()` to find the closest stop for each building. Because we are interested to find the closest stop geometry for each building, the `buildings` GeoDataFrame is the left hand side of the command. As inputs, we pass the `stops` GeoDataFrame as well as give a name for a column which is used to store information about the distance between a given building and the closest stop (this is optional):

```python
%time
closest = buildings.sjoin_nearest(stops, distance_col="distance")
closest
```

As a result, we now have found the closest stop for each building and also merged the attributes of the `stops` GeoDataFrame into the results. The last column in the table shows the distance in meters between a given building and the closest stop to it which we specified to be stored in the column `distance`. The `%time` command at the beginning of the cell provided us some details about the time it took to find the nearest neighbors and merge the data. As we can see the computations are very efficient taking only a matter of some microseconds for the almost 160 thousand observations. We can make this even faster by specifying a `max_distance` parameter the maximum search distance from a given geometry. Here, we specify the maximum distance to be 100 meters from each building:

```python
%time
closest_limited = buildings.sjoin_nearest(stops, max_distance=100, distance_col="distance")
closest_limited
```

As we can see, there was a slight improvement in the execution time compared to the previous call without specifying the `max_distance` parameter. One important aspect to notice from the results is that the number of rows in our results has decreased significantly from 160 to 40 thousand buildings. This happens because our search distance was very low (100 meters) which means that there were many buildings that did not have any buildings within 100 meters from them. Because the default join type in `sjoin_nearest` is `inner` join, all the records that did not have a match were dropped. If you would like to keep all the buildings in the results to e.g. investigate which buildings do not have any stops within 100 meters, you can add parameter `how="left"` which will retain all the records in the `buildings` GeoDataFrame.


```python
# Bring the geometry from the stops
stops["index"] = stops.index
closest = closest.merge(stops[["index", "geometry"]], left_on="index_right", right_on="index")
closest.head()
```

```python
from shapely import LineString
closest["geometry"] = closest.apply(lambda row: LineString([row["geometry_x"], row["geometry_y"]]), axis=1)
closest = closest.set_geometry("geometry")
closest.head()
```

- Let's see how our datasets look like:

```python
ax = closest.plot(lw=0.5, figsize=(10,10))
ax = closest.set_geometry("geometry_x").plot(ax=ax, color="red", markersize=2)
ax = closest.set_geometry("geometry_y").plot(ax=ax, color="black", markersize=8.5, marker="s")
ax.set_xlim(382000, 384100)
ax.set_ylim(6676000, 6678000)
```

There are also other fast and memory efficient alternatives for conducting nearest neighbor analysis between point datasets, based on a function called [BallTree](https://en.wikipedia.org/wiki/Ball_tree) from a [scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html) library. The Balltree algorithm has some nice features, such as the ability to calculate the distance between neighbors with various different distance metrics. Most importantly the function allows to calculate `euclidian` distance between neighbors (good if your data is in metric crs), as well as `haversine` distance which allows to determine [Great Circle distances](https://en.wikipedia.org/wiki/Great-circle_distance) between locations (good if your data is in lat/lon format). *Note: There is also an algorithm called [KDTree](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree) in scikit-learn, that is also highly efficient but less flexible in terms of supported distance metrics.* 

```python
import geopandas as gpd
import fiona
```

```python
# Define filepaths
fp1 = "data/Helsinki/PKS_suuralue.kml"
fp2 = "data/Helsinki/addresses.shp"
```

```python
# Enable KML driver
fiona.supported_drivers["KML"] = "rw"
```

```python
# Read in data with geopandas
df1 = gpd.read_file(fp1, driver="KML")
df2 = gpd.read_file(fp2)
```

```python
# District polygons:
df1.head()
```

```python
# Address points:
df2.head()
```

Before calculating any distances, we should re-project the data into a projected crs.

```python
df1 = df1.to_crs(epsg=3067)
df2 = df2.to_crs(epsg=3067)
```

Furthermore, let's calculate the centroids for each district area:

```python
df1["centroid"] = df1.centroid
df1.head()
```

SO, for each row of data in the disctricts -table, we want to figure out the nearest address point and fetch some attributes related to that point. In other words, we want to apply the Shapely `nearest_points`function so that we compare each polygon centroid to all address points, and based on this information access correct attribute information from the address table. 

For doing this, we can create a function that we will apply on the polygon GeoDataFrame:

```python
def get_nearest_values(
    row, other_gdf, point_column="geometry", value_column="geometry"
):
    """Find the nearest point and return the corresponding value from specified value column."""

    # Create an union of the other GeoDataFrame's geometries:
    other_points = other_gdf["geometry"].unary_union

    # Find the nearest points
    nearest_geoms = nearest_points(row[point_column], other_points)

    # Get corresponding values from the other df
    nearest_data = other_gdf.loc[other_gdf["geometry"] == nearest_geoms[1]]

    nearest_value = nearest_data[value_column].values[0]

    return nearest_value
```

By default, this function returns the geometry of the nearest point for each row. It is also possible to fetch information from other columns by changing the `value_column` parameter.


The function creates a MultiPoint object from `other_gdf` geometry column (in our case, the address points) and further passes this MultiPoint object to Shapely's `nearest_points` function. 

Here, we are using a method for creating an union of all input geometries called `unary_union`. 

- Let's check how unary union works by applying it to the address points GeoDataFrame:

```python
unary_union = df2.unary_union
print(unary_union)
```

Okey now we are ready to use our function and find closest address point for each polygon centroid.
 - Try first applying the function without any additional modifications: 

```python
df1["nearest_loc"] = df1.apply(
    get_nearest_values, other_gdf=df2, point_column="centroid", axis=1
)
```

- Finally, we can specify that we want the `id` -column for each point, and store the output in a new column `"nearest_loc"`:

```python
df1["nearest_loc"] = df1.apply(
    get_nearest_values,
    other_gdf=df2,
    point_column="centroid",
    value_column="id",
    axis=1,
)
```

```python
df1.head()
```

That's it! Now we found the closest point for each centroid and got the ``id`` value from our addresses into the ``df1`` GeoDataFrame.

```python
print(buildings.head(), "\n--------")
print(stops.head())
```

Okay, so both of our datasets consisting points, and based on the coordinates, they seem to be in WGS84 projection.

- Let's also make maps out of them to get a better understanding of the data

```python
%matplotlib inline
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

# Plot buildings
buildings.plot(ax=axes[0], markersize=0.2, alpha=0.5)
axes[0].set_title("Buildings")

# Plot stops
stops.plot(ax=axes[1], markersize=0.2, alpha=0.5, color="red")
axes[1].set_title("Stops");
```

_**Figure 6.38**. ADD PROPER FIGURE CAPTION!._

As we can see, we have a very densely distributed Point dataset that shows the location of the buildings (their centroid) in Helsinki Region. On the right, we have public transport stops that seem to cover a bit broader geographical extent with a few train stops reaching further North. Most importantly, we can see from the coordinates and the map that both of the layers share the same coordinate reference system, and they are approximately from the same geographical region. Hence, we are ready to find closest public transport stop (on the right) for each building on the left map.     


- Let's first prepare a couple of functions that does the work

```python
from sklearn.neighbors import BallTree
import numpy as np


def get_nearest(src_points, candidates, k_neighbors=1):
    """Find nearest neighbors for all source points from a set of candidate points"""

    # Create tree from the candidate points
    tree = BallTree(candidates, leaf_size=15, metric="haversine")

    # Find closest points and distances
    distances, indices = tree.query(src_points, k=k_neighbors)

    # Transpose to get distances and indices into arrays
    distances = distances.transpose()
    indices = indices.transpose()

    # Get closest indices and distances (i.e. array at index 0)
    # note: for the second closest points, you would take index 1, etc.
    closest = indices[0]
    closest_dist = distances[0]

    # Return indices and distances
    return (closest, closest_dist)


def nearest_neighbor(left_gdf, right_gdf, return_dist=False):
    """
    For each point in left_gdf, find closest point in right GeoDataFrame and return them.

    NOTICE: Assumes that the input Points are in WGS84 projection (lat/lon).
    """

    left_geom_col = left_gdf.geometry.name
    right_geom_col = right_gdf.geometry.name

    # Ensure that index in right gdf is formed of sequential numbers
    right = right_gdf.copy().reset_index(drop=True)

    # Parse coordinates from points and insert them into a numpy array as RADIANS
    # Notice: should be in Lat/Lon format
    left_radians = np.array(
        left_gdf[left_geom_col]
        .apply(lambda geom: (geom.y * np.pi / 180, geom.x * np.pi / 180))
        .to_list()
    )
    right_radians = np.array(
        right[right_geom_col]
        .apply(lambda geom: (geom.y * np.pi / 180, geom.x * np.pi / 180))
        .to_list()
    )

    # Find the nearest points
    # -----------------------
    # closest ==> index in right_gdf that corresponds to the closest point
    # dist ==> distance between the nearest neighbors (in meters)

    closest, dist = get_nearest(src_points=left_radians, candidates=right_radians)

    # Return points from right GeoDataFrame that are closest to points in left GeoDataFrame
    closest_points = right.loc[closest]

    # Ensure that the index corresponds the one in left_gdf
    closest_points = closest_points.reset_index(drop=True)

    # Add distance if requested
    if return_dist:
        # Convert to meters from radians
        earth_radius = 6371000  # meters
        closest_points["distance"] = dist * earth_radius

    return closest_points
```

Okay, now we have our functions defined. So let's use them and find the nearest neighbors!

```python
# Find closest public transport stop for each building and get also the distance based on haversine distance
# Note: haversine distance which is implemented here is a bit slower than using e.g. 'euclidean' metric
# but useful as we get the distance between points in meters
closest_stops = nearest_neighbor(buildings, stops, return_dist=True)

# And the result looks like ..
closest_stops
```

Great, that didn't take too long! Especially considering that we had quite a few points in our datasets (8400\*159000=1.33 billion connections). As a result, we have a new GeoDataFrame that reminds a lot the original `stops` dataset. However, as we can see there are much more rows than in the original dataset, and in fact, each row in this dataset corresponds to a single building in the `buildings` dataset. Hence, we should have exactly the same number of closest_stops as there are buildings. Let's confirm this: 

```python
# Now we should have exactly the same number of closest_stops as we have buildings
print(len(closest_stops), "==", len(buildings))
```

Indeed, that seems to be the case. Hence, it is easy to combine these two datasets together. Before continuing our analysis, let's take a bit deeper look, what we actually did with the functions above.  


### What did we just do? Explanation.

To get a bit more understanding of what just happened, let's go through the essential parts of the two functions we defined earlier, i.e. `nearest_neighbor()` and `get_closest()`.

The purpose of `nearest_neighbor()` function is to handle and transform the data from GeoDataFrame into `numpy arrays` (=super-fast data structure) in a format how `BallTree` function wants them. This includes converting the lat/lon coordinates into radians (and back), so that we get the distances between the neighboring points in a correct format: scikit-learn's [haversine distance metric](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html) wants inputs as radians and also outputs the data as radians. To convert a lat/lon coordinate to radian, we use formula: `Radian = Degree * PI / 180`. By doing this, we are able to get the output distance information in meters (even if our coordinates are in decimal degrees). 

The `get_closest()` function does the actual nearest neighbor search using [BallTree](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html) function. We initialize the `BallTree` object with the coordinate information from the **right_gdf** (i.e. the point dataset that contains all the nearest neighbor candidates), and we specify the distance metric to be `haversine` so that we get the Great Circle Distances. The `leaf_size` parameter adjusts the tradeoff between the cost of BallTree node traversal and the cost of a brute-force distance estimate. Changing leaf_size will not affect the results of a query, but can significantly impact the speed of a query and the memory required to store the constructed tree. We determine the leaf_size as 15 which has been found to be a good compromise when [benchmarked](https://jakevdp.github.io/blog/2013/04/29/benchmarking-nearest-neighbor-searches-in-python/). After we have built (initialized) the ball-tree, we run the nearest neighbor query with `tree.query(src_points, k=k_neighbors)`, where the src_points are the building-coordinates (as radians) and the `k` -parameter is the number of neighbors we want to calculate (1 in our case as we are only interested in the closest neighbor). Finally, we just re-arrange the data back into a format in which the closest point indices and distances are in separate numpy arrays. 

**Note:** The functions here assume that your input points are in WGS84 projection. If you pass the points in some other projection, it is highly likely that the distances between nearest neighbors are incorrect. Determining which is the nearest neighbor should not be affected, though.  


### Combining the neighboring datasets 

Okay, now as we have found closest stop for each building in the region, we can easily merge the information about closest stops back to the building layer. The order of the `closest_stops` matches exactly the order in `buildings`, so we can easily merge the datasets based on index. 

```python
# Rename the geometry of closest stops gdf so that we can easily identify it
closest_stops = closest_stops.rename(columns={"geometry": "closest_stop_geom"})

# Merge the datasets by index (for this, it is good to use '.join()' -function)
buildings = buildings.join(closest_stops)

# Let's see what we have
buildings.head()
```

Excellent! Now we have useful information for each building about the closest stop including the `distance` (in meters) and also e.g. the name of the stop in `stop_name` column. 

- Now it is easy to do some descriptive analysis based on this dataset, that gives information about levels of access to public transport in the region: 

```python
buildings["distance"].describe()
```

Okay, as we can see the average distance to public transport in the region is around 300 meters. More than 75 % of the buildings seem to be within within 5 minute walking time (~370 meters with walking speed of 4.5 kmph) which indicates generally a good situation in terms of accessibility levels in the region overall. There seem to be some really remote buildings in the data as well, as the longest distance to closest public transport stop is more than 7 kilometers.

- Let's make a map out of the distance information to see if there are some spatial patterns in the data in terms of accessibility levels:

```python
buildings.plot(
    column="distance",
    markersize=0.2,
    alpha=0.5,
    figsize=(10, 10),
    scheme="quantiles",
    k=4,
    legend=True,
)
```

_**Figure 6.39**. ADD PROPER FIGURE CAPTION!._

Okay, as we can see, there are some clear spatial patterns in the levels of access to public transport. The buildings with the shortest distances (i.e. best accessibility) are located in the densely populated areas, whereas the buildings locating in the periferial areas (such as islands on the South, and nature areas in the North-West) tend to have longer distance to public transport. 


### Are the results correct? Validation

As a final step, it's good to ensure that our functions are working as they should. This can be done easily by examining the data visually.

- Let's first create LineStrings between the building and closest stop points:

```python
from shapely.geometry import LineString

# Create a link (LineString) between building and stop points
buildings["link"] = buildings.apply(
    lambda row: LineString([row["geometry"], row["closest_stop_geom"]]), axis=1
)

# Set link as the active geometry
building_links = buildings.copy()
building_links = building_links.set_geometry("link")
```

- Let's now visualize the building points, stops and the links, and zoom to certain area so that we can investigate the results, and confirm that everything looks correct.

```python
# Plot the connecting links between buildings and stops and color them based on distance
ax = building_links.plot(
    column="distance",
    cmap="Greens",
    scheme="quantiles",
    k=4,
    alpha=0.8,
    lw=0.7,
    figsize=(13, 10),
)
ax = buildings.plot(ax=ax, color="yellow", markersize=1, alpha=0.7)
ax = stops.plot(ax=ax, markersize=4, marker="o", color="red", alpha=0.9, zorder=3)

# Zoom closer
ax.set_xlim([24.99, 25.01])
ax.set_ylim([60.26, 60.275])

# Set map background color to black, which helps with contrast
ax.set_facecolor("black")
```

_**Figure 6.40**. ADD PROPER FIGURE CAPTION!._

Voilá, these weird star looking shapes are formed around public transport stops (red) where each link is associated buildings (yellow points) that are closest to the given stop. The color intensity varies according the distance between the stops and buildings. Based on this figure we can conclude that our nearest neighbor search was succesfull and worked as planned.
