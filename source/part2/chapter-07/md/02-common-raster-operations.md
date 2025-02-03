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

# Common raster operations


Add introductory text.


## Clipping raster


One of the common operations when working with raster data is to clip a given raster `Dataset` by another layer. This process allows you to crop the data in a way that only the cells that are e.g. within a given Polygon are selected for further analysis. In the following, we will learn how to do this by using the `.rio.clip()` method that comes with the `rioxarray` library. Let's start by reading the `elevation` dataset that we used earlier in Chapter 7.2:

```python editable=true slideshow={"slide_type": ""}
import xarray as xr
import matplotlib.pyplot as plt

fp = "data/temp/kilimanjaro_dataset.nc"

data = xr.open_dataset(fp, decode_coords="all")
data
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's also plot the data to see how our values look on a map:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
data["elevation"].plot()
plt.title("Elevation in meters");
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
***Figure 7.7.** Elevation of the landscape in North-Eastern Tanzania.*

To be able to clip this `xarray.Dataset`, we first need to create a `geopandas.GeoDataFrame` that contains the geometry that we want to use as our clipping features. In our case, we want to create a simple bounding box that defines the area which we want to keep from the raster. To create the `GeoDataFrame`, we can specify the corner coordinates of our bounding box and utilize the `box` function of `shapely` library which can conveniently create us the geometry (as introduced in Chapter 6.1):
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
import geopandas as gpd
from shapely.geometry import box

# Bounding box coordinates
minx = 36.1
miny = -3
maxx = 36.3
maxy = -2.77

# Create a GeoDataFrame that will be used to clip the raster
bbox_geometry = box(minx, miny, maxx, maxy)
clipping_gdf = gpd.GeoDataFrame(geometry=[bbox_geometry], crs="epsg:4326")

# Explore the extent on a map
clipping_gdf.explore()
```

<!-- #raw editable=true slideshow={"slide_type": ""} raw_mimetype="" tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 7.8}. Our area of interest around the Mt Kitumbene in Tanzania which will be used to clip the raster dataset.}}, center, nofloat}{../img/figure_7-8.png}
{ \hspace*{\fill} \\}
<!-- #endraw -->

***Figure 7.8.** Our area of interest around the Mt Kitumbene in Tanzania which will be used to clip the raster dataset.*

Now after we have created the `GeoDataFrame` we can use it to clip the `xarray.Dataset`. To do this, we use the `.rio.clip()` method which wants as input the `geometries` that will be used for clipping the raster data. We can pass the `gpd.GeoSeries` as an input for this (i.e. the `geometry` column of our `GeoDataFrame`) and we also specify the `crs` to be the same as in out input raster data. It is important that the coordinate reference system of both layers are the same whenever doing GIS operations between multiple layers. Thus, we use a simple `assert` to check the match before doing the clipping:

```python
# Check that the CRS matches between layers (only continues if True)
assert clipping_gdf.crs == data.elevation.rio.crs

# Clip the raster
kitumbene = data.rio.clip(geometries=clipping_gdf.geometry, crs=data.elevation.rio.crs)
```

Perfect! Now we have succesfully clipped the raster with our bounding box. Let's make a map out of our results to see how our data looks like:

```python
kitumbene["elevation"].plot()
plt.title("Elevations around Mt Kitumbene");
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
***Figure 7.9.** Elevations in the area that was clipped based on a polygon.*

After clipping, it is possible to continue working with the clipped `Dataset` and e.g. find the mean elevation for this area around the Mt Kitumbene. Notice that the operations clipped all the variables in our `Dataset` simultaneously. We can extract basic statistics from `elevation` and inspect the relative height in this area as follows:
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Mean elevation
kitumbene["elevation"].mean().item()
```

```python
# Update the relative height considering the minimum elevation on this area
kitumbene["relative_height"] = kitumbene["elevation"] - kitumbene["elevation"].min()

# Mean of the relative height
kitumbene["relative_height"].max().item()
```

We can see that the mean elevation in this area is approximately 1470 meters while the maximum relative height is ~2100 meters. We needed to recalculate the relative height because the baseline minimum elevation in the landscape changed significantly after the clipping operation.


## Masking a raster

Another commonly used approach when working with raster data is to mask the data based on certain criteria or using another geographical layer as a mask. One common reasons for doing this is for example to exclude water bodies (e.g. lakes or oceans) from the terrain when doing specific analyses. In the following, we will continue working with the same elevation data and mask out the lakes from our raster dataset that exist in our study area. 

