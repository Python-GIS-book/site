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
# Representing geographic data in Python

In this section, we will learn how geometric objects (in vector format) are represented using the [shapely](https://shapely.readthedocs.io/en/stable/manual.html) [^shapely] library, which is one of the core vector data processing libraries in Python as discussed in Chapter 5. Basic knowledge of shapely is important for using higher-level tools that depend on it, such as **geopandas**, which we will use extensively in the following sections of this book for geographic data analysis.

Under the hood shapely uses a C++ library called [GEOS](https://trac.osgeo.org/geos) [^GEOS] to construct the geometries. GEOS is one of the standard libraries behind various GIS software, such as [PostGIS](https://postgis.net/) [^PostGIS] or [QGIS](http://www.qgis.org/en/site/) [^QGIS]. Objects and methods available in shapely adhere mainly to [the Open Geospatial Consortium’s Simple Features Access Specification](https://www.ogc.org/standards/sfa) [^OGC_sfa], making them compatible with various GIS tools. In this section, we give a quick overview of creating geometries using shapely.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Creating Point geometries

When creating geometries with shapely, we first need to import the geometric object class which we want to create, such as `Point`, `LineString` or `Polygon`. Let's start by creating a simple `Point` object. First, we need to import the `Point` class which we can then use to create the point geometry. When creating the geometry, we need to pass the `x` and `y` coordinates (with a possible `z` -coordinate) into the `Point()` -class constructor, which will create the point geometry for us, as follows:
<!-- #endregion -->

```python jupyter={"outputs_hidden": false} editable=true slideshow={"slide_type": ""}
from shapely import Point

point = Point(2.2, 4.2)
point3D = Point(9.26, -2.456, 0.57)
point
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 6.1**. A visual representation of a Point geometry._

As we can see in the online version, Jupyter Notebook is able to visualize the point shape on the screen. This point demonstrates a very simple geographic object that we can start using in geographic data analysis. Notice that without information about a coordinate reference system (CRS) attached to the geometry, these coordinates are ultimately just arbitrary numbers that do not represent any specific location on Earth. We will learn later in the book, how it is possible to specify a CRS for a set of geometries.

We can use the `print()` statement to get the text representation of the point geometry as [Well Known Text (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) [^WKT]. In the output, the letter `Z` after the `POINT` indicates that the geometry contains coordinates in three dimensions (x, y, z):
<!-- #endregion -->

```python jupyter={"outputs_hidden": false} editable=true slideshow={"slide_type": ""}
print(point)
print(point3D)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
It is also possible to access the WKT character string representation of the geometry using the `.wkt` attribute:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
point.wkt
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Points and other shapely objects have many useful built-in attributes and methods for extracting information from the geometric objects, such as the coordinates of a point. There are different approaches for extracting coordinates as numerical values from shapely objects. One of them is a property called `.coords`. It returns the coordinates of the point geometry as a `CoordinateSequence` which is a dedicated data structure for storing a list of coordinates. For our purposes, we can convert the `coords` into a list that makes the values visible and make it easy to access the contents: 
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
type(point.coords)
```

```python editable=true slideshow={"slide_type": ""}
list(point.coords)
```

It is also possible to access the coordinates directly using the `x` and `y` properties of the `Point` object:

```python jupyter={"outputs_hidden": false}
print(point.x)
print(point.y)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
For a full list of general attributes and methods for shapely objects, see [shapely documentation](https://shapely.readthedocs.io/en/stable/manual.html#general-attributes-and-methods) [^shapely]. For example, it is possible to calculate the Euclidian distance between points, or to create a buffer polygon for the point object. All of these attributes and methods can be accessed via the geopandas library, and we will go through them later in the book. 

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Creating LineString geometries


Creating a `LineString` -object is very similar to creating a `Point`-object. To create a `LineString`, we need at least two points that are connected to each other, which thus constitute a line. We can construct the line using either a list of `Point`-objects or pass the point coordinates as coordinate-tuples to the `LineString` constructor:
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
from shapely import Point, LineString

point1 = Point(2.2, 4.2)
point2 = Point(7.2, -25.1)
point3 = Point(9.26, -2.456)

line = LineString([point1, point2, point3])
line_from_tuples = LineString([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
line
```

_**Figure 6.2**. A visual representation of a LineString geometry._

```python editable=true slideshow={"slide_type": ""}
line.wkt
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
As we can see, the WKT representation of the `line` -variable consists of multiple coordinate-pairs. `LineString` -objects have many useful built-in attributes and methods similarly as `Point` -objects. It is for instance possible to extract the coordinates, calculate the length of the `LineString`, find out the centroid of the line, create points along the line at specific distance, calculate the closest distance from a line to specified Point, or simplify the geometry. See the [shapely documentation](https://shapely.readthedocs.io/en/stable/manual.html) [^shapely] for full details. Most of these functionalities are directly implemented in geopandas that will be introduced in the next chapter. Hence, you seldom need to parse these information directly from the shapely geometries yourself. However, here we go through a few of them for reference. We can extract the coordinates of a LineString similarly as with `Point`:
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
list(line.coords)
```

As a result, we have a list of coordinate tuples (x,y) inside a list. If you need to access all `x` -coordinates or all `y` -coordinates of the line, you can do it directly using the `xy` attribute: 

```python jupyter={"outputs_hidden": false}
xcoords = list(line.xy[0])
ycoords = list(line.xy[1])

print(xcoords)
print(ycoords)
```

It is possible to retrieve specific attributes such as `length` of the line and center of the line (`centroid`) straight from the `LineString` object itself:

```python jupyter={"outputs_hidden": false}
length = line.length
centroid = line.centroid
print(f"Length of our line: {length:.2f} units")
print(f"Centroid: {centroid}")
```

As you can see, the centroid of the line is again a `shapely.geometry.Point` object. This is useful, because it means that you can continue working with the line centroid having access to all of the methods that come with the shapely `Point` object.


## Creating Polygon geometries

Creating a `Polygon` -object continues the same logic as when creating `Point` and `LineString` objects. A `Polygon` can be created by passing a list of `Point` objects or a list of coordinate-tuples as input for the `Polygon` class. `Polygon` needs at least three coordinate-tuples to form a surface. In the following, we use the same points from the earlier `LineString` example to create a `Polygon`.

```python jupyter={"outputs_hidden": false}
from shapely import Polygon

poly = Polygon([point1, point2, point3])
poly
```

_**Figure 6.3**. A visual representation of a Polygon geometry._

```python editable=true slideshow={"slide_type": ""}
poly.wkt
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Notice that the `Polygon` WKT representation has double parentheses around the coordinates (i.e. `POLYGON ((<values in here>))` ). The current set of coordinates represents the outlines of the shape, i.e. the `exterior` of the polygon. However, a `Polygon` can also contain an optional *interior rings*, that can be used to represent holes in the polygon. You can get more information about the `Polygon` object by running `help(poly)` of from the [shapely online documentation](https://shapely.readthedocs.io/en/stable/manual.html?highlight=Polygon#Polygon) [^polygon]. Here is a simplified extract from the output of `help(Polygon)`:

```
class Polygon(shapely.geometry.base.BaseGeometry)
 |  Polygon(shell=None, holes=None)
 |  
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
 |  
 |  Parameters
 |  ----------
 |  shell : sequence
 |     A sequence of (x, y [,z]) numeric coordinate pairs or triples.
 |     Also can be a sequence of Point objects.
 |  holes : sequence
 |      A sequence of objects which satisfy the same requirements as the
 |      shell parameters above
```
<!-- #endregion -->

If we want to create a polygon with a hole, we can do this by using parameters `shell` for the exterior and `holes` for the interiors as follows. Notice that because a `Polygon` can have multiple holes, the `hole_coords` variable below contains nested square brackets (`[[ ]]`), which is due to the possibility of having multiple holes in a single `Polygon`. First, let's define the coordinates for the exterior and interior rings:

```python
# Define the exterior
exterior = [(-180, 90), (-180, -90), (180, -90), (180, 90)]

# Define the hole
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
```

The attribute `exterior` contains the `x` and `y` coordinates of all the corners of the polygon as a list of tuples. For instance, the first tuple `(-180, 90)` contains coordinates for the top-left corner of the polygon. With these four coordinate tuples, we can first create a polygon without a hole:

```python
poly_without_hole = Polygon(shell=exterior)
poly_without_hole
```

_**Figure 6.4**. A Polygon geometry (exterior)._


In a similar manner, we can make a `Polygon` with a hole by passing the variable containing the coordinates of the hole into the parameter `holes`:

```python
poly_with_hole = Polygon(shell=exterior, holes=hole)
poly_with_hole
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 6.5**. A Polygon geometry with a hole inside (exterior and interior)._

As we can see, now the Polygon contains a large hole, and the actual geometry is located at the borders, resembling a picture frame. Let's also take a look how the WKT representation of the polygon looks like (from running `poly_with_hole.wkt`):

```
POLYGON ((-180 90, -180 -90, 180 -90, 180 90, -180 90),
         (-170 80, -170 -80, 170 -80, 170 80, -170 80))
```

As we can see the `Polygon` has now two different tuples of coordinates. The first one represents the outer ring and the second one represents the inner ring, i.e. the hole. 

There are many useful attributes and methods related to shapely `Polygon`, such as `area`, `centroid`, `bounding box`, `exterior`, and `exterior-length`. For full details, see the `shapely` documentation [^shapely]. These attributes and methods are also available when working with polygon data in `geopandas`. Here are a couple of useful polygon attributes to remember:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
print("Polygon centroid: ", poly.centroid)
print("Polygon Area: ", poly.area)
print("Polygon Bounding Box: ", poly.bounds)
print("Polygon Exterior: ", poly.exterior)
print("Polygon Exterior Length: ", poly.exterior.length)
```

Notice, that the `length` and `area` information are presented here based on the units of the input coordinates. In our case, the coordinates actually represent longitude and latitude values. Thus, the lenght and area are represented as decimal degrees in this case. We can turn this information into a more sensible format (such as meters or square meters) when we start working with data in a projected coordinate system. 

Box polygons that represent the minimum bounding box of given coordinates are useful in many applications. `shapely.box` can be used for creating rectangular box polygons based on on minimum and maximum `x` and `y` coordinates that represent the coordinate information of the bottom-left and top-right corners of the rectangle. Here we will use `shapely.box` to re-create the same polygon exterior.  

```python
from shapely.geometry import box

min_x, min_y = -180, -90
max_x, max_y = 180, 90
box_poly = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)
box_poly
```

_**Figure 6.6**. A  Polygon geometry created with the `box` helper class._

```python editable=true slideshow={"slide_type": ""}
box_poly.wkt
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
In practice, the `box` function is quite useful, for example, when you want to select geometries from a specific area of interest. In such cases, you only need to find out the coordinates of two points on the map (bottom-left and top-righ corners) to be able create the bounding box polygon.   
<!-- #endregion -->

## Creating MultiPoint, MultiLineString and MultiPolygon geometries


Creating a collection of `Point`, `LineString` or `Polygon` objects is very straightforward now as you have seen how to create the basic geometric objects. In the `Multi` -versions of these geometries, you just pass a list of points, lines or polygons to the `MultiPoint`, `MultiLineString` or `MultiPolygon` constructors as shown below:

```python
from shapely import MultiPoint, MultiLineString, MultiPolygon

multipoint = MultiPoint([Point(2, 2), Point(3, 3)])
multipoint
```

_**Figure 6.7**. A MultiPoint geometry consisting of two Point objects._

```python
multiline = MultiLineString(
    [LineString([(2, 2), (3, 3)]), LineString([(4, 3), (6, 4)])]
)
multiline
```

_**Figure 6.8**. A MultiLineString geometry consisting of two LineString objects._

```python
multipoly = MultiPolygon(
    [Polygon([(0, 0), (0, 4), (4, 4)]), Polygon([(6, 6), (6, 12), (12, 12)])]
)
multipoly
```

_**Figure 6.9**. A MultiPolygon geometry consisting of two Polygon objects._


#### Question 6.1

Create examples of these shapes using your shapely skills:

- **Triangle**   
- **Square**    
- **Circle**

```python tags=["remove_cell"] editable=true slideshow={"slide_type": ""}
# Use this cell to enter your solution.
```

```python tags=["hide_cell", "remove_book_cell", "hide-cell"] editable=true slideshow={"slide_type": ""}
# Solution

# Triangle
Polygon([(0, 0), (2, 4), (4, 0)])

# Square
Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])

# Circle (using a buffer around a point)
point = Point((0, 0))
point.buffer(1)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Footnotes

[^GEOS]: <https://trac.osgeo.org/geos>
[^OGC_sfa]: <https://www.ogc.org/standards/sfa>
[^polygon]: <https://shapely.readthedocs.io/en/stable/manual.html#polygons>
[^PostGIS]: <https://postgis.net/>
[^QGIS]: <http://www.qgis.org/en/site/>
[^shapely]: <https://shapely.readthedocs.io/en/stable/manual.html>
[^WKT]: <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>
<!-- #endregion -->
