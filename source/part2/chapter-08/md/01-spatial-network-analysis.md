---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Shortest path analysis

In the previous section, we learned how to create graphs both from scratch and from existing street network data stored in a GeoPackage file. This section focuses on spatial networks and learning how to construct a routable directed graph for `networkx` library that can be used to find a shortest paths along the given street network based on travel times or distance by given transport mode (e.g. car or cycling). Finding a shortest path from A to B using a specific street network is a very common problem in GIS that has many practical applications. For example, navigation services use shortest path analysis to guide drivers, cyclists and pedestrians to their destination, emergency services use it to estimate how quickly an ambulance can reach a given address, and delivery companies use it to plan their routes. Network analysis is also commonly used in urban planning, for instance to study how easily people can reach services such as schools, health care or grocery stores (a topic that we return to in Chapter 11).

Python provides easy to use tools for conducting spatial network analysis. One of the easiest ways to start is to use a library called `networkx`[^networkx]
which is a Python module that provides a lot tools that can be used to analyze networks on various different ways. It also contains algorithms such as Dijkstra’s algorithm[^dijkstra] or A\*[^astar]
algorithm that are commonly used to find shortest paths along transportation network that can help e.g. in wayfinding.


## Typical workflow for routing

If you want to conduct network analysis (in any programming language) there are a few basic steps that typically needs to be done before you can start routing. These steps are:

 1. **Retrieve data** (such as street network from OSM or Digiroad + possibly transit data if routing with PT).
 2. **Modify the network** by adding/calculating edge weights (such as travel times based on speed limit and length of the road segment).
 3. **Build a routable graph** for the routing tool that you are using (e.g. for NetworkX, igraph or OpenTripPlanner).
 4. **Conduct network analysis** (such as shortest path analysis) with the routing tool of your choice.


## Retrieving network data

As a first step, we want to obtain data for routing. In the previous section, we used street network data from Digiroad, the national road and street database of Finland, which was stored in a GeoPackage file. National road databases like this provide detailed information about the streets, but they are openly available only in some countries, and their attributes differ from one country to another. One of the most widely used data sources for street networks is OpenStreetMap (OSM) that provides this type of data openly at a global scale. Hence, instead of relying on existing street network files, OSM is a handy data source for routing, especially in areas where no other street network data are available. There are a few Python libraries that you can use to easily find and download OSM data, including `osmnx`[^osmnx] and `pyrosm`[^pyrosm]. These libraries make it really easy to retrieve routable networks from OpenStreetMap with different transport modes (walking, cycling and driving). as well as retrieve other interesting data, such as buildings and Points of Interest (POIs). Here, we will first show how you can use `osmnx` to extract OSM data for Helsinki city centre that are drivable by car. In `osmnx`, you can specify the area from where you want to download the data by providing a point of interest, a bounding polygon or a place name. To fetch OSM data around a given center point, we can use a function called `ox.graph_from_point()`. We define the center point as a `(latitude, longitude)` pair and set how far around it to fetch data with the `dist` parameter (in meters). By default, `osmnx` fetches the data from a square-shaped area (a bounding box) that extends the given distance from the center point in each direction. It is possible to specify what kind of roads should be retrieved from OSM with `network_type` -parameter (supports e.g. `walk`, `drive`, `bike`, `all`). In the following, we fetch all the drivable roads that are within 2500 meters from the Helsinki city centre in each direction, i.e. from an area of 5 x 5 kilometers:

```python
import osmnx as ox
import geopandas as gpd
import pandas as pd
import networkx as nx

# The area of interest
center_point = (60.162, 24.937)

G = ox.graph_from_point(center_point, dist=2500, network_type="drive", simplify=False)

type(G)
```

As we can see, we have now fetched a routable graph from OpenStreetMap and stored it into variable `G`. The data is automatically returned as a `networkx` `MultiDiGraph` which is a directed graph with reciprocal edges allowing multiple edges between the same pair of nodes (which we discussed in previous section). We can easily extract the `nodes` and `edges` out of this graph by using the `ox.graph_to_gdfs()` function which returns those features from the graph into separate GeoDataFrames: 

```python
# Extract the nodes and edges
nodes, edges = ox.graph_to_gdfs(G)
nodes.head(2)
```

```python
edges.head(2)
```

```python
ax = edges.plot()
ax = nodes.plot(ax=ax, color="red", markersize=3.5)
```

_**Figure 8.X.** Drivable streets (edges) and their nodes (in red) in the Helsinki city centre, retrieved from OpenStreetMap._


