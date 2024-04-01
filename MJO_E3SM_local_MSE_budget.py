import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 

import glob
import os 

# calculate the MSE budget 
# The composites are based on Ma's paper
# xr.set_options(enable_cftimeindex=True)

# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM_data/regridded_data/'
# specify which case we use
case_dir = os.environ['case_dir']

lat_lim = 90  # for the horizontal composite

# read the 3D data
files_path = dirn + case_dir + '/3D'
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))
ds = xr.open_mfdataset(nc_files)

# calculate the MSE budget, sperate T and Q
mse_budget = mjo.get_local_MSE_budget_sep(ds, lat_lim=lat_lim, plim=100, latmean=False)

ds.close()

output_path = dirn+'analysis/local_MSE_budget/local_MSE_budget_'+case_dir+'.nc'  

mse = xr.Dataset(mse_budget)
mse.to_netcdf(output_path)

print('Budget saved. Output path:', output_path)

