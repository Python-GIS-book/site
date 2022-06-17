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

# Creating a raster mosaic

Quite often you need to merge multiple raster files together and create a `raster mosaic`. This can be done easily with the `merge()` -function in Rasterio.

Here, we will create a mosaic based on 2X2m resolution DEM files (altogether 12 files) covering the Helsinki Metropolitan region. If you have not downloaded the DEM files yet, you can do that by running the script from download-data -section of the tutorial.

As there are many `tif` files in our folder, it is not really pracical to start listing them manually. Luckily, we have a module and function called `glob` that can be used to create a list of those files that we are interested in based on search criteria.

Let's start by:
   
  - Importing required modules
  - Finding all `tif` files from the folder where the file starts with `L` -letter.



## Creating a raster mosaic with rioxarray

Read elevation data from S3 bucket for Kilimanjaro region in Africa.

```python
import xarray as xr
import os
import rioxarray as rxr
from rioxarray.merge import merge_datasets

# S3 bucket containing the data
bucket = "https://a3s.fi/swift/v1/AUTH_0914d8aff9684df589041a759b549fc2/PythonGIS"

# Generate urls for the elevation files
urls = [
    os.path.join(bucket, "elevation/kilimanjaro/ASTGTMV003_S03E036_dem.tif"),
    os.path.join(bucket, "elevation/kilimanjaro/ASTGTMV003_S03E037_dem.tif"),
    os.path.join(bucket, "elevation/kilimanjaro/ASTGTMV003_S04E036_dem.tif"),
    os.path.join(bucket, "elevation/kilimanjaro/ASTGTMV003_S04E037_dem.tif"),
]

# Read the files
datasets = [
    xr.open_dataset(url, engine="rasterio").squeeze("band", drop=True) for url in urls
]
```

Investigate how our data looks like:

```python
datasets[0]
```

Visualize the tiles to see how they look like separately:

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(16, 16))

# Plot the tiles to see how they look separately
datasets[0]["band_data"].plot(ax=axes[0][0], vmax=5900, add_colorbar=False)
datasets[1]["band_data"].plot(ax=axes[0][1], vmax=5900, add_colorbar=False)
datasets[2]["band_data"].plot(ax=axes[1][0], vmax=5900, add_colorbar=False)
datasets[3]["band_data"].plot(ax=axes[1][1], vmax=5900, add_colorbar=False)
```

Create a raster mosaic by merging these Datasets:

```python
# Create a mosaic out of the tiles
mosaic = merge_datasets(datasets)
```

Rename the data variable to more intuitive one:

```python
# Add a more intuitive name for the data variable
mosaic = mosaic.rename({"band_data": "elevation"})
```

Plot the end result where the tiles have been merged:

```python
# Plot the mosaic
mosaic["elevation"].plot(figsize=(12, 12))
```

## Clipping raster


Create a GeoDataFrame with bounding box that we can use for clipping the raster:

```python
import geopandas as gpd
from shapely.geometry import box

# Bounding box coordinates
minx = 37.1
miny = -3.3
maxx = 37.6
maxy = -2.85

# Create a GeoDataFrame that will be used to clip the raster
geom = box(minx, miny, maxx, maxy)
clipping_gdf = gpd.GeoDataFrame({"geometry": [geom]}, index=[0], crs="epsg:4326")

# Explore the extent on a map
clipping_gdf.explore()
```

Clip the mosaic with GeoDataFrame:

```python
# Clip the Mosaic with GeoDataFrame and specify CRS
kilimanjaro = mosaic.rio.clip(clipping_gdf.geometry, crs=mosaic.elevation.rio.crs)
kilimanjaro["elevation"].plot()
```

```python
kilimanjaro
```

Save the raster to a GeoTIFF file:

```python
# Save file to GeoTIFF
kilimanjaro.rio.to_raster("data/kilimanjaro.tif", compress="LZMA", tiled=True)
```
