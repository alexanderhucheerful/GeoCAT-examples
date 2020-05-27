
"""
NCL_proj_3_lg.py
================

This script illustrates the following concepts:
   - Drawing filled contours over an orthographic map
   - Changing the center latitude and longitude for an orthographic projection
   - Turning off map fill

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/proj_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/proj_3_lg.png
"""
###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
t = ds.TS.isel(time=0)

###############################################################################
# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_t = gvutil.xr_add_cyclic_longitudes(t, "lon")

###############################################################################
#Plot:
fig = plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
ax = plt.axes(projection=ccrs.Orthographic(-120, 50))

# Set extent to include latitudes between 0 and 90, and longitude between
# 0 and -180 only
ax.set_extent([0, -180, 0, 90], ccrs.PlateCarree())
ax.set_global()
ax.coastlines(linewidths=0.5)

# Import an NCL colormap
newcmp = gvcmaps.gui_default

# Contourf-plot data (for filled contours)
wrap_t.plot.contourf(
    ax=ax,
    transform=ccrs.PlateCarree(),
    levels=12,
    cmap='inferno',
    cbar_kwargs={
        "orientation": "horizontal",
        "ticks": np.linspace(
            210,
            310,
            11),
        "label": '',
        "shrink": 0.9})

# Contour-plot data (for borderlines)
wrap_t.plot.contour(ax=ax, transform=ccrs.PlateCarree(),
                    levels=12, linewidths=0.5, cmap='k')

# Use geocat.viz.util convenience function to add titles to left and right
# of the plot axis.
gvutil.set_titles_and_labels(ax, maintitle="Example of Orthogonal Projection",
                             lefttitle="Surface Temperature", righttitle="K")

# Show the plot
plt.show()
