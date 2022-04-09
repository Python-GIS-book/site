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

<!-- #region deletable=true editable=true -->
# From text to map

<!-- #endregion -->

## Creating geometries from text


### Creating new geometries from scratch

Since geopandas takes advantage of Shapely geometric objects, it is possible to create spatial data from scratch by passing Shapely's geometric objects into the GeoDataFrame. This is useful as it makes it easy to convert e.g. a text file that contains coordinates into spatial data layers. Next we will see how to create a new GeoDataFrame from scratch and save it into a file. Our goal is to define a geometry that represents the outlines of the [Senate square in Helsinki, Finland](https://fi.wikipedia.org/wiki/Senaatintori).



Let's start by creating a new empty `GeoDataFrame` object.

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

## Geocoding

Geocoding is the process of transforming place names or addresses into coordinates.
In this lesson we will learn how to geocode addresses using Geopandas and
[geopy](https://geopy.readthedocs.io/en/stable/).

Geopy and other geocoding libaries (such as [geocoder](http://geocoder.readthedocs.io/))
make it easy to locate the coordinates of addresses, cities, countries, and landmarks
across the globe using web services ("geocoders"). In practice, geocoders are often
Application Programming Interfaces (APIs) where you can send requests, and receive responses in the form of place names, addresses and coordinates.

Geopy offers access to several geocoding services. Check the geopy documentation for more details about how to use each service via Python.

Geopandas has a function called `geocode()` that can geocode a list of addresses (strings) and return a GeoDataFrame containing the resulting point objects in ``geometry`` column. 




### Geocoding addresses

Let's try this out.

We will geocode addresses stored in a text file called `addresses.txt`. These addresses are located in the Helsinki Region in Southern Finland.

The first rows of the data look like this:

```
id;addr
1000;Itämerenkatu 14, 00101 Helsinki, Finland
1001;Kampinkuja 1, 00100 Helsinki, Finland
1002;Kaivokatu 8, 00101 Helsinki, Finland
1003;Hermannin rantatie 1, 00580 Helsinki, Finland
```

We have an `id` for each row and an address on column `addr`.

Let's first read the data into a Pandas DataFrame using the `read_csv()` -function:

```python deletable=true editable=true
# Import necessary modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Filepath
fp = r"data/addresses.txt"

# Read the data
data = pd.read_csv(fp, sep=';')
```

Let's check that we imported the file correctly:

```python
len(data)
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data.head()
```

<!-- #region deletable=true editable=true -->
Now we have our data in a pandas DataFrame and we can geocode our addresses using the [geopandas geocoding function](http://geopandas.org/reference/geopandas.tools.geocode.html#geopandas-tools-geocode) that uses `geopy` package in the background. 

- Let's import the geocoding function and geocode the addresses (column `addr`) using Nominatim. 
- Remember to provide a custom string (name of your application) in the `user_agent` parameter.
- If needed, you can add the `timeout`-parameter which specifies how many seconds we will wait for a response from the service.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Import the geocoding tool
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
geo = geocode(data['addr'], provider='nominatim', user_agent='autogis_xx', timeout=4)
```

```python
geo.head()
```

<!-- #region deletable=true editable=true -->
And Voilà! As a result we have a GeoDataFrame that contains our original
address and a 'geometry' column containing Shapely Point -objects that
we can use for exporting the addresses to a Shapefile for example.
However, the ``id`` column is not there. Thus, we need to join the
information from ``data`` into our new GeoDataFrame ``geo``, thus making
a **Table Join**.
<!-- #endregion -->

<div class="alert alert-info">

**Rate-limiting**

When geocoding a large dataframe, you might encounter an error when geocoding. In case you get a time out error, try first using the `timeout` parameter as we did above (allow the service a bit more time to respond). In case of Too Many Requests error, you have hit the rate-limit of the service, and you should slow down your requests. To our convenience, geopy provides additional tools for taking into account rate limits in geocoding services. This script adapts the usage of [geopy RateLimiter](https://geopy.readthedocs.io/en/stable/#geopy.extra.rate_limiter.RateLimiter) to our input data:

```
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry import Point

# Initiate geocoder
geolocator = Nominatim(user_agent='autogis_xx')

# Create a geopy rate limiter:
geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Apply the geocoder with delay using the rate limiter:
data['temp'] = data['addr'].apply(geocode_with_delay)

# Get point coordinates from the GeoPy location object on each row:
data["coords"] = data['temp'].apply(lambda loc: tuple(loc.point) if loc else None)

# Create shapely point objects to geometry column:
data["geometry"] = data["coords"].apply(Point)
```
All in all, remember that Nominatim is not meant for super heavy use. 
</div>


<!-- #region deletable=true editable=true -->
## Table join (TODO: REMOVE TABLE JOIN FROM HERE!)

<div class="alert alert-info">

**Table joins in pandas**
    
For a comprehensive overview of different ways of combining DataFrames and Series based on set theory, have a look at pandas documentation about [merge, join and concatenate](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html).


</div>


Joining data between two or several tables is a common task in many (spatial) data analysis workflows. As you might remember from our earlier lessons, combining data from different tables based on common
**key** attribute can be done easily in pandas/geopandas using the [merge()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html) -function. We used this approach in the geo-python course [exercise 6](https://geo-python-site.readthedocs.io/en/latest/lessons/L6/exercise-6.html#joining-data-from-one-dataframe-to-another).

However, sometimes it is useful to join two tables together based on the **index** of those DataFrames. In such case, we assume
that there is **same number of records** in our DataFrames and that the **order of the records should be the same** in both DataFrames.

We can use this approach to join information from the original data to our geocoded addresses row-by-row 
``join()`` -function which merges the two DataFrames together
based on index by default. This approach works correctly because the order of the geocoded addresses in ``geo`` DataFrame is the same as in our original ``data`` DataFrame.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
join = geo.join(data)
join.head()
```

<!-- #region deletable=true editable=true -->
Let's also check the data type of our new ``join`` table.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
type(join)
```

<!-- #region deletable=true editable=true -->
As a result we have a new GeoDataFrame called ``join`` where we now have
all original columns plus a new column for ``geometry``. **Note!** If you would do the join the other way around, i.e. `data.join(geo)`, the output would be a pandas DataFrame, not a GeoDataFrame!


<!-- #endregion -->

Now it is easy to save our address points into a Shapefile

```python deletable=true editable=true
# Output file path
outfp = r"data/addresses.shp"

# Save to Shapefile
join.to_file(outfp)
```

<!-- #region deletable=true editable=true -->
That's it. Now we have successfully geocoded those addresses into Points
and made a Shapefile out of them. Easy isn't it!
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Nominatim works relatively nicely if you have well defined and well-known addresses such as the ones that we used in this tutorial. In practice, the address needs to exist in the OpenStreetMap database. Sometimes, however, you might want to geocode a "point-of-interest", such as a museum, only based on it's name. If the museum name is not on OpenStreetMap, Nominatim won't provide any results for it, but you might be able to geocode the place using some other geocoder.
<!-- #endregion -->
