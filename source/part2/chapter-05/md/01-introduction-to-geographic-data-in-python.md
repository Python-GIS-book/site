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

# Introduction to geographic data in Python

How do we represent geographic features such as roads, buildings, lakes or mountains on a computer? How can we analyze spatial relations between these features? How can we link abstract geometric objects to actual locations on the Earth? What is the difference between geographic and projected coordinate reference systems? How can we automate GIS operations or analyses in Python? This chapter introduces you to the basic concepts and approaches related to Geographic Information Systems (GIS) and spatial data analysis. Geographers and GIS professionals might already be familiar with most of these concepts, but we hope this section helps beginners to grasp the basic concepts essential to understad the approached presented in this part of the book.


## Ways to represent spatial data on a computer

To be able to work with real world geographic objects (such as roads or lakes) on a computer, we need to represented them in a format that the computer can understand and work with. These representations are simplifications of the real world which are typically represented either with **vector** or **raster** *{term}`data model`*. Vector and raster data formats are very different by nature. Figure 5.2 shows how physical objects, such as roads and buildings, can be represented as vectors or rasters. In addition, there are other models which *extend* the previous ones, such as *{term}`spatio-temporal data model`* which incorporates time as one additional dimension to the geographic dimension. There are also models that *integrate* vector or raster data models, such as *{term}`topological data model`* which is typically build around vector data. This model can be used to represent e.g. street **networks** in a way that the topological relationships are incorporated in the core model design, which happens to be very useful for example when aiming to find a shortest route between two locations. 

The vector representation of the road and building features (shown on the left in Figure 5.2) are constructed from points in geographical space which are connected to each other forming lines and polygons. The subplots on the right, shows raster representations of the same features. They are constructed from rectangular cells (also called as pixels) that form a uniform grid, i.e. a raster. The grid is associated to specific geographical location and each cell of the grid contains a value representing some information, such as elevation, temperature or presence/absence (as in this figure). The cell size of the grid can vary. For example, the top-right subplot represents the roads with 10 meter *{term}`spatial resolution`*, i.e. the size of an individual cell is 10 by 10 meters, whereas the bottom-right subplot represents the buildings with 1 meter spatial resolution. When working with raster data, the spatial resolution is an important aspect, because it determines how accurately the real-world entities, such as buildings, can be represented or identified from the data. Lastly, the roads on the top-left could be represented as a network, which is a vector-based data structure consisting of intersections (called *nodes*) that are represented as points, and streets connecting the nodes that are represented as lines (called *edges*). Because the vector and raster data models are very different, there are typically a different set of GIS tools and methodologies applied for raster and vector data. However, the vector and raster worlds are not totally isolated from each other, as in many cases it is useful to convert the data from one format to another for specific operations, as has been done in Figure 5.2.
 
![_**Figure 5.2.** Vector and raster representations of roads and buildings._](../img/vector_vs_raster.jpg)

_**Figure 5.2.** Vector and raster representations of roads and buildings._

<!-- #region -->
<!---
Vector data can be produced in many ways. 
- Points
- Lines
- Areas (Polygons)
- Collections
- Box
- Sidenote: storing geometry into WKT/WKB
- Surface / field:
  - Raster
  - TIN/Voronoi (tesseleations)
  - Hexagon (H3)
- Networks
-->



## Representing vector geometries with `shapely` 

The most fundamental geometric objects when working with spatial data in vector format are **points**, **lines** and **areas**. Figure 5.3 represents the vector data model and illustrates the variety of geometric objects that are available. `Point` -object represents a single point in geographic space and the location of the point in space is determined with coordinates. Points can be either two-dimensional (with x, y -coordinates) or three dimensional (with x, y, and z coordinates). A single pair of coordinates forming a point is commonly called as *`coordinate`* *{term}`tuple`*. `LineString` -object (i.e. a line) represents a sequence of points joined together to form a line. Hence, a line consist of a list of at least two coordinate tuples. `Polygon` -object represents a filled area that consists of a list of at least three coordinate tuples that forms the outerior ring (called `LinearRing`) and a possible list of holes (as seen in the last plot of Figure 5.3) It is also possible to have a collection of geometric objects (i.e. multiple points, lines or areas) represented as `MultiPoint`, `MultiLineString` and `MultiPolygon` as shown in the bottom row of Figure 5.3. Geometry collections can be useful for example when you want to present multiple building polygons belonging to the same property as a single entity (like a Finnish summer house that typically has a separate sauna building). In addition to these, you might sometimes hear about other geometry objects, such as `Curve`, `Surface` or `GeometryCollection`, but these are basically implemented by the same `Point`, `LineString` and `Polygon` geometry types, hence we don't really use them in practice. 

