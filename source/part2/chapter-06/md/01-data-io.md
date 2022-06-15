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

# Reading and writing vector data in Python

Reading data into Python is usually the first step of an analysis workflow. There are various different GIS data formats available such as [Shapefile](https://en.wikipedia.org/wiki/Shapefile), [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON), [KML](https://en.wikipedia.org/wiki/Keyhole_Markup_Language), and [GPKG](https://en.wikipedia.org/wiki/GeoPackage). Geopandas is capable of reading data from all of these formats (plus many more). 

This tutorial will show some typical examples how to read (and write) data from different sources. The main point in this section is to demonstrate the basic syntax for reading and writing data using short code snippets. You can find the example data sets in the data-folder. However, most of the example databases do not exists, but you can use and modify the example syntax according to your own setup.

## Creating new GeoDataFrame from scratch

Since geopandas takes advantage of Shapely geometric objects, it is possible to create spatial data from scratch by passing Shapely's geometric objects into the GeoDataFrame. This is useful as it makes it easy to convert e.g. a text file that contains coordinates into spatial data layers. Next we will see how to create a new GeoDataFrame from scratch and save it into a file. Our goal is to define a geometry that represents the outlines of the [Senate square in Helsinki, Finland](https://fi.wikipedia.org/wiki/Senaatintori).



Let's start by creating a new empty `GeoDataFrame` object.

```python
import geopandas as gpd
```

```python
newdata = gpd.GeoDataFrame()
```

```python
type(newdata)
```

We have an empty GeoDataFrame! A geodataframe is basically a pandas DataFrame that should have one column dedicated for geometries. By default, the geometry-column should be named `geometry` (geopandas looks for geometries from this column).  

Let's create the `geometry` column:

```python jupyter={"outputs_hidden": false}
# Create a new column called 'geometry' to the GeoDataFrame
newdata["geometry"] = None
```

```python
print(newdata)
```

Now we have a `geometry` column in our GeoDataFrame but we still don't have any data.

Let's create a Shapely `Polygon` repsenting the Helsinki Senate square that we can later insert to our GeoDataFrame:

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

Okay, now we have an appropriate `Polygon` -object.

Let's insert the polygon into our 'geometry' column of our GeoDataFrame on the first row:

```python jupyter={"outputs_hidden": false}
# Insert the polygon into 'geometry' -column at row 0
newdata.at[0, "geometry"] = poly
```

```python
# Let's see what we have now
print(newdata)
```

Great, now we have a GeoDataFrame with a Polygon that we could already now export to a Shapefile. However, typically you might want to include some attribute information with the geometry. 

Let's add another column to our GeoDataFrame called `location` with text `Senaatintori` that describes the location of the feature.

```python jupyter={"outputs_hidden": false}
# Add a new column and insert data
newdata.at[0, "location"] = "Senaatintori"

# Let's check the data
print(newdata)
```

Okay, now we have additional information that is useful for recognicing what the feature represents. 

The next step would be to **determine the coordinate reference system (CRS) for the GeoDataFrame.** GeoDataFrame has an attribute called `.crs` that shows the coordinate system of the data (we will discuss more about CRS in next chapter). In our case, the layer doesn't yet have any crs definition:

```python jupyter={"outputs_hidden": false}
print(newdata.crs)
```

We passed the coordinates as latitude and longitude decimal degrees, so the correct CRS is WGS84 (epsg code: 4326). In this case, we can simply re-build the geodataframe and pass the correct crs information to the GeoDataFrame constructor. You will learn more about how to handle coordinate reference systems using pyproj CRS objects later in this chapter.  

Re-create the GeoDataFrame with correct crs definition: 

```python
newdata = gpd.GeoDataFrame(newdata, crs=4326)
```

```python
newdata.crs.name
```

As we can see, now we have added coordinate reference system information into our `GeoDataFrame`. The CRS information is necessary for creating a valid projection information for the output file. 

Finally, we can export the GeoDataFrame using `.to_file()` -function. The function works quite similarly as the export functions in pandas, but here we only need to provide the output path for the Shapefile. Easy isn't it!:

```python
# Determine the output path for the Shapefile
outfp = "L2_data/Senaatintori.shp"

# Write the data into that Shapefile
newdata.to_file(outfp)
```

<!-- #region -->
Now we have successfully created a Shapefile from scratch using geopandas. Similar approach can be used to for example to read coordinates from a text file (e.g. points) and turn that information into a spatial layer.


#### Check your understanding


<div class="alert alert-info">

    
Check the output Shapefile by reading it with geopandas and make sure that the attribute table and geometry seems correct.

</div>

<div class="alert alert-info">
    
Re-project the data to ETRS-TM35FIN (EPSG:3067) and save into a new file!

</div>

<!-- #endregion -->


## Reading data to geopandas from different file formats

In geopandas, we can use a generic function [from_file()](http://geopandas.org/reference.html#geopandas.GeoDataFrame.to_file) for reading in different data formats. Esri Shapefile is the default file format. For other file formats we need to specify which driver to use for reading in the data. In the following section, we show how to read spatial data from a few of the most common vector file formats. To see all supported data formats, you can execute following: 

```python
import geopandas as gpd
gpd.io.file.fiona.drvsupport.supported_drivers
```

### Read / write Shapefile

Shapefile format originally developed by ESRI in the early 1990's is one of the most commonly used data formats (still) used today. The Shapefile is in fact comprised of several separate files that are all important for representing the spatial data. Typically a Shapefile includes (at least) four separate files with extensions `.shp`, `.dbx`, `.shx` and `.prj`. The first three of them are obligatory

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
