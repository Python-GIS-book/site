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

It is important to pay attention to the geocoding providers' Terms of Use. Geocoding services might require an API key in order to use them. (i.e. you need to register for the service before you can access results from their API). Furthermore, rate limiting also restrict the use of these services. The
geocoding process might end up in an error if you are making too many requests
in a short time period (eg.  trying to geocode large number of addresses). If you pay for the geocoding service, you can naturally make more requests to the API.

In this lesson we will use the Nominatim geocoder for locating a relatively small number of addresses. The Nominatim API is not meant for super heavy use. Nominatim doesn't require the use of an API key, but the usage of the Nominatim service is rate-limited to 1 request per second (3600 / hour). Users also need to provide an identifier for their application, and give appropriate attribution to using OpenStreetMap data. You can read more about Nominatim usage policy in [here](https://operations.osmfoundation.org/policies/nominatim/) [^nominatim_toc]. When using Nominatim via `geopandas` and `geopy`, we can specify a custom a custom `user_agent` parameter to idenfy our application, and we can add a `timeout` to allow enough time to get the response from the service. 




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

```python tags=["remove_cell"]
import os
os.environ["USE_PYGEOS"] = "0"
import geopandas
```

```python deletable=true editable=true
# Import necessary modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Filepath
fp = "data/Helsinki/addresses.txt"

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
Now we have our data in a `DataFrame` and we can geocode our addresses using the the geocoding function in `geopandas` that uses `geopy` package in the background. The function geocodes a list of addresses (strings) and returns a `GeoDataFrame` with the geocoded result. 

Here we import the geocoding function and geocode the addresses using Nominatim. The addressess are in the column `addr`. Note that we need to provide a custom string (name of your application) in the `user_agent` parameter. We can also add the `timeout`-parameter to specify how many seconds to wait for a response from the service.
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
from geopandas.tools import geocode

# Geocode addresses using Nominatim.
# You can provide your own
geo = geocode(
    data["addr"], provider="nominatim", user_agent="pythongis_book", timeout=10
)
```

```python
geo.head()
```

<!-- #region deletable=true editable=true -->
And Voilà! As a result we have a GeoDataFrame that contains an `address`-column with the geocoded addresses and a `geometry` column containing `Point`-objects representing the geographic locations of the addresses. Notice that these addresses are not the original addresses, but those identified by Nominatim. We can join the data from the original text file to the geocoded result to get the address idss and original addresses along. 

In this case, we can join the information using the `.join()` function because the original data frame and the geocoded output have an identical index and an identical number of rows.
<!-- #endregion -->
```python
join = geo.join(data)
```

```python
join.head()
```

Here we can see the geocoded address (column `address`) and original address (column `addr`) side-by side and verify that the results look correct for the five first rows. Note that in some cases, Nominatim has identified a spesific point-of-interest such as a restaurant as the exact location. Finally, we can save the geocoded addresses to a file.

```python deletable=true editable=true
# Output file path
outfp = "data/Helsinki/addresses.shp"

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

[^GeoJson]: <https://en.wikipedia.org/wiki/GeoJSON>
[^geopy]: <https://geopy.readthedocs.io/en/stable/>
[^nominatim]: <https://nominatim.org/>
[^nominatim_toc]: <https://operations.osmfoundation.org/policies/nominatim/>
[^photon]: <https://photon.komoot.io/>