All of these geometries are defined in *Simple Features Access Specification* {cite}`Herring_2011`, which is a standard (ISO 19125-1) formalized by the *Open Geospatial Consortium* and *International Organization for Standardization*. Most (if not all) programming languages follow this same standard to represent spatial data. The text underneath each geometry (e.g. `Point (25 60.5)`) shows how each of these geometries can be represented as text (Figure 5.3). The way the text is formatted follows a specification called *{term}`Well-known text` (WKT)* which is also defined in the Simple Features Access Specification. The geometries can also be represented in binary format, which is called  *{term}`Well-known binary` (WKB)*. WKB is useful for storing the geometries in a more compact form, but it is not human-readable. Most often, you don't need to worry about these technical details when working with spatial data in Python, but it is useful to know the foundations underlying most (if not all) GIS libraries.

![_**Figure 5.3**. Vector data model._](../img/vector_data_model.jpg)

_**Figure 5.3**. Vector data model._


<!-- #endregion -->

A core Python library for representing vector data in geospatial domain is called shapely [^shapely]. Although `shapely` library can be a bit hidden from most Python GIS user nowadays, it is one of the fundamental dependencies of `geopandas` library which is the go-to library when working with (vector) spatial data in Python. Hence, basic knowledge of shapely is fundamental to understand how geometries are stored and handled in `geopandas`. In the following, we give a quick overview, how to create geometries using `shapely`.


### Point geometries

When creating geometries in Python, we first need to import the geometric object class (such as `Point`) that we want to create from `shapely.geometry` which contains all possible geometry types. After importing the `Point` class, creating a point is easy: we just pass `x` and `y` coordinates into the `Point()` -class (with a possible `z` -coordinate) which will create the point for us:

```python jupyter={"outputs_hidden": false}
from shapely.geometry import Point

point = Point(2.2, 4.2)
point3D = Point(9.26, -2.456, 0.57)

point
```

As we see here, Jupyter notebook is able to display the shape of the `point` directly on the screen when we call it. The point object here is represented as it has been defined in the *Simple Features Access Specification*. Under the hood `shapely` actually uses a C++ library called GEOS [^GEOS] to construct the geometries, which is one of the standard libraries behind various Geographic Information Systems, such as QGIS [^QGIS]. We can use the print statement to get information about the actual definition of these objects:

```python jupyter={"outputs_hidden": false}
print(point)
print(point3D)
```

3D-point can be recognized from the capital Z -letter in front of the coordinates. Extracting the coordinates of a `Point` can be done in a couple of different ways. We can use the `coords` attribute contains the coordinate information as a `CoordinateSequence` which is a specific data type of Shapely. In addition, we can also directly use the attributes `x` and `y` to get the coordinates directly as plain decimal numbers.

```python
list(point.coords)
```

```python jupyter={"outputs_hidden": false}
print(
    point.x,
    point.y
)
```

Points and other shapely objects have many useful built-in attributes and methods [^shapely_methods], such as calculating the Euclidian distance between points or creating a buffer from the point that converts the point into a circle `Polygon` with specific radius. However, all of these functionalities are integrated into `geopandas` and we will go through them later in the book. 


<!-- #region -->
### LineString geometries


Creating LineString -objects is fairly similar to creating Shapely Points. 

