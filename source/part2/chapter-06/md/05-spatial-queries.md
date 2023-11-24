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

# Spatial queries

Finding out if a certain point is located inside of an area, or whether a line intersects with another line (or a polygon) are one of the fundamental geospatial operations that are needed when e.g. selecting data for a specific region. These kind of spatial queries relate to {term}`topological spatial relations` which are fundamental constructs that describe how two or more geometric objects relate to each other concerning their position and boundaries. Topological spatial relations can be exemplified by relationships such as *contains*, *touches* and *intersects* ({cite}`Clementini_1994`). In GIS, the topological relations play a crucial role as they enable queries that are less concerned with the exact coordinates or shapes of geographic entities but more focused on their relative arrangements and positions. For instance, regardless of their exact shape or size, a lake *inside* a forest maintains this relationship even if the forest's boundaries or the lake's size change slightly, as long as the lake remains enclosed by the forest. Next, we will learn a bit more details about these topological relations and how to use them for spatial queries in Python.


## Topological spatial relations

Computationally, conducting queries based on topological spatial relations, such as detecting if a point is inside a polygon can be done in different ways, but most GIS software rely on something called {term}`Dimensionally Extended 9-Intersection Model` ([DE-9IM](https://en.wikipedia.org/wiki/DE-9IM) [^DE-9IM]). DE-9IM is an ISO approved standard and a fundamental framework in GIS that is used to describe and analyze spatial relationships between geometric objects ({cite}`Clementini_1993`). DE-9IM defines the topological relations based on the interior, boundary, and exterior of two geometric shapes and how they intersect with each other (see **Figure 6.XX and Figure 6.XX**). The model also takes into account the dimensionality of the objects: The Point objects are 0-dimensional, LineString and LinearRing are 1-dimensional and Polygons are 2-dimensional. Considering the dimensionality of geometric objects in the DE-9IM model is important because it determines the nature of spatial relations, influences the complexity of interactions between objects, and defines topological rules.

![_**Figure 6.XX**. Interior, boundary and exterior for different geometric data types. The data types can be either 0, 1 or 2-dimensional._](../img/DE-9IM_topology_interior_boundary_exterior.png)

_**Figure 6.XX**. Interior, boundary and exterior for different geometric data types. The data types can be either 0, 1 or 2-dimensional._


By examining the intersections of the interior, boundary and exterior of two geometric objects, a detailed characterization of their spatial relationship can be achieved. One can for instance test whether a given Point or LineString is *within* a Polygon (returning True or False). When testing how two geometries relate to each other, the DE-9IM model gives a result which is called {term}`spatial predicate`. The **Figure 6.XX** shows eight common spatial predicates based on the spatial relationship between the geometries ({cite}`Egenhofer_1992`). Many of these predicates, such as *intersects*, *within*, *contains*, *overlaps* and *touches* are commonly used when selecting data for specific area of interest or when joining data from one dataset to another based on the spatial relation between the layers. 

![_**Figure 6.XX**. Eight common spatial predicates formed based on spatial relations between two geometries. Modified after Egenhofer et al. (1992)_.](../img/spatial-relations.png)

_**Figure 6.XX**. Eight common spatial predicates formed based on spatial relations between two Polygon geometries. Modified after Egenhofer et al. (1992)_.


The top row of the **Figure 6.XX** shows spatial predicates in which the geometries A and B are clearly disjoint from each other, contained or within each other, or identical to each other. When the geometries have at least one point in common, the geometries are said to be *intersecting* with each other. Thus, in this figure, all the comparisons except the first one (disjoint) are True, i.e. the geometries *intersect* with each other. The bottom row shows examples of spatial relationships that are slightly "special cases" in one way or another. When two geometries *touch* each other, they have at least one point in common (at the border in this case), but their interiors do not intersect with each other. When the interiors of the geometries A and B are partially on top of each other and partially outside of each other, the geometries are *overlapping* with each other. The spatial predicate for *covers* is when the interior of geometry B is almost totally within A, except at least one common coordinate at the border. Similarly, if geometry A is almost totally contained by the geometry B (except at least one common coordinate at the border) the spatial predicate is called *covered by*. These eight examples represent some of the common spatial predicates based on two Polygon shapes. When other shapes are considered (e.g. Points, LineStrings), there are plenty of more topological relations: altogether 512 with 2D data.


## Making spatial queries in Python

Now as we know the basics of topological spatial relations, we can proceed and see how to make such spatial queries using Python. Luckily, we do not need to worry about the exact DE-9IM implementation ourselves, as these functionalities are already implemented to shapely and geopandas libraries. With these libraries, we can evaluate the topolocical relationship between geographical objects easily and efficiently. In Python, all the basic spatial predicates listed in **Figure 6.XX** are available from shapely library, including:
 
 - `.intersects()`
 - `.within()`
 - `.contains()`
 - `.overlaps()`
 - `.touches()`
 - `.covers()`
 - `.covered_by()`
 - `.equals()`
 - `.disjoint()`
 - `.crosses()`

When you want to use Python to find out how two geometric objects are related to each other topologically, you start by creating the geometries using shapely library. In the following, we create a couple of `Point` objects and one `Polygon` object which we can use to test how they relate to each other: 

```python
from shapely.geometry import Point, Polygon

# Create Point objects
point1 = Point(24.952242, 60.1696017)
point2 = Point(24.976567, 60.1612500)

# Create a Polygon
coordinates = [
    (24.950899, 60.169158),
    (24.953492, 60.169158),
    (24.953510, 60.170104),
    (24.950958, 60.169990)
]
polygon = Polygon(coordinates)

# Print the objects
print(point1)
print(point2)
print(polygon)
```

<!-- #region deletable=true editable=true jupyter={"outputs_hidden": false} -->
If you want to test whether these `Point` geometries stored in `point1` and `point2` are within the `polygon`, you can call the `.within()` method as follows:
<!-- #endregion -->

```python
point1.within(polygon)
```

```python
point2.within(polygon)
```

As we can see, the first point seem to be located within the polygon where as the second one does not. In a similar manner, you can test all different spatial predicates and assess the spatial relationship between the geometries. The following prints results for all predicates between the `point1` and the `polygon`: 

```python
print("Intersects?", point1.intersects(polygon))
print("Within?", point1.within(polygon))
print("Contains?", point1.contains(polygon))
print("Overlaps?", point1.overlaps(polygon))
print("Touches?", point1.touches(polygon))
print("Covers?", point1.covers(polygon))
print("Covered by?", point1.covered_by(polygon))
print("Equals?", point1.equals(polygon))
print("Disjoint?", point1.disjoint(polygon))
print("Crosses?", point1.crosses(polygon))
```

By going through all the spatial predicates, we can see that the spatial relationship between our point and polygon object produces three `True` values: The point and polygon intersect with each other, the point is within the polygon, and the point is covered by the polygon. All the other tests correctly produce `False`, which matches with the logic of the `DE-9IM` standard. 

It is good to notice that some of these spatial predicates are closely related to each other. For example, the `.within()` and `covered_by()` in our tests produce similar result with our data. Also `.contains()` is closely related to `within()`. Our `point1` was within the `polygon`, but we can also say that the `polygon` contains `point1`. Hence, both tests produce the same result, but the logic for the relationship is inverse. Which one should you use then? Well, it depends:

-  if you have many points and just one polygon and you try to find out which one of them is inside the polygon: You might need to iterate over the points and check one at a time if it is `.within()` the polygon.
-  if you have many polygons and just one point and you want to find out which polygon contains the point: You might need to iterate over the polygons until you find a polygon that `.contains()` the point specified (assuming there are no overlapping polygons).


One of the most common spatial queries is to see if a geometry intersects or touches another one. Again, there are binary operations in shapely for checking these spatial relationships:

- `.intersects()` - Two objects intersect if the boundary or interior of one object intersect in any way with the boundary or interior of the other object.
- `.touches()` - Two objects touch if the objects have at least one point in common and their interiors do not intersect with any part of the other object.
   
Let's try these by creating two `LineString` geometries and test whether they intersect and touch each other:

```python deletable=true editable=true
from shapely.geometry import LineString, MultiLineString

# Create two lines
line_a = LineString([(0, 0), (1, 1)])
line_b = LineString([(1, 1), (0, 2)])
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
line_a.intersects(line_b)
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
line_a.touches(line_b)
```

<!-- #region deletable=true editable=true -->
As we can see, it seems that our two `LineString` objects are both intersecting and touching each other. We can confirm this by plotting the features together as a `MultiLineString`:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Create a MultiLineString from line_a and line_b
multi_line = MultiLineString([line_a, line_b])
multi_line
```

<!-- #region deletable=true editable=true -->
_**Figure 6.XX**. Two LineStrings that both intersect and touch each other._

As we can see, the lines `.touch()` each other because `line_b` continues from the same node ( (1,1) ) where the `line_a` ends.
However, if the lines are fully overlapping with each other they don't touch due to the spatial relationship rule in the DE-9IM. We can confirm this by checking if `line_a` touches itself:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
line_a.touches(line_a)
```

<!-- #region deletable=true editable=true -->
It does not. However, the `.intersects()` and `.equals()` should produce `True` for a case when we compare the `line_a` with itself:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
print("Intersects?", line_a.intersects(line_a))
print("Equals?", line_a.equals(line_a))
```

## Spatial queries using geopandas

Next we will do a practical example where we check which of the addresses from [the geocoding tutorial](geocoding_in_geopandas.ipynb) are located in Southern district of Helsinki. Let's start by reading a KML-file ``PKS_suuralue.kml`` that has the Polygons for districts of Helsinki Region (data openly available from [Helsinki Region Infoshare](http://www.hri.fi/fi/dataset/paakaupunkiseudun-aluejakokartat).

Let's start by reading the addresses from the Shapefile that we saved earlier.

```python deletable=true editable=true
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd

fp = "data/Helsinki/addresses.shp"
data = gpd.read_file(fp)

data.head()
```

<!-- #region deletable=true editable=true -->


It is possible to read the data from KML-files with GeoPandas in a similar manner as Shapefiles. However, we need to first, enable the KML-driver which is not enabled by default (because KML-files can contain unsupported data structures, nested folders etc., hence be careful when reading KML-files). Supported drivers are managed with a library called `fiona` that `geopandas` uses in the background to read files. Let's first check which formats are currently supported by calling [`fiona.supported_drivers`](https://github.com/Toblerity/Fiona/blob/master/fiona/drvsupport.py):
<!-- #endregion -->

```python
import geopandas as gpd
import fiona

fiona.supported_drivers
```

- Let's enable the read and write functionalities for KML-driver by passing ``'rw'`` to whitelist of fiona's supported drivers:

```python deletable=true editable=true
fiona.supported_drivers["KML"] = "rw"
```

Let's check again the supported drivers:

```python
fiona.supported_drivers
```

<!-- #region deletable=true editable=true -->
Now we should be able to read a KML file using the geopandas [read_file()](http://geopandas.org/reference/geopandas.read_file.html#geopandas.read_file) function.

- Let's read district polygons from a KML -file that is located in the data-folder:
<!-- #endregion -->

```python deletable=true editable=true
# Filepath to KML file
fp = "data/Helsinki/PKS_suuralue.kml"
polys = gpd.read_file(fp, driver="KML")
```

```python
# Check the data
print("Number of rows:", len(polys))
polys.head(11)
```

Nice, now we can see that we have 23 districts in our area. 
Let's quickly plot the geometries to see how the layer looks like: 

```python
polys.plot()
```

<!-- #region deletable=true editable=true -->
_**Figure 6.28**. ADD PROPER FIGURE CAPTION!._

We are interested in an area that is called ``Eteläinen`` (*'Southern'* in English).

Let's select the ``Eteläinen`` district and see where it is located on a map:

<!-- #endregion -->

```python
# Select data
southern = polys.loc[polys["Name"] == "Eteläinen"]
```

```python
# Reset index for the selection
southern.reset_index(drop=True, inplace=True)
```

```python
# Check the selction
southern.head()
```

- Let's create a map which shows the location of the selected district, and let's also plot the geocoded address points on top of the map:

```python deletable=true editable=true
import matplotlib.pyplot as plt

# Create a figure with one subplot
fig, ax = plt.subplots()

# Plot polygons
polys.plot(ax=ax, facecolor="gray")
southern.plot(ax=ax, facecolor="red")

# Plot points
data.plot(ax=ax, color="blue", markersize=5)

plt.tight_layout()
```

<!-- #region deletable=true editable=true -->
_**Figure 6.29**. ADD PROPER FIGURE CAPTION!._

Okey, so we can see that, indeed, certain points are within the selected red Polygon.

Let's find out which one of them are located within the Polygon. Hence, we are conducting a **Point in Polygon query**.

First, let's check that we have  `shapely.speedups` enabled. This module makes some of the spatial queries running faster (starting from Shapely version 1.6.0 Shapely speedups are enabled by default):
<!-- #endregion -->

```python deletable=true editable=true
# import shapely.speedups
from shapely import speedups

speedups.enabled

# If false, run this line:
# shapely.speedups.enable()
```

<!-- #region deletable=true editable=true -->
- Let's check which Points are within the ``southern`` Polygon. Notice, that here we check if the Points are ``within`` the **geometry**
  of the ``southern`` GeoDataFrame. 
- We use the ``.at[0, 'geometry']`` to parse the actual Polygon geometry object from the GeoDataFrame.
<!-- #endregion -->

```python deletable=true editable=true
pip_mask = data.within(southern.at[0, "geometry"])
print(pip_mask)
```

<!-- #region deletable=true editable=true -->
As we can see, we now have an array of boolean values for each row, where the result is ``True``
if Point was inside the Polygon, and ``False`` if it was not.

We can now use this mask array to select the Points that are inside the Polygon. Selecting data with this kind of mask array (of boolean values) is easy by passing the array inside the ``loc`` indexer:

<!-- #endregion -->

```python deletable=true editable=true
pip_data = data.loc[pip_mask]
pip_data
```

<!-- #region deletable=true editable=true -->
Let's finally confirm that our Point in Polygon query worked as it should by plotting the points that are within the southern district:
<!-- #endregion -->

```python deletable=true editable=true
# Create a figure with one subplot
fig, ax = plt.subplots()

# Plot polygons
polys.plot(ax=ax, facecolor="gray")
southern.plot(ax=ax, facecolor="red")

# Plot points
pip_data.plot(ax=ax, color="gold", markersize=2)

plt.tight_layout()
```

<!-- #region deletable=true editable=true -->
_**Figure 6.30**. ADD PROPER FIGURE CAPTION!._

Perfect! Now we only have the (golden) points that, indeed, are inside the red Polygon which is exactly what we wanted!
<!-- #endregion -->

## Footnotes

[^DE-9IM]: <https://en.wikipedia.org/wiki/DE-9IM>
