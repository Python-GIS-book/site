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
# Motivation

Now that you are familiar with the basics of Python programming and data analysis using `pandas` library, it is time to apply those skills to geographic data analysis. In this part of the book, you will learn how to deal with spatial data and analyze it using Python and various libraries that have been developed for geographic data and tasks related to geographic information systems (GIS). 
<!-- #endregion -->

## Why to use Python for geographic data analysis?

Python is an extremely useful language to learn if you are interested in geographic data analysis (often referred to as GIS-analysis or simply GIS). Many (if not most) of the various GIS software (such as ArcGIS, QGIS, PostGIS etc.) provide an interface to do analysis using Python scripting. In this book, we will focus on doing geoprocessing and geographic data analysis without any third party software, such as ESRI's ArcGIS. Why? There are several reasons for doing GIS using Python without any additional software:

- **Python has an extensive ecosystem of libraries and tools for GIS**: you can do almost anything with spatial data. In fact, there is an enormous geospatial industry who are heavily relying on open source Python libraries.
- **Python GIS libraries are easy to learn**: there are tons of good and free resources available to learn GIS with Python for free (the online version of this book is one example!).
- **Python is highly efficient**: used for analysing big (and small) geospatial data.
- **Python is highly flexible**: supports hundreds of spatial data formats (most likely many which you, or us, have never heard of).
- **Python allows to mix and match various libraries**: You can combine different libraries and methodological approaches together and create sophisticated analytical pipelines. 
- **Everything is free**: you don’t need to buy a license for using the tools.
- **You will learn and understand more deeply** how different geoprocessing operations work.
- By using Python's open source libraries and codes, **you support open science** by making it possible for everyone to reproduce your work, free-of-charge.
- **You can plug-in and chain different third-party software** (not necessarily written in Python) which allow you to build e.g. fancy web-GIS applications (using e.g. KeplerGL, Dask or GeoDjango for developing the user interface and having PostGIS as a back-end database).
- **Python libraries are developing fast**: an active open source community is continuously improving existing libraries and adding new functionalities to them, or creating new libraries for purposes that do not yet have an existing tool to work with. However, it is good to be aware that fast development is not necessarily a guarantee of stability or quality. Hence, as for any open source library (with any programming language), it is good to investigate a bit before starting to use a new open source library whether it has been actively maintained and if it seems to have an active community of users developing the library further. 

<!-- #region editable=true slideshow={"slide_type": ""} -->
## Core libraries for geographic data analysis in Python

We have already used a few Python modules for conducting different tasks, such as `pandas` for doing some basic data analysis tasks or `matplotlib` for visualizing our data. From now on, we will familiarize ourselves with a bunch of other Python modules that are useful for geographic data analysis. Python has a large ecosystem of libraries that can be used for doing analysis, visualization or geocomputation with spatial data, as shown in Figure 5.1 which shows how different Python geo-oriented libraries (n=145) are linked to each other. There is a dedicated website at ecosystem.pythongis.org [^ecosystem] that lists and provides useful information for a large set of tools available for doing GIS and Earth Observation (remote sensing) in Python. Naturally, we won't use all of these packages in this book, but we will explore kind many of them. Although the ecosystem is broad, there are a few core libraries that are widely used across the ecosystem:

- Core vector libraries: `geopandas`, `pyproj`, `shapely`
- Core raster libraries: `xarray`, `rioxarray`, `rasterio`

![_**Figure 5.1**. Python ecosystem for GIS and Earth Observation ({cite}`Tenkanen_2022`)._](../img/python-gis-ecosystem.png)

_**Figure 5.1**. Python ecosystem for GIS and Earth Observation ({cite}`Tenkanen_2022`)._
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
One drawback of such a broad open source ecosystem compared to using a specific GIS software such as ArcGIS, is that open source tools and their documentation are spread under different Python modules and created by different developers. This means that when working you need to familiarize yourself with many different tools and their  documentation, whereas in ArcGIS everything is packaged under a same module called arcpy and all the documentation can be found from a single location. However, open source libraries have many other benefits as described earlier.
<!-- #endregion -->

## Footnotes

[^ecosystem]: <https://ecosystem.pythongis.org/>