Let's start by downloading data from OpenStreetMap (OSM) about existing lakes in our study area. To do this, we first extract the bounds of our raster `Dataset` and then use `osmnx` library to fetch all OSM elements that have been tagged with key `"water"` and `"lake"` (read more about `osmnx` from Chapter 9.1):

```python
import osmnx as ox

# Extract the bounding box based on the extent of the raster
data_bounds_geom = box(*data["elevation"].rio.bounds())

# Retrieve lakes from the given area
lakes = ox.features_from_polygon(data_bounds_geom, tags={"water": ["lake"]})

# Plot the raster and lakes on top of each other
fig, ax = plt.subplots(figsize=(12, 8))
data["elevation"].plot(ax=ax)
lakes.plot(ax=ax, facecolor="lightblue", edgecolor="red", alpha=0.4);
```

***Figure 7.10.** Existing lakes that are present in our study area.*

As we can see from the Figure 7.10, there is one large lake and multiple smaller ones in our study that we might not want to be taken into account when analyzing the terrain. Luckily, we can easily mask these areas out of our `Dataset` by using `rioxarray`. To do this, we can use the same `.rio.clip()` method which we used in the previous example. However, in this case, we do not want to totally remove those cells from our `Dataset` but only mask them out, so that the values on those areas are replaced with NaN values. By using parameters `drop=False` and `invert=True`, the cells that are intersecting with the lake geometries will be masked with NaNs: 

```python
masked_data = data.rio.clip(geometries=lakes.geometry, 
                            drop=False,
                            invert=True,
                            crs=data.elevation.rio.crs, 
                           )
```

```python
masked_data["elevation"].plot()
plt.title("Elevation data with a mask");
```

***Figure 7.11.** A Dataset where the lakes have been masked out (shown with white color).*

As a result, we now have a new `Dataset` where the elevation values overlapping with the lakes have been converted to NaNs. We can now compare whether e.g. the mean land surface elevation differs from the original one where the lakes were still included:

```python
print("Mean elevation with lakes:", data["elevation"].mean().round().item())
print("Mean elevation without lakes:", masked_data["elevation"].mean().round().item())
```

Based on this comparison, we can see that masking out the lakes increases the mean elevation in the area by approximately 30 meters. In a similar manner, you can mask any `rioxarray.Dataset` with given mask features that you want to remove from the analysis. 


## Creating a raster mosaic by merging datasets

One very common operation when working with raster data is to combine multiple individual raster layers (also called as tiles) into a single larger raster dataset, often called as raster mosaic. This can be done easily with the `merge_datasets()` -function in `rioxarray`.
Here, we will create a mosaic based on DEM files (altogether 4 files) covering Kilimanjaro region in Tanzania. First we will read elevation data from an S3 bucket. Let's start by creating a list of URL paths to given `GeoTiff` files that we have

```python
import xarray as xr
from pathlib import Path
import rioxarray

# S3 bucket containing the data
bucket = "https://a3s.fi/swift/v1/AUTH_0914d8aff9684df589041a759b549fc2/PythonGIS"
path = Path(bucket)

# Generate urls for the elevation files
urls = [
    path / "elevation/kilimanjaro/ASTGTMV003_S03E036_dem.tif",
    path / "elevation/kilimanjaro/ASTGTMV003_S03E037_dem.tif",
    path / "elevation/kilimanjaro/ASTGTMV003_S04E036_dem.tif",
    path / "elevation/kilimanjaro/ASTGTMV003_S04E037_dem.tif",
]

# Show the first path
urls[0]
```

Now we have a list of URL paths to the files that we want to read into `xarray`. To do this, we create a nested loop where we iterate over the `urls` list one `url` at a time and read the `GeoTiff` file using the `.open_dataset()` function as we introduced in Chapter 7.2:

```python
datasets = [xr.open_dataset(url, engine="rasterio", masked=True, band_as_variable=True) for url in urls]
```

Now we have stored all the `xarray.Dataset` layers inside the list `datasets`. We can investigate the contents of the first `Dataset` in our list as follows:

```python
datasets[0]
```

```python
datasets[0].rio.shape
```

As we can see an individual `Dataset` has a shape with 3601 cells on each dimension (x and y) and the name of the data variable `band_1` which represents the elevation values. Let's visualize these four raster tiles in separate maps to see how they look like. To do this, we use `plt.subplots()` to initialize a figure with 2x2 subplots and then visualize the rasters one by one. We use `vmax` parameter to specify a same value scale for each layer that makes the colors in the map comparable:

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(16, 16))

