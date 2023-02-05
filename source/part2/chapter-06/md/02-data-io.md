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

# Preparing GeoDataFrames from geographic data

Reading data into Python is usually the first step of an analysis workflow. There are various different GIS data formats available such as [Shapefile](https://en.wikipedia.org/wiki/Shapefile) [^shp], [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) [^GeoJson], [KML](https://en.wikipedia.org/wiki/Keyhole_Markup_Language) [^KML], and [GeoPackage](https://en.wikipedia.org/wiki/GeoPackage) [^GPKG]. Geopandas is capable of reading data from all of these formats (plus many more). 

This tutorial will show some typical examples how to read (and write) data from different sources. The main point in this section is to demonstrate the basic syntax for reading and writing data using short code snippets. You can find the example data sets in the data-folder. However, most of the example databases do not exists, but you can use and modify the example syntax according to your own setup.


## Reading from different spatial data formats

In `geopandas`, we can use a generic function `.from_file()` for reading in various data formats. Esri Shapefile is the default file format. When reading files with `geopandas`, the data are passed on to the `fiona` library under the hood for reading the data. This means that you can read and write all data formats supported by `fiona` with `geopandas`. 

```python
import geopandas as gpd
import fiona
```

Let's check which drivers are supported by `fiona`.

```python
fiona.supported_drivers
```

### Read / write Shapefile

Shapefile format originally developed by the company Esri in the early 1990's is one of the most commonly used data formats (still) used today. The Shapefile is in fact comprised of several separate files that are all important for representing the spatial data. Typically a Shapefile includes (at least) four separate files with extensions `.shp`, `.dbx`, `.shx` and `.prj`. The first three of them are obligatory to have a functioning file, and the `.prj` file is highly recommended to have as it contains the coordiante reference system information.

```python
import geopandas as gpd

# Read file from Shapefile
fp = "data/Finland/municipalities_2023.shp"
data = gpd.read_file(fp)

# Write to Shapefile (just make a copy)
outfp = "data/temp/municipalities_2023.shp"
data.to_file(outfp)
```

### Read / write GeoJSON

```python
# Read file from GeoJSON
fp = "data/Finland/municipalities_2023.geojson"
data = gpd.read_file(fp, driver="GeoJSON")

# Write to GeoJSON (just make a copy)
outfp = "data/Temp/municipalities_2023.geojson"
data.to_file(outfp, driver="GeoJSON")
```

### Read / write KML

```python
# Enable KML driver
gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

# Read file from KML
fp = "data/Finland/municipalities_2023.kml"
#data = gpd.read_file(fp)

# Write to KML (just make a copy)
outfp = "data/Temp/municipalities_2023.kml"
#data.to_file(outfp, driver="KML")
```

### Read / write Geopackage

```python
# Read file from Geopackage
fp = "data/Finland/municipalities_2023.gpkg"
data = gpd.read_file(fp)

# Write to Geopackage (just make a copy)
outfp = "data/Temp/finland_municipalities.gpkg"
data.to_file(outfp, driver="GPKG")
```

### Read / write GeoDatabase

```python
# Read file from File Geodatabase
#fp = "data/Finland/finland.gdb"
#data = gpd.read_file(fp, driver="OpenFileGDB", layer="municipalities")

# Write to same FileGDB (just add a new layer) - requires additional package installations(?)
# outfp = "data/finland.gdb"
# data.to_file(outfp, driver="FileGDB", layer="municipalities_copy")
```

### Read / write MapInfo Tab

```python
# Read file from MapInfo Tab
fp = "data/Finland/municipalities_2023.tab"
data = gpd.read_file(fp, driver="MapInfo File")

# Write to MapInfo Tab (just make a copy)
outfp = "data/Temp/municipalities_2023.tab"
#data.to_file(outfp, driver="MapInfo File")
```

## Creating a GeoDataFrame from scratch

It is possible to create spatial data from scratch by using `shapely`'s geometric objects and `geopandas`. This is useful as it makes it easy to convert, for example, a text file that contains coordinates into spatial data layers. Let's first try creating a simple `GeoDataFrame` based on coordinate information that represents the outlines of the [Senate square in Helsinki, Finland](https://fi.wikipedia.org/wiki/Senaatintori). Here are the coordinates based on which we can create a `Polygon` object using `shapely.

```python
from shapely.geometry import Polygon

# Coordinates of the Helsinki Senate square in decimal degrees
coordinates = [
    (24.950899, 60.169158), (24.953492, 60.169158),
    (24.953510, 60.170104), (24.950958, 60.169990)
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
airports = pd.read_csv("data/Airports/airports.txt", 
                       usecols=["Airport ID", "Name", "City", "Country", "Latitude", "Longitude"])
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
airports["geometry"] = gpd.points_from_xy(x=airports["Longitude"], 
                                          y=airports["Latitude"], 
                                         crs="EPSG:4326")

airports = gpd.GeoDataFrame(airports)
airports.head()
```

Now we have the point geometries as `shapely`objects in the geometry-column ready to be plotted on a map.

```python
airports.plot(markersize=.1)
```

<!-- #region tags=[] -->
## Footnotes

[^GeoJson]: <https://en.wikipedia.org/wiki/GeoJSON>
[^GPKG]: <https://en.wikipedia.org/wiki/GeoPackage>
[^KML]: <https://en.wikipedia.org/wiki/Keyhole_Markup_Language>
[^openflights]: <https://openflights.org/data.html>
[^shp]: <https://en.wikipedia.org/wiki/Shapefile> 
<!-- #endregion -->
