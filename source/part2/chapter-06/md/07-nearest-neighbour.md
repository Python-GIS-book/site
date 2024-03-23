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


![_**Figure 6.43**. The basic idea of finding a nearest neighbour based on geographic distance.](../img/nearest-neighbour.png)

_**Figure 6.43**. The basic idea of finding a nearest neighbour based on geographic distance._


Quite often with very large datasets, we might want to limit the search area up to a specific maximum distance. This can be due to practical reasons as it can significantly speed up the computation time, or because we have specific reasoning that makes it sensible to limit the search area. For example, if we would aim to understand how easily accessible public transportation is to citizens living in a city, it would make sense to limit the search area e.g. up to 2 km from the homes of people, because people are not willing to walk for very long distances to get into a bus stop. It's important to notice that the distances in the calculations are commonly based on the Euclidian distance, i.e. we calculate the distances based on coordinates on a Cartesian plain, meaning that the distances do not consider changes in height (i.e. third dimension is omitted). It is of course possible also to consider 3D distances, but the most typical Python tools ignore the height information. 


## Nearest neighbour analysis in Python

In Python, there are various libraries that can be used to find nearest neighbors for given set of geometries, including `geopandas`, `shapely`, `scipy`, `scikit-learn`, and `pysal` among others. Here, we first introduce how `geopandas` can be used to find the nearest neighbors for all Point geometries in a given GeoDataFrame based on Points in another GeoDataFrame. Then we show how to find nearest neighbor between two Polygon datasets, and finally we show how to use `scipy` library to find K-Nearest Neighbors (KNN) with Point data.


In the following, we go through a very practical example that relates to our daily commute: Where is the closest public transport stop from my place of living? Hence, our aim is to search for each building point in the Helsinki Region the closest public transport stop. In geopandas, we can find nearest neighbors for all geometries in a given GeoDataFrame very easily by using a method called `.sjoin_nearest()`. To show how to use this method, let's start by reading two datasets representing buildings and stops into GeoDataFrames, and visualize them to understand a bit better what we have:

```python
import geopandas as gpd
import matplotlib.pyplot as plt

stops = gpd.read_file("data/Helsinki/pt_stops_helsinki.gpkg")
building_points = gpd.read_file("data/Helsinki/building_points_helsinki.zip")

print("Number of stops:", len(stops))
stops.head(2)
```

```python
print("Number of buildings:", len(building_points))
building_points.head(2)
```

As we can see, both GeoDataFrames contain Point geometries. There seems to be approximately 8400 stops and almost 159 thousand buildings in our data. Hence, we have already a fair amount of data and calculations to do, to find the nearest neighbor for each building. Let's still visualize the GeoDataFrames next to each other so that we can see them on a map:

```python
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 10))

# Plot buildings
building_points.plot(ax=ax1, markersize=0.2, alpha=0.5)
ax1.set_title("Buildings")

# Plot stops
stops.plot(ax=ax2, markersize=0.2, alpha=0.5, color="red")
ax2.set_title("Stops");
```

_**Figure 6.44**. Maps representing the buildings and public transport stops which we use to find the closest stop for each building._

As mentioned earlier, finding the nearest geometries between two GeoDataFrames (here building and stop points) can be done easily using the `.sjoin_nearest()` method in geopandas. As the name implies, this method is actually designed to merge data between GeoDataFrames in a similar manner as with regular `.sjoin()` method that we saw earlier in Chapter 6.7. However, in this case the method is actually searching for the closest geometries instead of relying on spatial predicates, such as *within*. The `sjoin_nearest()` can be used for different geometry types, so the input geometries do not necessarily need to be Point objects as in our example. Under the hood, the method uses a *{term}`spatial index`* called `STRTree` ({cite}`leutenegger_1997`) which is an efficient implementation of the *{term}`R-tree`* dynamic index structure for spatial searching ({cite}`guttman_1984`). The STRTree is implemented in the `shapely` library (used by geopandas) and the technique makes the nearest neighbor queries very efficient. You can read more about spatial indices in Appendices section of the book. For the method to work properly, it is recommended to ensure that the both GeoDataFrames are having the same coordinate reference system (CRS), and preferably having a projected (metric) CRS because that ensures that the reported distances are meaningful (in meters) and correct. Hence, let's start by reprojecting our latitude and longitude values into a metric system using the national EUREF-FIN coordinate reference system (EPSG code 3067) for Finland:

