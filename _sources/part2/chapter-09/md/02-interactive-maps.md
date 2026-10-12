---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
# Interactive maps

Interactive maps allow users to engage with the map content through, for example, zooming, panning, clicking, and searching. There are various tools available for creating interactive maps in Python. In this chapter, we will first see how we can create interactive maps directly from `geopandas`, and proceed to learning more about customizing the interactive maps in Python using the [`folium` library](https://python-visualization.github.io/folium/) [^folium]. Folium makes it easy to visualize geographic data by integrating with [`Leaflet.js`](http://leafletjs.com/) [^leaflet], a powerful JavaScript library for interactive mapping. JavaScript (JS) is a programming language commonly used to add dynamic and interactive elements to webpages, and Leaflet is one of the many JavaScript libraries designed specifically for rendering interactive maps. `Folium` makes these tools accessible for Python users who want to integrate dynamic map content in their data analysis workflows. By using `folium`, we can leverage the capabilities of `Leaflet.js` without needing to write JavaScript code. 
<!-- #endregion -->

## Interactive data exploration using `geopandas`

In previous chapters, we have already created simple examples of interactive maps via `geopandas` to explore our data interactively on top of a basemap. `Geopandas.GeoDataFrame.explore()` uses `folium`/`leaflet.js` to create the map and we can adjust the map object parameters directly from `geopandas`. 

Let's create an interactive map via `geopandas` using point data. Our sample dataset represent city bike stations in Espoo and Helsinki, Finland based on open data from [Helsinki Region Transport’s (HSL)](https://www.avoindata.fi/data/en_GB/dataset/hsl-n-kaupunkipyoraasemat) [^hsl_citybikedata].

```python editable=true slideshow={"slide_type": ""}
import geopandas as gpd

points_fp = "./../data/hrtopendata_citybikes_helsinki_espoo_2025.gpkg"
points = gpd.read_file(points_fp, columns=["ID", "Name", "Osoite", "Kapasiteet"])

points = points.rename(columns={"Osoite": "Address", "Kapasiteet": "Capacity"})
points.explore(marker_type="marker")
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 8.XX}. Interactive map with point data created using geopandas.GeoDataFrame.explore().}}, center, nofloat}{../img/figure_8-xx.png}
{ \hspace*{\fill} \\}
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 8.XX**. Interactive map with point data created using geopandas.GeoDataFrame.explore()._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
This interactive map allows us to zoom in and out to explore the locations of our point data. By default, we can hover over the point features to view attribute information. 
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Changing the basemap

The bacground map can be controlled  via the `tiles` argument. Folium includes built-in background map tiles (such as `"OpenStreetmap"` and `"CartoDB Positron"`) and allows the use of custom URLs to define the bacground map. All tilesets available in the [`xyzservices` library](https://xyzservices.readthedocs.io/en/stable/) [^xyzservices] can be used via `folium`. You can preview available basemaps in the [Leaflet providers preview](https://leaflet-extras.github.io/leaflet-providers/preview/) [^leaflet_providers]. 
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
points.explore(marker_type="marker", tiles="CartoDB Positron")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Note that `folium` automatically adds attribution to the default map-tiles in the bottom-right corner of the map. We can also pass a custom tileset using an URL in the format `https://{s}.yourtiles.com/{z}/{x}/{y}.png`. When using an URL, we also need to add the map tile attribution separately.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
points.explore(
    marker_type="marker",
    tiles="https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png",
    attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
)
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 8.XX}. Interactive map with point data and custom bacground tiles.}}, center, nofloat}{../img/figure_8-xxx.png}
{ \hspace*{\fill} \\}
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 8.XXX**. Interactive map with point data and custom bacground tiles._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Choropleth map

It is also possible to plot interactive choropleth maps using `GeoDataFrame.explore()`. Let's create a choropleth map displaying the spatial distribution of city bike stations in the Helsinki metropolitan area. For this, we can read in [postal code data provided by the Helsinki Region Environmental Services Authority](https://www.hsy.fi/en/environmental-information/open-data/avoin-data---sivut/-helsinki-metropolitan-postal-code-areas/) [^hsy_postalcodedata]. Columns `"Posno"`, `"Nimi"`, and `"Kunta"` contain relevant information about the postal code areas and we can rename these columns for clarity.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
polygons_fp = "./../data/PKS_postinumeroalueet_2023_manner_shp.zip"
polygons = gpd.read_file(polygons_fp, columns=["Posno", "Nimi", "Kunta"])

polygons = polygons.rename(
    columns={"Posno": "Postal code", "Nimi": "Name", "Kunta": "Municipality"}
)

polygons.explore()
```

<!-- #region editable=true slideshow={"slide_type": ""} tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 8.XXXX}. Interactive map with polygon data.}}, center, nofloat}{../img/figure_8-xxxx.png}
{ \hspace*{\fill} \\}
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 8.XXXX**. Interactive map with polygon data._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Let's combine information about city bike stations into the postal code data including the total number of stations and total station capacity per postal code area. Finally, let's calculate the average capacity per city bike station per postal code area to generate information that we can display on our thematic map.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Create spatial join
join = gpd.sjoin(polygons, points[["ID", "Capacity", "geometry"]])

# Get station count and total capacity per postal code
bike_count = join.groupby(["Postal code"]).ID.count()
capacity = join.groupby(["Postal code"]).Capacity.sum()

# Join statistics to polygons
polygons = polygons.merge(
    bike_count, left_on="Postal code", right_index=True, how="left"
)
polygons = polygons.merge(capacity, left_on="Postal code", right_index=True, how="left")

polygons = polygons.rename(
    columns={"ID": "Number of stations", "Capacity": "Total capacity"}
)
polygons["Average city bike station capacity"] = (
    polygons["Total capacity"] / polygons["Number of stations"]
)
```

