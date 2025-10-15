"""Data preprocessing steps"""

import geopandas as gpd
import numpy as np
from pathlib import Path
from rioxarray.merge import merge_datasets
import xarray as xr


def make_dem_mosiac(
    data_dir="data",
    lat_min=-44.8,
    lat_max=-41.8,
    lon_min=167.5,
    lon_max=172.5,
    mask_nodata=False,
):
    """Creates a mosiac of DEM tiles."""
    # Initialize the Path
    data_dir = Path(data_dir)
    input_folder = data_dir / "dem"

    # Create the DEM list
    dem_list = list(input_folder.glob(r"ALPSMLC30_S0*DSM.tif"))

    if mask_nodata:
        # Create the MSK list
        msk_list = list(input_folder.glob(r"ALPSMLC30_S0*MSK.tif"))

    # Echo something to the screen
    print(f"Creating mosiac from {len(dem_list)} DEM tiles...")

    # Read the files
    dems = [
        xr.open_dataset(dem, engine="rasterio", band_as_variable=True)
        for dem in dem_list
    ]
    if mask_nodata:
        msks = [
            xr.open_dataset(msk, engine="rasterio", band_as_variable=True)
            for msk in msk_list
        ]

    # Merge raster tiles into one
    if mask_nodata:
        south_island_dem = merge_datasets(dems, nodata=np.nan)
        south_island_msk = merge_datasets(msks, nodata=np.nan)
    else:
        south_island = merge_datasets(dems)

    # Mask out cloud/snow, land water/low correlation, and sea areas from dem (if requested)
    if mask_nodata:
        south_island = south_island_dem.where(
            (south_island_msk["band_1"].data != 1)
            & (south_island_msk["band_1"].data != 2)
            & (south_island_msk["band_1"].data != 3)
        )

    # Rename band_1 as elevation
    south_island = south_island.rename({"band_1": "elevation"})

    # Define clipping box bounds
    geometries = [
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [lon_min, lat_min],
                    [lon_min, lat_max],
                    [lon_max, lat_max],
                    [lon_max, lat_min],
                    [lon_min, lat_min],
                ]
            ],
        }
    ]
    clipped = south_island.rio.clip(geometries)

    # Write output to tif file
    outfile = "south_island_nz"
    if mask_nodata:
        outfile += "_masked_nodata"
    outfile += ".tif"
    clipped.rio.to_raster(data_dir / outfile)

    return None


def convert_fault_to_gpkg(data_dir=Path("data")):
    """Converts Alpine Fault shapefile to a geopackage."""
    # Read in fault shapefile
    input_fp = data_dir / "shp" / "NZAFD_250K_Feb_2025_WGS84.shp"
    data = gpd.read_file(input_fp)

    # Echo info to the screen
    print(f"Converting {input_fp} to geopackage...")

    # Create a output path for the data
    output_fp = data_dir / "alpine_fault.gpkg"

    # Write the file
    data.to_file(output_fp)

    return None
