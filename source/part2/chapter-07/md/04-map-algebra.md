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

# Map algebra

- Basic calculations
- Reclassify
- Focal function
- Local function
- Zonal function (zonal statistics)

**To be updated**

Conducting calculations between bands or raster is another common GIS task. Here, we will be calculating `NDVI` (Normalized difference vegetation index) based on the Landsat dataset that we have downloaded from Helsinki region. Conducting calculations with rasterio is fairly straightforward if the extent etc. matches because the values of the rasters are stored as `numpy` arrays (similar to the columns stored in Geo/Pandas, i.e. `Series`).


## Reclassify

To be added. 


## Local functions

To be added. 


## Focal functions

A focal function operates on a cell and its neighboring cells within a defined window (e.g., 3x3 or 5x5). The output value for each cell is derived by applying a mathematical or statistical operation to the values within that neighborhood.

### Focal mean

### Focal majority

### Focal range


### Slope

### Aspect

### Curvature

### Hillshade


## Global functions

In map algebra, global functions are operations where the output value of each cell depends on the entire dataset or a large spatial extent, not just local neighbors. These functions are used to analyze patterns, relationships, and spatial influences across the whole raster. They are essential for modeling cumulative effects, spatial dependencies, and large-scale patterns in fields like hydrology, transportation, and environmental science.

- Statistical summaries: global mean, max, min etc.
- Viewshed analysis
- Cost distance and least-cost path
- Proximity (distance, allocation, direction)


## Zonal functions

To be added. 


## Incremental functions

To be added. 

```python
a = slice(0, 2)
```

```python
b = "Testing"
```

```python
b[a]
```

```python

```