```python editable=true slideshow={"slide_type": ""}
polygons.explore(column="Average city bike station capacity")
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
_**Figure 8.XXXX**. Interactive choropleth map displaying the average city bike station capacity per postal code area._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Our map displays the average city bike station capacity across all postal code areas in the region. The highest capacity can be observed in downtown Helsinki. Other attributes, such as the total number of stations and total capacity per postal code can be viewed when hovering over the map. The city bike station data covers only the municipality of Helsinki and parts of the neighbouring municipality of Espoo. Those postal code areas without any city bike stations are visualized in gray.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Folium plugins

So far, we have used `folium` via geopandas to create the interactive maps. For further options, we can start using various plugins available from leaflet via [`folium` plugins](https://python-visualization.github.io/folium/plugins.html) [^folium_plugins].


First, create a simple interactive map and recap some of the basic settings we already used when plotting interactive maps via `geopandas`.  We will create [a `folium` map instance](https://python-visualization.github.io/folium/modules.html#folium.folium.Map) and define the initial location for the interactive map and add a simple [marker](https://python-visualization.github.io/folium/modules.html?highlight=marker#folium.map.Marker). Furthermore, we can adjusts the initial zoom-level for the map (the higher the number the closer the zoom is) using the `zoom_start` parameter, and display the scalebar using the `control_scale` parameter.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
import folium
```

```python deletable=true editable=true slideshow={"slide_type": ""}
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

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
To fully understand what happens, we can save the map as a HTML (Hypertext Markup Language) file and inspect how the interactive map is defined in text format. 
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
outfp = "./../data/base_map.html"
m.save(outfp)
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
You should now see a html file in the data directory. You can open the file in a web-browser in order to see the map, or in a text editor in order to see the source definition HTML.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Layer control

We can also allow users to control what contents are displayed on the map by adding add a [`LayerControl`](http://python-visualization.github.io/folium/docs-v0.5.0/modules.html#folium.map.LayerControl) object on our map. It is possible to control, for example, the position of the layer control icon while adding it. Note, that the `LayerControl` object should be added last, after all map layers have been added to ensure that it works correctly. 
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
# Create a layer control object and add it to our map instance
folium.LayerControl(position="topleft").add_to(m)

# Show map
m
```

<!-- #region deletable=true editable=true slideshow={"slide_type": ""} -->
### Heatmap

The [`HeatMap`](https://python-visualization.github.io/folium/plugins.html#folium.plugins.HeatMap) plugin creates a heatmap layer from input points. Let's visualize a heatmap of the city bike station data based on the original point locations. The `HeatMap` plugin requires a list of point coordinates (latitude, longitude), or a `numpy` array as input. Let's create the required input using our `geopandas` skills.
<!-- #endregion -->

```python deletable=true editable=true slideshow={"slide_type": ""}
points = points.to_crs(4326)

# Get x and y coordinates for each point
points["x"] = points["geometry"].x
points["y"] = points["geometry"].y

# Create a list of coordinate pairs
locations = list(zip(points["y"], points["x"]))

# Comment out the following line to check the result
# print(locations)
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
Now that we have a list of point coordinates, we can pass this list onto `folium` `HeatMap` plugin:
<!-- #endregion -->

```python deletable=true editable=true jupyter={"outputs_hidden": false} slideshow={"slide_type": ""}
from folium.plugins import HeatMap

# Create a Map instance
m = folium.Map(
    location=[60.25, 24.8], tiles="CartoDB Positron", zoom_start=10, control_scale=True
)

# Add heatmap to map instance
HeatMap(locations).add_to(m)

# Alternative syntax:
# m.add_child(HeatMap(points_array, radius=15))

# Show map
m
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Clustered point map

[`MarkerCluster`](https://python-visualization.github.io/folium/plugins.html?highlight=marker%20cluster#folium.plugins.MarkerCluster)  is another useful `folium` plugin that allows simplifying the displayed information according to the zoom level. When zooming out, the displayed markers are clustered together and more details appear when zooming in.  Let's visualize the address points (locations of transport stations in Helsinki) using this approach. Similar to the `HeatMap`plugin, the `MarkerCluster` plugin requires the input as a list of coordinate tuples, and we can use the same list of point coordinates also here.
<!-- #endregion -->

```python editable=true slideshow={"slide_type": ""}
from folium.plugins import MarkerCluster
```

```python editable=true slideshow={"slide_type": ""}
# Create a Map instance
m = folium.Map(
    location=[60.25, 24.8], tiles="CartoDB Positron", zoom_start=11, control_scale=True
)
```

```python editable=true slideshow={"slide_type": ""}
# Create a folium marker cluster
marker_cluster = MarkerCluster(locations)

# Add marker cluster to map
marker_cluster.add_to(m)

# Show map
m
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Footnotes

[^folium]: <https://python-visualization.github.io/folium/>
[^leaflet]: <http://leafletjs.com/>
[^hsl_citybikedata]: <https://www.avoindata.fi/data/en_GB/dataset/hsl-n-kaupunkipyoraasemat>
[^hsy_postalcodedata]: <https://www.hsy.fi/en/environmental-information/open-data/avoin-data---sivut/-helsinki-metropolitan-postal-code-areas/>
[^folium_api]: <https://python-visualization.github.io/folium/latest/reference.html>
[^xyzservices]: <https://xyzservices.readthedocs.io/en/stable/>
[^leaflet_providers]: <https://leaflet-extras.github.io/leaflet-providers/preview/>
[^folium_plugins]: <https://python-visualization.github.io/folium/plugins.html>
<!-- #endregion -->
