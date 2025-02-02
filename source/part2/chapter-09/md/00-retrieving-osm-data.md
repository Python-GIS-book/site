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

# Retrieving OpenStreetMap data



## What is OpenStreetMap?

[OpenStreetMap](https://www.openstreetmap.org/) [^OSM] (OSM) is a free, editable  map of the world that is created by a global community of mappers. OSM is often referred to as "the Wikipedia of maps" meaning that anyone can update the contents. When using OSM data, appropriate credit should be given to OpenStreetMap and its contributors (see [OSM Copyright and License](https://www.openstreetmap.org/copyright) [^OSM_license]). 

OpenStreetMap data are increasingly used in various map-based applications and as input for geographic data analysis. In many regions, OSM is the best data available on streets, buildings and amenities, or at least the best data source that is openly available. While the map is never complete, many regions and especially urban areas are relatively well covered in OSM. Various organized mapping campaings exists to update OSM in areas that lack detailed map data (check out [Humanitarian OpenStreetMap Team](https://www.hotosm.org) [^HOTOSM]).

OSM can be used as source data for various tasks such as routing and geocoding, and as bacground maps for visualizing analysis results. Relevant map feature categories include: 

- street networks
- buildings
- amenities
- landuse
- natural elements
- boundaries
  
In OpenStreetMap, map features are labeled using tags consisting of a key that describes the category (such as "highway" or "building") and a value that describes the type of object within the category (such as "motorway" or "aparments"). It is thus possible, for example, to fetch all available streets or limit the search only to specific types of streets. Information on various map features and their associated tags is fundamental for correctly querying the data. 

Excerpts of OSM data are available to download from different sources, such as the [Geofabrik Download Server](https://www.geofabrik.de/data/download.html) [^Geofabrik]. Computationally,  [the Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) [^Overpass_API_intro] can be used for querying and fetching parts of OSM data for further analysis. 

A good way to start working with OSM data is to view the map from an area you are familiar with. The great thing about OSM is that anyone can sign up and make edits to the map. There are various discussion forums and mapping projects that support new (and old) mappers. [The OSM wiki](https://wiki.openstreetmap.org/wiki/Main_Page) [^OSM_wiki] provides an extensive overview for anyone planning to use or produce OSM data. 


<!-- #region editable=true slideshow={"slide_type": ""} -->
#### Question 9.1

Go to [www.openstreetmap.org](https://www.openstreetmap.org/) and zoom the map to an area that you are familiar with. 
- Does the map look complete?
- Are there any geometric features (roads, buildings, bus stops, service locations) missing?
- Inspect further some of the features; are there any attribute information missing (street names, building addresses, service names or opening hours)?

You can check the intended tags for various map freatures from the [OSM wiki](https://wiki.openstreetmap.org/wiki/Map_features) [^OSM_wiki_tags]. If you spotted some missing information, freel free to create an OpenStreetMap account, log in, and update the map!
<!-- #endregion -->

## Downloading OpenStreetMap data with OSMnx

[Osmnx](https://github.com/gboeing/osmnx) [^OSMnx] is a Python package that makes it easy to download, model and analyze street networks and other geospatial features from OpenSteetMap ({cite}`Boeing2024`). `Osmnx` relies on `geopandas` and another module called `networkx`, which enables network analysis. For latest updates, installation instructions, and complete user reference, see [osmnx  documentation](https://osmnx.readthedocs.io/en/stable/index.html) [^osmnx_docs]. 

`Osmnx` uses  the Overpass API for querying data from OSM. Map queries can be defined by city name, polygon, bounding box or an address or a point location and a buffer distance. There are different functions available to query data from the Overpass API using `osmnx` depending on the way in which the spatial location is defined. In addition, a set of tags can be specified to select which map features to download. Tags are passed to these functions as a dictionary allowing querying multiple tags at the same time.

Here, we will see how to fetch OSM data from a central area in downtown Helsinki. We will define our queries using a place name ("Kamppi, Helsinki, Finland"). 


### Defining the area of interest


Let's start by importing `osmnx` and getting the boundaries of our area of interest. `Osmnx` uses `nominatim` to geocode the place name. Notice that the place name needs to exists in OpenStreetMap, otherwise the query will fail.

```python
import osmnx as ox

place = "Kamppi, Helsinki, Finland"
aoi = ox.geocoder.geocode_to_gdf(place)
```

```python
aoi.explore()
```

<!-- #raw editable=true slideshow={"slide_type": ""} raw_mimetype="" tags=["hide-cell"] -->
% This cell is only needed to produce a figure for display in the hard copy of the book.
\adjustimage{max size={0.9\linewidth}{0.9\paperheight}, caption={\emph{\textbf{Figure 9.1}. Interactive map displaying the area of interest with a background map.}}, center, nofloat}{../img/osmnx-aoi-example.png}
{ \hspace*{\fill} \\}
<!-- #endraw -->

_**Figure 9.1**. Interactive map displaying the area of interest with a background map. Source: OpenStreetMap contributors._


### Street network


We can download street network data usign the `osmnx` `graph` module. We will download the street network using the place name parameter that represents our area of interest in Kamppi, Helsinki. The function downloads  the street network data from OSM and construct a `networkx` graph model that can be used for routing. 

```python
graph = ox.graph.graph_from_place(place)
type(graph)
```

Let's have a closer look a the street nework using an `osmnx` function that plots the graph:


```python
# Plot the streets
fig, ax = ox.plot.plot_graph(graph, figsize=(6,6))
```

_**Figure 9.2**. Graph edges and nodes._


From here we can see that our graph contains nodes (the points) and edges (the lines) of the network graph. There are various tools available in `osmnx` and `networkx` to continue modifying and analyzing this network graph. It would also be possible to limit the search to contain only specific street segments, such as all public streets or all streets and paths that cyclists or pedestrians can use. You can read more about working with street network graphs in the `osmnx` online documentation.

For now, we are only interested in the geometry and attributes of the street network and will convert the streets (edges of the network) into a `GeoDataFrame` using the `osmnx` function `graph_to_gdfs()`. 

```python editable=true slideshow={"slide_type": ""}
edges = ox.convert.graph_to_gdfs(graph, nodes=False, edges=True)
edges.head(2)
```

### Other map features
Downloading building footprints, points of interests such as services and other map features is possible using the `osmnx` `features` module. Same as for street networks, map features can be queried based on varying spatial input (form bounding box, polygon, place name, or around a point or an address). Here, we will demonstrate the use of a place name search for downloading and visualizing OSM data for a central urban area in Helsinki, Finland.

```python
place = "Kamppi, Helsinki, Finland"
tags = { "building" : True}

buildings = ox.features.features_from_place(place, tags)
```

The downloaded OSM data comes with plenty of information representing various attributes of the features that OSM contributors have added. At the time of writing, the building data from central Helsinki contained 120 different columns.

```python
len(buildings.columns)
```

You can see names of all available columns by running `list(buildings.columns)`. Let's check the contents of some of the available columns:

```python
buildings[['building', 'name', 'addr:city', 'geometry']].head()
```


From here we can tell that some, but not all of the buildings contain more specific information about the type of building (e.g., a school) and building name and address. 

Let's plot the building footprints to get an overview of the data. While plotting, we can color the features according to the building tag values to get an overview of where different types of buildings are located. Notice that some buildings are tagged only with the generic tag "building=yes" without further information about the type of the building.

```python
buildings.plot(column="building", figsize=(8.2,8), cmap="tab20c", legend=True)
```

_**Figure 9.3**. Buildings visualized by building tag values._


Let's also fetch points of interests from our area of interest using the amenity tag:

```python
tags = {"amenity": True}
amenities = ox.features.features_from_place(place, tags)
```

Again, let's only plot a couple of available columns to check the contents of the data. You can see all column names  by running `list(amenities.columns)`.

```python
amenities[['amenity', 'name', 'opening_hours', 'geometry']].head()
```

Here, we received all amenities in the area of interest ranging from restaurants, cafes and so on. The type of amenity (i.e., the value of the OSM tag) is indicated in the `amenity` column. Again, some, but not all features have additional information such as opening hours available. The downloaded data contains more than 700 individual points of interests in the data:

```python
len(amenities)
```

#### Question 9.2

How many different amenity categories are there?

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# Get number of unique values in column `amenity`
amenities["amenity"].nunique()
```

Let's limit our query to contain only restaurants and cafes in our area of interest. We can do this by specifying one or several tag values in the dictionary.

```python
tags = {"amenity" : ["restaurant", "cafe"]}
amenities = ox.features.features_from_place(place, tags)
```

```python
len(amenities)
```

Urban green space and public open space are vital components of liveable urban areas. Let's see how we can fetch urban green space data from OSM using the `osmnx` `features` module. Fetching green spaces from OpenStreetMap requires a bit of investigation of appropriate tag values and these might vary across cities. 

One common way of tagging urban parks is `leisure=park`. If wanting to capture also other green infrastructure, additional tags such as `landuse=grass` may be added. Let's proceed with these two tags that should capture most of the available greenspaces in downtown Helsinki.

```python
# List key-value pairs for tags
tags = {"leisure": "park", "landuse": "grass"}
```

```python
# Get the data
parks = ox.features.features_from_place(place, tags)
```

```python
print("Retrieved", len(parks), "objects")
parks[['leisure', 'landuse', 'name', 'geometry']].head()
```

The first five rows of data contain different parks, which all have a name. Let's quicly plot the data to see the geometry. By adding transparency to the map with the `alpha` parameter, we can observe where some of the grass and park polygon features overlap.

```python
parks.plot(color="green", alpha=0.5)
```

_**Figure 9.4**. Polygons tagged with "leisure=park" or "landuse=grass"._


### Plotting the data

Let's create a map out of the streets, buildings, restaurants in our area of interest.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8.5, 8))

# Plot the footprint
aoi.plot(ax=ax, facecolor="black")

# Plot street edges
edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")

# Plot buildings
buildings.plot(ax=ax, facecolor="silver", alpha=0.7)

parks.plot(ax=ax, facecolor="green", alpha=0.7)

# Plot restaurants
amenities.plot(ax=ax, color="yellow", alpha=0.7, markersize=10)

plt.tight_layout()
```

_**Figure 9.5**. Streets, buildings, green spaces, restaurants and cafes from the Kamppi area in Helsinki._


Cool! Now we have a map where we have plotted the restaurants, buildings, streets and the boundaries of the selected region of 'Kamppi' in Helsinki. 


### Alternative spatial queries

If your area of interest is not represented by any existing featue in OSM, you can also query data based on custom polygon, bounding box or based on a buffer around a point or address location. Each way of querying the data is implemented in a distinct `osmnx` function. Here are the available fucntions for querying map features by:

- address: [osmnx.features.features_from_address(address, tags, dist)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_address)
- bounding box: [osmnx.features.features_from_bbox(bbox, tags)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_bbox)
- place: [osmnx.features.features_from_place(place, tags)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_place)
- point: [osmnx.features.features_from_point(center_point, tags, dist)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_point)
- polygon: [osmnx.features.features_from_polygon(polygon, tags)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_polygon)

Similar alternative search functions exists for querying the network graph. See `osmnx` user reference for exact syntax.

Let's try out querying data based on a pre-defined bounding box which centers around the Cental railway station in Helsinki. Bounding box coordinates should be given in the correct order (left, bottom, right, top). 

```python
bounds = (24.9351773, 60.1641551, 24.9534055, 60.1791068)
buildings = ox.features.features_from_bbox(bounds, {'building': True})
buildings.plot()
```

_**Figure 9.6**. Downloaded buildings within a bounding box._


Here is another example of querying data within a distance treshold from a geocodable address. The distance parameter is given in meters. 

```python
address = "Central railway station, Helsinki, Finland"
tags = {'building': True}
distance = 500 
buildings = ox.features.features_from_address(address, tags, distance)
buildings.plot()
```

_**Figure 9.7**. Downloaded buildings within a distance treshold from a geocoded address._


#### Question 9.3

Check your understanding and retrieve OpenStreetMap data from some other area in the world. Use `osmnx` and download:

- Polygon of your area of interest
- Street network
- Building footprints
- Restaurants and cafes (or why not also other amenities)
- Green spaces

Note that the larger the area you choose, the longer it takes to retrieve data from the API! When fetching the street network, you can use parameter `network_type=drive` to limit the graph query to filter out un-driveable roads.

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# Example solution 
place = "Gamla stan, Stockholm, Sweden"
aoi = ox.geocoder.geocode_to_gdf(place)

# Street network
graph = ox.graph.graph_from_place(place)
edges = ox.convert.graph_to_gdfs(graph, nodes=False, edges=True)

# Other map features
buildings = ox.features.features_from_place(place, tags={ "building" : True})
amenities = ox.features.features_from_place(place, tags = {"amenity" : ["restaurant", "cafe"]})
parks = ox.features.features_from_place(place, tags = {"leisure": "park", "landuse": "grass"})

# Plot the result
fig, ax = plt.subplots(figsize=(8.5, 8))

aoi.plot(ax=ax, facecolor="black")
edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")
buildings.plot(ax=ax, facecolor="silver", alpha=0.7)
parks.plot(ax=ax, facecolor="green", alpha=0.7)
amenities.plot(ax=ax, color="yellow", alpha=0.7, markersize=10)
plt.tight_layout()
```

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Footnotes

[^OSM]: <https://www.openstreetmap.org/>
[^OSM_license]: <https://www.openstreetmap.org/copyright>
[^Overpass_API_intro]: <https://wiki.openstreetmap.org/wiki/Overpass_API> 
[^HOTOSM]: <https://www.hotosm.org> 
[^Geofabrik]: <https://www.geofabrik.de/data/download.html>
[^OSM_wiki]: <https://wiki.openstreetmap.org/wiki/Main_Page>
[^OSM_wiki_tags]: <https://wiki.openstreetmap.org/wiki/Map_features> 
[^OSMnx]: <https://github.com/gboeing/osmnx>
[^osmnx_docs]: <https://osmnx.readthedocs.io/en/stable/index.html>
<!-- #endregion -->