Now instead using a single coordinate-tuple we can construct the line using either a list of shapely Point -objects or pass the points as coordinate-tuples:
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
# Create a LineString from our Point objects
line = LineString([point1, point2, point3])
```

```python
# It is also possible to produce the same outcome using coordinate tuples
line2 = LineString([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
```

```python
# Check if lines are identical
line == line2
```

Let's see how our line looks like: 

```python
line
```

```python
print(line)
```

As we can see from above, the `line` -variable constitutes of multiple coordinate-pairs.


Check also the data type:

```python
# Check data type of the line object
type(line)
```

```python
# Check geometry type of the line object
line.geom_type
```

<!-- #region -->
### LineString attributes and functions


`LineString` -object has many useful built-in attributes and functionalities. It is for instance possible to extract the coordinates or the length of a LineString (line), calculate the centroid of the line, create points along the line at specific distance, calculate the closest distance from a line to specified Point and simplify the geometry. See full list of functionalities from [Shapely documentation](http://toblerity.org/shapely/manual.html). Here, we go through a few of them.

We can extract the coordinates of a LineString similarly as with `Point`
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
# Get xy coordinate tuples
list(line.coords)
```

Again, we have a list of coordinate tuples (x,y) inside a list.

If you would need to access all x-coordinates or all y-coordinates of the line, you can do it directly using the `xy` attribute: 

```python jupyter={"outputs_hidden": false}
# Extract x and y coordinates separately
xcoords = list(line.xy[0])
ycoords = list(line.xy[1])
```

```python
print(xcoords)
print(ycoords)
```

It is possible to retrieve specific attributes such as lenght of the line and center of the line (centroid) straight from the LineString object itself:

```python jupyter={"outputs_hidden": false}
# Get the lenght of the line
l_length = line.length
print("Length of our line: {0:.2f} units".format(l_length))
```

```python
# Get the centroid of the line
print(line.centroid)
```

As you can see, the centroid of the line is again a Shapely Point object. 

<!-- #region -->
## Polygon


Creating a `Polygon` -object continues the same logic of how `Point` and `LineString` were created but Polygon object only accepts a sequence of coordinates as input. 

Polygon needs **at least three coordinate-tuples** (three points are reguired to form a surface):
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
# Create a Polygon from the coordinates
poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
```

We can also use information from the Shapely Point objects created earlier, but we can't use the point objects directly. Instead, we need to get information of the x,y coordinate pairs as a sequence. We can achieve this by using a list comprehension.

```python
# Create a Polygon based on information from the Shapely points
poly2 = Polygon([[p.x, p.y] for p in [point1, point2, point3]])
```

In order to understand what just happened, let's check what the list comprehension produces:

```python
[[p.x, p.y] for p in [point1, point2, point3]]
```

This list of lists was passed as input for creating the Polygon.

```python
# Check that polygon objects created using two different approaches are identical
poly == poly2
```

Let's see how our Polygon looks like

```python
poly
```

```python
print(poly)
```

Notice that `Polygon` representation has double parentheses around the coordinates (i.e. `POLYGON ((<values in here>))` ). This is because Polygon can also have holes inside of it. 


Check also the data type:

```python
# Data type
type(poly)
```

```python
# Geometry type
poly.geom_type
```

```python
# Check the help for Polygon objects:
# help(Polygon)
```

<!-- #region -->


As the help of [Polygon](https://shapely.readthedocs.io/en/stable/manual.html#polygons) -object tells, a Polygon can be constructed using exterior coordinates and interior coordinates (optional) where the interior coordinates creates a hole inside the Polygon:

<!-- #endregion -->

```
Help on Polygon in module shapely.geometry.polygon object:
     class Polygon(shapely.geometry.base.BaseGeometry)
      |  A two-dimensional figure bounded by a linear ring
      |
      |  A polygon has a non-zero area. It may have one or more negative-space
      |  "holes" which are also bounded by linear rings. If any rings cross each
      |  other, the feature is invalid and operations on it may fail.
      |
      |  Attributes
      |  ----------
      |  exterior : LinearRing
      |      The ring which bounds the positive space of the polygon.
      |  interiors : sequence
      |      A sequence of rings which bound all existing holes.
      
```


Let's see how we can create a `Polygon` with a hole:

```python
# Define the outer border
border = [(-180, 90), (-180, -90), (180, -90), (180, 90)]
```

```python
# Outer polygon
world = Polygon(shell=border)
print(world)
```

```python
world
```

```python
# Let's create a single big hole where we leave ten units at the boundaries
# Note: there could be multiple holes, so we need to provide list of coordinates for the hole inside a list
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
```

```python
# Now we can construct our Polygon with the hole inside
frame = Polygon(shell=border, holes=hole)
print(frame)
```

Let's see what we have now:

```python
frame
```

As we can see the `Polygon` has now two different tuples of coordinates. The first one represents the **outerior** and the second one represents the **hole** inside of the Polygon.

<!-- #region -->
### Polygon attributes and functions


We can again access different attributes directly from the `Polygon` object itself that can be really useful for many analyses, such as `area`, `centroid`, `bounding box`, `exterior`, and `exterior-length`. See a full list of methods in the [Shapely User Manual](https://shapely.readthedocs.io/en/stable/manual.html#the-shapely-user-manual).

Here, we can see a few of the available attributes and how to access them:
<!-- #endregion -->

```python
# Print the outputs
print("Polygon centroid: ", world.centroid)
print("Polygon Area: ", world.area)
print("Polygon Bounding Box: ", world.bounds)
print("Polygon Exterior: ", world.exterior)
print("Polygon Exterior Length: ", world.exterior.length)
```

As we can see above, it is again fairly straightforward to access different attributes from the `Polygon` -object. Note that distance metrics will make more sense when we start working with data in a projected coordinate system.


#### Question 6.1

Create these shapes using Shapely!

- **Triangle**   
- **Square**    
- **Cicrle**

```python
# Use this cell to enter your solution.
```

```python
# Solution

# Triangle
Polygon([(0, 0), (2, 4), (4, 0)])
```

```python
# Solution

# Square
Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
```

```python
# Solution

# Circle (using a buffer around a point)
point = Point((0, 0))
point.buffer(1)
```

<!-- #region -->
## Geometry collections


In some occassions it is useful to store multiple geometries (for example, several points or several polygons) in a single feature. A practical example would be a country that is composed of several islands. In such case, all these polygons share the same attributes on the country-level and it might be reasonable to store that country as geometry collection that contains all the polygons. The attribute table would then contain one row of information with country-level attributes, and the geometry related to those attributes would represent several polygon. 

In Shapely, collections of points are implemented by using a MultiPoint -object, collections of curves by using a MultiLineString -object, and collections of surfaces by a MultiPolygon -object. 
<!-- #endregion -->

```python
# Import constructors for creating geometry collections
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon
```

Let's start by creating MultiPoint and MultilineString objects:

```python
# Create a MultiPoint object of our points 1,2 and 3
multi_point = MultiPoint([point1, point2, point3])

# It is also possible to pass coordinate tuples inside
multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

# We can also create a MultiLineString with two lines
line1 = LineString([point1, point2])
line2 = LineString([point2, point3])
multi_line = MultiLineString([line1, line2])

# Print object definitions
print(multi_point)
print(multi_line)
```

```python
multi_point
```

```python
multi_line
```

MultiPolygons are constructed in a similar manner. Let's create a bounding box for "the world" by combinin two separate polygons that represent the western and eastern hemispheres. 

```python jupyter={"outputs_hidden": false}
# Let's create the exterior of the western part of the world
west_exterior = [(-180, 90), (-180, -90), (0, -90), (0, 90)]

# Let's create a hole --> remember there can be multiple holes, thus we need to have a list of hole(s).
# Here we have just one.
west_hole = [[(-170, 80), (-170, -80), (-10, -80), (-10, 80)]]

# Create the Polygon
west_poly = Polygon(shell=west_exterior, holes=west_hole)

# Print object definition
print(west_poly)
```

```python
west_poly
```

Shapely also has a tool for creating [a bounding box](https://en.wikipedia.org/wiki/Minimum_bounding_box) based on minimum and maximum x and y coordinates. Instead of using the Polygon constructor, let's use the [box](https://shapely.readthedocs.io/en/stable/manual.html#shapely.geometry.box) constructor for creating the polygon:  

```python
from shapely.geometry import box
```

```python
# Specify the bbox extent (lower-left corner coordinates and upper-right corner coordinates)
min_x, min_y = 0, -90
max_x, max_y = 180, 90

# Create the polygon using Shapely
east_poly = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)

# Print object definition
print(east_poly)
```

```python
east_poly
```

Finally, we can combine the two polygons into a MultiPolygon:

```python
# Let's create our MultiPolygon. We can pass multiple Polygon -objects into our MultiPolygon as a list
multi_poly = MultiPolygon([west_poly, east_poly])

# Print object definition
print(multi_poly)
```

```python
multi_poly
```

We can see that the outputs are similar to the basic geometric objects that we created previously but now these objects contain multiple features of those points, lines or polygons.

### Other useful attributes 
lenght of the geometry collection:

```python
print("Number of objects in our MultiLine:", len(multi_line))
print("Number of objects in our MultiPolygon:", len(multi_poly))
```

Area:

```python jupyter={"outputs_hidden": false}
# Print outputs:
print("Area of our MultiPolygon:", multi_poly.area)
print("Area of our Western Hemisphere polygon:", multi_poly[0].area)
```

From the above we can see that MultiPolygons have exactly the same attributes available as single geometric objects but now the information such as area calculates the area of **ALL** of the individual -objects combined. We can also access individual objects inside the geometry collections using indices.


Finally, we can check if we have a "valid" MultiPolygon. MultiPolygon is thought as valid if the individual polygons does not intersect with each other. 
Here, because the polygons have a common 0-meridian, we should NOT have a valid polygon. We can check the validity of an object from the **is_valid** -attribute that tells if the polygons or lines intersect with each other. This can be really useful information when trying to find topological errors from your data:

```python
print("Is polygon valid?: ", multi_poly.is_valid)
```

### Representing raster data with `xarray` and `numpy`

A typical source of information for raster data are images taken from space with specially equipped satellites that carry earth observation sensors. They are widely used e.g. for environmental monitoring, meteorology and cartography. 

### Representing networks with `networkx` 


## Footnotes

[^shapely]: <https://shapely.readthedocs.io/en/stable/manual.html>
[^shapely_methods]: <https://shapely.readthedocs.io/en/stable/manual.html#general-attributes-and-methods>
[^GEOS]: <https://trac.osgeo.org/geos>
[^QGIS]: <http://www.qgis.org/en/site/>
