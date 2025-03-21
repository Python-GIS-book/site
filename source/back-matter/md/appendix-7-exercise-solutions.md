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

# Exercise solutions


## Chapter 2

<!-- #region -->
### Exercise 2.1

```python
# Define main variables
ice_cream_rating = 9
sleep_rating = 8
name = "Dave"

# Calculate happiness
happiness_rating = (ice_cream_rating + sleep_rating) / 2

# Print variable types
print(type(ice_cream_rating))
print(type(sleep_rating))
print(type(name))
print(type(happiness_rating))

# Print formatted text
print("My name is", name, "and I give eating ice cream a score of", ice_cream_rating, "out of 10!")
print("My sleeping enjoyment rating is", sleep_rating, "/ 10!")
print("Based on the factors above, my happiness rating is", happiness_rating, "or", happiness_rating * 10, "%!")
```
<!-- #endregion -->

<!-- #region -->
### Exercise 2.2

```python
# Define left table lists
station_names = ["lighthouse", "Harmaja", "Suomenlinna aaltopoiju", "Kumpula", "Kaisaniemi"]
station_start_years = [2003, 1989, 2016, 2005, 1844]

# Add values from table on the right
station_names.append("Malmi airfield")
station_names.append("Vuosaari harbour")
station_names.append("Kaivopuisto")
station_start_years.append(1937)
station_start_years.append(2012)
station_start_years.append(1904)

# Sort lists as directed
station_names.sort()
station_start_years.sort()
station_start_years.reverse()

# Problem: List values are no longer correctly linked for same index value
```
<!-- #endregion -->

<!-- #region -->
### Exercise 2.3

```python
# Create lists of months and temperatures
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', \
          'September', 'October', 'November', 'December']
average_temp = [-3.5, -4.5, -1.0, 4.0, 10.0, 15.0, 18.0, 16.0, 11.5, 6.0, 2.0, -1.5]

# Select month and create print statement output
selected_month_index = 6
print_statement = f"The average temperature in Helsinki in {months[selected_month_index]} is {average_temp[selected_month_index]}"

# Alternative print statement format
print_statement = 'The average temperature in Helsinki in ' + str(months[selected_month_index]) + ' is ' + str(average_temp[selected_month_index])
```
<!-- #endregion -->

<!-- #region -->
### Exercise 2.4

```python
# Create variable with file base name
basename = "Station"

# Create empty list for filenames
filenames = []

# Use for loop to populate list of filenames
for i in range(21):
    station = basename + "_" + str(i) + ".txt"
    filenames.append(station)
```
<!-- #endregion -->

<!-- #region -->
### Exercise 2.5

```python
# Store list of temperatures in memory
temperatures = [-5.4, 1.0, -1.3, -4.8, 3.9, 0.1, -4.4, 4.0, -2.2, -3.9, 4.4,
                -2.5, -4.6, 5.1, 2.1, -2.4, 1.9, -3.3, -4.8, 1.0, -0.8, -2.8,
                -0.1, -4.7, -5.6, 2.6, -2.7, -4.6, 3.4, -0.4, -0.9, 3.1, 2.4,
                1.6, 4.2, 3.5, 2.6, 3.1, 2.2, 1.8, 3.3, 1.6, 1.5, 4.7, 4.0,
                3.6, 4.9, 4.8, 5.3, 5.6, 4.1, 3.7, 7.6, 6.9, 5.1, 6.4, 3.8,
                4.0, 8.6, 4.1, 1.4, 8.9, 3.0, 1.6, 8.5, 4.7, 6.6, 8.1, 4.5,
                4.8, 11.3, 4.7, 5.2, 11.5, 6.2, 2.9, 4.3, 2.8, 2.8, 6.3, 2.6,
                -0.0, 7.3, 3.4, 4.7, 9.3, 6.4, 5.4, 7.6, 5.2]

# Create empty lists for classification
cold = []
slippery = []
comfortable = []
warm = []

# Use for loop and conditional statements to populate category lists
for temp in temperatures:
    if temp < -2:
        cold.append(temp)
    elif temp >= -2 and temp < 2:
        slippery.append(temp)
    elif temp >= 2 and temp < 15:
        comfortable.append(temp)
    elif temp >= 15:
        warm.append(temp)

# Alternative solution
# Note: Because of the test order "greater than or equal to" tests are not required
for temp in temperatures:
    if temp < -2:
        cold.append(temp)
    elif temp < 2:
        slippery.append(temp)
    elif temp < 15:
        comfortable.append(temp)
    elif temp >= 15:
        warm.append(temp)

# Print out number of times it was cold, comfortable, or warm
print(f"It was cold {len(cold)} times in Helsinki in April 2013.")
print(f"It was cold {len(comfortable)} times in Helsinki in April 2013.")
print(f"It was cold {len(warm)} times in Helsinki in April 2013.")
```
<!-- #endregion -->

<!-- #region -->
### Exercise 2.6