# Plot the tiles to see how they look separately
datasets[0]["band_1"].plot(ax=axes[0][0], vmax=5900, add_colorbar=False)
datasets[1]["band_1"].plot(ax=axes[0][1], vmax=5900, add_colorbar=False)
datasets[2]["band_1"].plot(ax=axes[1][0], vmax=5900, add_colorbar=False)
datasets[3]["band_1"].plot(ax=axes[1][1], vmax=5900, add_colorbar=False);
```
***Figure 7.12.** Four elevation raster layers plotted next to each other.*

From the figure we can see that these four raster tiles seem to belong together naturally as the elevation values as well as the coordinates along the x- and y-axis continue smoothly. Hence, we can stitch them together into a single larger raster `Dataset`.
To merge multiple `xarray.Dataset`s together, we can use the `.merge_datasets()` function from `rioxarray`:

```python
from rioxarray.merge import merge_datasets

mosaic = merge_datasets(datasets)
mosaic
```

Excellent! Now we have successfully merged the individual datasets together which is evident from the shape of the new `Dataset` that has 7201 cells on x and y axis. Let's now rename our data variable to a more intuitive one and plot the result to see how the end result looks like:

```python
mosaic = mosaic.rename({"band_1": "elevation"})
```

```python
mosaic["elevation"].plot(figsize=(12, 12))
plt.title("Elevation values covering larger area in the region close to Kilimanjaro");
```

***Figure 7.13.** A raster mosaic where four raster tiles were merged together.*

The end result looks good and we can see clearly the Mount Kilimanjaro which is the highest mountain in Africa 5895 meters above sea level and the highest volcano in the Eastern Hemisphere. 


## Raster to vector conversion (vectorize)

Another commonly used technique commonly needed when working with geographic data is to convert the data from raster to vector format and vice versa. These conversion techniques are commonly called as `vectorize` or `rasterize` operations. When we convert a raster `Dataset` to vector format the raster cells are converted into `shapely.Polygon` objects and the values of the cells are stored as an attribute (column) in the resulting `GeoDataFrame`. To convert `xarray.DataArray` into vector format, you can use the `geocube` library that helps doing these kind of data conversions. In the following, we continue work with the `kitumbene` elevation data that we created earlier by clipping the data and convert this layer into vector format. Let's have a quick look on our input `DataArray` before continuing:

```python
kitumbene["elevation"]
```

To vectorize a given variable in your `xarray.Dataset`, you can use the `vectorize` function from the `geocube` library as follows:

```python
from geocube.vector import vectorize

gdf = vectorize(kitumbene["elevation"])
gdf.shape
```

```python
gdf.head()
```

Great! Now we have converted the `DataArray` into vector format and as a result we got a `GeoDataFrame` that contains the geometries of individual cells as `shapely.Polygon` objects in the `geometry` column, and the cell values in the column `elevation`. The name of the column will be automatically added based on the name of the `DataArray`. As we can see from the `gdf.shape` all the raster cells were added as individual rows into the `GeoDataFrame` which means that our 2D array with 828 rows and 728 columns result in approximately 500 thousand rows in the `GeoDataFrame`. 

When working with surface data (e.g. elevation), it is quite common that there are similar values close to each other in the raster cells and often there are specific regions where the elevation does not change. Therefore, after the vectorization operation it is a good idea to dissolve the geometries based on the data attribute which merges geometries with identical values into single geometries instead of representing all the values as separate polygons. To do this, we can use the `.dissolve()` function which we introduced in more detail in Chapter 6.3:


```python
gdf = gdf.dissolve(by="elevation", as_index=False)
gdf.shape
```

As we can see, the number of rows in our `GeoDataFrame` was reduced dramatically from more than 500 thousand rows into a bit over 2000 rows. Let's finally plot our `GeoDataFrame` to see how the data looks like:

```python
gdf.plot(column="elevation");
```

***Figure 7.14.** The elevation map made from the vectorized data.*

As we can see from the figure, the map looks identical to our original `DataArray` (Figure 7.9) which means that the conversion works as it should. 

It is good to keep in mind that the raster data structure (i.e. arrays) is much more efficient way to process continuous surfaces. When every cell in the 2D array is converted into polygon geometries, the processing and visualization of the data typically becomes more resource intensive for the computer (making things slower). There are approaches to deal with this issue e.g. by categorizing the data values of the surface into specific elevation classes (e.g. with 5 meter intervals) and then dissolving the geometries into larger Polygon shapes (as we did earlier without categorization). Another technique to consider is downscaling your data into lower resolution, meaning that the size of an individual cell will be larger. Naturally, both of these techniques has an impact on the quality of the data as the data is generalized and aggregated. It is a good idea to do the preprocessing steps for the raster data before vectorizing it, especially if you have large raster arrays because the array operations in `xarray` are very efficient. 


## Vector to raster conversion (rasterize)

Now as we have seen how to convert the data from raster to vector, let's continue and see how to do the conversion from vector to raster data format, i.e. how to rasterize a vector dataset. In this example, we aim to rasterize the lakes that we downloaded earlier from OpenStreetMap. Let's have a look how the data looks like:

```python
lakes = ox.features_from_polygon(data_bounds_geom, tags={"water": ["lake"]})

