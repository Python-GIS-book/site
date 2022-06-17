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

<!-- #region deletable=true editable=true -->
# Interactive maps

In this tutorial we will learn how to publish data from Python on interactive [leaflet.js](http://leafletjs.com/) maps. 

JavaScript (JS)  is a programming language for adding interactive content (such a zoomamble maps!) on webpages. [Leaflet](http://leafletjs.com/) is a popular JavaScript library for creating interactive maps for webpages ([OpenLayers](https://openlayers.org/) is another JavaScript library for the same purpose). 

Here, will mainly focus on [Folium](https://python-visualization.github.io/folium/) - a Python library that makes it easy to convert data from (Geo)DataFrames into interactive Leaflet maps.

<div class="alert alert-info">

**Explore also...**
    
Other interesting libraries for creating interactive visualizations from spatial data:
    
- [mapboxgl](https://github.com/mapbox/mapboxgl-jupyter)
- [Bokeh](https://docs.bokeh.org/en/latest/)
- [Geoviews](http://geoviews.org/)
- [plotly express](https://plotly.com/python/maps/)

</div>

<!-- #endregion -->

<!-- #region -->
## Folium


[Folium](https://github.com/python-visualization/folium)  is a Python library that makes
it possible visualize data on an interactive Leaflet map.

**Resources:**

- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Example Gallery](https://nbviewer.jupyter.org/github/python-visualization/folium/tree/master/examples/)
- [Folium Quickstart](https://python-visualization.github.io/folium/quickstart.html)

<!-- #endregion -->

### Creating a simple interactive web-map

Import folium and other useful packages:

```python
import folium
```

```python
from pyproj import crs
import geopandas as gpd
import matplotlib.pyplot as plt
```

We will start by creating a simple interactive web-map without any data on it. We just visualize OpenStreetMap on a specific location of the world.

First thing that we need to do is to create [a Map instance](https://python-visualization.github.io/folium/modules.html#folium.folium.Map) and define a location for zooming in the data: 

```python deletable=true editable=true
# Create a Map instance
m = folium.Map(location=[60.25, 24.8], zoom_start=10, control_scale=True)
```

<!-- #region deletable=true editable=true -->
The first parameter ``location`` takes a pair of lat, lon values as list as an input which will determine where the map will be positioned when user opens up the map. ``zoom_start`` -parameter adjusts the default zoom-level for the map (the higher the number the closer the zoom is). ``control_scale`` defines if map should have a scalebar or not.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Let's see what our map looks like: 
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
m
```

<!-- #region deletable=true editable=true -->
We can also save the map as a html file:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
outfp = "base_map.html"
m.save(outfp)
```

<!-- #region deletable=true editable=true -->

You should now see a html file in your working directory. You can open the file in a web-browser in order to see the map, or in a text editor in order to see the source definition.


Let's create another map with different settings (location, bacground map, zoom levels etc). See documentation of the [Map() object](https://python-visualization.github.io/folium/modules.html#folium.folium.Map) for all avaiable options.
    
``tiles`` -parameter is used for changing the background map provider and map style (see the [documentation](https://python-visualization.github.io/folium/modules.html#folium.folium.Map) for all in-built options).

<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Let's change the basemap style to 'Stamen Toner'
m = folium.Map(
    location=[40.730610, -73.935242],
    tiles="Stamen Toner",
    zoom_start=12,
    control_scale=True,
    prefer_canvas=True,
)

m
```

<!-- #region deletable=true editable=true -->
### Adding layers to the map

Let's first have a look how we can add a simple [marker](https://python-visualization.github.io/folium/modules.html?highlight=marker#folium.map.Marker) on the webmap:
<!-- #endregion -->

```python jupyter={"outputs_hidden": false}
# Create a Map instance
m = folium.Map(location=[60.20, 24.96], zoom_start=12, control_scale=True)

# Add marker
# Run: help(folium.Icon) for more info about icons
folium.Marker(
    location=[60.20426, 24.96179],
    popup="Kumpula Campus",
    icon=folium.Icon(color="green", icon="ok-sign"),
).add_to(m)

# Show map
m
```

<!-- #region deletable=true editable=true -->
As mentioned, Folium combines the strenghts of data manipulation in Python with the mapping capabilities of Leaflet.js. Eventually, we would like to include the plotting of interactive maps as the last part of our data analysis workflow. 

Let's see how we can plot data from a geodataframe using folium.


<!-- #endregion -->

```python
# File path
points_fp = "data/addresses.shp"

# Read the data
points = gpd.read_file(points_fp)

# Check input data
points.head()
```

```python
points.head()
```

- conver the points to GeoJSON features using folium:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Convert points to GeoJSON
points_gjson = folium.features.GeoJson(points, name="Public transport stations")
```

```python
# Check the GeoJSON features
# points_gjson.data.get('features')
```

<!-- #region deletable=true editable=true -->
Now we have our population data stored as GeoJSON format which basically contains the
data as text in a similar way that it would be written in the ``.geojson`` -file.
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Add the points onto the Helsinki basemap:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Create a Map instance
m = folium.Map(
    location=[60.25, 24.8], tiles="cartodbpositron", zoom_start=11, control_scale=True
)

# Add points to the map instance
points_gjson.add_to(m)

# Alternative syntax for adding points to the map instance
# m.add_child(points_gjson)

# Show map
m
```

### Layer control

We can also add a `LayerControl` object on our map, which allows the user to control which map layers are visible. See the [documentation](http://python-visualization.github.io/folium/docs-v0.5.0/modules.html#folium.map.LayerControl) for available parameters (you can e.g. change the position of the layer control icon).

```python
# Create a layer control object and add it to our map instance
folium.LayerControl().add_to(m)

# Show map
m
```

<!-- #region deletable=true editable=true -->
### Heatmap

[Folium plugins](https://python-visualization.github.io/folium/plugins.html) allow us to use popular tools available in leaflet. One of these plugins is [HeatMap](https://python-visualization.github.io/folium/plugins.html#folium.plugins.HeatMap), which creates a heatmap layer from input points. 

Let's visualize a heatmap of the public transport stations in Helsinki using the addresses input data. [folium.plugins.HeatMap](https://python-visualization.github.io/folium/plugins.html#folium.plugins.HeatMap) requires a list of points, or a numpy array as input, so we need to first manipulate the data a bit:
<!-- #endregion -->

```python deletable=true editable=true
# Get x and y coordinates for each point
points["x"] = points["geometry"].apply(lambda geom: geom.x)
points["y"] = points["geometry"].apply(lambda geom: geom.y)

# Create a list of coordinate pairs
locations = list(zip(points["y"], points["x"]))
```

Check the data:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
locations
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
from folium.plugins import HeatMap

# Create a Map instance
m = folium.Map(
    location=[60.25, 24.8], tiles="stamentoner", zoom_start=10, control_scale=True
)

# Add heatmap to map instance
# Available parameters: HeatMap(data, name=None, min_opacity=0.5, max_zoom=18, max_val=1.0, radius=25, blur=15, gradient=None, overlay=True, control=True, show=True)
HeatMap(locations).add_to(m)

# Alternative syntax:
# m.add_child(HeatMap(points_array, radius=15))

# Show map
m
```

<!-- #region editable=true -->
### Clustered point map

Let's visualize the address points (locations of transport stations in Helsinki) on top of the choropleth map using clustered markers using folium's [MarkerCluster](https://python-visualization.github.io/folium/plugins.html?highlight=marker%20cluster#folium.plugins.MarkerCluster) class.
<!-- #endregion -->

```python editable=true
from folium.plugins import MarkerCluster
```

```python
# Create a Map instance
m = folium.Map(
    location=[60.25, 24.8], tiles="cartodbpositron", zoom_start=11, control_scale=True
)
```

```python
# Following this example: https://github.com/python-visualization/folium/blob/master/examples/MarkerCluster.ipynb

# Get x and y coordinates for each point
points["x"] = points["geometry"].apply(lambda geom: geom.x)
points["y"] = points["geometry"].apply(lambda geom: geom.y)

# Create a list of coordinate pairs
locations = list(zip(points["y"], points["x"]))
```

```python
# Create a folium marker cluster
marker_cluster = MarkerCluster(locations)

# Add marker cluster to map
marker_cluster.add_to(m)

# Show map
m
```

<!-- #region deletable=true editable=true -->
### Choropleth map
<!-- #endregion -->

<!-- #region deletable=true editable=true -->
Next, let's check how we can overlay a population map on top of a basemap using [folium's choropleth method](http://python-visualization.github.io/folium/docs-v0.5.0/modules.html#folium.folium.Map.choropleth). This method is able to read the geometries and attributes directly from a geodataframe. 
This example is modified from the [Folium quicksart](https://python-visualization.github.io/folium/quickstart.html#Choropleth-maps).

- First read in the population grid from HSY wfs like we did in [lesson 3](https://automating-gis-processes.github.io/site/notebooks/L3/spatial-join.html):
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false}
import geopandas as gpd
from pyproj import CRS
import requests
import geojson

# Specify the url for web feature service
url = "https://kartta.hsy.fi/geoserver/wfs"

# Specify parameters (read data in json format).
# Available feature types in this particular data source: http://geo.stat.fi/geoserver/vaestoruutu/wfs?service=wfs&version=2.0.0&request=describeFeatureType
params = dict(
    service="WFS",
    version="2.0.0",
    request="GetFeature",
    typeName="asuminen_ja_maankaytto:Vaestotietoruudukko_2018",
    outputFormat="json",
)

# Fetch data from WFS using requests
r = requests.get(url, params=params)

# Create GeoDataFrame from geojson
data = gpd.GeoDataFrame.from_features(geojson.loads(r.content))

# Check the data
data.head()
```

```python
from pyproj import CRS

# Define crs
data.crs = CRS.from_epsg(3879)
```

Re-project layer into WGS 84 (epsg: 4326)

```python
# Re-project to WGS84
data = data.to_crs(epsg=4326)

# Check layer crs definition
print(data.crs)
```

<!-- #region deletable=true editable=true -->
Rename columns
<!-- #endregion -->

```python
# Change the name of a column
data = data.rename(columns={"asukkaita": "pop18"})
```

```python
# Create a Geo-id which is needed by the Folium (it needs to have a unique identifier for each row)
data["geoid"] = data.index.astype(str)
```

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Select only needed columns
data = data[["geoid", "pop18", "geometry"]]

# Convert to geojson (not needed for the simple coropleth map!)
# pop_json = data.to_json()

# check data
data.head()
```

Create an interactive choropleth map from the population grid:

```python deletable=true editable=true jupyter={"outputs_hidden": false}
# Create a Map instance
m = folium.Map(
    location=[60.25, 24.8], tiles="cartodbpositron", zoom_start=10, control_scale=True
)

# Plot a choropleth map
# Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
folium.Choropleth(
    geo_data=data,
    name="Population in 2018",
    data=data,
    columns=["geoid", "pop18"],
    key_on="feature.id",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    line_color="white",
    line_weight=0,
    highlight=False,
    smooth_factor=1.0,
    # threshold_scale=[100, 250, 500, 1000, 2000],
    legend_name="Population in Helsinki",
).add_to(m)

# Show map
m
```

### Tooltips

It is possible to add different kinds of pop-up messages and tooltips to the map. Here, it would be nice to see the population of each grid cell when you hover the mouse over the map. Unfortunately this functionality is not apparently implemented implemented in the Choropleth method we used before. 

Add tooltips, we can add tooltips to our map when plotting the polygons as GeoJson objects using the `GeoJsonTooltip` feature. (following examples from [here](http://nbviewer.jupyter.org/gist/jtbaker/57a37a14b90feeab7c67a687c398142c?flush_cache=true) and [here](https://nbviewer.jupyter.org/github/jtbaker/folium/blob/geojsonmarker/examples/GeoJsonMarkersandTooltips.ipynb))

For a quick workaround, we plot the polygons on top of the coropleth map as a transparent layer, and add the tooltip to these objects. *Note: this is not an optimal solution as now the polygon geometry get's stored twice in the output!*

```python
# Convert points to GeoJson
folium.features.GeoJson(
    data,
    name="Labels",
    style_function=lambda x: {
        "color": "transparent",
        "fillColor": "transparent",
        "weight": 0,
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=["pop18"], aliases=["Population"], labels=True, sticky=False
    ),
).add_to(m)

m
```

Rember that you can also save the output as an html file: 

```python
outfp = "choropleth_map.html"
m.save(outfp)
```

Extra: check out plotly express for an alternative way of plotting an interactive Choropleth map [in here](https://plotly.com/python/mapbox-county-choropleth/).
