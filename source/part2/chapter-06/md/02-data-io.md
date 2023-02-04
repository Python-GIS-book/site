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
fp = "data/finland_municipalities.shp"
data = gpd.read_file(fp)

# Write to Shapefile (just make a copy)
outfp = "temp/finland_municipalities.shp"
data.to_file(outfp)
```

### Read / write GeoJSON

```python
# Read file from GeoJSON
fp = "data/finland_municipalities.gjson"
data = gpd.read_file(fp, driver="GeoJSON")

# Write to GeoJSON (just make a copy)
outfp = "temp/finland_municipalities.gjson"
data.to_file(outfp, driver="GeoJSON")
```

### Read / write KML

```python
# Enable KML driver
gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

# Read file from KML
fp = "data/finland_municipalities.kml"
data = gpd.read_file(fp)

# Write to KML (just make a copy)
outfp = "temp/finland_municipalities.kml"
data.to_file(outfp, driver="KML")
```

### Read / write Geopackage

```python
# Read file from Geopackage
fp = "data/finland_municipalities.gpkg"
data = gpd.read_file(fp)

# Write to Geopackage (just make a copy)
outfp = "temp/finland_municipalities.gpkg"
data.to_file(outfp, driver="GPKG")
```

### Read / write GeoDatabase

```python
# Read file from File Geodatabase
fp = "data/finland.gdb"
data = gpd.read_file(fp, driver="OpenFileGDB", layer="municipalities")

# Write to same FileGDB (just add a new layer) - requires additional package installations(?)
# outfp = "data/finland.gdb"
# data.to_file(outfp, driver="FileGDB", layer="municipalities_copy")
```

### Read / write MapInfo Tab

```python
# Read file from MapInfo Tab
fp = "data/finland_municipalities.tab"
data = gpd.read_file(fp, driver="MapInfo File")

# Write to same FileGDB (just add a new layer)
outfp = "temp/finland_municipalities.tab"
data.to_file(outfp, driver="MapInfo File")
```

## Creating new GeoDataFrame from scratch

Since `geopandas` takes advantage of `shapely` geometric objects, it is possible to create spatial data from scratch by passing `shapely`'s geometric objects into the `GeoDataFrame`. This is useful as it makes it easy to convert, for example, a text file that contains coordinates into spatial data layers. Next we will see how to create a new `GeoDataFrame` from scratch and save it into a file. Our goal is to define a geometry that represents the outlines of the [Senate square in Helsinki, Finland](https://fi.wikipedia.org/wiki/Senaatintori). Let's start by creating a new empty `GeoDataFrame` object.

```python
newdata = gpd.GeoDataFrame()
```

```python
type(newdata)
```

```python
print(newdata)
```

We have an empty GeoDataFrame! Next, we should add some geometries in there. By default, the geometry-column should be named `"geometry"` (geopandas automatically looks for geometries from this column).  So, let's create a new column called `"geometry"`

```python jupyter={"outputs_hidden": false}
newdata["geometry"] = None
```

```python
print(newdata)
```

Now we have a `geometry` column but we still don't have any data values in there. Let's create a `Polygon` repsenting the Helsinki Senate square that we can later insert to our `GeoDataFrame`.

```python
from shapely.geometry import Polygon
```

```python jupyter={"outputs_hidden": false}
# Coordinates of the Helsinki Senate square in decimal degrees
coordinates = [
    (24.950899, 60.169158),
    (24.953492, 60.169158),
    (24.953510, 60.170104),
    (24.950958, 60.169990),
]
```

```python
# Create a Shapely polygon from the coordinate-tuple list
poly = Polygon(coordinates)
```

```python
# Check the polyogon
print(poly)
```

Okay, now we have a `Polygon` -object that represents the Senate Square. Let's insert the polygon into our geometry-column on the first row of the `GeoDataFrame`.

```python jupyter={"outputs_hidden": false}
# Insert the polygon into 'geometry' -column at row 0
newdata.at[0, "geometry"] = poly
```

```python
# Let's see what we have now
print(newdata)
```

Great, now we have a GeoDataFrame with a polygon geometry. Let's also add some attribute information in there by adding another column called `location` with the text `Senaatintori`, i.e. the name of the Senate Square in Finnish.

```python jupyter={"outputs_hidden": false}
# Add a new column and insert data
newdata.at[0, "location"] = "Senaatintori"

# Let's check the data
print(newdata)
```

There it is! Now we have two columns in our data; one representing the geometry and another with additional attribute information.

The next step would be to determine the coordinate reference system (CRS) for the GeoDataFrame. GeoDataFrame has an attribute called `.crs` that shows the coordinate system of the data (we will discuss more about CRS in next chapter). In our case, the layer doesn't yet have any crs definition.

```python jupyter={"outputs_hidden": false}
print(newdata.crs)
```

We passed the coordinates as latitude and longitude decimal degrees, so the correct coordinate reference system (CRS) is WGS84 (epsg code: 4326). We can now set the correct CRS information for our data. 

```python
newdata = newdata.set_crs(crs=4326)
```

```python
newdata.crs.name
```

As we can see, now we have added CRSinformation into our `GeoDataFrame`. The CRS information is necessary for creating a valid projection information for the output file. 

Finally, we can export the GeoDataFrame using `.to_file()` -function. The function works quite similarly as the export functions in pandas, but here we only need to provide the output path for the Shapefile. Easy isn't it!:

```python
# Determine the output path for the Shapefile
outfp = "../data/Results/Senaatintori.shp"

# Write the data into that Shapefile
newdata.to_file(outfp)
```

<!-- #region tags=[] -->
Now we have successfully created a Shapefile from scratch using geopandas. Similar approach can be used to for example to read coordinates from a text file (e.g. points) and turn that information into a spatial layer.


#### Question 6.4

- Check the output Shapefile by reading it with geopandas and make sure that the attribute table and geometry seems correct.

- Re-project the data to ETRS-TM35FIN (EPSG:3067) and save into a new file!


<!-- #endregion -->


```python tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["hide_cell", "remove_book_cell"]
# Solution

# Read in the data
senate_square = gpd.read_file(outfp)

# One pontial way to check the contents
senate_square.head()
```

```python tags=["hide_cell", "remove_book_cell"]
# Solution

# re-project
senate_square = senate_square.to_crs(crs=3067)

#check the result
print(senate_square)

# Save to new file
outfp = "../data/Results/Senaatintori_epsg3067.shp"
senate_square.to_file(outfp)
```

<!-- #region tags=[] -->
## Footnotes

[^shp]: <https://en.wikipedia.org/wiki/Shapefile> 
[^GeoJson]: <https://en.wikipedia.org/wiki/GeoJSON>
[^GPKG]: <https://en.wikipedia.org/wiki/GeoPackage>
[^KML]: <https://en.wikipedia.org/wiki/Keyhole_Markup_Language> 
<!-- #endregion -->
