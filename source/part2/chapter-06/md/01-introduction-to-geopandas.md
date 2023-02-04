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

Now as we have learned how to create and represent geographic data in Python using `shapely` objects, we will continue and use [geopandas](https://geopandas.org/) [^geopandas] as our main tool for spatial data analysis. Geopandas extends the capacities of pandas (which we covered in the Part I of the book) with geospatial operations. The main data structures in geopandas are `GeoSeries` and `GeoDataFrame` which extend the capabilities of `Series` and `DataFrames` from pandas. This means that we can use many familiar methods from pandas also when working with geopandas and spatial features. A `GeoDataFrame` is basically a `pandas.DataFrame` that contains one column for geometries. The geometry column is a `GeoSeries` which contains the geometries  as `shapely` objects (points, lines, polygons, multipolygons etc.). 

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

```python tags=["remove_cell"]
# You can use this cell to enter your solution.
```

```python tags=["remove_book_cell", "hide_cell"]
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

```python tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python tags=["remove_book_cell", "hide_cell"]
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
