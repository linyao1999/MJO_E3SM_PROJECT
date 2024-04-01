import numpy as np
import xarray as xr
import MJO_E3SM_util 

import os 

# ############# parameters to be set #######################
# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# specify which case we use
# case_dir = 'control'

case_dir = os.environ["case_dir"]

var_name = os.environ["var_name"]

spd = 1

# ##########################################################

# NOTE: DO NOT change any codes below
# read all files in the case directory
import glob
files_path = dirn + case_dir + '/'

# Find all .nc files in the directory
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))

ds = xr.open_mfdataset(nc_files)

sym, asym, background, sym_norm, asym_norm, sym_sig, asym_sig = MJO_E3SM_util.wk_analysis(ds[var_name].resample(time='D').mean().load(), remove_low=True, spd=spd)


# Create a new Dataset that contains each DataArray
output_ds = xr.Dataset({
    'sym': sym,
    'asym': asym,
    'background': background,
    'sym_norm': sym_norm,
    'asym_norm': asym_norm,
    'sym_sig': sym_sig,
    'asym_sig': asym_sig
})

# Specify path for saving the NetCDF file
output_path = dirn + 'analysis/'

import os

# Create the directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Save the Dataset as a NetCDF file
nc_file_path = output_path+case_dir+'_'+var_name+'_wk_dailyinput.nc'
# Check if the file exists
if os.path.exists(nc_file_path):
    # Delete the file
    os.remove(nc_file_path)
output_ds.to_netcdf(nc_file_path)

