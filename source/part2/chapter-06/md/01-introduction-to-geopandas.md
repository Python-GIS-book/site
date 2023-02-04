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

```python tags=["remove_book_cell", "hide_cell"]
# Solution

# You can also plot the data for a visual check
temp.plot()
```

## Footnotes

[^geopandas]: <https://geopandas.org/>
[^NLS_topodata]: <https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database>
[^NLS_lisence]: <https://www.maanmittauslaitos.fi/en/opendata-licence-cc40>
[^OGC_sfa]: <https://www.ogc.org/standards/sfa>
[^paituli]: <https://avaa.tdata.fi/web/paituli/latauspalvelu>
[^topodata_fair]: <https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae>
