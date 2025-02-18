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


<!-- #region editable=true slideshow={"slide_type": ""} tags=["hide-cell", "remove_cell"] -->
In addition to these concepts, a raster dataset may also be georeferenced using *{term}`Ground Control Points` (GCP)* or *{term}`Rational Polynomial Coefficients` (RPCs)*. Ground Control Points are known locations on the Earth's surface with accurately measured coordinates using e.g. GPS device or derived from high-resolution reference image. They are used to improve georeferencing accuracy by linking raster pixel positions to real-world coordinates. GCPs help correct distortions in aerial or satellite images by creating polynomial transformations. Typically a dataset will have multiple GCPs distributed across the image. 

Rational Polynomial Coefficients (RPCs) provide an alternative georeferencing method, often used for high-resolution satellite imagery. Instead of an affine transform, RPCs model the relationship between image coordinates and real-world coordinates using rational polynomial coefficients which are typically provided by satellite image providers. They allow for more complex transformations, especially in cases where elevation variations affect image positioning. 
<!-- #endregion -->

## Accessing metadata about coordinate reference system

Now as we know some basics about the georeferensing raster data, let's start and investigate how the coordinate reference system information is stored in `xarray` / `rioxarray`. Let's start by reading a raster dataset that we have also used in previous chapters:

```python
import xarray as xr
import matplotlib.pyplot as plt

fp = "data/temp/kilimanjaro_dataset.nc"

data = xr.open_dataset(fp, decode_coords="all")
data
```

As was already briefly shown in Chapter 7.2, we can call the `.rio.crs` to access the Coordinate Reference System information attached to our raster dataset:

```python
data.rio.crs
```

```python
type(data.rio.crs)
```

As we can see, the `.rio.crs` returns some basic information about the coordinate reference system, and in our case, reports that the EPSG code of the dataset is `4326` (i.e. WGS84). When checking the type of the object we can see that the `rio.crs` it is actually a `CRS` class object from `rasterio` library that contains some helpful functionalities related to working with CRS. For instance, if you want to extract the EPSG-code as a number, you can call the `.to_epsg()` method: 

```python
data.rio.crs.to_epsg()
```

In addition, in casse you are interested to investigate the CRS information in Well-Known Text (WKT) format, it is easy to parse this information using the `.to_wkt()` method:

```python
data.rio.crs.to_wkt()
```

There are also various other useful functionalities that you can explore via the `.crs` accessor, such as:

- `.is_geographic` which returns `True` if the data is in geographic CRS (`False` otherwise)
- `.is_projected` which returns `True` if the data is in projected CRS, e.g. UTM (`False` otherwise)
- `.units_factor` which returns information about the units of the coordinates (degree or meter)

Another place to find relevant information about the coordinate reference system is to look at the contents of the `spatial_ref` attribute in the `xarray.Dataset`. We can access various key attributes of the CRS by calling `.spatial_ref.attrs` that prints a Python `dictionary` containing the information:

```python
data.spatial_ref.attrs
```

To find out the names of the CRS related attributes, you can access the `.key()` of the dictionary which returns a collection of keys available in the `spatial_ref`:

```python
data.spatial_ref.attrs.keys()
```

To access individual items from the spatial reference attributes, we can do following:

```python
print(data.spatial_ref.attrs["reference_ellipsoid_name"])
print(data.spatial_ref.attrs["grid_mapping_name"])
```

## Accessing information about affine transformation

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

Transforming (i.e. reprojecting) a dataset from one CRS to another can be done easily using the `.rio.reproject()` method. The reprojection can be done in various different ways, but one of the most common way to reproject a dataset to given destination CRS is to use the `dst_crs` parameter that accepts the CRS information as EPSG code, OGC WKT string or Proj4 string (see Chapters 5.3 and 6.4 for further details). In the following, we reproject our data from WGS84 into UTM zone 37S by providing the EPSG code as input, as follows:

```python
data_utm = data.rio.reproject(dst_crs="EPSG:32737")
```

```python
# Alternatively, you can use the estimated UTM zone directly as input
data_utm2 = data.rio.reproject(data.rio.estimate_utm_crs())
```

Now our data has been successfully reprojected into `EPSG:32737` which means that the coordinates originally represented in decimal degrees were transformed into meters. Let's investigate the coordinates of our reprojected `Dataset` and compare those against the original coordinates:

```python
print("Reprojected X-coordinates:")
print(data_utm.x.values)

print("\nReprojected Y-coordinates:")
print(data_utm.y.values)
```

```python
print("Original X-coordinates:")
print(data.x.values)

print("\nOriginal Y-coordinates:")
print(data.y.values)
```

As we can see, the coordinates contain now much larger numbers compared to the original x- and y-coordinates represented as decimal degrees. This is expected because the coordinates are based on a false easting and northing in which the easting (X coordinate) represents the distance in meters from the central meridian of the given UTM zone while the northing (Y coordinate) is distance from the equator in meters. To avoid dealing with negative numbers, a false easting of 500,000 meters is added to the central meridian. Thus a point that has an easting of 400000 meters is about 100 km west of the central meridian.

Let's continue and compare the shape of our reprojected raster to the original one:

```python
print("Shape of the reprojected raster:")
data_utm.rio.shape
```

```python
print("Shape of the original raster:")
data.rio.shape
```

Wait. What?! As we can see, the shape of the raster has changed during the CRS transformation. This might seem weird, but it is actually quite expected. When you reproject raster data to a new coordinate reference system, like transforming from geographic WGS84 coordinate reference system to metric UTM zone 37S, a few things happen that can change the shape and size of the output raster. WGS84 is a geographic CRS that uses degrees, while UTM is a projected CRS in meters. When we transform to UTM, the curved surface of the Earth gets flattened, causing slight distortions. The grid cells, originally evenly spaced in degrees, now stretch and warp in the UTM projection, that can change the dimensions. In addition, the bounding box (extent) of the output raster might shift or expand. When projecting, `rioxarray` needs to make sure that the grid is properly aligned, so it adjusts the pixel grid to fit the new projection that aims to prevent data loss. These processes are reasons why `rioxarray` might add or remove rows/columns to preserve proper alignment when reprojecting data.

Let's finally plot our reprojected data to see that the output looks similar to the original data:

```python
data_utm["elevation"].plot()
plt.title("Reprojected elevation data in UTM Zone 37S");
```

_**Figure 7.21.** Reprojected raster data in which the coordinates are represented in meters._
