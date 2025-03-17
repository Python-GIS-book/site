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

<!-- #region editable=true slideshow={"slide_type": ""} -->
# B.1 Question solutions
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Chapter 2
<!-- #endregion -->

<!-- #region -->
### Question 2.1

```python
math.sin(math.pi)
```
<!-- #endregion -->

<!-- #region -->
### Question 2.2

```python
my_variable = "Python is cool!"
my_variable
```
<!-- #endregion -->

<!-- #region -->
### Question 2.3

```python
# Solutions may vary
first_variable = "Python"
second_variable = " is cool!"

print(first_variable + second_variable)  # Works
print(5 * first_variable)                # Works
print(first_variable - second_variable)  # Fails
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Question 2.4

```python
82.0
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Question 2.5

```python
ValueError
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Question 2.6

```python
'kitten'
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Question 2.7

```python
for i in range(2, 9, 3):
    print(i)
```
<!-- #endregion -->

<!-- #region -->
### Question 2.8

```bash
11
7
11
15
11
```
<!-- #endregion -->

<!-- #region -->
### Question 2.9

```python
weather = "rain"

if weather == "rain":
    print("Wear a raincoat")
    print("Wear rain boots")
else:
    print("No rainwear needed")
```
<!-- #endregion -->

<!-- #region -->
### Question 2.10

```python
'B'
```
<!-- #endregion -->

<!-- #region -->
### Question 2.11

```python
weather = "rain"
wind_speed = 14
comfort_limit = 10

# If it is windy or raining, print "stay at home",
# otherwise (else) print "go out and enjoy the weather!"
if (weather == "rain") or (wind_speed >= comfort_limit):
    print("Just stay at home")
else:
    print("Go out and enjoy the weather! :)")
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
### Question 2.12
```python
def celsius_to_newton(temp_celsius):
    return temp_celsius * 0.33
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Chapter 3
<!-- #endregion -->

<!-- #region -->
### Question 3.1
```python
temp_data = pd.read_csv(
    "data/kumpula-summer-2024.txt", skiprows=8, usecols=["YEARMODA", "TEMP1"]
)
```
<!-- #endregion -->

<!-- #region -->
### Question 3.2
```python
len(data.columns)
```
<!-- #endregion -->

<!-- #region -->
### Question 3.3
```python
data[["TEMP1", "TEMP2", "MAX", "MIN"]].describe()
```
<!-- #endregion -->

<!-- #region -->
### Question 3.4
```python
data["TEMP_KELVIN"] = data["TEMP"] + 273.15
```
<!-- #endregion -->

<!-- #region -->
### Question 3.5
```python
data.loc[85:91, "TEMP"].mean()
```
<!-- #endregion -->

<!-- #region -->
### Question 3.6
```python
data["TEMP"].loc[data["YEARMODA"] >= 20240825].mean()
```
<!-- #endregion -->

<!-- #region -->
### Question 3.7
```python
data["MONTH"] = data["DATE_STR"].str.slice(start=4, stop=6)
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Chapter 4

4.1
```python
# Define dates
start_time = pd.to_datetime("201910011800")
end_time = pd.to_datetime("201910020000")
warm_time = pd.to_datetime("201910012055")

# Adjust axis limits
ax = oct1_temps.plot(
    style="k--",
    title="Helsinki-Vantaa temperatures",
    xlabel="Date",
    ylabel="Temperature [°F]",
    xlim=[start_time, end_time],
    ylim=[35.0, 44.0],
    label="Observed temperature",
    figsize=(12, 6),
)

# Add plot text
ax.text(warm_time, 43.0, "Warmest temperature in the evening ->")
ax.legend(loc=4)
```

4.2
```python
len(data.dropna())
```

4.3
```python
# Create the new figure and subplots
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

# Rename the axes for ease of use
ax1 = axs[0]
ax2 = axs[1]

# Set plot line width
line_width = 1.5

# Plot data
winter_temps.plot(
    ax=ax1,
    c="blue",
    lw=line_width,
    ylim=[min_temp, max_temp],
    xlabel="Date",
    ylabel="Temperature [°C]",
    grid=True,
)
summer_temps.plot(
    ax=ax2,
    c="green",
    lw=line_width,
    ylim=[min_temp, max_temp],
    xlabel="Date",
    grid=True,
)

# Set figure title
fig.suptitle(
    "2012-2013 Winter and summer temperature observations - Helsinki-Vantaa airport"
)

# Rotate the x-axis labels so they don't overlap
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=20)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=20)

# Season label text
ax1.text(pd.to_datetime("20130215"), -25, "Winter")
ax2.text(pd.to_datetime("20130815"), -25, "Summer")
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Chapter 6

6.1

```python

# Triangle
Polygon([(0, 0), (2, 4), (4, 0)])

# Square
Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])

# Circle (using a buffer around a point)
point = Point((0, 0))
point.buffer(1)

```

6.2

```python

print("Number of rows", len(data["CLASS"]))
print("Number of classes", data["CLASS"].nunique())
print("Number of groups", data["GROUP"].nunique())

```


6.3