```python
stops = stops.to_crs(epsg=3067)
building_points = building_points.to_crs(epsg=3067)

stops.head(2)
```

Now the GeoDataFrames are surely in the same coordinate system and we can see that the coordinates in the `geometry` column have changed representing meters. Next, we will use the `buildings.sjoin_nearest()` to find the closest stop for each building. Because we are interested to find the closest stop geometry for each building, the `buildings` GeoDataFrame is the left hand side of the command. As inputs, we pass the `stops` GeoDataFrame as well as give a name for a column which is used to store information about the distance between a given building and the closest stop (this is optional):

```python
%time
closest = building_points.sjoin_nearest(stops, distance_col="distance")
closest
```

As a result, we now have found the closest stop for each building including the attributes of the closest stops that were merged into the results. The last column in the table shows the distance in meters between a given building and the closest stop. The distance is only returned upon request as we did by specifying `distance_col="distance"`. The column `index_right` provides information about the index number of the closest stop in the `stops` GeoDataFrame. If you look carefully, you can see that the number of rows in our result has actually increased slightly from the original (158731 vs 159818). This happens because for some geometries in the `buildings` GeoDataFrame, the distance between the building and two (or more) stops have been exactly the same (i.e. they are equidistant). In such cases, the `sjoin_nearest()` will store both records into the results by duplicating the building information and attaching information from the stops into separate rows accordingly. In some cases, this can cause trouble for further analysis, so it is good to be careful and investigate whether any duplicate buildings have emerged into the results. If they have emerged, and if this causes issues in your analysis, you might need to pick one of them based on some criteria. Alternatively, you can just pick the first (or last) one if you do not have any specific justification for making the selection.

The `%time` command at the beginning of the cell provides us some details about the time it took to find the nearest neighbors and merge the data between the two GeoDataFrames. As we can see, the computations are very efficient taking only a matter of some microseconds for almost 159 thousand observations. We can make this even faster by specifying a `max_distance` parameter that specifies the maximum search distance. Here, we specify the maximum distance as 100 meters from each building:

```python
%time
closest_limited = building_points.sjoin_nearest(stops, max_distance=100, distance_col="distance")
closest_limited
```

As we can see, there was a slight improvement in the execution time compared to the previous call without specifying the `max_distance` parameter. The difference can be more significant if you have larger datasets or more complicated geometries (e.g. Polygons). One important aspect to notice from these results is that the number of rows has decreased significantly: from 160 to 40 thousand buildings. This happens because our search distance was very low (100 meters), and as a consequence, there were many buildings that did not have any stops within 100 meter radius from them. Because the default join type in `sjoin_nearest` is `inner` join, all the records that did not have a stop within 100 meters were dropped. If you would like to keep all the records in the results, to e.g. investigate which buildings do not have any stops within the search radius, you can add parameter `how="left"`, which will retain all buildings from the original GeoDataFrame.

In some cases, you might actually want to connect the nearest neighbors to each other with a straight line. For doing this, we need to merge also the Point geometries from the other layer into our results, which can then be used to create a LineString connecting the points to each other. This can be useful for many purposes, but in our case, we want to do this to be able to validate whether our results are correct. For merging the closest stop geometries into our results, we can take advantage of the `index_right` column in our table and conduct a normal table join using the `.merge()` method. Below, we first store the index of the `stops` GeoDataFrame into a column called `stop_index` and then use this to make a table join with our `closest` GeoDataFrame. Notice that we only keep the `stop_index` and `geometry` columns from the `stops` GeoDataFrame because all the other attributes already exist in our results: 

```python
stops["stop_index"] = stops.index
closest = closest.merge(stops[["stop_index", "geometry"]], left_on="index_right", right_on="stop_index")
closest.head()
```