As a result, we have drivable roads as a GeoDataFrame for the Helsinki city centre in which the geometries are presented as `LineString` objects which we have mapped in **Figure 8.X**. The `nodes` GeoDataFrame contains information about the coordinates of each node, as well as a unique id for each node, called `osmid`. These id-values are used for constructing the edges, i.e. the from- and to-ids for each edge in the `edges` GeoDataFrame. To determine the structure and directionality of the network, `osmnx` stores the from-id as `u` in the index, while index level `v` stores the to-id accordingly. The third index level, `key`, is used to separate several edges that connect the same pair of nodes (i.e. reciprocal edge). If you look at the GeoDataFrame, we can see that `osmnx` has also calculated us the `length` of each road segment in meters automatically. Notice that if calculating the length yourself, it is important that your input data is in projected (metric) coordinate system (see Chapter 6.4). As our graph is a directed one, the data should include information about which direction the movement is allowed. In OSM, this information is stored in a column `oneway` (in the Digiroad data that we used in the previous section, the same information was stored in the `direction` column, see Table 8.1). Let's take a look what values do we have in this column:

```python
edges["oneway"].unique()
```

As we can see the unique values in that column are `True` and `False`. This information was used to construct the `directed` graph for routing. For walking and cycling, you may want create an `undirected` graph, because the travel is typically allowed in both directions at least in Finland. Notice, that the rules vary by country and for instance in Copenhagen you have oneway rules also for bikes. Column `maxspeed` contains information about the speed limit for a given road:

```python
edges["maxspeed"].unique()
```

As is visible here, there are also `None` values in the data, meaning that the speed limit has not been tagged for some roads. This is typical, and often you need to fill the non existing speed limits yourself (in the Digiroad data that we used in the previous section, all street segments had a speed limit value). This can be done by taking advantage of the road class that is always present in column `highway`:

```python
edges["highway"].unique()
```

Based on these values, we can make assumptions that e.g. `living_street` roads in Helsinki have a speed limit of 20 kmph. Hence, this information can be used to fill the missing values in `maxspeed`.


Notice that retrieving data around a center point is only one of the ways to define the area of interest. For instance, you can also retrieve the street network based on a place name with the `ox.graph_from_place()` function, which first finds the boundary polygon of the place with the Nominatim geocoding service (see Chapter 6.5) and then downloads the streets within this polygon. As an example, the following retrieves the drivable streets of the Kamppi district in Helsinki, but in the rest of this section we continue with the network that we retrieved around the center point:

```python
G_kamppi = ox.graph_from_place("Kamppi, Helsinki, Finland", network_type="drive")
fig, ax = ox.plot_graph(G_kamppi, bgcolor="white", edge_color="black", node_color="red")
```

_**Figure 8.X.** Drivable streets in the Kamppi district of Helsinki, retrieved from OpenStreetMap with `osmnx` based on the place name._


## Modifying the network

At this stage, we have the necessary components to build a routable graph (nodes and edges) based on distance. However, in real life the network distance is not the best cost metric to use, because the shortest path (based on distance) is not necessarily always the optimal route in terms of **travel time**. Time is typically the measure that people value more (plus it is easier to comprehend), so at this stage we want to **add a new cost attribute** to our edges GeoDataFrame that converts the metric distance information to travel time (in seconds). Before we can do this calculation, we need to ensure that all rows in `maxspeed` column have information about the speed limit. Let's check the value counts of the column and also include information about the `NaN` values with `dropna` parameter:

```python
# Count values
edges["maxspeed"].value_counts(dropna=False)
```

<!-- #region -->
As we can see, the rows which do not contain information about the speed limit is the second largest group in our data. Hence, we need to apply a criteria to fill these gaps. We can do this based on a following "rule of thumb" criteria in Finland presented in Table 8.3 (notice that these vary country by country).


: _**Table 8.3**. Typical speed limits (km/h) in Finland for different road classes within and outside urban regions._


| Road class           | Speed limit within urban region | Speed limit outside urban region |
|----------------------|---------------------------------|----------------------------------|
| motorway             | 100                             | 120                              |
| motorway_link        | 80                              | 80                               |
| trunk                | 60                              | 100                              |
| trunk_link           | 60                              | 60                               |
| primary              | 50                              | 80                               |
| primary_link         | 50                              | 50                               |
| secondary            | 50                              | 50                               |
| secondary_link       | 50                              | 50                               |
| tertiary             | 50                              | 60                               |
| tertiary_link        | 50                              | 50                               |
| unclassified         | 50                              | 80                               |
| unclassified_link    | 50                              | 50                               |
| residential          | 50                              | 80                               |
| living_street        | 20                              | NA                               |
| service              | 30                              | NA                               |
| other                | 50                              | 80                               |

For simplicity, we can consider that all the roads in Helsinki Region follows the *within urban region* speed limits, although this is not exactly true (the higher speed limits start somewhere at the outer parts of the city region). For making the speed limit values more robust / correct, you could use data about urban/rural classification which is available in Finland from Finnish Environment Institute[^ykr]. Let's first convert our `maxspeed` values to integers using `astype()` method:
<!-- #endregion -->

```python
edges["maxspeed"] = edges["maxspeed"].astype(float).astype(pd.Int64Dtype())
edges["maxspeed"].unique()
```

As we can see, now the maxspeed values are stored in integer format inside an `IntegerArray`, and the `None` values were converted into `pandas.NA` objects that are assigned with `<NA>`. Now we can create a function that returns a numeric value for different road classes based on the criteria in the table above:

```python
def road_class_to_kmph(road_class):
    """
    Returns a speed limit value based on road class,
    using typical Finnish speed limit values within urban regions.
    """
    if road_class == "motorway":
        return 100
    elif road_class == "motorway_link":
        return 80
    elif road_class in ["trunk", "trunk_link"]:
        return 60
    elif road_class == "service":
        return 30
    elif road_class == "living_street":
        return 20
    else:
        return 50
```

Now we can apply this function to all rows that do not have speed limit information:

```python
mask = edges["maxspeed"].isnull()
```

```python
mask
```

```python
# Separate rows with / without speed limit information
mask = edges["maxspeed"].isnull()
edges_without_maxspeed = edges.loc[mask].copy()
edges_with_maxspeed = edges.loc[~mask].copy()

# Apply the function and update the maxspeed
edges_without_maxspeed["maxspeed"] = edges_without_maxspeed["highway"].apply(
    road_class_to_kmph
)
edges_without_maxspeed.head(5).loc[:, ["maxspeed", "highway"]]
```

Okay, as we can see now the `maxspeed` value have been updated according our criteria, and e.g. the `living_street` road class have been given the speed limit 20 kmph. Now we can recreate the edges GeoDataFrame by combining the two frames: 

```python
edges = pd.concat([edges_with_maxspeed, edges_without_maxspeed])
edges["maxspeed"].unique()
```

Great, now all of our edges have information about the speed limit. We can also visualize them:

```python
# Convert the value into regular integer Series (the plotting requires having Series instead of IntegerArray)
edges["maxspeed"] = edges["maxspeed"].astype(int)
ax = edges.plot(column="maxspeed", figsize=(16, 10), legend=True)
```

_**Figure 8.X.** Speed limits (km/h) of the streets after filling in the missing values._


We will calculate the travel time it takes to cross a given street segment assuming that the person would be driving according the speed limits. The `maxspeed` column in our data provides information about the speed limit (km per hour) on a given street element. This is very useful information as we can use this to calculate the "free-flow" travel time which indicates the time it takes to cross a specific street segment assuming that a given person would be able to travel as fast as the speed limit allows.

Now we have all the information needed to calculate the free-flow travel time. To calculate the travel time in seconds, we can use a following formula that considers the speed limit information in km/h and the distance as meters (which is how our data is constructed):

$$
t = \frac{3.6 \, d}{v}
$$

Where:  

- $t$ = travel time in **seconds (s)**  
- $d$ = distance in **meters (m)**  
- $v$ = speed limit in **kilometers per hour (km/h)**

The multiplication of distance by 3.6 is a conversion factor between meters per second and kilometers per hour:

$$
1 \ \text{m/s} = \frac{3600}{1000} \ \text{km/h} = 3.6 \ \text{km/h}
$$



Finally, we can calculate the travel time in seconds using the formula above and add that as a new cost attribute for our network:

```python
edges["travel_time_seconds"] = edges["length"] / (edges["maxspeed"] / 3.6)
edges.iloc[0:10, -4:]
```

Excellent! Now our GeoDataFrame has all the information we need for creating a graph that can be used to conduct shortest path analysis based on length or travel time. Notice that here we assume that the cars can drive with the same speed as what the speed limit is. Considering the urban dynamics and traffic congestion, this assumption might not hold, but for simplicity, we assume so in this tutorial. 


### Building a routable graph from modified edges

In the previous section, we wrote our own function `gdf_to_directed_graph()` to build a directed graph from a GeoDataFrame of street segments. For OpenStreetMap data, we do not need to write such a function ourselves. We can use `osmnx` library to easily build a directed graph. Let's see how we can create a routable NetworkX graph using `osmnx` with one command:

```python
G = ox.graph_from_gdfs(gdf_nodes=nodes, gdf_edges=edges)
G
```

Now we have a similar routable graph as in the beginning, but now the network edges contain information about the speed limit and the travel time (`travel_time_seconds`) for all edges, which we can use as the cost when finding routes. We can easily visualize the graph with `osmnx` as follows: 

```python
import osmnx as ox

ox.plot_graph(G)
```

_**Figure 8.X.** The routable street network of the Helsinki city centre plotted with `osmnx`._


## Shortest path analysis 

Now we have everything we need to start routing with NetworkX (based on driving distance or travel time). Notice that the routing functions of `networkx` work with any graph that has a suitable cost attribute for its edges. Hence, you could conduct the routing in a similar manner also with the Digiroad data that we used in the previous section, by calculating the length and travel time for each street segment and building the graph with our `gdf_to_directed_graph()` function. One of the most widely used real-world use-cases for spatial networks relates to navigation, i.e. how to find a route from a given origin location to a given destination that would be as short (or quick) as possible. There are various approaches and algorithms that can be used to find such routes, but the one we introduce here is one of the most famous ones, called Dijkstra's algorithm, that is widely used to find an optimal least-cost path between given nodes. But first, let's again go through some basics about routing.


