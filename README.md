# FengWu-Weather
This project is developed based on https://github.com/OpenEarthLab/FengWu and https://github.com/HaxyMoly/Pangu-Weather-ReadyToGo. Thank for the authors of the two projects above!

## Preparation
Create an ECMWF account https://accounts.ecmwf.int/auth/realms/ecmwf/login-actions/registration?client_id=cms-www&tab_id=BSVdzoo7_xA and use it to sign in Climate Data Store (CDS) https://cds.climate.copernicus.eu

Go to CDS to find your own API key https://cds.climate.copernicus.eu/how-to-api

Open the terminal and create a cdsapirc file to save API info by running
```
 touch ~/.cdsapirc
```
Open the cdsapirc file by running the code below in your terminal.
```
nano ~/.cdsapirc
```
## Data Format
The shape of import data is [69, 721, 1440], where 69 is the meteorological parameters with order [u10, v10, t2m, msl, z50, z100, ..., z1000, q50, q100, ..., q1000, t50, t100, ..., t1000]; 721x1440 is the latitude and longitude, lat from [90, -90] and lon from [0,360], with precision of 0.125 degrees. The required input files are needed for two consecutive time ticks with a gap of 6 hours.

## Requirements
```
pip install -r requirement_gpu.txt
```
## File structure
```plain
├── root
│   ├── input_data
│   ├── output_data
        │   ├── input_surface1.nc
        │   ├── input_surface2.nc
        │   ├── input_upper1.nc
        │   ├── input_upper2.nc
        │   ├── input1.npy
        │   ├── input2.npy
│   ├── fengwu_v1.onnx
│   ├── fengwu_v2.onnx
│   ├── inference.py
│   ├── data_mean.npy
│   ├── data_std.npy
│   ├── era5_data_get.py
│   ├── locations.py
│   ├── output_decode.py
│   ├── visualization_t2m.py
│   ├── visualization_z.py
│   ├── visualization_10m_wind.py
```
## ERA5 Data Download
The code will create the input_data folder to save all the input data downloaded from CDS. All the input data is using ERA5-Reanalysis.

### Initial time field
The code allows the user to input a customized initial time field, and will automatically calculate the next 6h data to satisfy the input requirement of FengWu. Note that ERA5-Reanalysis does have a latency of around 5 days. 

### Download ERA5 data from CDS
Since the input requires both surface and pressure level data, the data should download separately from two different products of CDS. The surface variables are the u-component of 10m wind (m/s), v-component of 10m wind (m/s), 2m temperature (K), and mean sea level pressure (Pa). The upper variables are geopotential (m), specific humidity (kg/kg),  u-component of wind (m/s), v-component of wind (m/s), and temperature (K) in 13 pressure levels [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50] hPa from bottom to top. Therefore, the downloaded surface data is shaped [4, 721, 1440]; upper data is shaped [5, 13, 721, 1440]