As a result, we now brought two new columns into our results, namely `stop_index` and `geometry_y`. Because there was a column called `geometry` in both GeoDataFrames, geopandas automatically renamed the columns into `geometry_x` and `geometry_y` respectively. Now we have all the data that we need to create a connecting `LineString` between the buildings and the closest stops. We can do this by looping over the rows in our `closest` GeoDataFrame using the `.apply()` method (see Chapter 3.3 for more details) and then create the line by calling the shapely's `LineString` object which takes the Point geometries as input. We store these LineStrings into a column `geometry` which we lastly set to be the active geometry of the GeoDataFrame:    

```python
from shapely import LineString
closest["geometry"] = closest.apply(lambda row: LineString([row["geometry_x"], row["geometry_y"]]), axis=1)
closest = closest.set_geometry("geometry")
closest.head()
```

Great! Now we have created a new geometry column that contains the lines between buildings and the closest stops. To better understand the results, let's create a nice map that visualizes the buildings, stops and the connecting lines between the buildings and the closest stops in a single figure: 

```python
ax = closest.plot(lw=0.5, figsize=(10,10))
ax = building_points.plot(ax=ax, color="red", markersize=2)
ax = stops.plot(ax=ax, color="black", markersize=8.5, marker="s")
# Zoom to specific area
ax.set_xlim(382000, 384100)
ax.set_ylim(6676000, 6678000);
```

_**Figure 6.45**. A map showing the buildings (red points), the stops (black rectangles) and the lines between the buildings and the closest stops._

As we can see from the Figure 6.45, the nearest neighbor search have worked well as planned, and each building marked with red color has been correctly connected with a line to the closest stop. The map reveals that there are multiple isolated stops that do not have any buildings connected to them. As a practical example, this information could be used e.g. for transport planning by investigating whether these isolated stops are less used by citizens to get on board of the public transport vehicles. This information could again be used by transport planners to decide whether there is a need to maintain these isolated stops. Thus, with these rather simple computations, one can already provide useful information that has relevance in real life. Finally, because we have calculated the distance between buildings and the stops, it is easy to do some descriptive analysis based on this data providing information about levels of access to public transport in the region: 

```python
closest["distance"].describe()
```

As we can see, the average distance to public transport in the region is around 230 meters. More than 75 % of the buildings seem to be within within 3.5 minute walking time (~260 meters with walking speed of 4.5 kmph) which indicates very good situation in terms of accessibility levels in the region overall. There seem to be some really remote buildings in the data as well, as the longest distance to closest public transport stop is more than 7 kilometers.


### Nearest neighbors with Polygon and LineString data

In some cases, you might need to find the closest neighbors for a given set of Polygons or LineStrings. Luckily, the `sjoin_nearest()` method works in a similar manner with all geometry types, i.e. you can find the nearest neighbors using Point, LineString, Polygon, MultiPoint, MultiLineString and MultiPoint geometries as input. Also finding nearest neighbors between different geometry types is supported, meaning that you can for example search nearest LineStrings to Polygons, and so on. When using more complex geometries as input (e.g. LineStrings or Polygons), the nearest neighbor search uses spatial index, i.e. it creates bounding boxes around the input geometries and inserts them into an R-Tree which is used to make the search queries more efficient. However, the distance between the nearest neighbours is measured based on the true shapes of the geometric features. In the following, we demonstrate how to conduct nearest neighbor analysis with more complex geometries, such as Polygons and LineStrings.

As a real-life case, we first aim to find the closest urban park to building polygons in a neighborhood called Kamppi, which is located in Helsinki, Finland. Then, we aim to find the closest drivable road (LineString) to each building. Let's start by reading the data and visualize it on a map:

```python
import geopandas as gpd

buildings = gpd.read_file("data/Helsinki/Kamppi_buildings.gpkg")
parks = gpd.read_file("data/Helsinki/Kamppi_parks.gpkg")
roads = gpd.read_file("data/Helsinki/Kamppi_roads.gpkg")
buildings
```

```python
# Plot buildings, parks and roads
ax = buildings.plot(color="gray", figsize=(10,10))
ax = parks.plot(ax=ax, color="green")
ax = roads.plot(ax=ax, color="red")
```

_**Figure 6.46**. A map showing the buildings with gray color and the parks (green) in the neighborhood of Kamppi, Helsinki._

