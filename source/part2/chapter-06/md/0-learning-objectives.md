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

<!-- #region editable=true slideshow={"slide_type": ""} tags=["learning_objectives"] -->
# Learning objectives
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Chapter six provides an overview of vector data processing in Python. Basic knowledge of the pandas library for tabular data that was introduced in Part I is a prerequisite for learning to use geopandas for spatial data analysis in this section.

This chapter introduces how geographic objects can be represented and manipulated in Python, and provides an overview of coordinate reference systems, common geometric operations, spatial queries and other spatial analysis processes such as geocoding, nearest neighbor analysis, and geographic overlay analysis. 


<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["lo_box"] -->
```{admonition} Learning objectives
:class: tip

At the end of this chapter, you should be able to:

- Represent geographic vector objects in Python using the shapely library
- Understand the basic data structures and methods of geopandas GeoDataFrames
- Execute common geometric operations with points, lines and polygons
- Understand what coordinate reference systems (CRS) are
- Define and reproject the CRS of a spatial dataset
- Geocode addresses to coordinates using Python
- Perform spatial queries and spatial join operations
- Conduct nearest neighbor analysis
- Perform various geographic overlay analysis

```
<!-- #endregion -->
