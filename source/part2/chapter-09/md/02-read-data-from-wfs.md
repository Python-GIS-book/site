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

## Read Web Feature Service (WFS)

This script was used to generate input data for this tutorial (FileGDB and tab were created separately). Source: Statistics finland WFS.

```python
import geopandas as gpd
import requests
import geojson
from pyproj import CRS

# Specify the url for the backend.
# Here we are using data from Statistics Finland: https://www.stat.fi/org/avoindata/paikkatietoaineistot_en.html. (CC BY 4.0)
url = "http://geo.stat.fi/geoserver/tilastointialueet/wfs"

# Specify parameters (read data in json format).
params = dict(
    service="WFS",
    version="2.0.0",
    request="GetFeature",
    typeName="tilastointialueet:kunta4500k",
    outputFormat="json",
)

# Fetch data from WFS using requests
r = requests.get(url, params=params)

# Create GeoDataFrame from geojson and set coordinate reference system
data = gpd.GeoDataFrame.from_features(geojson.loads(r.content), crs="EPSG:3067")
```

```python
data.head()
```

```python
# Prepare data for writing to various file formats
data = data.drop(columns=["bbox"])
```

```python
# Check crs
data.crs
```

```python
# filename
layer_name = "finland_municipalities"

# enable writing kml
gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"

# drivers and extensions for different file formats
drivers = {
    "ESRI Shapefile": "shp",
    "GeoJSON": "gjson",
    "KML": "kml",
    "GPKG": "gpkg",
}

# Write layer to different file formats
for driver, extension in drivers.items():

    # Create file path and file name
    file_name = "data/{0}.{1}".format(layer_name, extension)

    # Write data using correct dricer
    data.to_file(file_name, driver=driver)
    print("Created file", file_name)
```
