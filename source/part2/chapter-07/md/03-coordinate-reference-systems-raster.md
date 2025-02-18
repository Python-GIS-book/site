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

# Coordinate reference system management


In this chapter, we focus on understanding how the coordinate reference system (CRS) can be managed with raster data using `rioxarray` library. As we discussed in Chapter 5.3, the process of attaching information about a location to a piece of information is commonly referred as *{term}`georeferencing`*. When considering raster data, there are ultimately two relevant parts to the georeferencing of a raster dataset: 

1. the definition of the local, regional, or global system in which a raster’s pixels are located (CRS), and
2. the parameters by which pixel coordinates are transformed into coordinates in that system.

In the following, we will focus on inspecting different kinds of georeferencing metadata that are supported by `rioxarray`/`rasterio`, as well as learn how to reproject a raster from one coordinate reference system to another which is a commonly needed GIS technique when doing geographic data analysis. 


## Georeferencing raster data - Key concepts

As we have seen from the previous chapters, raster data represents spatial information as a grid of pixels, commonly used for satellite imagery, elevation models, and land cover maps. However, for a raster to be meaningful in a geographic context, it must be correctly georeferenced. Georeferencing ensures that each pixel corresponds to a specific location on Earth. There are a few central concepts related to georeferencing raster data: the *{term}`coordinate reference system` (CRS)*, the *{term}`transform`* and the *{term}`affine`*. Understanding these concepts is crucial for working with spatial data, as they define how a raster aligns with real-world locations.

- The ***CRS*** defines the spatial reference of the raster, specifying how coordinates are measured. It includes a datum (e.g. WGS84) and a projection (e.g. UTM) that determine how the Earth's curved surface is represented in a flat raster dataset. Without a CRS, a raster lacks geographic context.
- The ***transform*** describes how pixel coordinates (row, column) map to real-world coordinates (e.g., meters or degrees). It defines the raster’s scale, rotation, and location.
- The ***affine*** transformation is a mathematical model commonly used in Python to define the spatial transformation of raster data. It consists of six parameters that control translation (position), scaling (resolution), and rotation/skew. 

In addition to these concepts, a raster dataset may also be georeferenced using *{term}`Ground Control Points` (GCP)* or *{term}`Rational Polynomial Coefficients` (RPCs)*. Ground Control Points are known locations on the Earth's surface with accurately measured coordinates using e.g. GPS device or derived from high-resolution reference image. They are used to improve georeferencing accuracy by linking raster pixel positions to real-world coordinates. GCPs help correct distortions in aerial or satellite images by creating polynomial transformations. Typically a dataset will have multiple GCPs distributed across the image. 

Rational Polynomial Coefficients (RPCs) provide an alternative georeferencing method, often used for high-resolution satellite imagery. Instead of an affine transform, RPCs model the relationship between image coordinates and real-world coordinates using rational polynomial coefficients which are typically provided by satellite image providers. They allow for more complex transformations, especially in cases where elevation variations affect image positioning. 



## Extracting geoferencing / CRS attributes

```python
import xarray as xr
import matplotlib.pyplot as plt

fp = "data/temp/kilimanjaro_dataset.nc"

data = xr.open_dataset(fp, decode_coords="all")
data
```

```python
data.spatial_ref.attrs
```

```python
data.rio.crs
```

```python
data.rio.crs.to_epsg()
```

```python
data.rio.crs.to_wkt()
```

```python
# Affine transform (how raster is scaled, rotated, skewed, and/or translated)
affine = data.rio.transform()
affine
```

```python
# Pixel size
print("Pixel size x-direction (a):", affine.a)
print("Pixel size y-direction (e):", affine.e)
```

```python
# Rotation/skew
print("Rotation/skew x-direction (b):", affine.b)
print("Rotation/skew y-direction (d):", affine.d)
```

```python
# Top-left corner's real-world coordinates
print("X-coordinate of the top-left pixel (c):", affine.c)
print("Y-coordinate of the top-left pixel (f):", affine.f)
```

## Estimating the UTM zone of a raster

As we saw previously, our `Dataset` currently has a `WGS84` coordinate reference system (EPSG:4326) in which the coordinates are represented as decimal degrees. For various reasons, you might want to reproject your data into a metric CRS, such as national coordinate reference frames (e.g. EUREF-FIN in Finland) or Universal Transverse Mercator (UTM) coordinate system which divides the Earth into 60 zones and projects each one to a plane (Figure 7.20). Most zones in UTM span 6 degrees of longitude, and each has a designated central meridian. UTM zones are widely used in (geographically) large countries, such as in United States and Canada to represent geographic data in a metric coordinate reference system. 

![_**Figure 7.20.** Universal Transverse Mercator (UTM) zones on an equirectangular world map with irregular zones labeled in red. Image source: cmglee, STyx, Wikialine and Goran tek-en (2019) via Wikimedia Commons, licensed under Creative Commons BY-SA 4.0._](../img/UTM_zones.png)

_**Figure 7.20.** Universal Transverse Mercator (UTM) zones on an equirectangular world map with irregular zones labeled in red. Image source: cmglee, STyx, Wikialine and Goran tek-en (2019) via Wikimedia Commons, licensed under Creative Commons BY-SA 4.0._


It is relatively common to use UTM coordinate reference system especially when working with raster data that covers large areas on a sub-national level. However, many datasets are typically distributed in WGS84, which means that you need to know the UTM zone for a given area that covers the raster dataset before you can reproject the data into metric system. Luckily, `rioxarray` includes a handy method called `.rio.estimate_utm_crs()` that makes it possible to make a sophisticated guess of the UTM-zone that the data falls under. In the following, we will find out the UTM-zone for our raster dataset located in Tanzania:

```python
utm_crs = data.rio.estimate_utm_crs()
utm_crs
```

```python
utm_crs.to_wkt()
```

As we can see, the EPSG-code for our dataset is `32737` which belongs to UTM zone 37S which is correctly identified. Notice that if your data covers large areas that span across multiple UTM zones, it might not be possible to identify the UTM zone for such data. 


## Reprojecting raster data

To reproject, the data we can use the `.rio.reproject()` method. 

```python
data_utm = data.rio.reproject("EPSG:32737")
data_utm
```

```python
data_utm["elevation"].plot()
```

```python

```
