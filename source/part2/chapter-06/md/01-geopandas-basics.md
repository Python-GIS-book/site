---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region -->
# Introduction to spatial data analysis with Geopandas

Here we cover basics steps needed for interacting with spatial data in Python using the geopandas (http://geopandas.org/) library:

- Managing filepaths
- Reading spatial data from file 
- Geometry calculations 
- Writing spatial data to file
- Grouping and splitting spatial data into multiple layers

Geopandas makes it possible to work with geospatial data in Python in a relatively easy way. Geopandas combines the capabilities of the data analysis library [pandas](https://pandas.pydata.org/pandas-docs/stable/) with other packages like [shapely](https://shapely.readthedocs.io/en/stable/manual.html) and [fiona](https://fiona.readthedocs.io/en/latest/manual.html) for managing spatial data. 

The main data structures in geopandas are `GeoSeries` and `GeoDataFrame` which extend the capabilities of `Series` and `DataFrames` from pandas. This means that we can use all our pandas skills also when working with geopandas!  If you need to refresh your memory about pandas, check out week 5 and 6 lesson materials from the [Geo-Python website](geo-python.github.io). 

The main difference between geodataframes and pandas dataframes is that a [geodataframe](http://geopandas.org/data_structures.html#geodataframe) should contain one column for geometries. By default, the name of this column is `'geometry'`. The geometry column is a [geoseries](http://geopandas.org/data_structures.html#geoseries) which contains the geometries (points, lines, polygons, multipolygons etc.) as shapely objects. 



![_**Figure X.X**. GeoDataFrame._](../img/geodataframe.png)

_**Figure X.X**. GeoDataFrame._

As we learned in the Geo-Python course, it is conventional to import pandas as `pd`. Similarly,we will import geopandas as `gpd`:
<!-- #endregion -->

```python
import geopandas as gpd
```

<!-- #region -->
## Input data: Finnish topographic database 

In this lesson we will work with the [National Land Survey of Finland (NLS) topographic database (from 2018)](https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database). 
- The data set is licensed under the NLS' [open data licence](https://www.maanmittauslaitos.fi/en/opendata-licence-cc40) (CC BY 4.0).
- Structure of the data is described in a separate Excel file ([download link](http://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/attachments/2018/10/maastotietokanta_kohdemalli_eng.xlsx)).
- Further information about file naming is available at [fairdata.fi](https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae).

For this lesson, we have acquired a subset of the topographic database as shapefiles from the Helsinki Region in Finland via the [CSC open data portal](https://avaa.tdata.fi/web/paituli/latauspalvelu):

![_**Figure X.X**. Paituli data download._](../img/Paituli_maastotietokanta_download.png)

_**Figure X.X**. Paituli data download._

In this lesson, we will focus on **terrain objects** (Feature group: "Terrain/1" in the topographic database). The Terrain/1 feature group contains several feature classes. **Our aim in this lesson is to save all the Terrain/1 feature classes into separate files**.

*Terrain/1 features in the Topographic Database:*

|  feature class | Name of feature                                            | Feature group |
|----------------|------------------------------------------------------------|---------------|
| 32421          | Motor traffic area                                         | Terrain/1     |
| 32200          | Cemetery                                                   | Terrain/1     |
| 34300          | Sand                                                       | Terrain/1     |
| 34100          | Rock - area                                                | Terrain/1     |
| 34700          | Rocky area                                                 | Terrain/1     |
| 32500          | Quarry                                                     | Terrain/1     |
| 32112          | Mineral resources extraction area, fine-grained material   | Terrain/1     |
| 32111          | Mineral resources extraction area, coarse-grained material | Terrain/1     |
| 32611          | Field                                                      | Terrain/1     |
| 32612          | Garden                                                     | Terrain/1     |
| 32800          | Meadow                                                     | Terrain/1     |
| 32900          | Park                                                       | Terrain/1     |
| 35300          | Paludified land                                            | Terrain/1     |
| 35412          | Bog, easy to traverse forested                             | Terrain/1     |
| 35411          | Open bog, easy to traverse treeless                        | Terrain/1     |
| 35421          | Open fen, difficult to traverse treeless                   | Terrain/1     |
| 33000          | Earth fill                                                 | Terrain/1     |
| 33100          | Sports and recreation area                                 | Terrain/1     |
| 36200          | Lake water                                                 | Terrain/1     |
| 36313          | Watercourse area                                           | Terrain/1     |


According to the [naming convention](https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae), all files that start with a letter `m` and end with `p` contain the objects we are interested in (Terrain/1 polygons). 
<!-- #endregion -->

## Downloading data

You can use `wget` program (available in Binder and CSC Notebooks) to download the data from the command line from this download link: https://github.com/AutoGIS/data/raw/master/L2_data.zip. Let's download the data into the same folder with the lesson 2 notebooks (`.../notebooks/L2`):

1. Open up a new terminal window
2. Navigate to the correct folder in the terminal:

```
# Navigate to lesson 2 notebooks directory:
cd autogis/notebooks/L2
    
```
3. Use `wget` to dowload the data from the dowload link:
    
```
wget https://github.com/AutoGIS/data/raw/master/L2_data.zip
    
```
<div class="alert alert-info">

**Copy-paste**
    
You can paste copied text in JupyterLab Terminal by pressing `SHIFT` + `RIGHT-CLICK` on your mouse and choosing `Paste`.

</div>

Once you have downloaded the `L2_data.zip` file into your (cloud) computer, you can unzip the file using `unzip` command in the Terminal (or e.g. 7zip on Windows if working with own computer). Run the following commands in the `.../notebooks/L2` -directory:

``` 
$ unzip L2_data.zip
$ ls L2_data

```
You can also check the contents of the downloaded and unzipped file in the file browser window. 

The L2_data folder contains several subfolders according to the file strucutre in the topographic database shapefile distribution. After unzipping the downloaded file, you can find the data for this tutorial under: `L2_data/NLS/2018/L4/L41/L4132R.shp`. Notice that Shapefile -fileformat contains many separate files such as `.dbf` that contains the attribute information, and `.prj` -file that contains information about coordinate reference system.


## Managing filepaths

Built-in module `os` provides many useful functions for interacting with the operating system. One of the most useful submodules in the os package is the [os.path-module](https://docs.python.org/2/library/os.path.html) for manipulating file paths. This week, we have data in different sub-folders and we can practice how to use `os` path tools when defining filepaths.

Let's import `os` and see how we can construct a filepath by joining a folder path and file name:

```python
import os

# Define path to folder
input_folder = r"L2_data/NLS/2018/L4/L41/L4132R.shp"

# Join folder path and filename 
fp = os.path.join(input_folder, "m_L4132R_p.shp")

# Print out the full file path
print(fp)
```

## Reading a Shapefile

Esri Shapefile is the default file format when reading in data usign geopandas, so we only need to pass the file path in order to read in our data:

```python
import geopandas as gpd
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
data = data[['RYHMA', 'LUOKKA',  'geometry']]
```

Define new column names in a dictionary:

```python
colnames = {'RYHMA':'GROUP', 'LUOKKA':'CLASS'}
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
print("Number of rows", len(data['CLASS']))
print("Number of classes", data['CLASS'].nunique())
print("Number of groups", data['GROUP'].nunique())
```

It is always a good idea to explore your data also on a map. Creating a simple map from a `GeoDataFrame` is really easy: you can use ``.plot()`` -function from geopandas that **creates a map based on the geometries of the data**. Geopandas actually uses matplotlib for plotting which we introduced in [Lesson 7 of the Geo-Python course](https://geo-python.github.io/site/notebooks/L7/matplotlib.html).

Let's try it out, and plot our GeoDataFrame:

```python jupyter={"outputs_hidden": false}
data.plot()
```

Voilá! As we can see, it is really easy to produce a map out of your Shapefile with geopandas. Geopandas automatically positions your map in a way that it covers the whole extent of your data.

*If you are living in the Helsinki region, you might recognize the shapes plotted on the map!*


## Geometries in Geopandas

Geopandas takes advantage of Shapely's geometric objects. Geometries are stored in a column called *geometry* that is a default column name for
storing geometric information in geopandas.


Let's print the first 5 rows of the column 'geometry':

```python jupyter={"outputs_hidden": false}
data['geometry'].head()
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
    poly_area = row['geometry'].area
    
    # Print info
    print("Polygon area at index {index} is: {area:.0f} square meters".format(index=index, area=poly_area))
```

As you see from here, all **pandas** methods, such as the `iterrows()` function, are directly available in Geopandas without the need to call pandas separately because Geopandas is an **extension** for pandas. 

In practice, it is not necessary to use the iterrows()-approach to calculate the area for all features. Geodataframes and geoseries have an attribute `area` which we can use for accessing the area for each feature at once: 

```python
data.area
```

Let's next create a new column into our GeoDataFrame where we calculate and store the areas of individual polygons:

```python jupyter={"outputs_hidden": false}
# Create a new column called 'area' 
data['area'] = data.area
```

Check the output:

```python
data['area']
```

These values correspond to the ones we saw in previous step when iterating rows.

Let's check what is the `min`, `max` and `mean` of those areas using familiar functions from our previous Pandas lessions.

```python
# Maximum area
round(data['area'].max(), 2)
```

```python
# Minimum area
round(data['area'].min(), 2)
```

```python
# Average area
round(data['area'].mean(), 2)
```

## Writing data into a shapefile

It is possible to export GeoDataFrames into various data formats using the [to_file()](http://geopandas.org/io.html#writing-spatial-data) method. In our case, we want to export subsets of the data into Shapefiles (one file for each feature class).

Let's first select one class (class number `36200`, "Lake water") from the data as a new GeoDataFrame:


```python
# Select a class
selection = data.loc[data["CLASS"]==36200]
```

Check the selection:

```python
selection.plot()
```

- write this layer into a new Shapefile using the `gpd.to_file()` -function:

```python
# Create a output path for the data
output_folder = r"L2_data/"
output_fp = os.path.join(output_folder, "Class_36200.shp")
```

```python
# Write those rows into a new file (the default output file format is Shapefile)
selection.to_file(output_fp)
```

#### Check your understanding


<div class="alert alert-info">

Read the output Shapefile in a new geodataframe, and check that the data looks ok.
</div>

```python
temp = gpd.read_file(output_fp)
```

```python
# Check first rows
temp.head()
```

```python
# You can also plot the data for a visual check
temp.plot()
```

## Grouping the Geodataframe

One really useful function that can be used in Pandas/Geopandas is [groupby()](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html) which groups data based on values on selected column(s). We saw and used this function already in Lesson 6 of the Geo-Python course. 

Next we will automate the file export task; we will group the data based on column `CLASS` and export a shapefile for each class.

Let's continue with the same input file we already read previously into the variable `data`. We also selected and renamed a subset of the columns.

Check again the first rows of our input data:

```python
data.head()
```

The `CLASS` column in the data contains information about different land use types. With `.unique()` -function we can quickly see all different values in that column:

```python jupyter={"outputs_hidden": false}
# Print all unique values in the column
data['CLASS'].unique()
```

- Now we can use that information to group our data and save all land use types into different layers:

```python jupyter={"outputs_hidden": false}
# Group the data by class
grouped = data.groupby('CLASS')

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
    print('Terrain class:', key)
    print('Number of rows:', len(group), "\n")
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

<!-- #region -->
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
<!-- #endregion -->

```python
# Determine output directory
output_folder = r"L2_data/"

# Create a new folder called 'Results' 
result_folder = os.path.join(output_folder, 'Results')

# Check if the folder exists already
if not os.path.exists(result_folder):
    
    print("Creating a folder for the results..")
    # If it does not exist, create one
    os.makedirs(result_folder)
    
else:
    print("Results folder exists already.")
```

At this point, you can go to the file browser and check that the new folder was created successfully.

- Iterate over groups, create a file name, and save group to file:

```python jupyter={"outputs_hidden": false}
# Iterate over the groups
for key, group in grouped:
    # Format the filename 
    output_name = "terrain_{}.shp".format(key)

    # Print information about the process
    print("Saving file", os.path.basename(output_name))

    # Create an output path
    outpath = os.path.join(result_folder, output_name)

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

- save area info to csv using pandas:

```python
# Create an output path
area_info.to_csv(os.path.join(result_folder, "terrain_class_areas.csv"), header=True)
```


## Creating a new GeoDataFrame

Since geopandas takes advantage of Shapely geometric objects, it is possible to create spatial data from scratch by passing Shapely's geometric objects into the GeoDataFrame. This is useful as it makes it easy to convert e.g. a text file that contains coordinates into spatial data layers. Next we will see how to create a new GeoDataFrame from scratch and save it into a Shapefile. Our goal is to define a geometry that represents the outlines of the [Senate square in Helsinki, Finland](https://fi.wikipedia.org/wiki/Senaatintori).



Let's create an empty `GeoDataFrame`

```python
newdata = gpd.GeoDataFrame()
```

```python
print(newdata)
```

We have an empty GeoDataFrame! A geodataframe is basically a pandas DataFrame that should have one column dedicated for geometries. By default, the geometry-column should be named `geometry` (geopandas looks for geometries from this column).  

Let's create the `geometry` column:

```python jupyter={"outputs_hidden": false}
# Create a new column called 'geometry' to the GeoDataFrame
newdata['geometry'] = None
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
coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
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
newdata.at[0, 'geometry'] = poly
```

```python
# Let's see what we have now
print(newdata)
```

Great, now we have a GeoDataFrame with a Polygon that we could already now export to a Shapefile. However, typically you might want to include some attribute information with the geometry. 

Let's add another column to our GeoDataFrame called `location` with text `Senaatintori` that describes the location of the feature.

```python jupyter={"outputs_hidden": false}
# Add a new column and insert data 
newdata.at[0, 'location'] = 'Senaatintori'

# Let's check the data
print(newdata)
```

Okay, now we have additional information that is useful for recognicing what the feature represents. 

The next step would be to **determine the coordinate reference system (projection) for the GeoDataFrame.** GeoDataFrame has an attribute called `.crs` that shows the coordinate system of the data. In our case, the layer doesn't yet have any crs definition:

```python jupyter={"outputs_hidden": false}
print(newdata.crs)
```

We passed the coordinates as latitude and longitude decimal degrees, so the correct CRS is WGS84 (epsg code: 4326). In this case, we can simply re-build the geodataframe and pass the correct crs information to the GeoDataFrame constructor. You will learn more about how to handle coordinate reference systems using pyproj CRS objects later in this chapter.  

Re-create the GeoDataFrame with correct crs definition: 

```python
newdata = gpd.GeoDataFrame(newdata, crs="EPSG:4326")
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

## Summary

In this section we introduced the first steps of using geopandas. More specifically you should know how to:

1. Read data from Shapefile using geopandas

2. Access geometry information in a geodataframe

4. Write GeoDataFrame data from Shapefile using geopandas

5. Automate a task to save specific rows from data into Shapefile based on specific key using `groupby()` -function

6. Extra: saving attribute information to a csv file.


 

```python

```