Similarly as finding the nearest neighbor using Points as input data, we can use the `.sjoin_nearest()` to find nearest neighbor between two Polygon datasets. Here, we find the nearest park for each building Polygon and store the distance into the column `distance`:

```python
nearest_parks = buildings.sjoin_nearest(parks, distance_col="distance")
nearest_parks
```

```python
print("Maximum distance:", nearest_parks["distance"].max().round(0))
print("Average distance:", nearest_parks["distance"].mean().round(0))
```

Now we have found the nearest park for each building, and as we can see on average the closest park seem to be 61 meters away from the buildings while the longest distance from one of the buildings to the closest park seems to be 229 meters. In a simimar, manner we can also find the nearest road from each building as follows:

```python
nearest_roads = buildings.sjoin_nearest(roads, distance_col="distance")
nearest_roads
```

As a result, we now have found the nearest road for each building. We have now 703 rows of data which means that for some buildings there have been more than one road that are exactly the same distance apart. To better understand how the spatial join between the buildings and roads have been conducted, we can again visualize the nearest neighbors with a straight line. To do this, we first bring the geometries from the `roads` GeoDataFrame into the same table with the buildings: 

```python
roads["index"] = roads.index
nearest_roads = nearest_roads.merge(roads[["geometry", "index"]], left_on="index_right", right_on="index")
nearest_roads.head()
```

Now we have the `geometry_x` column representing the building geometries and the `geometry_y` column representing the road geometries (LineStrings). To visualize the connecting lines between buildings and roads, we first need to create geometries that connect the building and closest road geometry from the locations where the distance is shortest. To do this, we can take advantage of a handy function called `nearest_points()` from the `shapely` library that returns a list of Point objects representing the locations with shortest distance between geometries. By using these points as input, we can create a LineString geometries that represent the connector between a given building and the closest road. Finally, we create a new GeoDataFrame called `connectors` out of these lines and also store the length of the LineStrings as a separate column:

```python
from shapely.ops import nearest_points

# Generate LineString between nearest points of two geometries
connectors = nearest_roads.apply(lambda row: LineString(nearest_points(row["geometry_x"], row["geometry_y"])), axis=1)

# Create a new GeoDataFrame out of these geometries 
connectors = gpd.GeoDataFrame({"geometry": connectors}, crs=roads.crs)
connectors["distance"] = connectors.length
connectors.head()
```

Great, now we have a new GeoDataFrame that represents the connectors between the buildings and the drivable roads. Finally, we can visualize the buildings, roads and these connectors to better understand the exact points where the distance between a given building and the closest road is shortest:

```python
m = buildings.explore(color="gray", tiles="CartoDB Positron")
m = roads.explore(m=m, color="red")
m = connectors.explore(m=m, color="green")
m
```

_**Figure 6.47**. A map showing the closest road for each building. The LineStrings marked with green color show the exact location where the distance between a given building and the road is shortest._


## K-Nearest Neighbor search

Thus far, we have only focused on finding the nearest neighbor to a given geometry. However, quite commonly you might want to find not only the closest geometry, but a specific number of closest geometries to a given location. For example, you might be interested to find 3-5 closest public transport stops from your home, because these stops might provide alternative connections to different parts of the city. Doing these kind of queries is actually quite common procedure for many data analysis techniques, and it is commonly called as *{term}`K-Nearest Neighbors search`* (or KNN search). Next, we will learn how to find *k* number of closest neighbors based on two GeoDataFrames. We will first aim to find the three nearest public transport stops for each building in the Helsinki Region, and then we will see how to make a *{term}`radius query`* to find all neighbors within specific distance apart from a given location. K-Nearest Neighbor search techniques are also typically built on top of *{term}`spatial indices <spatial index>`* to make the queries more efficient. Previously with `sjoin_nearest()`, we used an `R-tree` index structure to efficiently find the nearest neighbor for any kind of geometry. Because the R-tree implementation only supports finding the closest neighbor (similarly to other software relying on GEOS), we need to use another tree structure called *{term}`KD-tree`* that can provide us information about k-nearest neighbors (i.e. not only the closest). KD-tree is similar to R-tree, but the data is ordered and sorted in a bit different manner to make the spatial search operations faster (see Appendices for further details). 



```python
building_points.head()
```

```python
stops.head()
```

