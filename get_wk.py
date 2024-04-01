import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 

# # directory that stores all case data
# dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# # specify which case we use
# case_dir = 'FIX_QRT'

# lat_lim = 10

# import glob
# files_path = dirn + case_dir + '/'

# # Find all .nc files in the directory
# nc_files = sorted(glob.glob(f"{files_path}/*.nc"))

# ds1 = xr.open_mfdataset(nc_files)

# olr = ds1['FLNT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean()

# sym = mjo.spacetime_power_sym(olr)

# # save sym into a netcdf file
# # name the variable as 'sym'
# sym = sym.rename('sym')
# sym.to_netcdf(dirn + '/analysis/' + case_dir + '_OLR_wk_dailyinput_all.nc')

# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# specify which case we use
# case_dir = 'GBL_QRT'

lat_lim = 10

import glob

for case_dir in ['control', 'FIX_QRT', 'GBL_QRT']:
    files_path = dirn + case_dir + '/'

    # Find all .nc files in the directory
    nc_files = sorted(glob.glob(f"{files_path}/*.nc"))

    ds1 = xr.open_mfdataset(nc_files)
    print(case_dir)

    olr = ds1['FLNT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean()

    segsize = 200
    sym = mjo.spacetime_power_sym(olr,segsize=segsize, noverlap=int(segsize*2/3))
    print('spectra done')
    # save sym into a netcdf file
    # name the variable as 'sym'
    sym = sym.rename('sym')
    sym.to_netcdf(dirn + '/analysis/' + case_dir + '_OLR_wk_dailyinput_all_seg'+str(segsize)+'days.nc')