```python
# Create temperature conversion function
def fahr_to_celsius(temp_fahrenheit):
    """Converts Fahrenheit temperature into Celsius."""
    converted_temp = (temp_fahrenheit - 32) / 1.8
    
    return converted_temp

# Make a list of temperatures to convert and loop over them to convert
fahr_temps = [32, 68, 91, -17]
for fahr_temp in fahr_temps:
    print(f"{fahr_temp} °F is equal to {fahr_to_celsius(fahr_temp):.1f} °C.")
```
<!-- #endregion -->

<!-- #region -->
### Exercise 2.7

```python
def temp_classifier(temp_celsius):
    """
    Classifies temperatures into 4 different classes according following criteria:
    
    - Less than -2 degrees: returns 0
    - Less than +2 degrees and greater than or equal to -2 degrees: returns 1
    - Less than +15 degrees and greater than or equal to +2 degrees: returns 2
    - Greater than or equal to 15 degrees: returns 3        
    """
    if temp_celsius < -2:
        return 0
    elif temp_celsius >= -2 and temp_celsius < 2:
        return 1
    elif temp_celsius >= 2 and temp_celsius < 15:
        return 2
    else:
        return 3

# Create list of temperatures to classify and classify them
celsius_temps = [17, 2, 1.9, -2]
for celsius_temp in celsius_temps:
    print(f"The temperature {celsius_temp} °C is in category {temp_classifier(celsius_temp)}.")
```
<!-- #endregion -->

## Chapter 6

<!-- #region -->
### Exercise 6.1

```python
from shapely.geometry import Point, LineString
```
```python
#1. Line and line length (example values)
line = LineString([(0.0, 0.0), (3.0, 4.0), (1.5, 5.5)])
print("Line length:", line.length)

#Print out the variable for quick visualization
line
```
```python
#2. Point and buffer area (example values)
point = Point([3,3])
buffer = point.buffer(100)
print("Buffer area:", buffer.area)

#Print out the variable for quick visualization
buffer
```
<!-- #endregion -->

<!-- #region -->
### Exercise 6.2
```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
```
```python
# Problem 1: Read the file
fp = 'data/Helsinki/travelTimes_2015_Helsinki.txt'
data = pd.read_csv(fp, sep=';', usecols=['from_x','from_y','to_x','to_y', 'total_route_time'])
data.head()
```
```python
# Problem 2: Create geometries
data['from_geom'] = gpd.points_from_xy(data['from_x'], data['from_y'])
data['to_geom'] = gpd.points_from_xy(data['to_x'], data['to_y'])

data.head()

```
```python

# Problem 3: Create LineString geometries

# Option 1: Apply a lambda function that creates the LineString objects for each row
data['route_geom'] = data.apply(lambda x: LineString([x['from_geom'], x['to_geom']]), axis=1)

# Option 2: use zip and a for-loop
lines = []

for origin, destination in zip(data['from_geom'], data['to_geom']):
    # Create a LineString
    line = LineString([origin, destination])
    lines.append(line)
    
data['route_geom'] = lines

# Check the result
data.head()
```
```python
# Problem 4: Convert DataFrame into a GeoDataFrame. Set correct geometry column and crs.
data = gpd.GeoDataFrame(data, geometry="route_geom", crs=4326)

#Check crs name
print(data.crs.name)
```
```python
#Problem 5: Re-project the data
print("Old crs:", data.crs.name)
data = data.to_crs(epsg=3067)
print("New crs:", data.crs.name)
data.head()
```
```python
#Problem 6: Calculate average trip distance
data['route_length'] = data.length
data['route_length'].describe()
print("Median route length:", round(data['route_length'].median()), "meters.")
```
<!-- #endregion -->

### Exercise 6.3 - Buffer and spatial join

<!-- #region -->
```python
#1. Import needed modules and read in the data
import geopandas as gpd

addr_fp = "data/Helsinki/addresses.shp"
addresses = gpd.read_file(addr_fp)

pop_grid_fp = "data/Helsinki/Population_grid_2021_HSY.gpkg"
pop_grid = gpd.read_file(pop_grid_fp)
```

```python
#2. Check coordinate reference systems and re-project
print("Address points CRS:", addresses.crs.name)
print("Population grid CRS:", pop_grid.crs.name)
print("Same CRS?:", addresses.crs == pop_grid.crs)

# Re-project ot the metric CRS
addresses = addresses.to_crs(pop_grid.crs)
print("Same CRS?:", addresses.crs == pop_grid.crs)
```

```python
#3. Create a 500 meter buffer around each transit station.
addresses["geometry"] = addresses.buffer(500)
```

```python
#4. Convert the population grid geometries (polygons) into centroid points 
pop_grid["geometry"] = pop_grid.centroid
```
```python
#5. Join information about the buffer into each intersecting point
joined = gpd.sjoin(pop_grid, addresses, how="inner", predicate="intersects")
```
```python
#6. Aggregate the results for each buffer so that you get population sum per buffer
pop_per_station = joined.groupby("id").inhabitants.sum()
```
```python
# 7. Get total number of people living within 500 meters from the nearest transit station.
pop_per_station.sum()
```
<!-- #endregion -->
