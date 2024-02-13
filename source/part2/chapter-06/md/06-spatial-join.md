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

# Spatial join

Spatial join is yet another classic GIS problem. Getting attributes from one layer and transferring them into another layer based on their spatial relationship is something you most likely need to do on a regular basis. In the previous section (Chapter 6.6), we learned how to perform spatial queries, such as investigating if a Point is located within a Polygon. We can use this same logic to conduct a spatial join between two layers based on their spatial relationship and transfer the information stored in one layer into the other. We could, for example, join the attributes of a polygon layer into a point layer where each point would get the attributes of a polygon that `intersects` with the point. 

**Figure 6.xx** illustrates the basic logic of a spatial join by showing how we can combine information between spatial data layers that are located in the same area (i.e. they overlap with each other). The target here is to combine attribute information of three layers: properties, land use and buildings. Each of these three layers has their own attribute information. Transfering the information between the layers is based on how the individual points in the Properties layer intersect with these layers as shown on the left, i.e. considering different land use areas (commercial, residential, industrial, natural), as well as the building footprints containing a variety of building-related attibute information. On the right, we show the table attributes for these three layers considering the features that intersect with the four Point observations. The table at the bottom shows how the results look after all the attribute data from these layers has been combined into a single table. 

It is good to remember that spatial join is always conducted between two layers at a time. Hence, in practice, if we want to make a spatial join between these three layers shown in **Figure 6.xx**, we first need to conduct the spatial join between Properties and Land use, and then store this information into an intermediate result. After the first join, we need to make another spatial join between the intermediate result and the third layer (here, the Buildings dataset). After these two separate spatial joins, we have achieved the final result shown at the bottom, showing for each property (row) the corresponding attributes from the land use and building layers as separate columns. In a similar manner, you could also continue joining data (attributes) from other layers as long as you need.  

![_**Figure 6.XX**. Spatial join allows you to combine attribute information from multiple layers based on spatial relationship._](../img/spatial-join-basic-idea.png)

_**Figure 6.XX**. Spatial join allows you to combine attribute information from multiple layers based on spatial relationship._


<!-- #region -->
Now as we understand the basic idea behind the spatial join, let's continue to learn a bit more about the details of spatial join. **Figure 6.XX**, illustrates how we can do a spatial join between Point and Polygon layers, and how changing specific parameters in the way the join is conducted influence the results. In spatial join, there are two set of options that you can control, which ultimately influence how the data is transferred between the layers. You can control: 

1) How the spatial relationship between geometries should be checked (i.e. spatial predicates)?, and
2) What kind of table join you want to conduct? (inner, left, or right outer join)

The spatial predicates control how the spatial relationship between the geometries in the two data layers is checked. Only those cases where the spatial predicate returns `True` will be kept in the result. Thus, changing this option (parameter) can have a big influence on your final results after the join. In **Figure 6.XX** this difference is illustrated at the bottom when you compare the result tables *i* and *ii*: In the first table (*i*) the spatial predicate is `within` that gives us 4 rows that is shown in the table. However, on the second result table (*ii*), the spatial predicate is `intersects` which gives us 5 rows. Why is there a difference? This is because the Point with id-number 6 happens to lie exactly at the border of the Polygon C. As you might remember from the  Chapter 6.6, there is a certain difference between these two spatial predicates: The `within` expects that the Point should be inside the Polygon (`False` in our case), whereas the `intersects` returns `True` if at least one point is common between the geometries (`True` in our case). In a similar manner, you could change the spatial predicate to `contains`, `touches`, `overlaps` etc. and the result would change accordingly. 

It is also important to ensure that the logic for investigating these spatial relationships makes sense when deciding which spatial predicate to use. For example, it would not make any sense to check whether Layer 1 (points) contain the Layer 2 (polygons) because Point objects do not have an interior or boundary, thus lacking the ability to contain any geometric object. Doing this kind of spatial join is possible, but the result from this type of spatial join would always return an empty GeoDataFrame.  However, if we change the spatial join criteria and join the data between layers if the Layer 2 (polygons) contain the Layer 1 (points), this would make a perfect sense, and the query would return rows that match with this criteria.   

