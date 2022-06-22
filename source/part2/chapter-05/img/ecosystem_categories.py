# Packages that require installing desktop software,
# such as database (Postgres/GIS) or GIS software (QGIS, ArcGIS etc.) are not included.

# Categories
categories = {
    "core / data structures": {
        "generic": ["pyproj", "pycrs", "pyepsg", "fiona", "numpy", "scipy", "rtree", "pandas", "networkx",
                    "python-igraph", "dask", "vaex", "geoalchemy2", "cudf", "zarr", "pyarrow", "GDAL", "PROJ"],
        "vector": ["geopandas", "shapely", "pygeos", "libpysal", "geojson", "dask-geopandas", "laspy", "pdal", "pyshp",
                   "geographiclib", "geos", "cuspatial"],
        "raster": ["rasterio", "xarray", "rioxarray", "pyogrio", "pyrat", "sarsen", "iris", "simpleitk", "sarpy",
                   "geowombat", "rio-cogeo"],
    },
    "visualization": {
        "generic": ["matplotlib", "seaborn", "bokeh", "folium", "plotly", "cartopy", "holoviews",
                    "hvplot", "geoviews", "datashader", "mapclassify", "keplergl",
                    "earthpy", "geemap", "eomaps", "pyvista", "leafmap", "gempy", "voila",
                    "pydeck", "proplot"],
        "vector": ["legendgram", "geoplot", "vizent"],
        "raster": ["xarray_leaflet", "contextily"],
    },
    "analysis / modelling": {
        "generic": ["obspy"],
        "vector": ["pysal", "spglm", "inequality", "movingpandas", "segregation", "mesa", "mesa-geo",
                   "splot", "pyinterpolate", "spint", "pointpats", "geosnap", "r5py", "giddy",
                   "spaghetti", "spreg", "pandana", "urbanaccess", "access", "mgwr", "esda", "tobler",
                   "spvcm", "spopt", "momepy", "transbigdata", "scikit-mobility", ],
        "raster": ["rasterstats", "pykrige", "scikit-learn", "xarray-spatial", "pyspatialml", "spyndex", "richdem",
                   "gstools"],
    },
    "data extraction / processing": {
        "generic": ["owslib", "geocube", "whitebox"],
        "vector": ["osmnx", "pyrosm", "osmnet", "geopy", "h3", "snkit", "pyntcloud", "lidar"],
        "raster": ["xyzservices", "eemont", "pyrosar", "scikit-image", "sentinelsat", "xarray-sentinel", "pyotb",
                   "stackstac", "earthengine-api", "satpy", "radiant-mlhub", "pystac", "easystac",
                   "planetary-computer", "odc-stac", "salem", "pystac-client"],
    }
}

# Combine all packages
core = "core / data structures"
categories[core]["pkgs"] = categories[core]["generic"] + categories[core]["vector"] + categories[core]["raster"]

processing = "data extraction / processing"
categories[processing]["pkgs"] = categories[processing]["generic"] + categories[processing]["vector"] + \
                                 categories[processing]["raster"]

analysis = "analysis / modelling"
categories[analysis]["pkgs"] = categories[analysis]["generic"] + categories[analysis]["vector"] + \
                               categories[analysis]["raster"]
viz = "visualization"
categories[viz]["pkgs"] = categories[viz]["generic"] + categories[viz]["vector"] + categories[viz]["raster"]

# Libraries with no distro
no_distro = ["pyrat", "geowombat"]

# Libraries that which do not seem to be actively maintained
generic_core = ["numpy", "scipy", "pandas", "scikit-learn", "dask", "networkx", "pyarrow", "h5py", "vaex", "cudf", "python-igraph"]
fundamental_core = ["numpy"]
generic_visuals = ["matplotlib", "seaborn", "holoviews", "pydeck"]
pygis_core = ["fiona", "pyproj", "shapely", "rtree", "rasterio", "xarray", "geopandas", "pysal"]
gis_core = ["GDAL", "GEOS", "PROJ"]

# Libraries that which do not seem to be actively maintained
not_active = ["pyrat", "vizent"]

# Libraries in their early development
early_dev = ["r5py", "easystack"]

# External or generic "language-independent" libraries (bindings for Python)
external = ["GDAL", "GEOS", "simpleitk", "PDAL", "whitebox", "pyarrow"]