**Basic logic in routing.** Most (if not all) routing algorithms work more or less in a similar manner. The basic steps for finding an optimal route from A to B are to:
 1. Find the nearest node for origin location (+ get info about its node-id and distance between origin and node)
 2. Find the nearest node for destination location (+ get info about its node-id and distance between destination and node)
 3. Use a routing algorithm to find the shortest path between A and B
 4. Retrieve edge attributes for the given route(s) and summarize them (can be distance, time, CO2, or whatever)
 
This same logic should be applied always when searching for an optimal route between a single origin and a single destination, or when calculating one-to-many -type of routing queries (producing e.g. travel time matrices). 


### Find the optimal route between two locations

Next, we will learn how to find the shortest path between two locations using Dijkstra's[^dijkstra_algorithm] algorithm. The idea behind Dijkstra's algorithm is quite intuitive. The algorithm starts from the origin and explores the network step by step, always continuing from the node that is closest to the origin at that point (in terms of the chosen cost, such as distance or travel time). For every node it reaches, the algorithm keeps track of the shortest known way to get there, and updates it whenever it finds a shorter one. In this way, the search spreads outwards from the origin, a bit like water flowing along the streets, and once it reaches the destination, the route that it has found is the shortest possible one.

Dijkstra's algorithm is not the only way to find shortest paths. Table 8.4 lists some commonly used shortest path algorithms, what they are suited for, and which `networkx` function implements them.


: _**Table 8.4**. Commonly used shortest path algorithms and when to use them._

| Algorithm | Description | When to use | In `networkx` |
|:----------|:------------|:------------|:--------------|
| Breadth-first search | Explores the network one edge at a time and ignores edge weights, so it finds the path with the fewest edges. | When every edge counts the same, e.g. the number of street segments or stops between two places. | `nx.shortest_path()` without `weight` |
| Dijkstra's algorithm | Spreads out from the origin, always continuing from the closest node it has not yet visited. Works with any cost that is not negative, such as distance or travel time. | The default choice for routing in street networks, from one origin to one or all destinations. | `nx.dijkstra_path()`, `nx.single_source_dijkstra_path_length()` |
| A* | Like Dijkstra, but uses an estimate of the remaining cost (e.g. the straight-line distance to the destination) to search towards the destination first. The estimate must never be larger than the real remaining cost. | One origin and one destination in a large network, where node coordinates give a good estimate. | `nx.astar_path()` with `heuristic` |
| Bellman–Ford | Slower than Dijkstra, but also works when some edge costs are negative. | Rarely needed in transport networks; e.g. the energy use of an electric vehicle, which can be negative downhill when the battery recharges. | `nx.bellman_ford_path()` |
| Floyd–Warshall | Calculates the shortest paths between all pairs of nodes at once. | Complete travel time matrices for small networks. Computation time and memory grow quickly with network size, so for large networks running Dijkstra from each origin is faster. | `nx.floyd_warshall()` |
| Contraction hierarchies | Prepares the network once by adding shortcut edges, after which each query is very fast. Used by routing engines such as OSRM. | Very many queries on a large network that does not change, e.g. travel time matrices for a whole country. | not available |
| RAPTOR | Built for public transport timetables. It works in rounds, one per transfer, instead of searching a graph. R5 (and so `r5py`) uses an extended version of it. | Routing with public transport. | not available |


Before we can find a route, we need to define the origin and destination of our trip. In this example, we will find a route by car from Ruoholahdenkatu 24 to Annankatu 18, which are two addresses located in the Helsinki city centre. To find the closest nodes for these locations, we first need to know their coordinates. OSMnx provides a handy function for geocoding an address `ox.geocode()` (we discussed geocoding in more detail in Chapter 6.5). We can use that to retrieve the x and y coordinates of our origin and destination:

```python
# OSM data is in WGS84 so typically we need to use lat/lon coordinates when searching for the closest node

# Origin
orig_address = "Ruoholahdenkatu 24, Helsinki"
orig_y, orig_x = ox.geocode(orig_address)  # notice the coordinate order (y, x)!

# Destination
dest_address = "Annankatu 18, Helsinki"
dest_y, dest_x = ox.geocode(dest_address)

print("Origin coords:", orig_x, orig_y)
print("Destination coords:", dest_x, dest_y)
```

Now we have coordinates for our origin and destination. The coordinates are longitude (x) and latitude (y) values in the WGS84 coordinate reference system, which is the same as in our street network. Hence, we can use them directly for finding the closest nodes from the graph.


### Find the nearest nodes

Next, we need to find the closest nodes from the graph for both of our locations, which correspond to the first two steps of the basic logic of routing that we described above. This step is needed because the routing algorithm finds paths between the nodes of the graph, and our origin and destination are not necessarily located exactly at any of the nodes. For calculating the closest point we use `ox.distance.nearest_nodes()` -function and specify `return_dist=True` to get the distance in meters:

```python
# Find the closest nodes for origin and destination
orig_node_id, dist_to_orig = ox.distance.nearest_nodes(
    G, X=orig_x, Y=orig_y, return_dist=True
)
dest_node_id, dist_to_dest = ox.distance.nearest_nodes(
    G, X=dest_x, Y=dest_y, return_dist=True
)

print("Origin node-id:", orig_node_id, "and distance:", dist_to_orig, "meters.")
print("Destination node-id:", dest_node_id, "and distance:", dist_to_dest, "meters.")
```

