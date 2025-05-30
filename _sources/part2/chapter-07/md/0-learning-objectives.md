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

<!-- #region editable=true slideshow={"slide_type": ""} tags=["learning_objectives"] -->
# Learning objectives
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Chapter 7 provides an overview of raster data processing in Python. You will learn how raster surfaces can be represented and manipulated in Python, how coordinate reference system for a given raster layer can be defined and modified, and learn how to conduct common geocomputational techniques with raster data, such as clipping, masking, merging or reprojecting raster datasets or conducting map algebraic operations between one or multiple raster layers or between raster and vector layers.

Basic knowledge of raster data and arrays introduced in Chapter 5.2 as well as knowing how the data structures work in `pandas` (Chapter 3) and `geopandas` (Chapter 6) are recommended for learning efficiently how to use `xarray` and related libraries to work with raster data in Python.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["lo_box"] -->
```{admonition} Learning objectives
:class: tip

At the end of this chapter, you should be able to:

- Represent raster data in Python using the `numpy` arrays
- Understand the basic data structures and methods of `xarray` (`Dataset` and `DataArray`)
- Execute common raster operations on a single or between multiple raster datasets (select, clip, mask, resample, merge, rasterize, etc.)
- Define and reproject the coordinate reference system of a raster 
- Understand and perform various mathematical operations using map algebra: focal operations, local operations, global operations, zonal operations and incremental operations

```
<!-- #endregion -->
