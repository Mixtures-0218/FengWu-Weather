# FengWu-Weather
This project is developed based on https://github.com/OpenEarthLab/FengWu and https://github.com/HaxyMoly/Pangu-Weather-ReadyToGo. Thank for the authors of the two projects above!

*The code is not official and may contain some potential mistakes! Do not use it in commercial and formal use!

If you have questions, please contact leoluo@uw.edu

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
Since the input requires both surface and pressure level data, the data should be downloaded separately from two different products of CDS. The surface variables are the u-component of 10m wind (m/s), v-component of 10m wind (m/s), 2m temperature (K), and mean sea level pressure (Pa). The upper variables are geopotential (m), specific humidity (kg/kg),  u-component of wind (m/s), v-component of wind (m/s), and temperature (K) in 13 pressure levels [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50] hPa from bottom to top. Therefore, the downloaded surface data is shaped [4, 721, 1440]; the upper data is shaped [5, 13, 721, 1440].
The code will automatically download the data 6h after the initial field. Hence, there will be 4 raw downloaded nc files in 2 time ticks.

### Convert nc file to numpy
Since FengWu requires input in the shape of [69, 721, 1440], and the first 5 parameters are coming from the surface data. Therefore, the surface and upper data should be merged into one numpy file. The code will create an empty numpy file with the required shape [69, 721, 1440]. Then the first 5 parameters will be filled with the surface parameters in the required order. For upper data, the pressure levels should be flipped to the order of up to bottom, and in axis = 0 to ensure the latitude won't flip. The code then will fill the numpy file with upper variable data in the required order, and finally save it in the input_data file as the name of input1. The same operation for data 6h after.

## Inference
The code allows the user to input a forecast time tick. However, since the FengWu model only provides a step in 6h, the time difference between the initial field and the terminal time field should be a multiple of 6.

An output file will then be created for the output data.

Load the model and set the GPU behavior.

The model requires a standardized data input. The mean and standard deviation values are provided in the parent file from https://github.com/OpenEarthLab/FengWu. The code will merge the two standardized input files into a single input with the shape of [138, 721, 1440]. After a round of output, the model merges the last 69 parameters of the input file with the first 69 parameters of the output file to get the next input file, and so on

## Output Decode
The basic logic here is to convert numpy file back to nc file in order to access it more easily. The precision of the data is in float32.

The code will first extract surface parameters in the required order and save them in a temporary variable. For upper data, since the parameters are too many (69-5=64) to write their names, we use a for loop to name all the parameters based on pressure levels and variables and use a dictionary to match them with indexes from index = 4 (as the first 5 are the surface parameters) in the required order.

Create an empty nc file and fill in the variables and their units. For upper variables without specific temporary variables, we here use a for loop to temporarily store values of each upper-air parameter and give them the units based on their names according to the variable name list we created in the previous process. As we have multiple output numpy files, we use a for loop and function to deal with every file.

## Visualization
### 2m temperature visualization
The code first will traverse all the output nc files in the output folder and deal with them with the visualization function. Then an output folder will be created to save the output images. The latitude and longitude in the nc file will be extracted and meshed in grids for further plotting use.

In the function, the 2m temperature data will be extracted according to the variable name named in the output decode process and then converted to Celsius from Kelvin. The min and max of temperatures are set at -60 and 60 separately, but the steps will be set according to the region the user chooses in the location.py file (The location.py file isn't complete for plotting cities). The projection in this case will be flat and with basic setups like displaying the border among countries. The contour line will be plotted with important values in different colors. Finally, the graph will be saved after adding the color bar and title. The name of the png file is named based on the output number and the plotting parameter.

