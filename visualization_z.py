import numpy as np
import matplotlib.pyplot as plt
import os
import xarray as xr
import math
from cartopy import crs as ccrs, feature as cfeature
    

def z_visualization(nc_file, file_name, z_name, z_step):

    ht = getattr(ds, z_name) / 9.80665  # Convert to m

    # Find max and min
    max_z = 0
    min_z = 10000000
    for z in ht.values:
        if max(z) > max_z:
            max_z = max(z)
        if min(z) < min_z:
            min_z = min(z)
    print(max_z, min_z)
    
    # Boundaries and step of geopotential
    clevs_hght = np.arange(math.floor(min_z), math.ceil(max_z), z_step)

    # Using meshgrid to generate longitude and latitude grid
    lonall, latall = np.meshgrid(lon, lat)

    # Setting projection type and range
    projPC = ccrs.PlateCarree()
    projStr = ccrs.Stereographic(central_longitude=-140, central_latitude=60)
    lonW = -150
    lonE = -100
    latS = 30
    latN = 70

    # Plot setting
    fig = plt.figure(figsize=(11, 8.5))
    ax = plt.subplot(1, 1, 1, projection=projStr)
    ax.set_extent([lonW, lonE, latS, latN], crs=projPC)
    ax.coastlines()
    ax.add_feature(cfeature.STATES)
    ax.gridlines(draw_labels=True, dms=True, color='black')

    # Fill color of the map
    contourf = ax.contourf(lonall, latall, ht, levels=clevs_hght, transform=projPC, cmap='viridis', extend='both', alpha=0.8)

    # Add colorbar
    cbar = plt.colorbar(contourf, ax=ax, orientation='vertical', shrink=0.8)
    cbar.set_label('Geopotential Height (m)', fontsize=12)

    # Plotting contour lines and lables
    contour = ax.contour(lonall, latall, ht, levels=clevs_hght, transform=projPC, colors='k')
    plt.clabel(contour, fontsize=10)

    # Entitle
    ax.set_title(str(z_input) + ' hPa Geopotential Heights_' + str(file_name[:-3]))

    # plt.show()
    plt.savefig((os.path.join(output_dir, str(file_name[:-3]) + "_" + z_name + ".png"))) # save


# Geopotential level and steps
z_dict = {"1000": 20,
            "925": 30,
            "850": 30,
            "700": 30,
            "600": 30,
            "500": 60,
            "400": 60,
            "300": 60,
            "250": 60,
            "200": 60,
            "150": 60,
            "100": 60,
            "50": 100
            }

keys = []
# Geopotential input
flag = 0
while flag == 0:
    z_input = input("geopotential level:")
    for key in z_dict:
        keys.append(key)
        if key == z_input:
            z_name = 'z' + str(z_input)
            z_step = z_dict[key]
            flag = 1
            break
    if z_input not in keys:
        print("no such geopotential")

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
    os.path.join(os.getcwd(), z_name + "_output"),
)
os.makedirs(output_dir, exist_ok=True)

# Visualize for all nc files
for nc_file in output_lst:
    ds = xr.open_dataset(os.path.join(path, nc_file))
    lon = ds.longitude
    lat = ds.latitude
    z_visualization(ds, nc_file, z_name, z_step)