As a result, we get the id of the closest node for both locations, together with the distance (in meters) between the location and the node. Both nodes are located only a few tens of meters away from the given addresses. Now we are ready to start the actual routing with NetworkX. 


### Find the shortest and the fastest route

Now we can do the routing and find the shortest path between the origin and target locations by using the `dijkstra_path()` function of NetworkX. For getting only the cumulative cost of the trip, we can directly use a function `dijkstra_path_length()` that returns the total cost of the route (e.g. the distance or the travel time) without the actual path.

The function takes our graph `G` as input which will be the network used for finding the shortest path. In addition, we need to define the nodes that are used as the origin (i.e. `source`) and destination points (`target`) for the analysis. Lastly, we need to define the `weight` (also called as `cost` or `impedance`) which is needed to find the optimal least-cost path between the given `source` and `target` nodes. With `weight` -parameter we can specify the attribute that we want to use as cost/impedance. We have now two possible weight attributes available: `'length'` and `'travel_time_seconds'`. Let's calculate the routes between our locations using both weights, and also retrieve the total distance and travel time of these routes:

```python
# Calculate the paths
metric_path = nx.dijkstra_path(
    G, source=orig_node_id, target=dest_node_id, weight="length"
)
time_path = nx.dijkstra_path(
    G, source=orig_node_id, target=dest_node_id, weight="travel_time_seconds"
)

# Get also the actual travel times (summarize)
travel_length = nx.dijkstra_path_length(
    G, source=orig_node_id, target=dest_node_id, weight="length"
)
travel_time = nx.dijkstra_path_length(
    G, source=orig_node_id, target=dest_node_id, weight="travel_time_seconds"
)
```

Now we have found two routes: `metric_path` is the shortest route based on distance and `time_path` is the fastest route based on travel time. Both of them are stored as lists of the nodes that the route goes through (we will take a closer look at these lists later in this section). In addition, we stored the total distance (in meters) of the shortest route into the variable `travel_length` and the total travel time (in seconds) of the fastest route into the variable `travel_time`. Let's print these values, and convert the travel time into minutes by dividing it by 60:

```python
print(f"Shortest path distance {travel_length: .1f} meters.")
print(f"Shortest path time {travel_time/60: .1f} minutes.")
```

As we can see, the shortest route is roughly one kilometer long, and driving the fastest route takes about two minutes. Let's now see what we got by visualizing the results. For visualization purposes, we can use a handy function again from OSMnx called `ox.plot_graph_route()` that plots the route in a simple map. The function takes the graph and the route as input, and draws the route as a red line on top of the street network. With the other parameters, we can adjust how the map looks: here, we draw the streets as thin (`edge_linewidth`) black (`edge_color`) lines on a white background (`bgcolor`), and hide the nodes of the network by setting their size to zero (`node_size`). Let's start by plotting the shortest route based on distance:

```python
fig, ax = ox.plot_graph_route(
    G,
    metric_path,
    edge_linewidth=0.2,
    node_size=0,
    bgcolor="white",
    edge_color="black",
    figsize=(14, 10),
)
```

_**Figure 8.X.** The shortest route between the origin and the destination based on distance._


In Figure 8.X, the shortest route starts from our origin at Ruoholahdenkatu and ends at our destination at Annankatu. The circles at both ends of the route show the nodes that are closest to these locations. Next, let's plot the fastest route based on travel time in a similar manner:

```python
fig, ax = ox.plot_graph_route(
    G,
    time_path,
    edge_linewidth=0.2,
    node_size=0,
    bgcolor="white",
    edge_color="black",
    figsize=(14, 10),
)
```

_**Figure 8.X.** The fastest route between the origin and the destination based on travel time._


The routes in the two previous figures look exactly the same. We can confirm this by checking whether the lists of nodes in the two routes are equal:

```python
metric_path == time_path
```

Great! Now we have successfully found the optimal route between our origin and destination and we also have estimates about the travel time that it takes to travel between the locations by driving. As we can see, the routes optimized based on travel time and distance are exactly the same, which is natural, as the network here is relatively small and there are no big differences in the speed limits. However, with larger networks, you might get alternative routes as travelling e.g. via ring roads is typically faster than driving through the city (as an example).


### Summarizing the route

The last step of the basic routing logic that we went through earlier is to retrieve the edge attributes for the given route and summarize them. The route that we got from the `dijkstra_path()` function is a list of visited nodes of the shortest path. Let's take a look at the first nodes of our fastest route:

```python
time_path[:5]
```

As we can see, the route is stored as a list of node ids. To find out which streets the route uses, we need to construct the path edges from these nodes by using the `nx.utils.pairwise()` function. This function converts the list of visited nodes into a collection of node-tuples that represent the edges of the shortest path:

```python
path_edges = list(nx.utils.pairwise(time_path))
path_edges[:5]
```

