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

# Retrieving data from Web Feature Service (WFS)

Contents:
- Introduce OGC WFS
- Use OWSLib to get capabilities of WFS API
- Retrieve data to geopandas

```python
import geopandas as gpd
import requests
import geojson
from pyproj import CRS
from owslib.wfs import WebFeatureService

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
layer_name = "finland_municipalities.gpkg"

# Write data to disk
#data.to_file(file_name, driver="GPKG")
```
