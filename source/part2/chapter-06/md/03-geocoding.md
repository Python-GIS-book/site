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

# Geocoding

Geocoding is the process of transforming place names or addresses into coordinates. In this section we will learn how to geocode addresses using `geopandas` and [geopy](https://geopy.readthedocs.io/en/stable/) [^geopy].

Geopy and other geocoding libaries (such as [geocoder](http://geocoder.readthedocs.io/)) make it easy to locate the coordinates of addresses, cities, countries, and landmarks across the globe using web services ("geocoders"). In practice, geocoders are often *{term}`Application Programming Interfaces (APIs) <API>`* where you can send requests, and receive responses in the form of place names, addresses and coordinates. Geopy offers access to several geocoding services, such as [Photon](https://photon.komoot.io/]) [^photon] and [Nominatim](https://nominatim.org/) [^nominatim] that rely on data from OpenStreetMap, among various other services. Check the [geopy documentation](https://geopy.readthedocs.io/en/stable/) [^geopy] for more a list of supported geocoding services and usage details.

Geocoding services might require an API key in order to use them. (i.e. you
need to register for the service before you can access results from their API).
Furthermore, rate limiting also restrict the use of these services. The
geocoding process might end up in an error if you are making too many requests
in a short time period (eg.  trying to geocode large number of addresses). If you pay for the geocoding service, you can naturally make more requests to the
API.

In this lesson we will use the Nominatim geocoder for locating a relatively
small number of addresses. 

It is important to pay attention to the geocoding providers' Terms of Use. For example, the Nominatim API is not meant for super heavy use. Nominatim doesn't require the use of an API key, but the usage of the Nominatim service is rate-limited to 1 request per second (3600 / hour). Users also need to provide an identifier for their application, and give appropriate attribution to using OpenStreetMap data. You can read more about Nominatim usage policy in [here](https://operations.osmfoundation.org/policies/nominatim/) [^nominatim_toc]. When using Nominatim via `geopandas` and `geopy`, we can specify a custom a custom `user_agent` parameter to idenfy our application, and we can add a `timeout` to allow enough time to get the response from the service. 




### Geocoding addresses

We will geocode addresses stored in a text file called `addresses.txt`. These addresses are located in the Helsinki Region in Southern Finland. The first rows of the data look like this:

```
id;addr
1000;Itämerenkatu 14, 00101 Helsinki, Finland
1001;Kampinkuja 1, 00100 Helsinki, Finland
1002;Kaivokatu 8, 00101 Helsinki, Finland
1003;Hermannin rantatie 1, 00580 Helsinki, Finland
```

We have an `id` for each row and an address on column `addr`. Let's first read the data into a pandas DataFrame using the `read_csv()` -function.

```python deletable=true editable=true
# Import necessary modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Filepath
fp = r"../data/Helsinki/addresses.txt"

# Read the data
data = pd.read_csv(fp, sep=";")
```

Let's check that we imported the file correctly.

```python
len(data)
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
data.head()
```

<!-- #region deletable=true editable=true -->
Now we have our data in a `DataFrame` and we can geocode our addresses using the the geocoding function in `geopandas` that uses `geopy` package in the background. The function geocodes a list of addresses (strings) and return a `GeoDataFrame` containing the resulting point objects in ``geometry`` column. 

Here we import the geocoding function and geocode the addresses (column `addr`) using Nominatim. Note that we need to provide a custom string (name of your application) in the `user_agent` parameter. We can also add the `timeout`-parameter to specifies how many seconds to wait for a response from the service.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Import the geocoding tool
from geopandas.tools import geocode

# Geocode addresses using Nominatim. 
# You can provide your own
geo = geocode(data["addr"], 
              provider="nominatim", 
              user_agent="pythongis_book", 
              timeout=4)
```

```python
geo.head()
```

<!-- #region deletable=true editable=true -->
And Voilà! As a result we have a GeoDataFrame that contains an `address`-column containing the geocoded addresses and a `geometry` column containing `Point`-objects representing the geographic locations of the addresses. Notice that these addresses are given However, the ``id`` column is not there. Thus, we need to join the
information from ``data`` into our new GeoDataFrame ``geo``, thus making
a Table Join.
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
All in all, remember that 
</div>


Now it is easy to save our address points into a Shapefile

```python deletable=true editable=true
# Output file path
outfp = r"../data/Results/addresses.shp"

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

## Footnotes

[^shp]: <https://en.wikipedia.org/wiki/Shapefile> 
[^GeoJson]: <https://en.wikipedia.org/wiki/GeoJSON>
[^geopy]: <https://geopy.readthedocs.io/en/stable/>
[^GPKG]: <https://en.wikipedia.org/wiki/GeoPackage>
[^KML]: <https://en.wikipedia.org/wiki/Keyhole_Markup_Language> 
[^nominatim]: <https://nominatim.org/>
[^nominatim_toc]: <https://operations.osmfoundation.org/policies/nominatim/>
[^photon]: <https://photon.komoot.io/>