Using these node pairs, we could look up the attributes of each street segment along the route from our graph. `osmnx` has a handy function `ox.routing.route_to_gdf()` that does this for us and returns the edges of the route as a GeoDataFrame in the order they are traveled. We also pass the same `weight` that we used for finding the route, so that the function picks the same street segments as the routing algorithm did:

```python
route_edges = ox.routing.route_to_gdf(G, time_path, weight="travel_time_seconds")
route_edges[["name", "maxspeed", "length", "travel_time_seconds"]]
```

Now we can see the names of the streets along the route, together with their speed limits, lengths and travel times. Finally, we can summarize the route by calculating the total length and travel time of the trip:

```python
route_edges[["length", "travel_time_seconds"]].sum()
```

As we can see, the total travel time is the same as the one we calculated earlier with the `dijkstra_path_length()` function. In addition, we now know the total length of the fastest route.


## One-way streets and the direction of travel

In the examples thus far, we have searched the route only to one direction, i.e. from the origin to the destination. However, many trips are made to both directions. A real-life example of these kind of two-way trips is when commuting between home and work locations. Because our graph is directed, traveling to both directions using identical paths is not necessarily possible due to one-way streets. Let's see what happens if we search for the fastest route back from the destination to the origin:

```python
time_path_back = nx.dijkstra_path(
    G, source=dest_node_id, target=orig_node_id, weight="travel_time_seconds"
)
travel_time_back = nx.dijkstra_path_length(
    G, source=dest_node_id, target=orig_node_id, weight="travel_time_seconds"
)

print(f"Travel time to the destination {travel_time/60: .1f} minutes.")
print(f"Travel time back to the origin {travel_time_back/60: .1f} minutes.")
```

Let's compare the two routes by plotting them on the same map. For this, we can use the `ox.plot_graph_routes()` function that works in a similar manner as the `ox.plot_graph_route()` function we used earlier, but takes a list of routes as input. We draw the route to the destination with red and the route back to the origin with blue color:

```python
fig, ax = ox.plot_graph_routes(
    G,
    [time_path, time_path_back],
    route_colors=["r", "b"],
    edge_linewidth=0.2,
    node_size=0,
    bgcolor="white",
    edge_color="black",
    figsize=(14, 10),
)
```

_**Figure 8.X.** The fastest route from the origin to the destination (red) and back from the destination to the origin (blue)._


Where the red and blue routes do not overlap, the route back uses different streets than the route to the destination, because some of the streets along the way can be driven only to one direction. Depending on how long a detour these one-way streets cause, the travel times to the two directions can also differ. With an undirected graph, we could not capture this: the route back could always use the same streets as the route to the destination, and the travel times to both directions would be identical.


## Shortest paths from one origin to many destinations

Thus far, we have searched routes between a single origin and a single destination. However, as we mentioned earlier, the same logic can also be used when calculating one-to-many -type of routing queries. For instance, we might want to know how long it takes to drive from our origin to all other locations in the street network. For this purpose, we can use the `nx.single_source_dijkstra_path_length()` function that calculates the shortest path lengths from a given `source` node to all nodes that can be reached from it:

```python
travel_times = nx.single_source_dijkstra_path_length(
    G, source=orig_node_id, weight="travel_time_seconds"
)
list(travel_times.items())[:5]
```

As a result, we get a dictionary in which the keys are the ids of the nodes and the values are the travel times (in seconds) from the origin to these nodes. The first item is the origin node itself, which is why its travel time is 0. To see the result on a map, let's add the travel times as a new column to the `nodes` GeoDataFrame that we extracted from the graph earlier. We first convert the dictionary into a `pandas` `Series` that uses the node ids as its index, which makes it possible to match the travel times with the correct nodes. At the same time, we convert the travel times from seconds to minutes:

```python
nodes["travel_time_min"] = pd.Series(travel_times) / 60
nodes[["travel_time_min", "geometry"]].head()
```

Nodes that cannot be reached from the origin get a missing value (`NaN`), because they do not have a travel time in the result. Now we can visualize the travel times on a map. Here, we first plot the streets with light gray color as a background and then plot the nodes on top of them, colored by the travel time:

```python
ax = edges.plot(color="lightgrey", linewidth=0.5, figsize=(10, 10))
ax = nodes.plot(
    ax=ax,
    column="travel_time_min",
    cmap="RdYlBu",
    markersize=5,
    legend=True,
    legend_kwds={"label": "Travel time by car (minutes)"},
)
```

_**Figure 8.X.** Travel time by car (in minutes) from the origin to all nodes in the street network._


As we can see, the travel times generally increase the further away the nodes are from the origin. Calculating travel times from one or many origins to all destinations like this is the basis of accessibility analysis, which we will discuss in more detail in Chapter 11.

In accessibility analyses, the travel times are often reported for areal units, such as the cells of a statistical grid, instead of the nodes of the network. Let's see how we can link our travel times to the population grid of the Helsinki Region Environmental Services Authority (HSY) that we used in Chapter 6.7. The grid consists of 250 x 250 meter cells, and it contains the number of inhabitants living in each cell. Because our street network covers only the Helsinki city centre, we keep only the grid cells that are located within the area of the network. For this purpose, we create a polygon that covers all the nodes of the network, i.e. their convex hull (see Chapter 6.2), and select the grid cells that are within it:

