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
<!-- #endregion -->

```python

```
