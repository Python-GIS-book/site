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

### Exercise 6.1 - Geometric objects

In this exercise your task is to create custom functions for creating geometries. We start with a very simple function, and proceed to creating functions that can handle invalid input values. In addition to the contents of chapter 6, you will need basic knowledge of creating functions (see Part I chapter 2.6) and using assertions (see Appendix).

#### Problem 1

Create a simple function called `create_point_geom()` that has two parameters (`x_coord`, `y_coord`). The function should return a `shapely` `Point`  object. Demonstrate the use of the function.

You can test your function with these code snippets: 

```
point1 = create_point_geom(0.0, 1.1)
print(point1.geom_type)
```


#### Problem 2

Create a function called `create_line_geom()` that takes a list of `shapely` `Point` objects as parameter called `points` and returns a `LineString` object based on those input points. The function should: 

- Check that the parameter `points` is a list. You can do this by using the `assert` -functionality
- If the `points` parameter is something else than a list, the function should return an Error message: `"Input should be a list!"`
- Check that the input list contains at least two values (again, using `assert`). If not, return an Error message: `"LineString object requires at least two Points!"`
- (optional) check that all values in the input list are truly `shapely` `Points`. If not, return an Error message: `"All list values should be Shapely Point objects!"`

You can test your function with these code snippets: 

```
# Demonstrate basic usage
line1 = create_line_geom([Point(45.2, 22.34), Point(100.22, -3.20)])
print(line1.geom_type)
```
```
# Check if the assertion error works correctly with false input
try:
    # Pass something else than a list
    create_line_geom(45.2, 22.34, 100.22, -3.20)
except AssertionError:
    print("Found an assertion error. List check works correctly.")
except Exception as e:
    raise e
```


#### Problem 3

Create a function called `create_poly_geom()` that has one parameter called `coords` which should contain a list of coordinate tuples. The function should create and return a `Polygon` object based on these coordinates. The function should:  

  -  Check with `assert` -functionality that the input is a list. If something else than a list is passed for the function, you should return an Error message: `"Input should be a list!"`
  - You should also check with `assert` that the input list contains at least three values. If not, return an Error message: `"Polygon object requires at least three Points!"`
  - Check the data type of the objects in the input list. All values in the input list should be tuples. If not, return an error message: "All list values should be coordinate tuples!" using assert.
  - **Optional:** Allow also an input containing a list of `shapely` `Point` objects, in which case the function should return a polygon based on these points. If the input is neither a list of tuples, nor a list of points, return an appropriate error message using `assert`.

You can test your function with these code snippets:

```
# Demonstrate basic usage
poly1 = create_poly_geom([(45.2, 22.34), (100.22, -3.20), (33.33, 0)])
print(poly1.geom_type)
```

```
# Check if the assertion error works correctly with false input
try:
    # Pass something else than a list
    create_poly_geom("Give me a polygon")
except AssertionError:
    print("List check works")
except Exception as e:
    raise e
```


#### Problem 4

Did you add a docstring to all the functions you defined? If not, add them now! A short one-line docstring is enough in this exercise.


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