```python

# Calculate population density
data["pop_density_km2"] = data["pop2019"] / data["area_km2"]

# Print out average and maximum values
print("Average:", 
      round(data["pop_density_km2"].mean()), "pop/km2")

print("Maximum:", 
      round(data["pop_density_km2"].max()), "pop/km2")

```

6.4

```python

# Save to file
temp = gpd.read_file(output_fp)

# Check first rows
temp.head()

# You can also plot the data for a visual check
temp.plot()

```

6.5

```python
# Plot the admin borders as background
ax1 = data.plot(color="grey")

# Plot the buffer zone of dense areas on top
dissolved.loc[dissolved["dense"]==1].buffer(500).plot(ax=ax1, 
                                                      alpha=0.5, 
                                                      color="yellow")
```

6.6

```python
# Select Finland and reproject
finland_wgs84 = data_wgs84.loc[data_wgs84["NAME_ENGL"]=="Finland"].copy()
finland_etrs89 = finland_wgs84.to_crs(epsg=3067)

# Make subplots that are next to each other
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(1, 1))

# Plot the data in WGS84 CRS
finland_wgs84.plot(ax=ax1, facecolor="gray")

# Plot the one with ETRS-LAEA projection
finland_etrs89.plot(ax=ax2, facecolor="blue", edgecolor="white", lw=0.5)

# Add titles
ax1.set_title("WGS84")
ax2.set_title("ETRS89 / TM35FIN")

# Set aspect ratio as 1
ax1.set_aspect(aspect=1)
ax2.set_aspect(aspect=1)

# Remove empty white space around the plot
plt.tight_layout()
```

6.7

```python

# Example list of addresses
adress_list = ["Pietari Kalmin katu 5, Helsinki, Finland", 
               "Konetekniikka 1, Espoo, Finland"]

# Do the geocoding
geo = geocode(
    adress_list, provider="nominatim", user_agent="pythongis_book", timeout=10
)

# Check if the result looks correct on a map
geo.explore()
```

6.8

```python
print("Line a is equal to line b: ", line_a.equals(line_b))
```

6.9
```python
# Check column names in the spatial join result
print(districts_with_points.columns.values)

# Group by district name
grouped = districts_with_points.groupby("Name")

# Count the number of rows (adress locations) in each district
grouped.index_right.count()
```

6.10

```python

# Join information from address points to the grid
result = pop_grid.sjoin(addresses)

# Check the structure
print(result.head(2))

# Visualize the result
result.explore()

```
How does the result differ from the version where we joined information from the grids to the points? 
- this result has polygon geometry in stead of points
- order of the columns is different
  
What would be the benefit of doing the join this way around?
- If your research question is related to the population grid, then it might make more sense to join additional information to those statistical units.
- If the point data would be somehow sensitive, joining the information to a coarser spatial unit might be meaningful


6.11

```python
#insert solution here
```

6.12

```python

# Create a 200 meter buffer
stop_buffer = stops.copy()
stop_buffer["geometry"] = stops.buffer(200)

# Find all the building points intersecting with the buffer
buffer_buildings = stop_buffer.sjoin(building_points, predicate="intersects")

# Calculate the number of buildings per stop by grouping
building_count = buffer_buildings.groupby("stop_id").stop_name.count().to_frame().reset_index()

# Now the "stop_name" column contains information about building count, rename
building_count = building_count.rename(columns={"stop_name": "building_cnt_buffer"})

# Join the information into the stops
stop_buffer = stop_buffer.merge(building_count, on="stop_id")

# As a result, we should have identical number of buildings identified per stop (see the last two columns)
stop_buffer.head()
```
<!-- #endregion -->

<!-- #region -->
## Chapter 8


8.1

```python

# Example solution:

# Create one subplot. Control figure size in here.
fig, ax = plt.subplots(figsize=(6, 4))

# Visualize the travel times using a classification scheme and add a legend
grid.plot(ax=ax,
          column="car_r_t",
          cmap="RdYlBu",
          linewidth=0,
          scheme="FisherJenks",
          k=9,
          legend=True,
          legend_kwds={"title": "Travel times (min)",
                 "bbox_to_anchor": (1.4, 1)}
         )

# Add scalebar
ax.add_artist(ScaleBar(1, location="lower right"))

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = "static_map2.png"
plt.savefig(outfp, dpi=300)
```

8.2

```python
# Example solution: 

# Control figure size in here
fig, ax = plt.subplots(figsize=(8, 5))

# Visualize the travel times using a classification scheme and add a legend
grid.plot(ax=ax,
          column="pt_r_t",
          cmap="RdYlBu",
          linewidth=0,
          scheme="user_defined",
          classification_kwds={'bins': break_values},
          k=9,
          alpha=0.5,
          legend=True,
          legend_kwds={"title": "Travel times (min)",
                       "bbox_to_anchor": (1.27, 1),
                      "frameon": False}
         )

# Set the x and y axis off and adjust padding around the subplot
plt.axis("off")
plt.tight_layout()

# Add scalebar
ax.add_artist(ScaleBar(1, location="lower right", box_alpha=0.5))

# Add basemap with basic OpenStreetMap visualization
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager, crs=grid.crs)

<!-- #endregion -->
