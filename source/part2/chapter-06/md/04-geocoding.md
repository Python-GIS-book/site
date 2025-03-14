---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} -->
# Geocoding

Geocoding is the process of transforming place names or addresses into coordinates (and vice versa). In this section, you will learn how to geocode addresses using `geopandas` and `geopy` [^geopy] libraries. `Geopy` and other geocoding libaries (such as [geocoder](http://geocoder.readthedocs.io/)) make it easy to locate the coordinates of addresses, cities, countries, and landmarks across the globe. In practice, geocoding libraries are often based on *{term}`Application Programming Interfaces (APIs) <API>`* where you can send requests, and receive responses in the form of place names, addresses and coordinates. `Geopy` offers access to several geocoding services, such as Photon [^photon] and Nominatim [^nominatim] that rely on data from OpenStreetMap, among various other services. You can see a full list of supported geocoding services and usage details from the [geopy documentation](https://geopy.readthedocs.io/en/stable/) [^geopy].

It is important to pay attention to the geocoding providers' Terms of Use. Geocoding services might require an API key in order to use them which means that you need to register for the service before you can access results from their API. Furthermore, rate limiting also restrict the use of these services. The geocoding process might end up in an error if you are making too many requests in a short time period (such as when trying to geocode large number of addresses). If you pay for the geocoding service, you can naturally make more requests to the API.
<!-- #endregion -->

### Geocoding addresses

Next, you will learn how to use the `Nominatim` geocoder for locating a relatively small number of addresses. The Nominatim API is not meant for super heavy use. Nominatim doesn't require the use of an API key, but the usage of the Nominatim service is rate-limited to 1 request per second (3600 / hour). Users also need to provide an identifier for their application, and give appropriate attribution to using OpenStreetMap data. You can read more about Nominatim usage policy from their [documentation](https://operations.osmfoundation.org/policies/nominatim/) [^nominatim_toc]. When using Nominatim via `geopandas` and `geopy`, we can specify a custom `user_agent` parameter to idenfy our application, and we can add a `timeout` to allow enough time to get the response from the service.  

We will geocode addresses stored in a text file called `addresses.txt`. These addresses are located in the Helsinki Region in Southern Finland. The first rows of the data look like this:

```
id;addr
1000;Itämerenkatu 14, 00101 Helsinki, Finland
1001;Kampinkuja 1, 00100 Helsinki, Finland
1002;Kaivokatu 8, 00101 Helsinki, Finland
1003;Hermannin rantatie 1, 00580 Helsinki, Finland
```

As we can see, we have an `id` for each row and an address on a column `addr`. Let's first read the data into a pandas DataFrame using the `read_csv()` -function:

```python deletable=true editable=true
# Import necessary modules
import pandas as pd
import geopandas as gpd

# Filepath
fp = "data/Helsinki/addresses.txt"

# Read the data
data = pd.read_csv(fp, sep=";")
data.head()
```

<!-- #region deletable=true editable=true -->
Now we have our data in a `DataFrame` and we can geocode our addresses using the the `geopandas.tools.geocode()` function in `geopandas` that uses `geopy` library under the hood. The function geocodes a list of addresses (strings) and returns a `GeoDataFrame` with the geocoded result. In the following, we import the `geocode()` function and geocode the addresses using Nominatim. Then we pass the addressess to the function from the column `addr`. As discussed earlier, we need to provide a custom string (name of your application) in the `user_agent` parameter to identify ourselves. We also use the `timeout`-parameter to specify how many seconds to wait for a response from the service:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
from geopandas.tools import geocode

geo = geocode(
    data["addr"], provider="nominatim", user_agent="pythongis_book", timeout=10
)
geo.head()
```

<!-- #region deletable=true editable=true -->
Voilà! As a result we have a `GeoDataFrame` that contains an `address`-column with the geocoded addresses and a `geometry` column containing `Point`-objects representing the geographic locations of the addresses. Notice that these addresses are not the original addresses but those identified by Nominatim. We can join the data from the original text file to the geocoded result to get the address ids and original addresses along. In this case, we join the information using the `.join()` function that makes the table join based on index. We do this because the original data frame and the geocoded output have an identical index and an identical number of rows:
<!-- #endregion -->
```python
join = geo.join(data)
join.head()
```

Here we can see the geocoded address (column `address`) and original address (column `addr`) side-by-side and verify that the result looks correct for the first five rows. Note that in some cases, Nominatim has identified a specific point-of-interest, such as a restaurant, as the exact location. Finally, we can have a look how the points look on a map and save the geocoded addresses to a file:

```python
join.explore(color="red", marker_kwds={"radius": 5})
```

<!-- #raw editable=true slideshow={"slide_type": ""} raw_mimetype="" tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 6.34}. Geocoded addresses on a map.}}, center, nofloat}{../img/figure_6-34.png}
{ \hspace*{\fill} \\}
<!-- #endraw -->

_**Figure 6.34**. Geocoded addresses on a map._

```python deletable=true editable=true
# Output file path
outfp = "data/Helsinki/addresses.gpkg"

# Save to Shapefile
join.to_file(outfp)
```

<!-- #region deletable=true editable=true -->
That's it. Now we have successfully geocoded those addresses into Points and made a GeoPackage out of them. Easy isn't it! Nominatim works relatively nicely if you have well defined and well-known addresses such as the ones that we used in this tutorial. In practice, the address needs to exist in the OpenStreetMap database. Sometimes, however, you might want to geocode a "point-of-interest", such as a museum, only based on it's name. If the museum name is not on OpenStreetMap, Nominatim won't provide any results for it, but you might be able to geocode the place using some other geocoders.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["question"] -->
#### Question 6.7

Do another round of geocoding with your own list of addresses from anywhere in the world. Are you happy with the result?

In the above example we passed the address column to the geocoding function. [The geopandas documentation of geopandas.tools.geocode](https://geopandas.org/en/stable/docs/reference/api/geopandas.tools.geocode.html#geopandas-tools-geocode) [^geopandas_geocode] confirms that we should also be able to pass a list of strings to the geocoding tool. So, you should be able to answer this question by defining a list of addresses and using this list as input strings.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# Example list of addresses
address_list = [
    "Pietari Kalmin katu 5, Helsinki, Finland",
    "Konetekniikka 1, Espoo, Finland",
]

# Do the geocoding
geo2 = geocode(
    address_list, provider="nominatim", user_agent="pythongis_book", timeout=10
)

# Check if the result looks correct on a map
geo2.explore(
    color="red", max_zoom=12, marker_kwds=dict(radius=8), tiles="CartoDB Positron"
)
```
## Reverse geocoding

Naturally, it is also possible to do geocoding in a reverse manner, meaning that we have a list of points / coordinates and we want to find out the address for these points. In the following, we continue using the same points that we stored previously into the `geo` `GeoDataFrame`, but at this time, we do the reverse geocoding with them. Let's start by selecting only the `geometry` column from the data:


```python
points = geo[["geometry"]].copy()
points.head()
```

Now we have a simple `GeoDataFrame` with only point objects stored into the `geometry` column. To do the reverse geocoding, i.e. finding addresses to these points, we can use the `reverse_geocode()` function of `geopandas`. The `reverse_geocode()` works similarly as the `geocode()` function that we saw earlier, but in this case the function accepts as an input either a `GeoSeries`, or a list of `shapely` `Point` objects. Similarly as described before, you also should specify the geocoding `provider`, the `user_agent` and the `timeout` value. In the following, we use the geometries stored in the `points` geodataframe and use those to do the reverse geocoding:

```python
from geopandas.tools import reverse_geocode

reverse_geocoded = reverse_geocode(
    points.geometry, provider="nominatim", user_agent="pythongis_book", timeout=10
)
reverse_geocoded.head()
```

As a result, we now have the addresses for each point stored into the `address` column which can be useful, e.g., if you want to visualize the points on a map and also show the address to these locations as an extra information. 


## Footnotes

[^GeoJson]: <https://en.wikipedia.org/wiki/GeoJSON>
[^geopy]: <https://geopy.readthedocs.io/en/stable/>
[^nominatim]: <https://nominatim.org/>
[^nominatim_toc]: <https://operations.osmfoundation.org/policies/nominatim/>
[^photon]: <https://photon.komoot.io/>
[^geopandas_geocode]: <https://geopandas.org/en/stable/docs/reference/api/geopandas.tools.geocode.html#geopandas-tools-geocode>



