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

In the following, we will focus on inspecting different kinds of georeferencing metadata that is supported by `rioxarray`, as well as learn how to reproject a raster from one coordinate reference system to another which is a commonly needed GIS technique when doing geographic data analysis. 


## Georeferencing raster data - Key concepts

As we have seen from the previous chapters, raster data represents spatial information as a grid of pixels, commonly used for satellite imagery, elevation models, and land cover maps. However, for a raster to be meaningful in a geographic context, it must be correctly georeferenced. Georeferencing ensures that each pixel corresponds to a specific location on Earth. There are a few central concepts related to georeferencing raster data: the *{term}`coordinate reference system` (CRS)*, the *{term}`transform`* and the *{term}`affine`*. Understanding these concepts is crucial for working with spatial data, as they define how a raster aligns with real-world locations.

- The ***CRS*** defines the spatial reference of the raster, specifying how coordinates are measured. It includes a datum (e.g. WGS84) and a projection (e.g. UTM) that determine how the Earth's curved surface is represented in a flat raster dataset. Without a CRS, a raster lacks geographic context.
- The ***transform*** describes how pixel coordinates (row, column) map to real-world coordinates (e.g., meters or degrees). It defines the raster’s scale, rotation, and location.
- The ***affine*** transformation is a mathematical model commonly used in Python to define the spatial transformation of raster data. It consists of six parameters that control translation (position), scaling (resolution), and rotation/skew. 

In addition to these concepts, a raster dataset may also be georeferenced using *{term}`Ground Control Points` (GCP)* or *{term}`Rational Polynomial Coefficients` (RPCs)*. Ground Control Points are known locations on the Earth's surface with accurately measured coordinates using e.g. GPS device or derived from high-resolution reference image. They are used to improve georeferencing by linking raster pixel positions to real-world coordinates. GCPs help correct distortions in aerial or satellite images by creating polynomial transformations. Typically a dataset will have multiple GCPs distributed across the image. 

Rational Polynomial Coefficients (RPCs) provide an alternative georeferencing method, often used for high-resolution satellite imagery. Instead of an affine transform, RPCs model the relationship between image coordinates and real-world coordinates using rational polynomial coefficients which are typically provided by satellite image providers. They allow for more complex transformations, especially in cases where elevation variations affect image positioning. 



## Extracting Coordinate Reference System information

```python
import xarray as xr
import matplotlib.pyplot as plt

fp = "data/temp/kilimanjaro_dataset.nc"

data = xr.open_dataset(fp, decode_coords="all")
data
```

```python

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
data.rio.transform()
```

```python

```
