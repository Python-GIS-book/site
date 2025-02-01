"""Functions for basin analysis"""

import numpy as np


def to_xarray(catchment):
    """Converts from pysheds clipped catchment elevations to xarray."""
    data = catchment.data
    lat = np.unique(catchment.coords[:, 0])
    lat = np.flip(lat)
    lon = np.unique(catchment.coords[:, 1])
    catch_xr = xr.DataArray(catchment.base, coords={"y": lat, "x": lon}, dims=["y", "x"])
    return catch_xr


def calculate_relief(elevations):
    """Calculates basin relief."""
    return elevations.max() - elevations.min()


def calculate_area(elevations, catchments_xr=None, calc_dxdy=False):
    """Calculates drainage basin area assuming 30m resolution."""
    if calc_dxdy:
        dx = abs(catch_xr.x.values[1] - catch_xr.x.values[0])
        dy = abs(catch_xr.y.values[1] - catch_xr.y.values[0])
        pixel_area = dx * dy * 111.0**2
    else:
        pixel_area = 0.03 * 0.03
    return len(elevations) * pixel_area


def calculate_hypsometry(elevations, binsize=100.0, normalize=True):
    """Calculates a cumulative elevation histogram."""
    minbin = elevations.min() - elevations.min() % +binsize
    maxbin = elevations.max() - elevations.max() % -binsize
    inbins = np.arange(minbin, maxbin+1.0, binsize)
    counts, bins = np.histogram(elevations, bins=inbins)

    # Normalize area distribution
    counts = counts.cumsum() / counts.cumsum().max()

    # Convert to area above min elevation
    counts = 1 - counts

    # Normalize elevations if requested
    if normalize:
        bins = (bins - bins.min()) / (bins.max() - bins.min())

    return counts, bins


def calculate_hypsometric_integral(counts, bins):
    """Calculates a hypsometric integral from a cumulative elevation histogram."""
    bin_width = bins[1] - bins[0]
    hyps_integral = sum(counts * bin_width)
    return hyps_integral


def continue_pysheds(file):
    """Loads a tif file from Pysheds to continue analysis."""
    grid = Grid.from_raster(file)
    data = grid.read_raster(file)
    return grid, data