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

# Exercise solutions

<!-- #region -->
## Chapter 2

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
```
<!-- #endregion -->
