import os
import netCDF4 as nc
import numpy as np

output_path = os.path.join(os.getcwd(), "output_data")


def decode(file, file_name, file_path):
    data = np.load(file)
    # Surface variables
    u10 = data[0].astype(np.float32)
    v10 = data[1].astype(np.float32)
    t2m = data[2].astype(np.float32)
    mslp = data[3].astype(np.float32)
    # upper-air variables
    pressure_levels = ['1000', '925', '850', '700', '600', '500', '400', '300', '250', '200', '150', '100', '50']
    pressure_levels.reverse()
    variables = ['z', 'q', 'u', 'v', 't']
    # Naming upper-air variables
    upper_var_names = []
    for var in variables:
        for level in pressure_levels:
            upper_var_names.append(var + level)
    flag = 4
    index = []
    for i in range(65):
        index.append(flag)
        flag += 1
    upper_dict = {}
    # Giving corresponding index fr upper-air variables
    for name, idx in zip(upper_var_names, index):
        upper_dict[name] = data[idx].astype(np.float32)

    # Create empty nc file
    with nc.Dataset(
        os.path.join(file_path, file_name),'w', format='NETCDF4'
    )as nc_file:
        # Naming surface variables' values
        nc_file.createDimension("longitude", 1440)
        nc_file.createDimension("latitude", 721)
        nc_lon = nc_file.createVariable("longitude", np.float32, ("longitude"))
        nc_lat = nc_file.createVariable("latitude", np.float32, ("latitude"))
        nc_u10 = nc_file.createVariable("u10", np.float32, ("latitude", "longitude"))
        nc_v10 = nc_file.createVariable("v10", np.float32, ("latitude", "longitude"))
        nc_t2m = nc_file.createVariable("t2m", np.float32, ("latitude", "longitude"))
        nc_mslp = nc_file.createVariable("mslp", np.float32, ("latitude", "longitude"))
        # Filling upper-air variables' values and units
        for name in upper_var_names:
            var = nc_file.createVariable(name, np.float32, ("latitude", "longitude"))
            if "z" in name:
                var.unit = "m^2/s^2"
            elif "q" in name:
                var.unit = "kg/kg"
            elif "u" in name or "v" in name:
                var.unit = "m/s"
            elif "t" in name:
                var.unit = "K"
            var[:] = upper_dict[name]

        # Sufrace variables' units
        nc_lon.unit = "degrees_east"
        nc_lat.unit = "degrees_north"
        nc_mslp.unit = "Pa"
        nc_u10.unit = "m/s"
        nc_v10.unit = "m/s"
        nc_t2m.unit = "K"
        
        # Filling surface variables' values
        nc_lon[:] = np.linspace(0,360,1440)
        nc_lat[:] = np.linspace(90,-90,721)
        nc_u10[:] = u10
        nc_v10[:] = v10
        nc_t2m[:] = t2m
        nc_mslp[:] = mslp

# Decode each of the nc file in folder
output_lst = []
for file in os.listdir(output_path):
    if file.endswith('.npy'):
        output_lst.append(file)
        decode(os.path.join(output_path, file), str(file[:-4])+'.nc', output_path)
    else:
        print(f"Skipping directory or non-NPY file: {file}")
