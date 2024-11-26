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

<!-- #region editable=true slideshow={"slide_type": ""} tags=["learning_objectives"] -->
# Learning objectives
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Chapter six provides an overview of vector data processing in Python. You will learn how geographic objects can be represented and manipulated in Python, how coordinate reference systems can be defined and modified, and learn how to conduct common GIS techniques, such as geocoding, spatial queries, spatial join, nearest neighbor analysis and vector overlay operations. 

Basic knowledge of tabular data manipulation using the `pandas` library introduced in Part I is a prerequisite for learning to use `geopandas` for spatial data analysis in this section.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["lo_box"] -->
```{admonition} Learning objectives
:class: tip

At the end of this chapter, you should be able to:

- Represent geographic vector objects in Python using the `shapely` library
- Understand the basic data structures and methods of `geopandas` `GeoDataFrame`s
- Execute common geometric operations with points, lines and polygons
- Define and reproject the coordinate reference system of a spatial dataset
- Geocode addresses to coordinates using Python
- Perform spatial queries and spatial join operations
- Conduct nearest neighbor analysis
- Perform and understand how different vector overlay operations work

```
<!-- #endregion -->
