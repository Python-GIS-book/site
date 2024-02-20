Overview
========

Examples in this book are based on real data from different data providers.
This section contains data files, download instructions and relevant metadata (add "metadata" to glossary!)
for all input data used in this book.

This section is under construction.

Data sets
----------

Preliminary list of data sets used in this book (data set name / Source):

- Weather observation data / NOAA
- Helsinki Region Travel Time Matrix / Digital Geography Lab, University of Helsinki
- Administrative areas
    - global / Natural Earth or GADM?
    - Finland / Statistics Finland
- OpenStreetMap
- Landsat / U.S. Geological Survey


Population_grid_2021_HSY.gpkg
-----------------------------

The population grid dataset covers population statistics in a 250x250 meter polygon grid layer. The data is produced by the Helsinki Region Environmental Services Authority (HSY). The original data contains following attributes: id, index, asukkaita, asvaljyys, ika0_9, ika10_19, ika20_29, ika30_39, ika40_49, ika50_59, ika60_69, ika70_79, ika_yli80, geometry. 

For the purpose of the book, the data was minimized and translated into English. The ``Population_grid_2021_HSY.gpkg`` contains following attributes:

- ``"id"`` - unique id for the grid cell
- ``"inhabitants"`` - Number of inhabitants (orig column: *asukkaita*)
- ``"occupancy_rate"`` - Occupancy rate % (orig column: *asvaljyys*)