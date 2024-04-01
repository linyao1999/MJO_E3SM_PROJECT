import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 
import pickle

# calculate the MSE budget 
# The composites are based on Ma's paper

# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# specify which case we use
# case_dir = 'control'
# case_dir = 'FIX_QRT'
case_dir = 'GBL_QRT'
lat_lim_olr = 10
lat_lim = 90 

# read all files in the case directory
import glob
ndays = 2000
files_path = dirn + case_dir + '/3D/'
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))
ds = xr.open_mfdataset(nc_files[:ndays])

files_path = dirn + case_dir + '/'
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))
ds1 = xr.open_mfdataset(nc_files[:ndays])

# average the OLR over 10S-10N
olr = ds1['FLNT'].sel(lat=slice(-lat_lim_olr,lat_lim_olr)).resample(time='1D').mean().load()
olravg = olr.mean(dim='lat') # average over 10S-10N

# filter the olr data (k=1-9, f=0.01-0.05)
# olravg[time, lon]
Tlow = 150
flow = 1.0/Tlow
olrflt = mjo.get_MJO_signal(olravg, d=1, kmin=1, kmax=9, flow=flow, fhig=0.05)
# get the location of the miminum OLR
olrmin = olrflt.argmin(dim='lon')

# calculate the composite of z200
geop = ds['Z3'].sel(lev=200, method='nearest').sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
# # calculate the composite of OLR
# olrcomp = ds1['FLNT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
# # calculate the composite of u200
# geop = ds['U'].sel(lev=200, method='nearest').sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
# # calculate the composite of PRECT m/s
# geop = ds1['PRECT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()

mse_ano = geop - geop.mean(dim='lon')
mse_sft = mse_ano.copy()

for i in range(olrmin.size):
    mse_sft[i,:,:] = np.roll(mse_ano[i, :, :], shift=90-olrmin[i], axis=-1)

prep = mse_sft.mean(dim='time') # * 86400 * 100 # convert to cm/day

# Write to a JSON file MJO_E3SM/regridded_data/analysis/
with open(dirn+'analysis/z200_composite_'+case_dir+'_latavg_Tlow'+str(Tlow)+'days.json', 'wb') as file:
    pickle.dump(prep, file)


