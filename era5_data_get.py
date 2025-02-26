import cdsapi
import numpy as np
import netCDF4 as nc
import os
from datetime import datetime, timedelta


# save input_data folder
input_data_dir = os.path.join(
    os.path.join(os.getcwd(), "input_data"),
)
os.makedirs(input_data_dir, exist_ok=True)


def init_time_get():
    print("Please enter the initial time of the data you want to download:")
    valid_time = (datetime.now() - timedelta(days=5)).replace(hour=0, minute=0, second=0)
    # ERA5 data has 5 days latency
    print("The available date is before", valid_time.strftime("%Y-%m-%d"), "00:00...")

    # Entering a date for data
    while True:
        init_time = datetime(
            year=int(input("year: ")),
            month=int(input("month: ")),
            day=int(input("day: ")),
            hour=int(input("hour (recommend 0, 6, 12, 18): ")),
            minute=0
        )
        if init_time >= valid_time:
            print("The available date is before", valid_time.strftime("%Y-%m-%d"), "00:00...", "Please enter again!")
        else:
            print(f"Downloading ERA5 data for {init_time.strftime('%Y-%m-%d-%H')}" + ":00...")
            init_time_6h = init_time + timedelta(hours=6) # FengWu requires for additional data after 6h
            return init_time, init_time.strftime('%Y-%m-%d'), init_time.strftime('%H:%M'), init_time_6h.strftime('%Y-%m-%d'), init_time_6h.strftime('%H:%M')


def download_era5_data(input_path, init_date, init_hour, init_date_6h, init_hour_6h):
    # required download variables
    surface_variables = ['10m_u_component_of_wind', '10m_v_component_of_wind',
                         '2m_temperature','mean_sea_level_pressure',]
    upper_variables = ['geopotential', 'specific_humidity', 'u_component_of_wind', 'v_component_of_wind', 'temperature']
    pressure_levels = ['1000', '925', '850', '700', '600', '500', '400', '300', '250', '200', '150', '100', '50']

    # required area
    area = [90, 0, -90, 360]


    # download variables for input1
    c = cdsapi.Client()
    print("Start to download surface data 1...")
    c.retrieve('reanalysis-era5-single-levels',
               {
                   'product_type': 'reanalysis',
                   'format': 'netcdf',
                   'variable': surface_variables,
                   'date': init_date,
                   'time': init_hour,
                   'area': area
               },os.path.join(input_path, 'input_surface1.nc'))
    print("Surface data 1 downloaded successfully")
    print("Start to download upper air data 2...")

    # download upper air variables
    c.retrieve('reanalysis-era5-pressure-levels',
               {
                   'product_type': 'reanalysis',
                   'format': 'netcdf',
                   'variable': upper_variables,
                   'pressure_level': pressure_levels,
                   'date': init_date,
                   'time': init_hour,
                   'area': area
               }, os.path.join(input_path, 'input_upper1.nc'))
    print("Upper air data 2 downloaded successfully")
    
    # download variables for input2
    print("Start to download surface data 2...")
    c.retrieve('reanalysis-era5-single-levels',
               {
                   'product_type': 'reanalysis',
                   'format': 'netcdf',
                   'variable': surface_variables,
                   'date': init_date_6h,
                   'time': init_hour_6h,
                   'area': area
               },os.path.join(input_path, 'input_surface2.nc'))
    print("Surface data 2 downloaded successfully")
    print("Start to download upper air data 2...")

    # download upper air variables
    c.retrieve('reanalysis-era5-pressure-levels',
               {
                   'product_type': 'reanalysis',
                   'format': 'netcdf',
                   'variable': upper_variables,
                   'pressure_level': pressure_levels,
                   'date': init_date_6h,
                   'time': init_hour_6h,
                   'area': area
               }, os.path.join(input_path, 'input_upper2.nc'))
    print("Upper air data 2 downloaded successfully")


def convert_to_numpy(input_path):
    print("Converting to numpy array for input1...")
    input_data_1 = np.zeros((69, 721, 1440), dtype = np.float32) 
    # FengWu's dimension is 69, 721, 1440 include surface and upper data
    with nc.Dataset(os.path.join(input_path, 'input_surface1.nc')) as nc_surface_file:
        input_data_1[0] = nc_surface_file.variables['u10'][:].astype(np.float32)
        input_data_1[1] = nc_surface_file.variables['v10'][:].astype(np.float32)
        input_data_1[2] = nc_surface_file.variables['t2m'][:].astype(np.float32)
        input_data_1[3] = nc_surface_file.variables['msl'][:].astype(np.float32)
    with nc.Dataset(os.path.join(input_path, 'input_upper1.nc')) as nc_upper_file:
        variables = ['z', 'q', 'u', 'v', 't'] # Upper data
        flag = 4
        for var in variables:
            data = np.flip(nc_upper_file.variables[var][0,: 13,: ,: ], axis=0)
            # FengWu requires for inverse sorting of pressure level (from top to bottom)
            for i in data:
                input_data_1[flag] = i
                flag += 1
    np.save(os.path.join(input_path, 'input1.npy'), input_data_1)

    #Data for 6h after
    print("Converting to numpy array for input2...")
    input_data_2 = np.zeros((69, 721, 1440), dtype = np.float32)
    with nc.Dataset(os.path.join(input_path, 'input_surface2.nc')) as nc_surface_file:
        input_data_2[0] = nc_surface_file.variables['u10'][:].astype(np.float32)
        input_data_2[1] = nc_surface_file.variables['v10'][:].astype(np.float32)
        input_data_2[2] = nc_surface_file.variables['t2m'][:].astype(np.float32)
        input_data_2[3] = nc_surface_file.variables['msl'][:].astype(np.float32)
    with nc.Dataset(os.path.join(input_path, 'input_upper2.nc')) as nc_upper_file:
        variables = ['z', 'q', 'u', 'v', 't']
        flag = 4
        for var in variables:
            data = np.flip(nc_upper_file.variables[var][0,: 13,: ,: ], axis=0)
            for i in data:
                input_data_2[flag] = i
                flag += 1
    np.save(os.path.join(input_path, 'input2.npy'), input_data_2)
    print("convert to numpy done!")


init_time, init_date, init_hour, init_date_6h, init_hour_6h = init_time_get()
download_era5_data(input_data_dir, init_date, init_hour, init_date_6h, init_hour_6h)
convert_to_numpy(input_data_dir)