```python
from scipy.spatial import cKDTree
```

```python
building_coords = building_points.get_coordinates().to_numpy()
stop_coords = stops.geometry.get_coordinates().to_numpy()
```

```python
stop_coords
```

```python
stop_kdt = cKDTree(stop_coords)
```

```python
# Find the three nearest neighbors from stop KD-Tree for each building
k_nearest_dist, k_nearest_ix = stop_kdt.query(building_coords, k=3)
```

```python
k_nearest_dist
```

```python
k_nearest_ix
```

```python
k_nearest_ix.T[0]
```

```python
k_nearest = building_points.copy()
```

```python
# Add indices of nearest stops
k_nearest["1st_nearest_idx"] = k_nearest_ix.T[0]
k_nearest["2nd_nearest_idx"] = k_nearest_ix.T[1]
k_nearest["3rd_nearest_idx"] = k_nearest_ix.T[2]

# Add distances 
k_nearest["1st_nearest_dist"] = k_nearest_dist.T[0]
k_nearest["2nd_nearest_dist"] = k_nearest_dist.T[1]
k_nearest["3rd_nearest_dist"] = k_nearest_dist.T[2]
```

```python
k_nearest.head()
```

```python
stops["stop_index"] = stops.index
```

```python
# Merge the geometries of the nearest stops to the GeoDataFrame
k_nearest_1 = k_nearest.merge(stops[["stop_index", "geometry"]], left_on="1st_nearest_idx", right_on="stop_index", suffixes=('', '_knearest'))
k_nearest_1.head(2)
```

```python
# Merge the geometries of the 2nd nearest stops to the GeoDataFrame
k_nearest_2 = k_nearest.merge(stops[["stop_index", "geometry"]], left_on="2nd_nearest_idx", right_on="stop_index", suffixes=('', '_knearest'))
k_nearest_2.head(2)
```

```python
# Merge the geometries of the 3rd nearest stops to the GeoDataFrame
k_nearest_3 = k_nearest.merge(stops[["stop_index", "geometry"]], left_on="3rd_nearest_idx", right_on="stop_index", suffixes=('', '_knearest'))
k_nearest_3.head(2)
```

```python
from shapely import LineString

# Generate LineStrings connecting the building point and K-nearest neighbor
k_nearest_1["geometry"] = k_nearest_1.apply(lambda row: LineString([ row["geometry"], row["geometry_knearest"] ]), axis=1)
k_nearest_2["geometry"] = k_nearest_2.apply(lambda row: LineString([ row["geometry"], row["geometry_knearest"] ]), axis=1)
k_nearest_3["geometry"] = k_nearest_3.apply(lambda row: LineString([ row["geometry"], row["geometry_knearest"] ]), axis=1)
```

```python
# Find unique building names
k_nearest.name.unique()
```

```python
# Visualize 3 nearest stops to
selected_name = "Hartwall Arena"

m = k_nearest_1.loc[k_nearest_1["name"]==selected_name].explore(color="red", tiles="CartoDB Positron", max_zoom=16)
m = k_nearest_2.loc[k_nearest_2["name"]==selected_name].explore(m=m, color="orange")
m = k_nearest_3.loc[k_nearest_3["name"]==selected_name].explore(m=m, color="blue")
m = stops.explore(m=m, color="green")
m
```

## Range search

```python
# Find the three nearest neighbors from stop KD-Tree for each building
k_nearest_ix = stop_kdt.query_ball_tree(building_kdt, r=200)
```

```python
len(k_nearest_ix)
```

```python
k_nearest_ix[0]
```

```python
stops.head()
```

```python
stops["building_ids_within_range"] = k_nearest_ix
```

```python
stops.head()
```

```python
stops["building_cnt"] = stops["building_ids_within_range"].apply(lambda id_list: len(id_list))
```

```python
stops.head()
```

```python
print("Max number of buildings:", stops["building_cnt"].max())
print("Average number of buildings:", stops["building_cnt"].mean().round(1))
```

```python
stops.loc[stops["building_cnt"] == stops["building_cnt"].max()].explore(tiles="CartoDB Positron", color="red", marker_kwds={"radius": 5}, max_zoom=16)
```

```python

```
