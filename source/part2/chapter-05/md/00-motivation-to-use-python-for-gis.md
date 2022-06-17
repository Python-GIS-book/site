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

# Motivation: Why to use Python for geographic data analysis?

Now that you are familiar with the basics of Python programming and data analysis using `pandas` library, it is time to apply those skills to geographic data analysis. In this part of the book, you will learn how to deal with spatial data and analyze it using Python and various libraries that have been developed for GIS-related tasks. 


Python is extremely useful language to learn if you are interested in geographic data analysis (or GIS as it is often called). Many (if not most) of the various GIS softwares (such as ArcGIS, QGIS, PostGIS etc.) provide an interface to do analysis using Python scripting. In this book, we will focus on doing geoprocessing and geographic data analysis without any third party softwares, such as ESRI's ArcGIS. Why? There are several reasons for doing GIS using Python without any additional software:

- **Python has an extensive ecosystem of libraries and tools for GIS**: you can do almost anything with spatial data. In fact, there is an enormous geospatial industry who are heavily relying on open source Python libraries.
- **Python GIS libraries are easy to learn**: There are tons of good and free resources available to learn GIS with Python for free (the online version of this book is one example!) 
- **Python is highly efficient**: used for analysing big (and small) geospatial data
- **Python is highly flexible**: supports hundreds of spatial data formats (most likely many which you, or us, have never heard of)
- **Python allows to mix and match various libraries**: You can combine different libraries and methodological approaches together and create sophisticated analytical pipelines 
- **Everything is free**: you don’t need to buy a license for using the tools
- **You will learn and understand more deeply** how different geoprocessing operations work
- By using Python's open source libraries and codes, **you support open science** by making it possible for everyone to reproduce your work, free-of-charge.
- **You can plug-in and chain different third-party softwares** (not necessarily written in Python) which allow you to build e.g. fancy web-GIS applications (using e.g. KeplerGL, Dask or GeoDjango for developing the user interface and having PostGIS as a back-end database).


## Python GIS ecosystem: Core libraries for doing GIS and geographic data analysis

We have already used a few Python modules for conducting different tasks, such as `pandas` for doing some basic data analysis tasks or `matplotlib` for visualizing our data. From now on, we will familiarize ourselves with a punch of other Python modules that are useful when for geographic data analysis or different GIS tasks. One drawback when compared to using a specific GIS-software such as ArcGIS, is that open source GIS tools for Python are spread under different Python modules and created by different developers. This means that you need to familiarize yourself with many different modules (and their documentation), whereas e.g. in ArcGIS everything is packaged under a same module called arcpy. Below we have listed most of the crucial modules (and links to their docs) that helps you get going when doing data analysis or GIS in Python. If you are interested or when you start using these modules in your own work, you should read the documentation from the web pages of the module that you need:


**ADD IMAGE** about the ecosystem and linkages


The core libraries for doing GIS and geographic data analysis in Python:

- Core vector libraries: `geopandas`, `pyproj`, `shapely`
- Core raster libraries: `xarray`, `rioxarray`, `rasterio`
- Libraries for analysis and modelling: `pysal`, `scipy.spatial`, `xarray-spatial`
- Libraries for data download and extraction: `OWSLib`, `osmnx`, `pyrosm`
