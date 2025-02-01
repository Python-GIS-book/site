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

[OpenStreetMap](www.openstreetmap.org) [^OSM] (OSM) is a free, editable  map of the world that is created by a global community of mappers. OSM is often referred to as "the Wikipedia of maps" meaning that anyone can update the contents and use them freely. When using OSM data, appropriate credit should be given to OpenStreetMap and its contributors (see [OSM Copyright and License](https://www.openstreetmap.org/copyright) [^OSM_license]). 

OpenStreetMap data are increasingly used in various map-based applications and as research data. In many regions, OSM is the best data available on streets, buildings and amenities, or at least the best data source that is openly available. OSM data are often most complete from urban regions as many public transport organizations and companies also update the map to improve their services. Various organized mapping campaings exists to update OSM in areas that lack detailed map data (check out [Humanitarian OpenStreetMap Team](https://www.hotosm.org) [^HOTOSM]).

For geographic data analysis, OSM may be used as source data for various tasks such as routing and geocoding, and as bacground maps for visualizing analysis results. [The Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) [^Overpass_API_intro] can be used for querying and fetching data for further analysis. Relevant map feature categories include: 

- street networks
- buildings
- amenities
- landuse
- natural elements
- boundaries

In OpenStreetMap, different types of map features are labeled using tags, which consist of a key which describes the category (such as "highway" or "building") and a value, which describes the type of object within the category (such as "primary road" or "aparment"). Information on various map features and their associated tags is fundamental for correctly using the data. 

A good way to start working with OSM data is to view the map from an area you are familiar with and inspect the map features and their tags. The great thing about OSM is that anyone can sign up and make edits to the map. There are various discussion forums and mapping projects that support new (and old) mappers. [The OSM wiki](https://wiki.openstreetmap.org/wiki/Main_Page) [^OSM_wiki] provides an extensive overview for anyone planning to use or produce OSM data. 



#### Question 9.1

Go to www.openstreetmap.org and zoom the map to an area that you are familiar with. 
- Does the map look complete?
- Are there any geometric features (roads, buildings, bus stops, service locations) missing?
- Inspect further some of the features; are there any attribute information missing (street names, building addresses, service names or opening hours)?

You can check the intended tags for various map freatures from the [OSM wiki](https://wiki.openstreetmap.org/wiki/Map_features) [^OSM_wiki_tags]. If you spotted some missing information, freel free to create an OpenStreetMap account, log in, and update the map!


## Downloading OpenStreetMap data with OSMnx

[Osmnx](https://github.com/gboeing/osmnx) [^OSMnx] is a Python package that makes it easy to download, model and analyze street networks and other geospatial features from OpenSteetMap ({cite}`Boeing2024`). `Osmnx` relies on `geopandas` and another module called `networkx`, which enables network analysis. For latest updates, installation instructions, and complete user reference, see [osmnx  documentation](https://osmnx.readthedocs.io/en/stable/index.html) [^osmnx_docs]. 


### Defining the area of interest

```python
import osmnx as ox
```

```python
place = "Kamppi, Helsinki, Finland"

# ADD CODE FOR DOWNLOADING THE AOI POLYGON
```

### Street network


Street networks are downloaded using the `osmnx` `graph` module which can be used to retrieve the street network data and to construct a `networkx` graph model that can be used for routing. 

```python
# Fetch OSM street network from the location
graph = ox.graph_from_place(place)
```

Let's check the type of data we got: 

```python
type(graph)
```

Let's have a closer look a the street nework. OSMnx has its own function [plot_graph()](https://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=plot_graph#osmnx.plot.plot_graph) for visualizing graph objects. The function utilizes Matplotlib for visualizing the data,
hence as a result it returns a matplotlib figure and axis objects:


```python
# Plot the streets
fig, ax = ox.plot_graph(graph)
```

From here we can see that our graph contains nodes (the points) and edges (the lines) that connects those nodes to each other. For now, we won't dive deeper into routing analysis, but you can find further examples from the `osmnx` online documentation. 


Instead, we can convert the streets (edges of the network) into a `GeoDataFrame` using the `osmnx` function `graph_to_gdfs()`. 

```python
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
```

```python
edges.head(2)
```

### Other map features
Downloading building footprints, points of interests such as services and other map features is possible using the `osmnx` `features` module.  Map queries can be defined by city name, polygon, bounding box or an address or a point location and a buffer distance. In addition, a set of tags can be specified to select which map features to download. Tags are passed to these functions as a dictionary allowing querying multiple tags at the same time.There are different functions available to query data from the Overpass API using `osmnx` depending on the way in which the spatial location is defined: 

- address: [osmnx.features.features_from_address(address, tags, dist)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_address)
- bounding box: [osmnx.features.features_from_bbox(bbox, tags)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_bbox)
- place: [osmnx.features.features_from_place(place, tags)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_place)
- point: [osmnx.features.features_from_point(center_point, tags, dist)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_point)
- polygon: [osmnx.features.features_from_polygon(polygon, tags)](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_polygon)

These functions return a `GeoDataFrame` object.  Here, we will demonstrate the use of a place name search for downloading and visualizing OSM data for a central urban area in Helsinki, Finland.

```python
place = "Kamppi, Helsinki, Finland"
tags = { "building" : True}

buildings = ox.features.features_from_place(place, tags)
```

Notice that the  place name and an associated polygon should exist on OpenStreetMap, otherwise the query will fail. The downloaded OSM data comes with plenty of information representing various attributes of the features that OSM contributors have added. Each column in the data contains information about a spesific tag that OpenStreetMap contributors have added. At the time of writing, the building data from central Helsinki containe 120 different columns.

```python
len(buildings.columns)
```

You can see names of all available columns, for example, by running `list(buildings.columns)`. Let's check the contents of some of the available columns:

```python
buildings[['building', 'name', 'addr:city', 'geometry']].head()
```


From here we can tell that some, but not all of the buildings have a more specific information of the type of building (e.g., a school) and name and address. Let's plot the building footprints to get an overview of the data. While plotting,` we can add color the map according to the building tag values to get an overview of where different types of buildings are located. Notice that some buildings are tagged only with the generic tag "building=yes" without further information about the type of the building.

```python
buildings.plot(column="building", figsize=(8.2,8), cmap="tab20c", legend=True)
```

### Amenities


Continuing with the same place, let's also fetch all points of interests using the amenity tag:

```python
tags = {"amenity": True}
amenities = ox.features.features_from_place(place, tags)
```

Again, let's only plot a couple of available columns to check the contents of the data. You can see all column names  by running `list(buildings.columns)`.

```python
amenities[['amenity', 'name', 'opening_hours', 'addr:city', 'geometry']].head()
```

Here, we received all amenities in the area of interest ranging from restaurants, cafes and so on. The type of amenity (i.e. the value of the OSM tag) is indicated in the `amenity` column. Again, some, but not all features have additional information such as opening hours available. The downloaded data contains more than 700 individual points of interests in the data:

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

### Green space

Urban green space and public open space are vital components of liveable urban areas. Let's see how we can fetch urban green space data from OSM using the `osmnx` `features` module. Fetching green spaces from OpenStreetMap requires a bit of investigation of appropriate tag values - these might vary across cities. One common way of tagging urban parks is `leisure=park`. If wanting to capture also other green infrastructure, additional tags such as `landuse=grass` may be added. Let's proceed with these two tags that should capture rather well the available greenspaces in downtown Helsinki.

```python
# List key-value pairs for tags
tags = {"leisure": "park", "landuse": "grass"}
```

```python
# Get the data
parks = ox.features.features_from_place(place, tags)
```

```python
# Check number of downloaded objects
print("Retrieved", len(parks), "objects")
```

let's check the first rows:

```python
parks[['leisure', 'landuse', 'name', 'geometry']].head()
```

The first five rows of data contain different parks, which all have a name. Let's quicly plot the data to see the geometry:

```python
parks.plot(color="green")
```

### Plotting the data

Let's create a map out of the streets, buildings, restaurants in our area of interest.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 8))

# Plot the footprint
#area.plot(ax=ax, facecolor="black")

# Plot street edges
edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")

# Plot buildings
buildings.plot(ax=ax, facecolor="silver", alpha=0.7)

parks.plot(ax=ax, facecolor="green", alpha=0.7)

# Plot restaurants
amenities.plot(ax=ax, column="amenity", alpha=0.7, markersize=10)

plt.tight_layout()
```

Cool! Now we have a map where we have plotted the restaurants, buildings, streets and the boundaries of the selected region of 'Kamppi' in Helsinki. And all of this required only a few lines of code. Pretty neat! 



#### Question 9.3

Check your understanding and retrieve OpenStreetMap data from some other area in the world. Use `osmnx`and download:

- Polygon of your area of interest
- Street network
- Building footprints
- Restaurants and cafes (or why not also other amenities)
- Green spaces

*Note, the larger the area you choose, the longer it takes to retrieve data from the API! Use parameter `network_type=drive` to limit the graph query to filter out un-driveable roads.*

```python editable=true slideshow={"slide_type": ""} tags=["remove_cell"]
# Use this cell to enter your solution.
```

```python editable=true slideshow={"slide_type": ""} tags=["remove_book_cell", "hide-cell"]
# Solution

# INSERT EXAMPLE SOLUTION HERE
#streets = 
#builginds = 
#amenities =
#parks = 
```

```python
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the footprint
area.plot(ax=ax, facecolor="black")

# Plot the parks
parks.plot(ax=ax, facecolor="green")

# Plot street edges
edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")

# Plot buildings
buildings.plot(ax=ax, facecolor="silver", alpha=0.7)

# Plot restaurants
restaurants.plot(ax=ax, color="yellow", alpha=0.7, markersize=10)
plt.tight_layout()
```

## Footnotes

[^OSM]: <https://www.openstreetmap.org/>
[^OSM_license]: <https://www.openstreetmap.org/copyright>
[^Overpass_API_intro]: <https://wiki.openstreetmap.org/wiki/Overpass_API> 
[^HOTOSM]: <https://www.hotosm.org> 
[^OSM_wiki]: <https://wiki.openstreetmap.org/wiki/Main_Page>
[^OSM_wiki_tags]: <https://wiki.openstreetmap.org/wiki/Map_features> 
[^OSMnx]: <https://github.com/gboeing/osmnx>
[^osmnx_docs]: <https://osmnx.readthedocs.io/en/stable/index.html>

```python

```
