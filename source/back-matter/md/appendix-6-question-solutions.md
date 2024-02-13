---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.15.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} -->
# Solutions to questions
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Chapter 2

### Question 2.1

```python
math.sin(math.pi)
```

### Question 2.2

```python
my_variable = "Python is cool!"
my_variable
```

### Question 2.3

```python
# Solutions may vary
first_variable = "Python"
second_variable = " is cool!"

print(first_variable + second_variable)  # Works
print(5 * first_variable)                # Works
print(first_variable - second_variable)  # Fails
```

### Question 2.4

```python
'kitten'
```

### Question 2.5

```python
132334.96
```

### Question 2.6

```python
'Helsinki Kaivopuisto132310'
```

### Question 2.7

```python
for i in range(2, 9, 3):
    print(i)
```

### Question 2.8

```bash
11
7
11
15
11
```

### Question 2.9

```python
weather = "rain"

if weather == "rain":
    print("Wear a raincoat")
    print("Wear rain boots")
else:
    print("No rainwear needed")
```

### Question 2.10

```python
'B'
```

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

2.12
```python
def celsius_to_newton(temp_celsius):
    return temp_celsius * 0.33
```
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Chapter 3

3.1
```python
len(data.columns)
```

3.2
```python
data["TEMP_KELVIN"] = data["TEMP_CELSIUS"] + 273.15
```

3.3
```python
data.loc[23:29, "TEMP_CELSIUS"].mean()
```

3.4
```python
data["TEMP_CELSIUS"].loc[data["YEARMODA"] >= 20160624].mean()
```

3.5
```python
data["MONTH"] = data["TIME_STR"].str.slice(start=4, stop=6)
```
<!-- #endregion -->

<!-- #region -->
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

<!-- #region -->
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
<!-- #endregion -->
