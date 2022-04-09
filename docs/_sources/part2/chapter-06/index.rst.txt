Vector data processing
=======================

Here we introduce basics of vector data processing.

**This chapter is under construction.**

Sub-sections:

- Intro Geographic objects in Python

- Introduction to spatial data analysis with geopandas

- Reading and writing vector data (Data I/O)

- Coordinate reference systems

- Analyzing spatial relationships

  - Spatial queries and selections
  - Neighborhood analysis - Spatial weights (linkage to Rey et al. 2020)
  - Improving performance - Spatial index

- Geometric data conversions – from form to another

  - Dissolving and merging geometries
  - Geocoding (addresses <-> points)
  - Interpolation (e.g. IDW)
  - Tesselation
  - Overlay analysis

.. toctree::
    :maxdepth: 1
    :caption: Sections:

    nb/00-geometric-objects.ipynb
    nb/01-geopandas-basics.ipynb
    nb/02-data-io.ipynb
    nb/03-projections.ipynb
    nb/04-from-text-to-map.ipynb
    nb/05-spatial-queries.ipynb
    nb/06-spatial-join.ipynb
    nb/07-nearest-neighbour.ipynb
    nb/08-spatial_index.ipynb
    nb/09-nearest-neighbor-faster.ipynb
    nb/10-geometric-operations.ipynb

