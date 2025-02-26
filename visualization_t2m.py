import numpy as np
import matplotlib.pyplot as plt
import os
import xarray as xr
from cartopy import crs as ccrs, feature as cfeature
import math
from locations import region #, cities


def temp_visualization(nc_file, file_name):
    lonall, latall = np.meshgrid(lon, lat)

    t2m = ds.t2m[:, :] - 273.15 # Convert to Celcius from Kelvin'
    
    # Contour setup
    clevs_t2m = np.arange(-60, 60, region["temp_contour"])

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
    
    # Fill color of the map
    contourf = ax.contourf(lonall, latall, t2m, levels=clevs_t2m, transform=projPC, cmap='coolwarm', extend='both', alpha=0.8)

    # Add colorbar
    cbar = plt.colorbar(contourf, ax=ax, orientation='horizontal', shrink=0.8)
    cbar.set_label('2m Temperature (C)', fontsize=12)

    # Plotting contour lines and lables
    contour = ax.contour(lonall, latall, t2m, levels=clevs_t2m, transform=projPC, colors='k', linewidths=1)
    contour_0 = ax.contour(lonall, latall, t2m, levels=[0], transform=projPC, colors='red', linewidths=1.5)
    contour_10 = ax.contour(lonall, latall, t2m, levels=[10], transform=projPC, colors='yellow', linewidths=1.5)
    contour_20 = ax.contour(lonall, latall, t2m, levels=[20], transform=projPC, colors='orange', linewidths=1.5)
    contour_neg10 = ax.contour(lonall, latall, t2m, levels=[-10], transform=projPC, colors='blue', linewidths=1.5)
    contour_neg20 = ax.contour(lonall, latall, t2m, levels=[-20], transform=projPC, colors='purple', linewidths=1.5)

    # Contour line setup for important values
    plt.clabel(contour, inline=True, fontsize=8, colors='black')
    plt.clabel(contour_0, inline=True, fontsize=8, colors='red')
    plt.clabel(contour_10, inline=True, fontsize=8, colors='yellow')
    plt.clabel(contour_20, inline=True, fontsize=8, colors='orange')
    plt.clabel(contour_neg10, inline=True, fontsize=8, colors='blue')
    plt.clabel(contour_neg20, inline=True, fontsize=8, colors='purple')

    # Entitle
    ax.set_title('2m Temperature_'+str(file_name[:-3]))

    # Plt.show()
    plt.savefig((os.path.join(t2m_output_dir, str(file_name[:-3])+"_t2m.png"))) # save


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
t2m_output_dir = os.path.join(
    os.path.join(os.getcwd(), "t2m_output"),
)
os.makedirs(t2m_output_dir, exist_ok=True)

# Visualize for all nc files
for nc_file in output_lst:
    ds = xr.open_dataset(os.path.join(path, nc_file))
    lon = ds.longitude
    lat = ds.latitude
    temp_visualization(ds, nc_file)
