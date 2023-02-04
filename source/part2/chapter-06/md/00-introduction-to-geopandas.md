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

# Introduction to spatial data analysis with geopandas

In this chapter, we will first learn how geometric objects are represented in Python using a library called [shapely](https://shapely.readthedocs.io/en/stable/manual.html) [^shapely]. After this, we will use [geopandas](https://geopandas.org/) [^geopandas] as our main tool for spatial data analysis. In the first part of this book, we covered the basics of data analysis using the pandas library. Geopandas extends the capacities of pandas with geospatial operations. The main data structures in geopandas are `GeoSeries` and `GeoDataFrame` which extend the capabilities of `Series` and `DataFrames` from pandas. This means that we can use many familiar methods from pandas also when working with geopandas and spatial features. A `GeoDataFrame` is basically a `pandas.DataFrame` that contains one column for geometries. The geometry column is a `GeoSeries` which contains the geometries  as `shapely` objects (points, lines, polygons, multipolygons etc.). 

<!-- #region -->
## Representing vector geometries with `shapely` 

`Shapely` is a fundamental Python package for representing vector data geometries on a computer. Basic knowledge of shapely is important for using higher-level tools that depend on it, such as `geopandas`.  


 Under the hood `shapely` actually uses a C++ library called [GEOS](https://trac.osgeo.org/geos) [^GEOS] to construct the geometries, which is one of the standard libraries behind various Geographic Information Systems (GIS) software, such as [PostGIS](https://postgis.net/) [^PostGIS] or [QGIS](http://www.qgis.org/en/site/) [^QGIS]. Objects and methods available in shapely adhere mainly to [the Open Geospatial Consortium’s Simple Features Access Specification](https://www.ogc.org/standards/sfa) [^OGC_sfa] making them compatible with various GIS tools.

In this section, we give a quick overview of creating geometries using `shapely`. For a full list of `shapely` objects and methods, see [the shapely user manual online](https://shapely.readthedocs.io/en/stable/manual.html) [^shapely].
<!-- #endregion -->

### Creating point geometries

When creating geometries with `shapely`, we first need to import the geometric object class (such as `Point`) that we want to create from `shapely.geometry` which contains all possible geometry types. After importing the `Point` class, creating a point is easy: we just pass `x` and `y` coordinates into the `Point()` -class (with a possible `z` -coordinate) which will create the point for us:

```python jupyter={"outputs_hidden": false}
from shapely.geometry import Point

point = Point(2.2, 4.2)
point3D = Point(9.26, -2.456, 0.57)

point
```

Jupyter Notebook is automatically able to visualize the point shape on the screen. We can use the print statement to get the text representation of the point geometry as [Well Known Text (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) [^WKT]. The letter Z indicates 3D coordinates. 

```python jupyter={"outputs_hidden": false}
print(point)
print(point3D)
```

There are different approaches for extracting the coordinates of a `Point` as numerical values. The property the `coords` gives us to access the coordinates of the point geometry as a `CoordinateSequence` which data structure for storing a list of coordinates. For our purposes, we can convert the `coords` into a list to access its contents. 

```python
list(point.coords)
```

We can also access the coordinates directly using the `x` and `y` properties of the `Point` object.

```python jupyter={"outputs_hidden": false}
print(point.x)
print(point.y)
```

Points and other shapely objects have many useful built-in attributes and methods. See [shapely documentation ](https://shapely.readthedocs.io/en/stable/manual.html#general-attributes-and-methods) [^shapely] for a full list. For example, it is possible to calculate the Euclidian distance between points, or to create a buffer polygon for the point object. However, all of these functionalities are integrated into `geopandas` and we will go through them later in the book. 


<!-- #region -->
### Creating LineString geometries


Creating `LineString` -objects is fairly similar to creating `Point`-objects. We need at least two points for creating a line. We can construct the line using either a list of `Point`-objects or pass the point coordiantes as coordinate-tuples to the `LineString` constructor.
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
from shapely.geometry import Point, LineString

point1 = Point(2.2, 4.2)
point2 = Point(7.2, -25.1)
point3 = Point(9.26, -2.456)

line = LineString([point1, point2, point3])
line_from_tuples = LineString([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
line
```

```python
print(line)
```

As we can see from above, the WKT representation of the `line` -variable constitutes of multiple coordinate-pairs. `LineString` -objects have many useful built-in attributes and methods similarly as `Point` -objects. It is for instance possible to extract the coordinates, calculate the length of the `LineString`, find out the centroid of the line, create points along the line at specific distance, calculate the closest distance from a line to specified Point, or simplify the geometry. A full list of functionalities can be read from `shapely` documentation [^shapely]. Most of these functionalities are directly implemented in `geopandas` (see next chapter), hence you very seldom need to parse these information directly from the `shapely` geometries yourself. However, here we go through a few of them for reference. We can extract the coordinates of a LineString similarly as with `Point`:

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

As you can see, the centroid of the line is again a Shapely Point object. In practice, you would rarely access these attributes directly from individual `shapely` geometries, but we can do the same things for a set of geometries at once using `geopandas`. 


### Creating Polygon geometries

Creating a `Polygon` -object continues the same logic of creating `Point` and `LineString` objects. A `Polygon` can be created by passing a list of `Point` objects or a list of coordinate-tuples as input for the `Polygon` class. Polygon needs at least three coordinate-tuples to form a surface. In the following, we use the same points from the earlier `LineString` example to create a `Polygon`.

```python jupyter={"outputs_hidden": false}
from shapely.geometry import Polygon

poly = Polygon([point1, point2, point3])
poly
```

```python
print(poly)
```

Notice that the `Polygon` WKT representation has double parentheses around the coordinates (i.e. `POLYGON ((<values in here>))` ). This is because Polygon can also have holes inside of it. A `Polygon` is constructed from *exterior* ring and and optiona *interior* ring, that can be used to represent a hole in the polygon. You can get more information about the `Polygon` object by running `help(poly)` of from the [shapely online documentation](https://shapely.readthedocs.io/en/stable/manual.html?highlight=Polygon#Polygon) [^polygon]. Here is a simplified extract from the output of `help(Polygon)`:

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


If we want to create a `Polygon` with a hole, we can do this by using parameters `shell` for the exterior and `holes` for the interiors. 

Let's see how we can create a `Polygon` with a hole in it. Notice, that because a `Polygon` can have multiple holes, the `hole_coords` variable below contains nested square brackets (`[[ ]]`), which is due to the possibility of having multiple holes in a single `Polygon`. First, let's define the coordinates for the exterior and interior rings.

```python
# Define the exterior
exterior = [(-180, 90), (-180, -90), (180, -90), (180, 90)]

# Define the hole
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
```

Create the polygon with and without the hole:

```python
poly_without_hole = Polygon(shell=exterior)
poly_without_hole
```

```python
poly_with_hole = Polygon(shell=exterior, holes=hole)
poly_with_hole
```

Let's also check how the WKT representation of the polygon looks like.

```python
print(poly_with_hole)
```

<!-- #region -->
As we can see the `Polygon` has now two different tuples of coordinates. The first one represents the outer ring and the second one represents the inner ring, i.e. the hole.


There are many useful attributes and methods related to shapely `Polygon`, such as `area`, `centroid`, `bounding box`, `exterior`, and `exterior-length`. For a full list, the `shapely` documentation [^shapely]. Same attributes and methods are also available when working with polygon data in `geopandas`. Here are a couple of polygon attributes that are often useful when doing geographic data analysis.
<!-- #endregion -->

```python
print("Polygon centroid: ", poly.centroid)
print("Polygon Area: ", poly.area)
print("Polygon Bounding Box: ", poly.bounds)
print("Polygon Exterior: ", poly.exterior)
print("Polygon Exterior Length: ", poly.exterior.length)
```

Notice, that the `length` and `area` information are presented here in decimal degrees because our input coordinates were passed as longitudes and latitudes. We can get this information in more sensible format (in meters and m2) when we start working with data in a projected coordinate system later in the book. 

Box polygons that represent the minimum bounding box of given coordinates are useful in many applications. `shapely.box` can be used for creating rectangular box polygons based on on minimum and maximum `x` and `y` coordinates that represent the coordinate information of the bottom-left and top-right corners of the rectangle. Here we will use `shapely.box` to re-create the same polygon exterior.  

```python
from shapely.geometry import box

min_x, min_y = -180, -90
max_x, max_y = 180, 90
box_poly = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)
box_poly
```

```python
print(box_poly)
```

In practice, the `box` function is quite useful for example when you want to select geometries from a specific area of interest. In these cases, you only need to find out the coordinates of two points on the map to be able create the bounding box polygon.   


### Creating MultiPoint, MultiLineString and MultiPolygon geometries


Creating a collection of `Point`, `LineString` or `Polygon` objects is very straightforward now as you have seen how to create the basic geometric objects. In the `Multi` -versions of these geometries, you just pass a list of points, lines or polygons to the `MultiPoint`, `MultiLineString` or `MultiPolygon` constructors as shown below:

```python
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon

multipoint = MultiPoint([Point(2, 2), Point(3, 3)])
multipoint
```

```python
multiline = MultiLineString(
    [LineString([(2, 2), (3, 3)]), LineString([(4, 3), (6, 4)])]
)
multiline
```

```python
multipoly = MultiPolygon(
    [Polygon([(0, 0), (0, 4), (4, 4)]), Polygon([(6, 6), (6, 12), (12, 12)])]
)
multipoly
```

### Question 6.1

Create these shapes using Shapely!

- **Triangle**   
- **Square**    
- **Circle**

```python
# Use this cell to enter your solution.
```

```python
# Solution

# Triangle
Polygon([(0, 0), (2, 4), (4, 0)])

# Square
Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])

# Circle (using a buffer around a point)
point = Point((0, 0))
point.buffer(1)
```

## Getting started with geopandas


![_**Figure 6.1**. Geometry column in a GeoDataFrame._](../img/geodataframe.png)

_**Figure 6.1**. Geometry column in a GeoDataFrame._

Similar to importing import pandas as `pd`, we will import geopandas as `gpd`:

```python
import geopandas as gpd
```

## Reading a Shapefile

Esri Shapefile is the default file format when reading in data usign geopandas, so we only need to pass the file path in order to read in our data:

```python
from pathlib import Path

input_folder = Path("../data/NLS")
fp = input_folder / "m_L4132R_p.shp"
```

```python
# Read file using gpd.read_file()
data = gpd.read_file(fp)
```

Let's check the data type:

```python jupyter={"outputs_hidden": false}
type(data)
```

Here we see that our `data` -variable is a `GeoDataFrame`. GeoDataFrame extends the functionalities of
`pandas.DataFrame` in a way that it is possible to handle spatial data using similar approaches and datastructures as in pandas (hence the name geopandas). 

Let's check the first rows of data: 

```python jupyter={"outputs_hidden": false}
data.head()
```

- Check all column names:

```python
data.columns.values
```

As you might guess, the column names are in Finnish.
Let's select only the useful columns and rename them into English:

```python
data = data[["RYHMA", "LUOKKA", "geometry"]]
```

Define new column names in a dictionary:

```python
colnames = {"RYHMA": "GROUP", "LUOKKA": "CLASS"}
```

Rename:

```python
data.rename(columns=colnames, inplace=True)
```

Check the output:

```python
data.head()
```

#### Question 6.2

Figure out the following information from our input data using your pandas skills:
    
- Number of rows?
- Number of classes?
- Number of groups?

```python
# You can use this cell to enter your solution.
```

```python
# Solution 

print("Number of rows", len(data["CLASS"]))
print("Number of classes", data["CLASS"].nunique())
print("Number of groups", data["GROUP"].nunique())
```

It is always a good idea to explore your data also on a map. Creating a simple map from a `GeoDataFrame` is really easy. You can use ``.plot()`` -function from geopandas that **creates a map based on the geometries of the data**. Geopandas actually uses matplotlib for plotting which we introduced in Part 1 of this book. Let's try it out, and do a quick visualization of our data.

```python jupyter={"outputs_hidden": false}
data.plot()
```

Voilá! As we can see, it is really easy to produce a map out of your geospatial data with `geopandas`. *If you are living in the Helsinki region in Finland, you might recognize the shapes plotted on the map!*


## Geometries in geopandas

Geopandas takes advantage of Shapely's geometric objects. Geometries are stored in a column called `geometry` that is a default column name for storing geometric information in geopandas.


Let's print the first 5 rows of the column 'geometry':

```python jupyter={"outputs_hidden": false}
data["geometry"].head()
```

As we can see the `geometry` column contains familiar looking values, namely shapely `Polygon` -objects. Since the spatial data is stored as shapely objects, it is possible to use shapely methods when dealing with geometries in geopandas. Also,  all `pandas` methods are directly available in `geopandas` without the need to import `pandas` separately. Let's have a closer look at the polygons and try to apply some of the methods we are already familiar with. Let's start by checking the area of the first polygon in the data.

```python
# Access the geometry on the first row of data
data.at[0, "geometry"]
```

```python
# Print information about the area
print("Area:", round(data.at[0, "geometry"].area, 0), "square meters")
```


Geodataframes and geoseries have an attribute `area` which we can use for accessing the area for each feature at once.

```python
data.area
```

Let's next create a new column into our GeoDataFrame where we calculate and store the areas of individual polygons:

```python jupyter={"outputs_hidden": false}
# Create a new column called 'area'
data["area"] = data.area
```

Check the output:

```python
data["area"]
```

Let's check what is the `min`, `max` and `mean` of those areas using `pandas` functions introduced in Part 1.

```python
# Maximum area
round(data["area"].max(), 2)
```

```python
# Minimum area
round(data["area"].min(), 2)
```

```python
# Average area
round(data["area"].mean(), 2)
```

## Writing data into a file

It is possible to export GeoDataFrames into various data formats using the [to_file()](http://geopandas.org/io.html#writing-spatial-data) method. In our case, we want to export subsets of the data into Shapefiles (one file for each feature class).

Let's first select one class (class number `36200`, "Lake water") from the data as a new GeoDataFrame:


```python
# Select a class
selection = data.loc[data["CLASS"] == 36200]
```

Check the selection:

```python
selection.plot()
```

Write this layer into a new Shapefile using the `gpd.to_file()` -function.

```python
# Create a output path for the data
output_folder = Path("results")

if not output_folder.exists():
    output_folder.mkdir()

output_fp = output_folder / "Class_36200.shp"
```

```python
# Write those rows into a new file (the default output file format is Shapefile)
selection.to_file(output_fp)
```

#### Question 6.3

Read the output Shapefile in a new geodataframe, and check that the data looks ok.

```python
# Use this cell to enter your solution.
```

```python
# Solution

temp = gpd.read_file(output_fp)

# Check first rows
temp.head()
```

```python
# Solution

# You can also plot the data for a visual check
temp.plot()
```

## Grouping the GeoDataFrame

Next we will automate the file export task. we will group the data based on column `CLASS` and export a shapefile for each class. Here we can use the `.groupby()` method from `pandas` and apply it on our `GeoDataFrame`. The function groups data based on values on selected column(s).  We will want to group the data by distinct classes. Before continuing, let's check the structure of our data from the first rows.

```python
data.head()
```

The `CLASS` column in the data contains information about different land use types represeted with class codes. We can also check all unique values in that column and the number of unique values.

```python jupyter={"outputs_hidden": false}
# Print all unique values in the column
data["CLASS"].unique()
```

```python
#Check the number of unique values
data["CLASS"].nunique()
```

Now we can group the data into 20 distinct groups based on the land use class code.

```python jupyter={"outputs_hidden": false}
# Group the data by class
grouped = data.groupby("CLASS")

# Let's see what we have
len(grouped)
```

The grouped object is similar to a list of keys and values in a dictionary and we can access, for example, information about the group keys.

```python
grouped.groups.keys()
```

As it should be, the group keys are unique values from the column by which we grouped the dataframe. Let's also check how many rows of data belongs to each group.

```python jupyter={"outputs_hidden": false}
# Iterate over the grouped object
for key, group in grouped:

    # Check how many rows each group has:
    print("Terrain class:", key)
    print("Number of rows:", len(group), "\n")
```

There are, for example, 56 lake polygons (class number 36200) in the input data. To get a better sense of the data structure, we can also check how the _last_ group looks like (because at this point, we have the variables in memory from the last iteration of the for-loop).

```python
group.head()
```

Notice that the index numbers refer to the row numbers in the original data. Check also the data type of the group.

```python
type(group)
```

At this point, the data are now grouped into separate GeoDataFrames by class. From here, we can save them into separate files.

### Saving multiple output files

Let's export each class into a separate Shapefile. While doing this, we also want to create unique filenames for each class.

When looping over the grouped object, information about the class is stored in the variable `key`, and we can use this information for creating new variable names inside the for-loop. For example, we want to name the shapefile containing lake polygons as "terrain_36200.shp".

```python
# Determine output directory
output_folder = Path("../data")

# Create a new folder called 'Results'
result_folder = output_folder / "Results"

# Check if the folder exists already
if not result_folder.exists():

    print("Creating a folder for the results..")
    # If it does not exist, create one
    result_folder.mkdir()
```

At this point, you can go to the file browser and check that the new folder was created successfully. Finally, we will iterate over groups, create a file name, and save each group to a separate file.

```python jupyter={"outputs_hidden": false}
# Iterate over the groups
for key, group in grouped:
    # Format the filename
    output_name = Path("terrain_{}.shp".format(key))

    # Print information about the process
    print("Saving file", output_name.name)

    # Create an output path
    outpath = result_folder / output_name

    # Export the data
    group.to_file(outpath)
```

Excellent! Now we have saved those individual classes into separate files and named the file according to the class name. Imagine how long time it would have taken to do the same thing manually.


### Save attributes to a text file


We can also extract basic statistics from our geodataframe, and save this information as a text file. Let's summarize the total area of each group.

```python
data.head()
```

```python
area_info = grouped.area.sum().round()
```

```python
area_info
```

Save area info to csv using pandas:

```python
# Create an output path
area_info.to_csv(result_folder / "terrain_class_areas.csv", header=True)
```


## Footnotes

[^bounding_box]: <https://en.wikipedia.org/wiki/Minimum_bounding_box>
[^box]: <https://shapely.readthedocs.io/en/stable/manual.html#shapely.geometry.box>
[^geopandas]: <https://geopandas.org/>
[^GEOS]: <https://trac.osgeo.org/geos>
[^NLS_topodata]: <https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database>
[^NLS_lisence]: <https://www.maanmittauslaitos.fi/en/opendata-licence-cc40>
[^OGC_sfa]: <https://www.ogc.org/standards/sfa>
[^paituli]: <https://avaa.tdata.fi/web/paituli/latauspalvelu>
[^polygon]: <https://shapely.readthedocs.io/en/stable/manual.html#polygons>
[^PostGIS]: <https://postgis.net/>
[^QGIS]: <http://www.qgis.org/en/site/>
[^shapely]: <https://shapely.readthedocs.io/en/stable/manual.html>
[^topodata_fair]: <https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae>
[^WKT]: <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>
