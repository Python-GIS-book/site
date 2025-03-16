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

<!-- #region -->
# Map algebra

Map algebra is often used as an umbrella term for conducting various mathematical and logical operations, as well as spatial analysis operations, based on raster data. These techniques were first developed by Dana Tomlin in the 1970's ({cite}`Tomlin1990`) and they have since then been a fundamental part of raster data analysis in GIS. Map algebra provides a set of operators that can be applied to single or multiple raster layers to produce a new raster layer. For instance, you can do basic mathematical calculations (multiply, sum, divide, etc.) between multiple raster layers that are central to map overlay analysis, or conduct mathematical operations on a single raster to compute values based on a given neighborhood. The latter can be used e.g. to detect hot spots based on the pixel values, in which high values are surrounded by other high values. Map algebra is widely used in terrain analysis, land suitability modeling, hydrological modeling, and environmental assessments. By integrating spatial data with mathematical functions, it enables powerful spatial decision-making.

The operations of map algebra can be divided into different categories:

- **Focal operations** compute values based on a specified neighborhood (e.g. 3x3 window) on a given raster layer.
- **Local operations** apply functions on a cell-by-cell basis between multiple raster layers.
- **Global operations** use all raster cells in computations to calculate e.g. statistical summaries.
- **Zonal operations** analyze values within defined zones, such as calculating average elevation within a watershed.
- **Incremental operations** apply iterative calculations or cumulative functions over space or time (e.g. cumulative cost surfaces, time-step modeling in environmental simulations).


There are various Python libraries that can be used for map algebra. In here, we are focusing on `xarray`, `xarray-spatial` and `rasterstats` libraries that provide numerous useful functionalities to conduct focal, local, global, zonal and incremental operations using raster data. In the following, we will apply map algebra to Digital Elevation Model (DEM) raster data obtained from Eastern Finland to gain knowledge of the topography in this area. In addition, we will learn how it is possible to conduct suitability analysis to find an optimal location to build a new summer house based on specific criteria, and how to conduct path finding on raster data to find least-cost route between two locations across the raster cost surface. 
<!-- #endregion -->

## Focal operations

A focal function operates on a cell and its neighboring cells within a defined window (e.g., 3x3 or 5x5). The output value for each cell is derived by applying a mathematical or statistical operation to the values within that neighborhood.


```python
import xarray as xr
import xrspatial
import matplotlib.pyplot as plt

fp = "data/Tuupovaara_DEM.nc"
data = xr.open_dataset(fp, decode_coords="all")
data
```

```python
# Plot the elevation values and contours
fig, ax = plt.subplots(figsize=(9,7))
data["elevation"].plot(ax=ax)
cs = data["elevation"].plot.contour(ax=ax, colors="red", linewidths=0.5)

# Label contours
ax.clabel(cs, cs.levels, inline=True, fontsize=6);
plt.title("Elevation in Tuupovaara, Finland");
```

_**Figure 7.X.** Elevation surface with contour lines._


### Slope

```python
# Calculate slope 
data["slope"] = xrspatial.slope(data["elevation"])
```

```python
data["slope"].plot(cmap="Greens")
plt.title("Slope (degrees)");
```

_**Figure 7.X.** Slope in degrees calculated from the elevation data._


### Aspect

```python
# Calculate aspect
data["aspect"] = xrspatial.aspect(data["elevation"])
# Filter values that are below 0 (areas without aspect defined)
data["aspect"] = data["aspect"].where(data["aspect"] >=0)
data["aspect"].plot(cmap="jet")
plt.title("Aspect (degree between 0-360)\n0 faces North");
```

_**Figure 7.X.** Aspect surface shows the direction of the slope in degrees._


### Curvature

```python
data["curvature"] = xrspatial.curvature(data["elevation"])
data["curvature"].plot()
plt.title("Curvature");
```

_**Figure 7.X.** Curvature describes the rate of change in the slope._

Curvature describes how fast the slope is increasing or decreasing as we move along a surface. A positive curvature means the surface is curving up (upwardly convex) at that cell. A negative curvature means the surface is curving down (downwardly convex) at that cell. A curvature of 0 means the surface is straight and constant in whatever angle it is sloped towards.