lakes.plot();
```

***Figure 7.15.** Lakes represented in vector format.*

```python
lakes.shape
```

```python
lakes.tail(2)
```

As we can see the `lakes` `GeoDataFrame` contains polygons and have various attributes associated with them, although majority of these attributes do not contain any relevant data. Thus, let's just pick a few columns that are most interesting to us:

```python
lakes = lakes[["geometry", "water", "name"]].copy().reset_index()
lakes.shape
#lakes.tail(3)
```

Our `GeoDataFrame` does not currently really include any useful numerical data (except `id`) that we would perhaps want to store as an attribute into our raster `DataArray`. Thus, let's create one numerical attribute into our data and calculate the area of the lakes as something we will use as values in our raster. We can use some of the vector data processing tricks to do this which were introduced in Chapter 6:

```python
# Reproject to metric system
lakes_utm = lakes.to_crs(epsg=21037)

# Calculate the area in km2
lakes_utm["area_km2"] = lakes_utm.area / 1000000

# Join the area information with the original gdf
lakes = lakes.join(lakes_utm[["area_km2"]])
```

```python
lakes.head(5)
```

In the previous, we first reprojected the data into EPSG:21037 (Arc 1960 / UTM zone 37S) which is a UTM (Universal Transverse Mercator) projection that covers most of Tanzania and provides accurate distance and area calculations. Then we calculated the area of the lakes into square kilometers and finally joined the information about the area into our original `GeoDataFrame`that is in WGS84 coordinate reference system. 

By looking at the resulting table we can see something interesting. It appears that the `lakes` data contain some duplicate rows as the `Lake Natron` is present twice in our table (something to do with fetching data from OSM). This can cause issues when rasterizing the data because there should not be geometries that overlap with each other. Thus, we want to remove all duplicate rows from the data before continuing:

```python
lakes = lakes.drop_duplicates()
lakes.shape
```

As a result, two duplicates were dropped from the `GeoDataFrame`. Now we are ready to rasterize our `GeoDataFrame` into `xarray`. To do this, we can use the `make_geocube()` function from the `geocube` library:

```python
from geocube.api.core import make_geocube

lakes_ds = make_geocube(vector_data=lakes,
                        measurements=["id", "area_km2"],
                        resolution=(-0.01, 0.01),
                        output_crs="epsg:4326"
                       )
lakes_ds
```

As a result, we now have an `xarray.Dataset` with two data variables. In the code above, we specified that the `lakes` `GeoDataFrame` is used as the input `vector_data` and the columns `id` and `area_km2` should be included as the `measurements`, i.e. the data that are stored into separate `xarray` variables. The `resolution` parameter defines the spatial resolution of the output grid, i.e. size of a single pixel in the raster. In our case, we specified a tuple with values `(-0.01, 0.01)` that are presented as decimal degrees because the coordinate reference system of our input data is WGS84. Thus, resolution `0.01` indicates that the size of a single pixel in our raster is approximately 1x1 kilometers (1.11km). The negative sign for x-resolution is used because raster transformations often use negative values for the y-axis in many CRS systems, where the y-coordinates decrease as you move down the raster. Finally, the `output_crs` defines the CRS for the resulting `Dataset`. Let's make a map out of our data to see how the result looks like:

```python
lakes_ds["area_km2"].plot()
plt.title("Rasterized lakes");
```

***Figure 7.16.** Lakes that have been rasterized into `DataArray` at approximately 1 km resolution.*

Quite often when rasterizing vector data, you actually want to fit the output to have identical resolution to an already existing `xarray.Dataset` and align it with the other raster layer. For example in our case, we can use the `data` raster (with elevation values) as a target so that the resolution, dimensions and alignment would fit with the existing `Dataset`. We can achieve this by using the `like` parameter in `make_geocube()` function. This will ensure that the output aligns with the existing raster having same resolution and dimensions:

```python
aligned_ds = make_geocube(vector_data=lakes,
                          measurements=["id", "area_km2"],
                          like=data)
