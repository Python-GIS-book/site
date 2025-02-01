"""Data preprocessing steps"""

import geopandas as gpd
from pathlib import Path
import rioxarray as rxr
from rioxarray.merge import merge_arrays


def make_dem_mosiac(data_dir=Path("data"), lat_min=-44.8, lat_max=-41.8, lon_min=167.5, lon_max=172.5):
    """Creates a mosiac of DEM tiles."""
    # Initialize the Path
    input_folder = data_dir / "dem"
    
    # Create the DEM list
    dem_list = list(input_folder.glob(r"ALPSMLC30_S0*DSM.tif"))

    # Echo something to the screen
    print(f"Creating mosiac from {len(dem_list)} DEM tiles...")
    
    # Read the files
    dems = [rxr.open_rasterio(dem).drop_vars("band")[0] for dem in dem_list]
    
    # Merge dems into one
    south_island = merge_arrays(dems)
        
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
    clipped.rio.to_raster(data_dir / "south_island_nz.tif")

    return None


def convert_fault_to_gpkg(data_dir=Path("data")):
    """Converts Alpine Fault shapefile to a geopackage."""
    # Read in fault shapefile
    input_fp = data_dir / "shp"/ "NZAFD_250K_Feb_2025_WGS84.shp"
    data = gpd.read_file(input_fp)

    # Echo info to the screen
    print(f"Converting {input_fp} to geopackage...")

    # Create a output path for the data
    output_fp = data_dir / "alpine_fault.gpkg"

    # Write the file
    data.to_file(output_fp)

    return None