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

# Storing data into a GeoDataFrame

Now as we have learned how to create and represent geographic data in Python using `shapely` objects, we will continue and use [geopandas](https://geopandas.org/) [^geopandas] as our main tool for spatial data analysis. Geopandas extends the capacities of pandas (which we covered in the Part I of the book) with geospatial operations.




## GeoDataFrame data structures

The main data structures in geopandas are `GeoSeries` and `GeoDataFrame` which extend the capabilities of `Series` and `DataFrames` from pandas. This means that we can use many familiar methods from pandas also when working with geopandas and spatial features. A `GeoDataFrame` is basically a `pandas.DataFrame` that contains one column for geometries. The geometry column is a `GeoSeries` which contains the geometries  as `shapely` objects (points, lines, polygons, multipolygons etc.). 


![_**Figure 6.10**. Geometry column in a GeoDataFrame._](../img/geodataframe.png)

_**Figure 6.10**. Geometry column in a GeoDataFrame._

Similar to importing import pandas as `pd`, we will import geopandas as `gpd`:

```python tags=["remove_cell"]
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas
```

```python
import geopandas as gpd
```

## Reading a file

In `geopandas`, we can use a generic function `.from_file()` for reading in various data formats. The data-folder contains some census data from Austin, Texas downloaded from the [U.S Census bureau](https://www.census.gov/programs-surveys/acs/data.html) [^us_census]. Let's first define the path to the file.

```python
from pathlib import Path

data_folder = Path("data/Austin")
fp = data_folder / "austin_pop_2019.gpkg"
print(fp)
```

Now we can pass this filepath to `geopandas`.

```python
data = gpd.read_file(fp)
```

Let's check the data type.

```python jupyter={"outputs_hidden": false}
type(data)
```

Here we see that our `data` -variable is a `GeoDataFrame` which extends the functionalities of
`DataFrame` to handle spatial data. We can apply many familiar `pandas` methods to explore the contents of our `GeoDataFrame`. Let's have a closer look at the first rows of the data. 

```python jupyter={"outputs_hidden": false}
data.head()
```

#### Question 6.2

Figure out the following information from our input data using your `pandas` skills:
    
- Number of rows?
- Number of census tracts (based on column `tract`)?
- Total population (based on column `pop2019`)?

```python tags=["remove_cell"]
# You can use this cell to enter your solution.
```

```python tags=["remove_book_cell", "hide_cell"]
# Solution

print("Number of rows", len(data))
print("Number of census tract", data["tract"].nunique())
print("Total population", data["pop2019"].sum())
```

It is always a good idea to explore your data also on a map. Creating a simple map from a `GeoDataFrame` is really easy. You can use the ``.plot()`` -function from geopandas that creates a map based on the geometries of the data. `geopandas` actually uses `matplotlib` for plotting which we introduced in Part 1 of this book. Let's try it out, and do a quick visualization of our data.

```python jupyter={"outputs_hidden": false}
data.plot()
```

_**Figure 6.11**. Census tract polygons for Austin, Texas, USA._

Voilá! Now we have a quick overview of the geometries in this data. The x and y axes in the plot are based on the coordiante values of the geometries.


## Geometries in geopandas

A `GeoDataFrame` has one column for storing geometries. By default, `geopandas` looks for the geometries from a column called `geometry`. It is also possible to define other columns as the geometry column. Th geometry column is a `GeoSeries` that contains shapely's geometric objects.  Let's have a look at the geometry column of our sample data.

```python jupyter={"outputs_hidden": false}
data["geometry"].head()
```

As we can see here,  the `geometry` column contains polygon geometries. Since these polygons are  `shapely` objects, it is possible to use `shapely` methods for handling them also in `geopandas`. Many of the methods can be applied all at once to the whole `GeoDataFrame`. 

Let's proceed to calculating area of the census tract polygons. At this point, it is good to note that the census data are in a metric coordinate reference system, so the area values will be given in square meters.

```python
data["geometry"].area
```

The same result can be achieved by using the syntax `data.area`. Let's convert the area values from square meters to square kilometers and store them into a new column.

```python
# Get area and convert from m2 to km2
data["area_km2"] = data.area / 1000000
```

Check the output.

```python
data["area_km2"].head()
```

#### Question 6.3

Using your `pandas` skills, create a new column `pop_density_km2` and populate it with population density values (population / km2) calculated based on columns `pop2019` and `area_km2`. Print out answers to the following questions:

- What was the average population density in 2019?
- What was the maximum population density per census tract?

```python tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["remove_book_cell", "hide_cell"]
# Solution

# Calculate population density
data["pop_density_km2"] = data["pop2019"] / data["area_km2"]

# Print out average and maximum values
print("Average:", round(data["pop_density_km2"].mean()), "pop/km2")

print("Maximum:", round(data["pop_density_km2"].max()), "pop/km2")
```

## Writing data into a file

It is possible to export spatial data into various data formats using the `.to_file()` method in `geopandas`. Let's practice writing data into the geopackage file format. Before proceeding, let's check how the data looks like at this point.

```python
data.head()
```

Write the data into a file using the `.to_file()` method.

```python
# Create a output path for the data
output_fp = data_folder / "austin_pop_density_2019.gpkg"

# Write the file
data.to_file(output_fp)
```

#### Question 6.4

Read the output file using `geopandas` and check that the data looks ok.

```python tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["remove_book_cell", "hide_cell"]
# Solution

temp = gpd.read_file(output_fp)

# Check first rows
temp.head()
```

```python tags=["remove_book_cell", "hide_cell"]
# Solution

# You can also plot the data for a visual check
temp.plot()
```

## Preparing GeoDataFrames from different file formats

Reading data into Python is usually the first step of an analysis workflow. There are various different GIS data formats available such as [Shapefile](https://en.wikipedia.org/wiki/Shapefile) [^shp], [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) [^GeoJson], [KML](https://en.wikipedia.org/wiki/Keyhole_Markup_Language) [^KML], and [GeoPackage](https://en.wikipedia.org/wiki/GeoPackage) [^GPKG]. Geopandas is capable of reading data from all of these formats (plus many more). 

This tutorial will show some typical examples how to read (and write) data from different sources. The main point in this section is to demonstrate the basic syntax for reading and writing data using short code snippets. You can find the example data sets in the data-folder. However, most of the example databases do not exists, but you can use and modify the example syntax according to your own setup.


### Reading vector data

In `geopandas`, we can use a generic function `.from_file()` for reading in various vector data formats. When reading files with `geopandas`, the data are passed on to the `fiona` library under the hood for reading the data. This means that you can read and write all data formats supported by `fiona` with `geopandas`. 

```python tags=["remove_cell"]
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas
```

```python
import geopandas as gpd
import fiona
```

Let's check which drivers are supported by `fiona`.

```python
fiona.supported_drivers
```

In the list of supported drivers, `r` is for file formats `fiona` can read, and `w` is for file formats it can write. Letter `a` marks formats for which `fiona` can append new data to existing files.


Let's read in some sample data to see the basic syntax.

```python
# Read Esri Shapefile
fp = "data/Austin/austin_pop_2019.shp"
data = gpd.read_file(fp)
data.head()
```

The same syntax works for other commong vector data formats. 

```python
# Read file from Geopackage
fp = "data/Austin/austin_pop_2019.gpkg"
data = gpd.read_file(fp)

# Read file from GeoJSON
fp = "data/Austin/austin_pop_2019.geojson"
data = gpd.read_file(fp)

# Read file from MapInfo Tab
fp = "data/Austin/austin_pop_2019.tab"
data = gpd.read_file(fp)
```

Some file formats such as GeoPackage and File Geodatabase files may contain multiple layers with different names wihich can be speficied using the `layer` -parameter. Our example geopackage file has only one layer with the same name as the file, so we don't actually need to specify it to read in the data.

```python
# Read spesific layer from Geopackage
fp = "data/Austin/austin_pop_2019.gpkg"
data = gpd.read_file(fp, layer="austin_pop_2019")
```

```python
# Read file from File Geodatabase
# fp = "data/Finland/finland.gdb"
# data = gpd.read_file(fp, driver="OpenFileGDB", layer="municipalities")
```

(write intro about enabling additional drivers and reading in the KML file)

```python
# Enable KML driver
gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

# Read file from KML
fp = "data/Austin/austin_pop_2019.kml"
# data = gpd.read_file(fp)
```

### Writing vector data

We can save spatial data to various vector data formats using the `.to_file()` function in `geopandas` which also relies on `fiona`. It is possible to specify the output file format using the `driver` parameter, however, for most file formats it is not needed as the tool is able to infer the driver from the file extension. 

```python
# Write to Shapefile (just make a copy)
outfp = "data/Temp/austin_pop_2019.shp"
data.to_file(outfp)

# Write to Geopackage (just make a copy)
outfp = "data/Temp/austin_pop_2019.gpkg"
data.to_file(outfp, driver="GPKG")

# Write to GeoJSON (just make a copy)
outfp = "data/Temp/austin_pop_2019.geojson"
data.to_file(outfp, driver="GeoJSON")

# Write to MapInfo Tab (just make a copy)
outfp = "data/Temp/austin_pop_2019.tab"
data.to_file(outfp)

# Write to same FileGDB (just add a new layer) - requires additional package installations(?)
# outfp = "data/finland.gdb"
# data.to_file(outfp, driver="FileGDB", layer="municipalities_copy")

# Write to KML (just make a copy)
outfp = "data/Temp/austin_pop_2019.kml"
# data.to_file(outfp, driver="KML")
```

## Creating a GeoDataFrame from scratch

It is possible to create spatial data from scratch by using `shapely`'s geometric objects and `geopandas`. This is useful as it makes it easy to convert, for example, a text file that contains coordinates into spatial data layers. Let's first try creating a simple `GeoDataFrame` based on coordinate information that represents the outlines of the [Senate square in Helsinki, Finland](https://fi.wikipedia.org/wiki/Senaatintori). Here are the coordinates based on which we can create a `Polygon` object using `shapely.

```python
from shapely.geometry import Polygon

# Coordinates of the Helsinki Senate square in decimal degrees
coordinates = [
    (24.950899, 60.169158),
    (24.953492, 60.169158),
    (24.953510, 60.170104),
    (24.950958, 60.169990),
]

# Create a Shapely polygon from the coordinate-tuple list
poly = Polygon(coordinates)
```

Now we can use this polygon and `geopandas` to create a `GeoDataFrame` from scratch. The data can be passed in as a list-like object. In our case we will only have one row and one column of data. We can pass the polygon inside a list, and name the column as `geometry` so that `geopandas` will use the contents of that column the geometry column. Additionally, we could define the coordinate reference system for the data, but we will skip this step for now. For details of the syntax, see documentation for the `DataFrame` constructor and `GeoDataFrame` constructor online.

```python
newdata = gpd.GeoDataFrame(data=[poly], columns=["geometry"])
```

```python
newdata
```

We can also add additional attribute information to a new column. 

```python jupyter={"outputs_hidden": false}
# Add a new column and insert data
newdata.at[0, "name"] = "Senate Square"

# Check the contents
newdata
```

There it is! Now we have two columns in our data; one representing the geometry and another with additional attribute information. From here, you could proceed into adding additional rows of data, or printing out the data to a file. 


## Creating a GeoDataFrame from a text file


A common case is to have coordinates in a delimited textfile that needs to be converted into spatial data. We can make use of `pandas`, `geopandas` and `shapely` for doing this. 

The example data contains point coordinates of airports derived from [openflights.org](https://openflights.org/data.html) [^openflights]. Let's read in a couple of useful columns from the data for further processing.

```python
import pandas as pd
```

```python
airports = pd.read_csv(
    "data/Airports/airports.txt",
    usecols=["Airport ID", "Name", "City", "Country", "Latitude", "Longitude"],
)
```

```python
airports.head()
```

```python
len(airports)
```

There are over 7000 airports in the data and we can use the coordinate information available in the `Latitude` and `Longitude` columns for visualizing them on a map. The coordinates are stored as *{term}`Decimal degrees <Decimal degrees>`*, meaning that the appropriate coordinate reference system for these data is WGS 84 (EPSG:4326).  

There is a handy tool in `geopandas` for generating an array of `Point`objects based on x and y coordinates called `.points_from_xy()`. The tool assumes that x coordinates represent longitude and that y coordinates represent latitude. 

```python
airports["geometry"] = gpd.points_from_xy(
    x=airports["Longitude"], y=airports["Latitude"], crs="EPSG:4326"
)

airports = gpd.GeoDataFrame(airports)
airports.head()
```

Now we have the point geometries as `shapely`objects in the geometry-column ready to be plotted on a map.

```python
airports.plot(markersize=0.1)
```

_**Figure 6.12**. A basic plot showing the airports from openflights.org._

<!-- #region tags=[] -->
## Footnotes

[^GeoJson]: <https://en.wikipedia.org/wiki/GeoJSON>
[^geopandas]: <https://geopandas.org/>
[^GPKG]: <https://en.wikipedia.org/wiki/GeoPackage>
[^KML]: <https://en.wikipedia.org/wiki/Keyhole_Markup_Language>
[^NLS_topodata]: <https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database>
[^NLS_lisence]: <https://www.maanmittauslaitos.fi/en/opendata-licence-cc40>
[^OGC_sfa]: <https://www.ogc.org/standards/sfa>
[^openflights]: <https://openflights.org/data.html>
[^paituli]: <https://avaa.tdata.fi/web/paituli/latauspalvelu>
[^shp]: <https://en.wikipedia.org/wiki/Shapefile> 
[^topodata_fair]: <https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae>
[^us_census]: <https://www.census.gov/programs-surveys/acs/data.html>
<!-- #endregion -->