### Hot and cold spots


Hot and cold spots identify statistically significant hot spots and cold spots in an input raster. To be a statistically significant hot spot, a feature will have a high value and be surrounded by other features with high values as well. Thus, it is a similar measure to local spatial autocorrelation (LISA) although hot/cold spot analysis focuses on identifying only high-high and low-low areas, where as LISA also identify outliers (high values surrounded by low values). 

```python
data["hot_cold"] = xrspatial.focal.hotspots(data["elevation"], kernel)
data["hot_cold"].plot(cmap="RdYlBu_r", figsize=(6,4));
plt.title("Identified hot and cold spots based the elevation");
```

_**Figure 7.X.** Hot spots are clusters with high values surrounded by other high values._


### Hillshade

```python
data["hillshade"] = xrspatial.hillshade(data["elevation"])
data["hillshade"].plot(cmap="Greys")
```

_**Figure 7.X.** Hillshade is a shaded relief based on the surface raster considering the illumination source angle and shadows._

```python
# Calculate relative height
data["relative_height"] = data["elevation"] - data["elevation"].min().item()
```

```python
from matplotlib.colors import LightSource, Normalize
import matplotlib.colorbar as cbar
import matplotlib.cm as cm
import numpy as np

fig, ax = plt.subplots()

# Specify the colormap to use
colormap = plt.cm.terrain

# Specify the light source
ls = LightSource(azdeg=225, altdeg=25)

# Convert DataArray into numpy array
array = data["relative_height"].to_numpy()

# Normalize elevation for color mapping
norm = Normalize(vmin=np.min(array), vmax=np.max(array))

# Create hillshade based on elevation
hillshade = ls.shade(array, cmap=colormap, vert_exag=1, blend_mode="overlay")
ax.imshow(hillshade)
ax.set_title("Hillshade with color blending");

# Create a ScalarMappable for colorbar
sm = cm.ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])  # Needed for colorbar creation

# Add colorbar
cbar = fig.colorbar(sm, ax=ax, orientation="vertical", label="Relative Height (m)")
```

_**Figure 7.X.** Hillshade with color blending can give a more realistic appearance of the landscape_


### Smoothing and focal statistics

```python
# Kernel size
k = 15

# Generate a kernel (basically produces a boolean matrix full with numbers 1 and 0)
kernel = xrspatial.convolution.circle_kernel(1, 1, k)
```

```python
# Smoothen the surface
data["smoothed_elevation"] = xrspatial.focal.focal_stats(data["elevation"], kernel, stats_funcs=["mean"])

data["smoothed_elevation"].plot(cmap="RdYlBu_r", figsize=(6,4))
plt.title("Kernel smoothing with kernel size 15");
```

_**Figure 7.X.** Smoothed surface based on the average elevation of 15 neighboring cells at each pixel._


### Reclassification

The goal in the following section is to calculate and use different surface features to find a suitable place for building a new summer house. To do this, we will use information for example about elevation, slope and aspect of the terrain. so think of a scenario where all of these can be utilized. The criteria for finding a suitable place for a summer cottage will be based on following preferences:

- The higher the elevation, the better
- Some slope is good but not too steep
- The ridge should be pointing South (who wouldn't like more sun on their patio..)

```python
# Take 20 % sample to reduce the time it takes to classify
percentage = 0.2

# The sample size
n = int(round(int(data["elevation"].count()) * percentage, 0))

# Reclassify elevation into 5 classes and add number 1 to the result to make the scale from 1-5
data["elevation_points"] = xrspatial.classify.natural_breaks(data["elevation"], k=5, num_sample=n) + 1

# Plot the result
fig, ax = plt.subplots(figsize=(8,5))
data["elevation"].plot(ax=ax);
data["elevation_points"].plot(ax=ax)
plt.title("Elevation categories");
```

_**Figure 7.X.** Elevation categories (k=5) based on natural breaks classification scheme._

```python
bins = [1,2,3,4,5]
new_values = [4,5,3,2,1]

data["slope_nb"] = xrspatial.classify.natural_breaks(data["slope"], k=5, num_sample=n) + 1
data["slope_points"] = xrspatial.classify.reclassify(data["slope_nb"], bins=bins, new_values=new_values)

# Plot
fig, ax = plt.subplots(figsize=(6,4))
data["slope_points"].plot(ax=ax, cmap="Greens")
plt.title("Slope categories");
```

_**Figure 7.X.** Slope categories (k=5) based on natural breaks classification scheme._

```python
bins = [90, 150, 210, 270, 360]
new_values = [1, 3, 5, 3, 1]

# Classify
data["aspect_points"] = xrspatial.classify.reclassify(data["aspect"], bins=bins, new_values=new_values) 

# Make a plot
fig, ax = plt.subplots(figsize=(6,4))
data["aspect_points"].plot(ax=ax, cmap="RdYlBu_r", alpha=0.7)
plt.title("Aspect categories based on custom classifier");
```

_**Figure 7.X.** Aspect categories based on a custom a custom classification scheme._


## Local operations

A local function operates .. Chapter 7.6 includes many more examples of using local operations related to working with multiband satellite data and geospatial timeseries data spanning multiple years.

```python
# Calculate the suitability index by weighting the "points" given for different layers
data["suitability_index"] = data["elevation_points"]*0.2 + data["aspect_points"]*0.6 + data["slope_points"]*0.2

# Plot the suitability index
data["suitability_index"].plot(cmap="RdYlBu_r", figsize=(6,4))
plt.title("Suitability index");
```

_**Figure 7.X.** Suitability index calculated based on elevation, aspect and slope._


## Global operations

In map algebra, global functions are operations where the output value of each cell depends on the entire dataset or a large spatial extent, not just local neighbors. These functions are used to analyze patterns, relationships, and spatial influences across the whole raster. They are essential for modeling cumulative effects, spatial dependencies, and large-scale patterns in fields like hydrology, transportation, and environmental science.


### Statistical summaries

```python
data["elevation"].min().item()
```

```python
data["elevation"].max().item()
```

```python
data["elevation"].mean().item()
```

```python
data["elevation"].median().item()
```

```python
data["elevation"].std().item()
```

### Viewshed

```python
from shapely import box, Point
import geopandas as gpd

# Extract the center coordinates of the raster
bbox = box(*data.rio.bounds())
xcoord = bbox.centroid.x
ycoord = bbox.centroid.y

# Create a GeoDataFrame of the centroid
observer_location = gpd.GeoDataFrame(geometry=[Point(xcoord, ycoord)], 
                                     crs=data.rio.crs
                                    )
```

```python
# Elevation at a given point
elevation = data["elevation"].interp(x=xcoord, y=ycoord).item()
print("Elevation in the location of observer:", elevation, "meters.")
```

Let's imagine that there is a bird watching tower that rises 10 meters above the ground. In the following, we assume that a person is viewing the landscape on top of this tower to improve the visibility of the landscape. To calculate viewshed from this observation point, we can use `.viewshed()` function from the `xrspatial` library as follows:

```python
# Observer elevation
observer_elevation = 10

# Calculate viewshed
data["viewshed"] = xrspatial.viewshed(data["elevation"], 
                                      x=xcoord, 
                                      y=ycoord,
                                      observer_elev=observer_elevation
                                     )
```

```python
fig, ax = plt.subplots()

# Plot hillshade that was calculated earlier
data["hillshade"].plot(ax=ax, cmap="Greys")

# Plot viewshed
data["viewshed"].plot(ax=ax, cmap="RdYlBu_r", alpha=0.6)

# Observer location
observer_location.plot(ax=ax, color="black", marker="x", markersize=15, label="Observer location")

# Add legend and title
ax.legend(loc="upper left")
ax.set_title("Visible areas from the observer location");
```

_**Figure 7.X.** Visible areas from the observer location based on the viewshed analysis._


## Zonal operations

To be added. 

```python
import osmnx as ox
from shapely import box

# Fetch lake "Riuttanen" from OSM
lake = ox.geocode_to_gdf("Riuttanen, Joensuu")
lake = gdf1.to_crs(crs=data.rio.crs)

# Fetch peak Riuttavaara based on OSM Node ID
peak = ox.geocode_to_gdf("N11034739930", by_osmid=True)
peak = peak.to_crs(crs=data.rio.crs)

# Create a buffer around the peak
peak["geometry"] = peak.buffer(200)

# Plot
fig, ax = plt.subplots()

data["elevation"].plot(ax=ax, cmap="terrain")
lake.plot(ax=ax, facecolor="None")
peak.plot(ax=ax, edgecolor="red", facecolor="None")
ax.set_title("Lake and Peak polygons");
```

_**Figure 7.X.** Two zones that are used for comparison and calculating zonal statistics._

```python
# Merge zones into a single GeoDataFrame
zones = pd.concat([peak, lake]).reset_index(drop=True)
```

```python
import rasterstats
import pandas as pd

elevation_array = data["elevation"].to_numpy()
affine = data.rio.transform()

# Run the zonal statistics
stats = rasterstats.zonal_stats(
    zones,  
    elevation_array,  
    affine=affine,  
    stats=["mean", "min", "max", "std"],  # Statistics to calculate
    nodata=data["elevation"].rio.nodata  # Handle nodata values
)

stats
```

```python
stats = pd.DataFrame(stats)
stats
```

```python
zones = zones.join(stats)
zones
```

```python
# What is the maximum difference in elevation between peak and lake?
difference = zones.at[0, "mean"] - zones.at[1, "mean"]
print(f"Elevation difference between the peak and lake: {difference:.0f} m.")
```

## Incremental operations

Incremental operations .. 


### Least-cost path calculation based on raster surface

```python
origin = gpd.GeoDataFrame(geometry=[Point(3691000, 6942000)], crs=data.rio.crs)
destination = gpd.GeoDataFrame(geometry=[Point(3698500, 6948000)], crs=data.rio.crs)
```

```python
fig, ax = plt.subplots()

data["hillshade"].plot(ax=ax, cmap="Greys")
origin.plot(ax=ax, color="red", markersize=58, label="Origin")
destination.plot(ax=ax, color="blue", markersize=58, label="Destination")
ax.legend(loc="upper left")
plt.title("Origin and destination");
```

_**Figure 7.X.** Origin and destination points that are used to find the least-cost path across the surface._

```python
barriers = list(range(1400,1580))
barriers += list(range(2000,2200))

origin_latlon = (origin.geometry.y.item(), origin.geometry.x.item())
destination_latlon = (destination.geometry.y.item(), destination.geometry.x.item())
```

```python
least_cost_path = xrspatial.a_star_search(data["elevation"], origin_latlon, destination_latlon, barriers)
```

```python
route = xr.where(~np.isnan(least_cost_path), 1, least_cost_path)
```

```python
fig, ax = plt.subplots()

origin.plot(ax=ax, color="red", markersize=58, label="Origin")
destination.plot(ax=ax, color="blue", markersize=58, label="Destination")
route.plot(ax=ax, cmap="gist_heat")
ax.legend(loc="upper left")
plt.title("Origin and destination");
```

_**Figure 7.X.** The calculated least-cost path from origin to destination based on A\* algorithm._

```python
from shapely import LineString

# Convert (row, col) path to geographic coordinates
transform = data.rio.transform()

# Extract (row, col) indices where path is not NaN
path_indices = np.argwhere(~np.isnan(least_cost_path.values)) 

coords = [transform * (int(col), int(row)) for row, col in path_indices] 

# Create a LineString from the path
line = LineString(coords)

# Convert to a GeoDataFrame
shortest_path = gpd.GeoDataFrame({"geometry": [line]}, crs=data.rio.crs)
```

```python
fig, ax = plt.subplots()

data["elevation"].plot(ax=ax, cmap="terrain")
shortest_path.plot(ax=ax, color="red", label="Least cost path")
origin.plot(ax=ax, color="red", markersize=58, label="Origin")
destination.plot(ax=ax, color="blue", markersize=58, label="Destination")
ax.legend(loc="upper left")
plt.title("Least cost path between origin and destination");
```

_**Figure 7.X.** Vectorized least-cost path (LineString) across the terrain._


### Flow accumulation

Flow accumulation for example related to watershed analysis is another example of incremental operation. **ADD MORE INFO**. Chapter 12 will cover examples how incremental operations are used to calculate watersheds based in digital elevation model in New Zealand.
