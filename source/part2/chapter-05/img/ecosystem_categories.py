# Categories
categories = {
    "core / data structures": {
        "generic": ["pyproj", "pycrs", "fiona", "numpy", "scipy", "rtree", "pandas", "networkx", "python-igraph",
                    "vaex", "geoalchemy2"],
        "vector": ["geopandas", "shapely", "pygeos", "libpysal", "geojson", "dask-geopandas", "laspy", "pyshp",
                   "geographiclib"],
        "raster": ["rasterio", "xarray", "rioxarray", "pyogrio", "pyrat", "sarsen"],
    },
    "visualization": {
        "pkgs": ["matplotlib", "seaborn", "bokeh", "folium", "plotly", "cartopy", "contextily", "holoviews", "hvplot",
                 "geoplot", "geoviews", "datashader", "mapclassify", "keplergl", "xarray_leaflet", "legendgram",
                 "earthpy", "geemap", "eomaps", "pyvista", "leafmap"],
    },
    "analysis / modelling": {
        "pkgs": ["pysal", "spglm", "inequality", "movingpandas", "segregation", "pyinterpolate", "mesa", "mesa-geo",
                 "splot", "rasterstats", "spint", "pointpats", "pykrige", "scikit-learn", "geosnap", "r5py", "giddy",
                 "spaghetti", "spreg", "pandana", "urbanaccess", "access", "mgwr", "xarray-spatial", "esda", "tobler",
                 "spvcm", "spopt", "scikit-mobility", "pyspatialml", "momepy", "gempy", "transbigdata", "obspy"],
    },

    "data extraction / processing": {
        "pkgs": ["owslib", "osmnx", "pyrosm", "osmnet", "geopy", "geocube", "xyzservices", "pyepsg", "eemont",
                 "pyrosar", "scikit-image", "h3", "snkit", "sentinelsat", "xarray-sentinel"],
        "radius": 10.0
    }
}

# Update all packages
core = "core / data structures"
categories[core]["pkgs"] = categories[core]["generic"] + categories[core]["vector"] + categories[core]["raster"]