![_**Figure 6.XX**. Different approaches to join two data layers with each other based on spatial relationships._](../img/spatial-join-alternatives.png)

_**Figure 6.XX**. Different approaches to join two data layers with each other based on spatial relationships._


Luckily, [spatial join is already implemented in Geopandas](http://geopandas.org/mergingdata.html#spatial-joins), thus we do not need to create our own function for doing it. There are three possible types of join that can be applied in spatial join that are determined with ``op`` -parameter in the ``gpd.sjoin()`` -function:

-  ``"intersects"``
-  ``"within"``
-  ``"contains"``

Sounds familiar? Yep, all of those spatial relationships were discussed in the [Point in Polygon lesson](point-in-polygon.ipynb), thus you should know how they work. 

Furthermore, pay attention to the different options for the type of join via the `how` parameter; "left", "right" and "inner". You can read more about these options in the [geopandas sjoin documentation](http://geopandas.org/mergingdata.html#sjoin-arguments) and pandas guide for [merge, join and concatenate](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html).

Let's perform a spatial join between these two layers:
- **Addresses:** the geocoded address-point (we created this Shapefile in the geocoding tutorial)
- **Population grid:** 250m x 250m grid polygon layer that contains population information from the Helsinki Region.
    - The population grid a dataset is produced by the **Helsinki Region Environmental
Services Authority (HSY)** (see [this page](https://www.hsy.fi/fi/asiantuntijalle/avoindata/Sivut/AvoinData.aspx?dataID=7) to access data from different years).
    - You can download the data from [from this link](https://www.hsy.fi/sites/AvoinData/AvoinData/SYT/Tietoyhteistyoyksikko/Shape%20(Esri)/V%C3%A4est%C3%B6tietoruudukko/Vaestotietoruudukko_2018_SHP.zip) in the  [Helsinki Region Infroshare
(HRI) open data portal](https://hri.fi/en_gb/).

<!-- #endregion -->

- Here, we will access the data directly from the HSY wfs:

<!-- #endregion -->

```python
import geopandas as gpd
from pyproj import CRS
import requests
import geojson

# Specify the url for web feature service
url = "https://kartta.hsy.fi/geoserver/wfs"

# Specify parameters (read data in json format).
# Available feature types in this particular data source: http://geo.stat.fi/geoserver/vaestoruutu/wfs?service=wfs&version=2.0.0&request=describeFeatureType
params = dict(
    service="WFS",
    version="2.0.0",
    request="GetFeature",
    typeName="asuminen_ja_maankaytto:Vaestotietoruudukko_2018",
    outputFormat="json",
)

# Fetch data from WFS using requests
r = requests.get(url, params=params)

# Create GeoDataFrame from geojson
pop = gpd.GeoDataFrame.from_features(geojson.loads(r.content))
```

Check the result: 

```python
pop.head()
```

Okey so we have multiple columns in the dataset but the most important
one here is the column `asukkaita` ("population" in Finnish) that
tells the amount of inhabitants living under that polygon.

-  Let's change the name of that column into `pop18` so that it is
   more intuitive. As you might remember, we can easily rename (Geo)DataFrame column names using the ``rename()`` function where we pass a dictionary of new column names like this: ``columns={'oldname': 'newname'}``.

```python
# Change the name of a column
pop = pop.rename(columns={"asukkaita": "pop18"})

# Check the column names
pop.columns
```

Let's also get rid of all unnecessary columns by selecting only columns that we need i.e. ``pop18`` and ``geometry``

```python
# Subset columns
pop = pop[["pop18", "geometry"]]
```

```python
pop.head()
```

Now we have cleaned the data and have only those columns that we need
for our analysis.


## Join the layers

Now we are ready to perform the spatial join between the two layers that
we have. The aim here is to get information about **how many people live
in a polygon that contains an individual address-point** . Thus, we want
to join attributes from the population layer we just modified into the
addresses point layer ``addresses.shp`` that we created trough gecoding in the previous section.

-  Read the addresses layer into memory:

```python
# Addresses filpath
addr_fp = "data/Helsinki/addresses.shp"

# Read data
addresses = gpd.read_file(addr_fp)
```

```python
# Check the head of the file
addresses.head()
```

In order to do a spatial join, the layers need to be in the same projection

- Check the crs of input layers:

```python
addresses.crs
```

```python
pop.crs
```

If the crs information is missing from the population grid, we can **define the coordinate reference system** as **ETRS GK-25 (EPSG:3879)** because we know what it is based on the [population grid metadata](https://hri.fi/data/dataset/vaestotietoruudukko). 

```python
# Define crs
pop.crs = CRS.from_epsg(3879).to_wkt()
```

```python
pop.crs
```

```python
# Are the layers in the same projection?
addresses.crs == pop.crs
```

Let's re-project addresses to the projection of the population layer:

```python
addresses = addresses.to_crs(pop.crs)
```

-  Let's make sure that the coordinate reference system of the layers
are identical

```python
# Check the crs of address points
print(addresses.crs)

# Check the crs of population layer
print(pop.crs)

# Do they match now?
addresses.crs == pop.crs
```

Now they should be identical. Thus, we can be sure that when doing spatial
queries between layers the locations match and we get the right results
e.g. from the spatial join that we are conducting here.

-  Let's now join the attributes from ``pop`` GeoDataFrame into
   ``addresses`` GeoDataFrame by using ``gpd.sjoin()`` -function:

```python
# Make a spatial join
join = gpd.sjoin(addresses, pop, how="inner", predicate="within")
```

```python
join.head()
```

Awesome! Now we have performed a successful spatial join where we got
two new columns into our ``join`` GeoDataFrame, i.e. ``index_right``
that tells the index of the matching polygon in the population grid and
``pop18`` which is the population in the cell where the address-point is
located.

- Let's still check how many rows of data we have now:

```python
len(join)
```

Did we lose some data here? 

- Check how many addresses we had originally:

```python
len(addresses)
```

If we plot the layers on top of each other, we can observe that some of the points are located outside the populated grid squares (increase figure size if you can't see this properly!)

```python
import matplotlib.pyplot as plt

# Create a figure with one subplot
fig, ax = plt.subplots(figsize=(15, 8))

# Plot population grid
pop.plot(ax=ax)

# Plot points
addresses.plot(ax=ax, color="red", markersize=5)
```

_**Figure 6.34**. ADD PROPER FIGURE CAPTION!._

Let's also visualize the joined output:


Plot the points and use the ``pop18`` column to indicate the color.
   ``cmap`` -parameter tells to use a sequential colormap for the
   values, ``markersize`` adjusts the size of a point, ``scheme`` parameter can be used to adjust the classification method based on [pysal](http://pysal.readthedocs.io/en/latest/library/esda/mapclassify.html), and ``legend`` tells that we want to have a legend:


```python
# Create a figure with one subplot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the points with population info
join.plot(
    ax=ax, column="pop18", cmap="Reds", markersize=15, scheme="quantiles", legend=True
)

# Add title
plt.title("Amount of inhabitants living close the the point")

# Remove white space around the figure
plt.tight_layout()
```

_**Figure 6.35**. ADD PROPER FIGURE CAPTION!._

In a similar way, we can plot the original population grid and check the overall population distribution in Helsinki:

```python
# Create a figure with one subplot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the grid with population info
pop.plot(ax=ax, column="pop18", cmap="Reds", scheme="quantiles", legend=True)

# Add title
plt.title("Population 2018 in 250 x 250 m grid squares")

# Remove white space around the figure
plt.tight_layout()
```

_**Figure 6.36**. ADD PROPER FIGURE CAPTION!._

Finally, let's save the result point layer into a file:

```python
# Output path
outfp = "data/Helsinki/addresses_population.shp"

# Save to disk
join.to_file(outfp)
```

## Spatial join nearest

ADD Materials