```python
pop_grid = gpd.read_file("data/Population_grid_2021_HSY.gpkg")
network_area = nodes.to_crs(pop_grid.crs).union_all().convex_hull
pop_grid = pop_grid.loc[pop_grid.within(network_area)].copy()
len(pop_grid)
```

To find the travel time for each grid cell, we use the center point of the cell to represent it. We calculate the centroids of the cells (the grid is already in a projected coordinate reference system), convert them to WGS84 and find the nearest node of the network for each centroid with the `ox.distance.nearest_nodes()` function, in the same way as we did for our origin and destination earlier. Then we look up the travel time of each node from the `travel_time_min` column of the `nodes` GeoDataFrame with the `.map()` method:

```python
centroids = pop_grid.centroid.to_crs(epsg=4326)
pop_grid["node_id"] = ox.distance.nearest_nodes(G, X=centroids.x, Y=centroids.y)
pop_grid["travel_time_min"] = pop_grid["node_id"].map(nodes["travel_time_min"])
pop_grid[["inhabitants", "node_id", "travel_time_min"]].head()
```

Now each grid cell has the id of its nearest node and the travel time (in minutes) from our origin to the cell. Let's plot the grid cells colored by the travel time:

```python
ax = pop_grid.plot(
    column="travel_time_min",
    cmap="RdYlBu",
    linewidth=0,
    legend=True,
    legend_kwds={"label": "Travel time by car (minutes)"},
    figsize=(10, 10),
)
ax.set_axis_off()
```

_**Figure 8.X.** Travel time by car (in minutes) from the origin to the populated 250 x 250 meter grid cells in the Helsinki city centre._


As we can see in Figure 8.X, the travel times of the grid cells follow the same pattern as the travel times of the nodes in the previous figure. However, the grid covers only the places where people live, and it tells how many people live in each cell. In Chapter 11, we will use this kind of information to study how easily the people living in different parts of a city can reach the places that they need.


## Routing in large networks with `pyrosm`

Thus far, we have used `osmnx` to retrieve the street network for the Helsinki city centre. Under the hood, `osmnx` downloads the OpenStreetMap data from a web service called Overpass API[^overpass]. This works well for relatively small areas, such as a city centre or a neighborhood. However, the larger the area, the more data needs to be downloaded, and the Overpass server limits how long each query can run and how many queries each user can make. Very large areas also need to be split into many smaller queries. Hence, downloading the street network of a large city region, not to mention a whole country, can take a long time or even fail if the server is busy.

For large areas, a better option is to use the `pyrosm` library which reads OpenStreetMap data from **PBF files**[^pbf]. A PBF file (short for Protocolbuffer Binary Format) is a compressed file that contains all the OpenStreetMap data for a given area, such as a city, a region or a whole country. These files are distributed by data providers such as Geofabrik[^geofabrik] and Movisda[^movisda] (countries and regions) and BBBike[^bbbike] (cities). Because `pyrosm` reads the data from a file on your own computer instead of a server, it can read the street network for large areas quickly. To get the data, we can use the `get_data_by_geocoding()` function of `pyrosm`, which works in a similar manner as the `ox.graph_from_place()` function that we used earlier. Under the hood, the function geocodes the place name with Nominatim to find the boundary polygon of the place, downloads the smallest available PBF file that covers the place, and crops the data to the boundaries of the place. Instead of a single place name, we can also pass a list of place names, in which case the function combines the places into one area. Let's use it to download the data for the Helsinki metropolitan area, which consists of four cities: Helsinki, Espoo, Vantaa and Kauniainen:

```python
from pyrosm import OSM, get_data_by_geocoding

places = [
    "Helsinki, Finland",
    "Espoo, Finland",
    "Vantaa, Finland",
    "Kauniainen, Finland",
]
fp = get_data_by_geocoding(places)
fp
```

As a result, we get the path to a new PBF file that contains the data for the four cities. In this case, `pyrosm` downloaded a PBF file for the whole Uusimaa region from Movisda and cropped it to the boundaries of the cities. By default, `get_data_by_geocoding()` saves the files into a temporary folder on your computer, but you can also choose the folder yourself with the `directory` parameter. Notice also the warning that `pyrosm` printed: the downloaded PBF file does not cover a tiny part of the boundary polygons that Nominatim returned (here, a small area in the sea south of Helsinki). When the part that is left out is less than 0.1 % of the area, `pyrosm` uses the file anyway and only warns about it, which is fine for our purposes. Next, we initialize a reader object called `OSM` with the path to our file, and read the drivable streets with the `get_network()` method. The `network_type` parameter works in a similar manner as in `osmnx` (supported values include e.g. `"walking"`, `"cycling"`, `"driving"` and `"all"`). By specifying `nodes=True`, we get also the nodes of the network which we need for building the graph:

```python
osm = OSM(fp)
nodes_large, edges_large = osm.get_network(network_type="driving", nodes=True)
edges_large.head(2)
```

As we can see, the edges are returned as a GeoDataFrame in which the `u` and `v` columns contain the ids of the from- and to-nodes of each street segment, and the `length` column contains the length of the segment in meters. Now we can build a routable graph out of the nodes and edges with the `to_graph()` method. By default, `pyrosm` builds a graph for another network analysis library called `igraph`, so we need to specify `graph_type="networkx"` to get a `networkx` graph:

```python
G_large = osm.to_graph(nodes_large, edges_large, graph_type="networkx")
G_large
```

As a result, we have a `MultiDiGraph` similar to the one that we retrieved earlier with `osmnx`. In the same way as `osmnx`, `pyrosm` takes the one-way streets into account when building a graph for driving. In addition, `pyrosm` simplifies the graph by default, i.e. it merges the street segments between two intersections into a single edge, which makes the graph considerably smaller (we will discuss simplification in more detail in Chapter 8.4). The graph is also compatible with `osmnx`, which means that we can use the same `osmnx` functions with it as earlier. For instance, `osmnx` provides handy functions for adding travel times to the graph: the `ox.routing.add_edge_speeds()` function fills in the missing speed limits with the average speed limit of the streets in the same road class, and the `ox.routing.add_edge_travel_times()` function calculates the travel time in seconds for each edge using the same formula that we used earlier:

```python
G_large = ox.routing.add_edge_speeds(G_large)
G_large = ox.routing.add_edge_travel_times(G_large)
```

Now the edges of our graph have information about the speed in km/h (`speed_kph`) and the travel time in seconds (`travel_time`). Let's use the graph to find the fastest route by car from our origin location to Helsinki Airport, which is located in Vantaa about 16 kilometers north of the city centre. This trip would not have been possible with the network that we used earlier, because it covered only the city centre. We find the nearest nodes and the fastest route in the same way as earlier, using the coordinates of the airport terminal as the destination:

```python
airport_x, airport_y = 24.9645, 60.3165

orig_node_large = ox.distance.nearest_nodes(G_large, X=orig_x, Y=orig_y)
airport_node = ox.distance.nearest_nodes(G_large, X=airport_x, Y=airport_y)

route_large = nx.dijkstra_path(
    G_large, source=orig_node_large, target=airport_node, weight="travel_time"
)

fig, ax = ox.plot_graph_route(
    G_large,
    route_large,
    edge_linewidth=0.2,
    node_size=0,
    bgcolor="white",
    edge_color="black",
    figsize=(14, 10),
)
```

_**Figure 8.X.** The fastest route by car from the origin to Helsinki Airport, based on a street network read from a PBF file with `pyrosm`._


Figure 8.X shows the street network that we read with `pyrosm` together with the fastest route to the airport. Finally, let's summarize the route in the same way as earlier by calculating the total length (in meters) and travel time (in seconds) of the trip:

```python
route_large_edges = ox.routing.route_to_gdf(G_large, route_large, weight="travel_time")
route_large_edges[["length", "travel_time"]].sum()
```

As we can see, the fastest route to the airport is about 20 kilometers long and the trip takes around 21 minutes by car, assuming that we can drive according to the speed limits. The same steps work also for much larger areas. For example, `get_data_by_geocoding("Finland")` downloads the OpenStreetMap data for the whole of Finland (a file of about 700 MB), from which you can build a graph for the whole country in the same way as above. Reading data for a whole country naturally requires more memory and time. If you only need a part of the data, you can pass a bounding box to the `OSM` reader with the `bounding_box` parameter as a list of coordinates in the order `[min_lon, min_lat, max_lon, max_lat]` (e.g. `OSM(fp, bounding_box=[24.8, 60.1, 25.1, 60.3])`), in which case `pyrosm` keeps only the data within the given area.


In this section, we learned how to retrieve a street network from OpenStreetMap, prepare it for routing by calculating travel times for the streets, and use it for finding the shortest paths between locations. However, routing is only one of the many things that we can do with networks. In the next three sections, we will look at other common network operations: identifying the connected components of a network, checking and cleaning its topology, and measuring the centrality of its nodes and edges.


## Footnotes

[^networkx]: <https://networkx.org/documentation/stable/>
[^dijkstra]: <https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.single_source_dijkstra.html>
[^astar]: <https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html>
[^osmnx]: <https://osmnx.readthedocs.io/en/stable/>
[^pyrosm]: <https://pyrosm.readthedocs.io/en/stable/>
[^ykr]: <https://www.avoindata.fi/data/fi/dataset/kaupunki-maaseutu-luokitus-ykr>
[^dijkstra_algorithm]: <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>
[^overpass]: <https://wiki.openstreetmap.org/wiki/Overpass_API>
[^pbf]: <https://wiki.openstreetmap.org/wiki/PBF_Format>
[^geofabrik]: <https://download.geofabrik.de/>
[^movisda]: <https://osm.download.movisda.io/>
[^bbbike]: <https://download.bbbike.org/osm/>