aligned_ds
```

```python
aligned_ds["area_km2"].plot();
```

***Figure 7.17.** Lakes that have been rasterized and aligned with an existing `Dataset`.*

As a result, we have now rasterized the lakes in a way that the `aligned_ds` aligns with the existing `Dataset` containing the elevation values. This technique can be very useful especially when you want to do calculations (map algebra) between multiple raster layers (more about map algebra in Chapter 7.5). 


## Resampling raster data

Finally, we will introduce a technique that allows you to resample your raster data. Resampling refers to changing the cell values due to changes in the raster grid for example due to changing the effective cell size of an existing dataset. There are two ways to resample your raster data. Upscaling (or upsampling) refers to cases in which convert the raster to higher resolution, i.e. smaller cells. Downscaling (or downsampling) is resampling to lower resolution, i.e. having larger cell sizes. In the following, we will see how we can resample an `xarray.Dataset` by downscaling and upscaling the data. 

We can resample `xarray` data by using the `rioxarray` library that can be used to downscale and upscale raster data. Whenever downscaling data, you are ultimately aggregating the information because multiple individual cells are merged into one larger cell that is then stored in the output grid. Thus, it is important to decide the `resampling` method which determines how the data values are aggregated. Depending on the input data, you might for example calculate the `average` of the input cells which will then be stored in the output grid cell. In our case, taking the average makes sense, because our input data represents elevation. However, in some cases you might be interested to `sum` all the cell values for example if your input data would represent population counts in a given region. There are also various other ways to resample the data, such as extracting the minimum (`min`), maximum (`max`), median (`med`) or the `mode` from the input cells. The `mode` means that the value which appears most often in the input raster cells is selected to the output raster cell.  


### Downscaling

In the following, we will downscale our elevation data significantly by using a downscale factor of `50`. This means that the output raster will be 50 times smaller in terms of its dimensions compared to the input raster. To downscale the data, you need to define the new `shape` for our target raster `Dataset`. Here, we use a specific `downscale_factor` that is used to calculate the new width and height for the output `Dataset`. The width and height for the target `Dataset` need to be provided as integer values. Thus we ensure that the dimensions are integers by rounding (`round()`) and converting the number with`int()`. The `.rio.reproject()` method is then used to downscale the data using the new `shape`. The `resampling` parameter defines the resampling method which in our case will be `Resampling.average`. The `Resampling` class from `rasterio` library provides the methods for resampling:

```python
from rasterio.enums import Resampling

# Define the new shape
downscale_factor = 50
new_width = int(round(data.rio.width / downscale_factor))
new_height = int(round(data.rio.height / downscale_factor))

# Downscale the data
data_downscaled = data.rio.reproject(
    dst_crs=data.rio.crs,
    shape=(new_height, new_width),
    resampling=Resampling.average,
)
```

```python
data_downscaled
```

As we can see, now the dimensions of the new downscaled `Dataset` is 72x72 cells on x and y axis which is 50 times smaller compared to the original `data` that we used as input:

```python
data.rio.shape
```

```python
print("Original resolution:", data.rio.resolution())
print("Downscaled resolution:", data_downscaled.rio.resolution())
```

By comparing the spatial resolution between the datasets, we can see that the new resolution of the downscaled `Dataset` is approximately 1x1 km (0.013 Decimal degrees). Let's finally visualize the downscaled `Dataset` to investigate how the result looks on a map:

```python
data_downscaled["elevation"].plot()
plt.title("Downscaled elevation data");
```

***Figure 7.18.** Downscaled data using a downscale factor of 50.*

The downscaling operation seem to have worked well as the patterns are still clearly similar compared to the input data (Figure 7.7), although the spatial resolution is much lower. The data is downscaled so much that it is actually possible to identify individual pixels of the grid. 


### Upscaling

The process of upscaling is very similar to downscaling and we use the same methods to increase the resolution of the input raster. In the following, we will specify that the new shape of the output `Dataset` will be two times larger than the input data. When upscaling, you are ultimately estimating values to given locations based on existing raster values. In this case, 

```python
from rasterio.enums import Resampling

# Define the new shape
upscale_factor = 2
new_width = data.rio.width * upscale_factor
new_height = data.rio.height * upscale_factor

# Upscale the data
data_upscaled = data.rio.reproject(
    data.rio.crs,
    shape=(new_height, new_width),
    resampling=Resampling.bilinear,
)
```

```python
data_upscaled
```

```python
data["elevation"].plot();
```

```python

```
