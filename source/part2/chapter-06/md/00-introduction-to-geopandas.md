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

# Introduction to spatial data analysis with geopandas

In this chapter, we will first learn how geometric objects are represented in Python using a library called [shapely](https://shapely.readthedocs.io/en/stable/manual.html) [^shapely]. After this, we will use [geopandas](https://geopandas.org/) [^geopandas] as our main tool for spatial data analysis. In the first part of this book, we covered the basics of data analysis using the pandas library. Geopandas extends the capacities of pandas with geospatial operations. The main data structures in geopandas are `GeoSeries` and `GeoDataFrame` which extend the capabilities of `Series` and `DataFrames` from pandas. This means that we can use many familiar methods from pandas also when working with geopandas and spatial features. A `GeoDataFrame` is basically a `pandas.DataFrame` that contains one column for geometries. The geometry column is a `GeoSeries` which contains the geometries  as `shapely` objects (points, lines, polygons, multipolygons etc.). 


## Representing vector geometries with `shapely` 

`Shapely` is a fundamental Python package for representing vector data geometries on a computer. Basic knowledge of shapely is important for using higher-level tools that depend on it, such as `geopandas`.  In this section, we give a quick overview of creating geometries using `shapely`. For a full list of `shapely` objects and functions, see [the shapely user manual online](https://shapely.readthedocs.io/en/stable/manual.html) [^shapely] 


### Creating point geometries

When creating geometries with `shapely`, we first need to import the geometric object class (such as `Point`) that we want to create from `shapely.geometry` which contains all possible geometry types. After importing the `Point` class, creating a point is easy: we just pass `x` and `y` coordinates into the `Point()` -class (with a possible `z` -coordinate) which will create the point for us:

```python jupyter={"outputs_hidden": false}
from shapely.geometry import Point

point = Point(2.2, 4.2)
point3D = Point(9.26, -2.456, 0.57)

point
```

As we see here, Jupyter notebook is able to display the shape of the `point` directly on the screen when we call it. The point object here is represented as it has been defined in the *Simple Features Access Specification*. Under the hood `shapely` actually uses a C++ library called [GEOS](https://trac.osgeo.org/geos) [^GEOS] to construct the geometries, which is one of the standard libraries behind various Geographic Information Systems, such as [PostGIS](https://postgis.net/) [^PostGIS] or [QGIS](http://www.qgis.org/en/site/) [^QGIS]. We can use the print statement to get the coordinate information of these objects in WKT format:

```python jupyter={"outputs_hidden": false}
print(point)
print(point3D)
```

3D-point can be recognized from the capital Z -letter in front of the coordinates. Extracting the coordinates of a `Point` can be done in a couple of different ways. We can use the `coords` attribute contains the coordinate information as a `CoordinateSequence` which is a specific data type of Shapely. In addition, we can also directly use the attributes `x` and `y` to get the coordinates directly as plain decimal numbers.

```python
list(point.coords)
```

```python jupyter={"outputs_hidden": false}
print(point.x, point.y)
```

Points and other shapely objects have many useful built-in attributes and methods [^shapely_methods], such as calculating the Euclidian distance between points or creating a buffer from the point that converts the point into a circle `Polygon` with specific radius. However, all of these functionalities are integrated into `geopandas` and we will go through them later in the book. 


<!-- #region -->
### Creating LineString geometries


Creating `LineString` -objects is fairly similar to creating Shapely Points. Now, instead using a single coordinate-tuple we can construct the line using either a list of shapely `Point` -objects or pass the points as coordinate-tuples:
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

As we can see from above, the WKT representation of the `line` -variable constitutes of multiple coordinate-pairs. `LineString` -object has many useful built-in attributes and methods similarly as `Point` -objects. It is for instance possible to extract the coordinates, calculate the length of the `LineString`, find out the centroid of the line, create points along the line at specific distance, calculate the closest distance from a line to specified Point, or simplify the geometry. A full list of functionalities can be read from `shapely` documentation [^shapely]. Most of these functionalities are directly implemented in `geopandas` (see next chapter), hence you very seldom need to parse these information directly from the `shapely` geometries yourself. However, here we go through a few of them for reference. We can extract the coordinates of a LineString similarly as with `Point`:

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

Creating a `Polygon` -object continues the same logic how `Point` and `LineString` were created. A `Polygon` can be created by passing a list of `Point` objects or a list of coordinate-tuples as input for the `Polygon` class. Polygon needs at least three coordinate-tuples to form a surface. In the following, we use the same points from the earlier `LineString` example to create a `Polygon`:

```python jupyter={"outputs_hidden": false}
poly = Polygon([point1, point2, point3])
poly
```

```python
print(poly)
```

Notice that the `Polygon` WKT representation has double parentheses around the coordinates (i.e. `POLYGON ((<values in here>))` ). This is because Polygon can also have holes inside of it. As the help of the `Polygon` [^polygon] object tells us (*output here is slightly simplified from the original*), a `Polygon` is constructed from *exterior* and *interior* (optional) which are the attributes of the `Polygon` object. The interior can be used to create holes inside the `Polygon`: 

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


If we want to create a `Polygon` with a hole, we can do this by using parameters `shell` for the exterior and `holes` for the interiors. Let's see how we can create a `Polygon` with a single hole by passing the coordinates in decimal degrees (lon, lat). Notice, that because a `Polygon` can have multiple holes, the `hole_coords` variable below contains nested square brackets (`[[ ]]`), which is due to the possibility of having multiple holes in a single `Polygon`: 

```python
border_coords = [(-180, 90), (-180, -90), (180, -90), (180, 90)]
hole_coords = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
poly2 = Polygon(shell=border_coords, holes=hole_coords)
poly2
```

```python
print(poly2)
```

As we can see the `Polygon` has now two different tuples of coordinates. The first one represents the **outerior** and the second one represents the **interior**, i.e. a hole inside of the Polygon. 
We can access different attributes directly from the `Polygon` object itself that can be really useful for many analyses, such as `area`, `centroid`, `bounding box`, `exterior`, and `exterior-length` (and you guessed it, these are available directly in `geopandas` as well).  See a full list of methods in the `shapely` documentation [^shapely]. Here, we can see a few of the available attributes and how to access them:

```python
print("Polygon centroid: ", poly2.centroid)
print("Polygon Area: ", poly2.area)
print("Polygon Bounding Box: ", poly2.bounds)
print("Polygon Exterior: ", poly2.exterior)
print("Polygon Exterior Length: ", poly2.exterior.length)
```

As we can see above, it is again fairly straightforward to access different attributes from the `Polygon` -object. Notice, that the `length` and `area` information are presented here in decimal degrees because our input coordinates were passed as longitudes and latitudes. We can get this information in more sensible format (in meters and m2) when we start working with data in a projected coordinate system later in the book. 

Now you have learned how all the basic geometries can be created in Python using `shapely`. As a one last thing related to vector geometries, we will show you one useful tool that comes with `shapely` called `box` [^box]. The `box` -function can be used for creating a rectangular *{term}`bounding box`* [^bounding_box] based on minimum and maximum `x` and `y` coordinates, i.e. giving coordinate information of the bottom-left and top-right corners of the rectangle. Next, we will use `box` instead normal `Polygon` constructorto create the same polygon exterior as above:  

```python
from shapely.geometry import box

min_x, min_y = -180, -90
max_x, max_y = 180, 90
poly3 = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)
poly3
```

```python
print(poly3)
```

As we can see, creating a rectangular bounding box `Polygon` can be done very easily by merely passing four coordinates to the `box` -function. Quite handy! In practice, the `box` function is quite useful for example when you want to select geometries from specific area of interest. In these cases, you only need to find out the coordinates of two points on the map to be able create the polygon, which you can use to select the data.   


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

### Question 5.1

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

#### Check your understanding


<div class="alert alert-info">
    
Figure out the following information from our input data using your pandas skills:
    
- Number of rows?
- Number of classes?
- Number of groups?
</div>

```python
print("Number of rows", len(data["CLASS"]))
print("Number of classes", data["CLASS"].nunique())
print("Number of groups", data["GROUP"].nunique())
```

It is always a good idea to explore your data also on a map. Creating a simple map from a `GeoDataFrame` is really easy: you can use ``.plot()`` -function from geopandas that **creates a map based on the geometries of the data**. Geopandas actually uses matplotlib for plotting which we introduced in [Lesson 7 of the Geo-Python course](https://geo-python.github.io/site/notebooks/L7/matplotlib.html).

Let's try it out, and plot our GeoDataFrame:

```python jupyter={"outputs_hidden": false}
data.plot()
```

Voilá! As we can see, it is really easy to produce a map out of your Shapefile with geopandas. Geopandas automatically positions your map in a way that it covers the whole extent of your data.

*If you are living in the Helsinki region, you might recognize the shapes plotted on the map!*


## Geometries in geopandas

Geopandas takes advantage of Shapely's geometric objects. Geometries are stored in a column called *geometry* that is a default column name for
storing geometric information in geopandas.


Let's print the first 5 rows of the column 'geometry':

```python jupyter={"outputs_hidden": false}
data["geometry"].head()
```

As we can see the `geometry` column contains familiar looking values, namely Shapely `Polygon` -objects. Since the spatial data is stored as Shapely objects, **it is possible to use Shapely methods** when dealing with geometries in geopandas.

Let's have a closer look at the polygons and try to apply some of the Shapely methods we are already familiar with.

Let's start by checking the area of the first polygon in the data:

```python
# Access the geometry on the first row of data
data.at[0, "geometry"]
```

```python
# Print information about the area
print("Area:", round(data.at[0, "geometry"].area, 0), "square meters")
```


Let's do the same for the first five rows in the data; 

- Iterate over the GeoDataFrame rows using the `iterrows()` -function that we learned [during the Lesson 6 of the Geo-Python course](https://geo-python.github.io/site/notebooks/L6/pandas/advanced-data-processing-with-pandas.html#Iterating-rows-and-using-self-made-functions-in-Pandas).
- For each row, print the area of the polygon (here, we'll limit the for-loop to a selection of the first five rows):

```python jupyter={"outputs_hidden": false}
# Iterate over rows and print the area of a Polygon
for index, row in data[0:5].iterrows():

    # Get the area from the shapely-object stored in the geometry-column
    poly_area = row["geometry"].area

    # Print info
    print(
        "Polygon area at index {index} is: {area:.0f} square meters".format(
            index=index, area=poly_area
        )
    )
```

As you see from here, all **pandas** methods, such as the `iterrows()` function, are directly available in Geopandas without the need to call pandas separately because Geopandas is an **extension** for pandas. 

In practice, it is not necessary to use the iterrows()-approach to calculate the area for all features. Geodataframes and geoseries have an attribute `area` which we can use for accessing the area for each feature at once: 

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

These values correspond to the ones we saw in previous step when iterating rows.

Let's check what is the `min`, `max` and `mean` of those areas using familiar functions from our previous Pandas lessions.

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

- write this layer into a new Shapefile using the `gpd.to_file()` -function:

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

#### Question 6.2

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

Next we will automate the file export task. we will group the data based on column `CLASS` and export a shapefile for each class.

This can be achieved using the [groupby()](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html) familiar from the pandas library and also available in GeoDataFrames. This function groups data based on values on selected column(s).  

Before continuing, let's check the first rows of our input data:

```python
data.head()
```

The `CLASS` column in the data contains information about different land use types. With `.unique()` -function we can quickly see all different values in that column:

```python jupyter={"outputs_hidden": false}
# Print all unique values in the column
data["CLASS"].unique()
```

Now we can use that information to group our data and save all land use types into different layers:

```python jupyter={"outputs_hidden": false}
# Group the data by class
grouped = data.groupby("CLASS")

# Let's see what we have
grouped
```

As we can see, `groupby` -function gives us an object called `DataFrameGroupBy` which is similar to list of keys and values (in a dictionary) that we can iterate over.

Check group keys:

```python
grouped.groups.keys()
```

The group keys are unique values from the column by which we grouped the dataframe.

Check how many rows of data each group has:

```python jupyter={"outputs_hidden": false}
# Iterate over the grouped object
for key, group in grouped:

    # Let's check how many rows each group has:
    print("Terrain class:", key)
    print("Number of rows:", len(group), "\n")
```

There are, for example, 56 lake polygons in the input data.


We can also check how the _last_ group looks like (we have the variables in memory from the last iteration of the for-loop):

```python
group.head()
```

Notice that the index numbers refer to the row numbers in the original data -GeoDataFrame.


Check also the data type of the group:

```python
type(group)
```

As we can see, each set of data are now grouped into separate GeoDataFrames, and we can save them into separate files.

### Saving multiple output files

Let's **export each class into a separate Shapefile**. While doing this, we also want to **create unique filenames for each class**.

When looping over the grouped object, information about the class is stored in the variable `key`, and we can use this information for creating new variable names inside the for-loop. For example, we want to name the shapefile containing lake polygons as "terrain_36200.shp".


<div class="alert alert-info">

**String formatting**
    
There are different approaches for formatting strings in Python. Here are a couple of different ways for putting together file-path names using two variables:

```
basename = "terrain"
key = 36200

# OPTION 1. Concatenating using the `+` operator:
out_fp = basename + "_" + str(key) + ".shp"

# OPTION 2. Positional formatting using `%` operator
out_fp = "%s_%s.shp" %(basename, key)
    
# OPTION 3. Positional formatting using `.format()`
out_fp = "{}_{}.shp".format(basename, key)
```
    
Read more from here: https://pyformat.info/
</div>


Let's now export terrain classes into separate Shapefiles.

- First, create a new folder for the outputs:

```python
# Determine output directory
output_folder = Path("results")

# Create a new folder called 'Results'
result_folder = output_folder / "Results"

# Check if the folder exists already
if not result_folder.exists():

    print("Creating a folder for the results..")
    # If it does not exist, create one
    result_folder.mkdir()
```

At this point, you can go to the file browser and check that the new folder was created successfully.

- Iterate over groups, create a file name, and save group to file:

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

Excellent! Now we have saved those individual classes into separate Shapefiles and named the file according to the class name. These kind of grouping operations can be really handy when dealing with layers of spatial data. Doing similar process manually would be really laborious and error-prone.


### Save attributes to a text file


We can also extract basic statistics from our geodataframe, and save this information as a text file. 

Let's summarize the total area of each group:

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
[^paituli]: <https://avaa.tdata.fi/web/paituli/latauspalvelu>
[^polygon]: <https://shapely.readthedocs.io/en/stable/manual.html#polygons>
[^PostGIS]: <https://postgis.net/>
[^QGIS]: <http://www.qgis.org/en/site/>
[^shapely]: <https://shapely.readthedocs.io/en/stable/manual.html>
[^shapely_methods]: <https://shapely.readthedocs.io/en/stable/manual.html#general-attributes-and-methods>
[^topodata_fair]: <https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae>
