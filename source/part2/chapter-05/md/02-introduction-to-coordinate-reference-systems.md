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

# Coordinate reference systems


## Georeferencing

Majority of all the information in the world can be traced to a specific location {cite}`Hahmann_2013`. This process of attaching information about a location to a piece of information is commonly referred as {term}`georeferencing` or {term}`geocoding`. There are various commonly used systems for georeferencing that represent the data at different positional accuracy {cite}`Longley_2015`, such as place names (varying accuracy),  postal codes (accuracy at areal level), postal addresses (accuracy at door/mailbox level), or latitude and longitude coordinates (up to millimeter level accuracy) to mention a few. In this book, we will do a bit of georeferencing by learning how to convert addresses into coordinates (and vice versa), which is a common operation to do when working with data that is not directly delivered in geospatial format. 

Being able to position oneself on Earth (and in the universe) has been an important task for humans for hundreds (or thousands) of years. The most spatially accurate information about the location of a specific object can be obtained by using positioning with geodetic method. Geodesy is the science that focuses on accurately measuring and understanding different properties of the Earth, such as its shape, orientation in space and gravity. Hence, geodesy is a fundamental field of science that enables us to locate ourselves, and use e.g. various location based services (such as navigation) and do spatial analysis with GIS in a meaningful manner. 


## Map projection - Representing curved surface in two dimensions

Previously, you learned how geographic data can be represented on a computer as vector, raster or network data. However, we didn't yet touch upon one fundamental aspect to geographic data: coordinate reference system (CRS). A coordinate reference system is important because without the CRS, the geographic data is simply a collection of coordinates in an arbitrary space. A CRS tells the GIS tools how the coordinates or geometries are related to the places on Earth. In addition, the coordinate reference system determines how we draw the geometries representing earth's curved surface on a two-dimensional plane. This process is called *{term}`map projection`*, which is a mathematical method to map the coordinates of a location (latitude and longitude) onto a flat surface, i.e. on a map {cite}`Vermeer2019`. As it happens, transforming data from 3D to 2D is not a very straightforward process, and when we use a map projection the output will always be distorted in some way or another (Figure 5.9). 

![_**Figure 5.9**. When representing the curved surface of the Earth in 2D space, the output will always be somehow distorted. Modified after Vermeer (2019)._
](../img/curved_surface_to_flat_plane.png)

_**Figure 5.9**. When representing the curved surface of the Earth in 2D space, the output will always be somehow distorted. Modified after {cite}`Vermeer2019`._


When using map projections, we always make approximations and hence lose something. There are no projections that would not distort anything or have the same scale throughout the map. Hence, a projection needs to be chosen according to the purpose of use, in order to preserve specific aspects of the map that are the most important to the user. These can be for example the shapes of objects, their surface areas, correct distances between locations, or the compass direction {cite}`Vermeer2019`.
- If we want to preserve angles and ratios of distances, we speak of a conformal, or angle-preserving projections (such as Mercator projection). These kind of projections has historically been important e.g. for ship navigation. With conformal map projection, both the distances and surface areas are distorted, except at some special points of the map.
- If we want to preserve correct area measure, we speak of an equivalent or equal-area projection (such as Mollweide or Albers equal area). Here, the angles and shapes are distorted, again with the exception of special points or lines. 
- If we want to preserve correct distances, we speak of an equidistant projection (such as Azimuthal equidistant). A projection can be equidistant only for a certain point (i.e. it is centered to specific location) or along certain lines, never everywhere. 



Figure 5.10 illustrates nine different map projections, where the latitude and longitude coordinates representing the land areas of the earth have been systematically transformated into a plain surface. As you can see, there are numerous ways to represent the world in "flattened" state, and all the projections have their unique characteristics, strengths and weaknesses. In other words, there is no perfect or "correct" projection (but they are still useful), and one needs to choose a projection depending on what is the purpose of the map and the best one for your needs. Choosing an appropriate projection for your map is not always straightforward because it depends on what you actually want to represent with your map, and what is the spatial scale of your data.


![_**Figure 5.10**. Different map projections that can be used to represent the geographic data on a two-dimensional plane._](../img/projections.jpg)
_**Figure 5.10**. Different map projections that can be used to represent the geographic data on a two-dimensional plane._


## Describing Coordinate Reference Systems

PROJ system.

A good way to understand the way how map projection works, is the "orange peel analogy". You can imagine that the Earth is a citrus fruit which you are peeling. A datum is the fruit that you choose to peal (orange, satsuma, grapefruit, lemon), and they all have a bit different shape and size. The map projection then is the approach you choose to peel the fruit and make it flat. 

![_**Figure 5.11**. Representing the process of map projection with an orange._
](../img/orange_peel_analogy.png)

_**Figure 5.11**. Representing the process of map projection with an orange ([Source](http://profdrikageografia.blogspot.com/2010_12_01_archive.html))._

```python

```
