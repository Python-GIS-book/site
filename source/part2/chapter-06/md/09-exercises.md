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

# Exercises

### Exercise 6.1 - Geometric Objects

Refresh your memory about `shapely` objects and 

1. Create a `LineString` that goes trough at least three points. What is the length of your line?
2. Create a `shapely` `Point` and create a buffer around it. What is the area of the buffer?


### Exercise 6.2 - From text file to GeoDataFrame


The goal of this exercise is to create geometries based on text file input in Python. You will combine basic knowledge of the `pandas` module (see Part I) with `geopandas` methods introduced in this chapter. The text file **[travelTimes_2015_Helsinki.txt](data/travelTimes_2015_Helsinki.txt)** is located in the data folder and consist of travel times between multiple origin locations and one destination location. This file is an extract of the Helsinki Region Travel Time Matrix dataset - an open data set that contains multimodal travel time information across the Helsinki Region in Finland (ref). Here, we will focus on the public transport travel times to the Helsinki railway station. 

The first four rows of our data look like this:

```
   from_id;to_id;fromid_toid;route_number;at;from_x;from_y;to_x;to_y;total_route_time;route_time;route_distance
   5861326;5785640;5861326_5785640;1;08:10;24.9704379;60.3119173;24.8560344;60.399940599999994;125.0;99.0;22917.6
   5861326;5785641;5861326_5785641;1;08:10;24.9704379;60.3119173;24.8605682;60.4000135;123.0;102.0;23123.5
   5861326;5785642;5861326_5785642;1;08:10;24.9704379;60.3119173;24.865102;60.4000863;125.0;103.0;23241.3
```

In this exercise, we are interested in these columns:

| Column | Description |
|--------|-------------|
| from_x | x-coordinate of the **origin** location (longitude) |
| from_y | y-coordinate of the **origin** location (latitude) |
| to_x   | x-coordinate of the **destination** location (longitude)|
| to_y   | y-coordinate of the **destination** location (latitude) |
| total_route_time | Travel time with public transportation at the route |

Your task is to read in the file and create two new colums with `Point` objects representing the origin and destination points. Problems 1-3 will guide you through the necessary steps.



#### Problem 1: Read the file

- Import required modules.
- Read in the text file using `pandas` into a variable called `data` and subset the `DataFrame` to contain only those columns we are interested in
- Check that data looks ok



#### Problem 2: Create Point geometries

Continue working with the `DataFrame`:
- Create new columns `from_geom` and `to_geom`
- Populate these columns with point objects that represent the origin and destination geometries using the `points_from_xy()` function in `geopandas`:
    - `from_geom` based on columns `from_x` and `from_y`
    - `to_geom` based on columns `to_x` and `to_y`



#### Problem 3: Create LineString geometries

Continue working with the `DataFrame` and create `LineString` `shapely` objects based on the origin and destination point coordinates:

- Create new column `route_geom`
- Populate the new columns with `LineString` objects that represent a straight line between each origin (`from_geom`) and destination (`to_geom`) coordinates.

- You can achieve this at least in two different ways:
    - Option 1: Apply a lambda-function on the `DataFrame` that creates a `LineString` based on `from_geom` and `to_geom` columns for each row (`axis=1`).
    - Option 2: Use `zip()` and a `for`-loop to create the `LineString` for each coorinate pair. You can store the `LineStrings` in a list inside the loop and outside the loop insert the list into the `route_geom` column.



#### Problem 4: Convert DataFrame into a GeoDataFrame

Convert the `DataFrame` into a `GeoDataFrame`. While doing this, you should:
- Define `route_geom` as the geometry column.
- Set a coordinate reference system for the data. Think carefully what is the correct crs definition for the input coordinates.

Check the result. 


#### Problem 5: Re-project the data

Our data is located in the Helsinki Region, Finland and the data should be converted into a projected coordinate reference system if we want to draw maps or measure distances. 

- Check the crs definition of the data. 
- Re-project the data into ETRS89 / TM35FIN (EPSG:3067).
- Check the result. You should notice that the `route_geom` coordinate values have changed.


#### Problem 6: Calculate average trip distance

Now that we have the `GeoDataFrame` in a projected coordinate reference system we can calculate some distance metrics based on the line objects.

- Calculate the lenght of each route based on the `route_geom` column.
- Add the length information into a new column `route_length`.
- Generate descriptive statistics of route lengths. What is the median route length?


### Exercise 6.3 - Buffer and spatial join

In this exercise your task is to find out how many people live within a 500 meter buffer zone from the nearest transit station in Helsinki. We will re-use data from chapter six. Locations of transit stations is available in the file `data/Helsinki/addresses.shp`. Population information is available in the file `data/Helsinki/Population_grid_2021_HSY.gpkg`.

You should join the buffers with the population information based on the spatial intersection of the buffer polygons and the population grid polygon centroids. Follow these steps to achieve the wanted result:

1. Create a 500 meter buffer around each transit station
2. Convert the population grid geometries (polygons) into points based on the grid centroid
3. Codunct a spatial join where you find out which points are located within each buffer and join information about the buffer into each point
4. Aggregate the results for each buffer so that you get population sum per buffer
5. Sum up the results to get total number of people living within 500 meters from the nearest transit station.
