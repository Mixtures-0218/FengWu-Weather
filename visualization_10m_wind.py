import numpy as np
import matplotlib.pyplot as plt
import os
import xarray as xr
from cartopy import crs as ccrs, feature as cfeature
import math
from locations import region #, cities


def wind_10m_visualization(nc_file, file_name):
    lonall, latall = np.meshgrid(lon, lat)

    # Components of wind
    u10 = ds.u10[:, :]
    v10 = ds.v10[:, :]

    # Projection setup
    projPC = ccrs.PlateCarree()
    lonW = region["lonW"]
    lonE = region["lonE"]
    latS = region["latS"]
    latN = region["latN"]

    # Plotting setup
    fig = plt.figure(figsize=(11, 8.5))
    ax = plt.subplot(1, 1, 1, projection=projPC)
    ax.set_extent([lonW, lonE, latS, latN], crs=projPC)
    ax.add_feature(cfeature.STATES)
    # ax.gridlines(draw_labels=True, dms=True, color='black')
    ax.coastlines(resolution='110m', linewidth=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

    '''
    # City setup (incomplete func)
    for city in cities:
        ax.plot(city['lon'], city['lat'], 'ro', markersize=8)  # red dots are cities (only for Sichuan and Seattle area)
        ax.text(city['lon'] + 0.01, city['lat'] + 0.01, city['name'], fontsize=10, ha='left', va='bottom')
    '''

    ax.quiver(lonall[::, ::], latall[::, ::], u10[::, ::], v10[::, ::], angles='uv', scale_units='xy', scale=6, color='b')

    # Entitle
    ax.set_title('10m Wind_'+str(file_name[:-3]))

    # plt.show()
    plt.savefig((os.path.join(output_dir, str(file_name[:-3])+"_10m_wind.png"))) # save


# Read the data
path = os.path.join(os.getcwd(), "output_data")

# Select all .nc files
output_lst = []
for file in os.listdir(path):
    if file.endswith('.nc'):
        output_lst.append(file)
    else:
        print(f"Skipping directory or non-NPY file: {file}")

# Create folder for output
output_dir = os.path.join(
    os.path.join(os.getcwd(), "10m_output"),
)
os.makedirs(output_dir, exist_ok=True)

# Visualize for all nc files
for nc_file in output_lst:
    ds = xr.open_dataset(os.path.join(path, nc_file))
    lon = ds.longitude
    lat = ds.latitude
    wind_10m_visualization(ds, nc_file)