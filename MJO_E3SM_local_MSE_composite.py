import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 
import glob
import os 

# calculate the MSE budget 
# The composites are based on Ma's paper

# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM_data/regridded_data/'
# specify which case we use
case_dir = os.environ['case_dir']

# parameters to get uncertainty
lat_lim_olr = int(os.environ['lat_lim'])  # 5, 10, 15
kmax = int(os.environ['kmax'])  # 7, 9, 11
Tlow = int(os.environ['Tlow'])  # 90, 100, 110, 150
Thig = int(os.environ['Thig'])  # 10, 20, 30    

lat_lim = 90  # for the horizontal composite

flg = str(lat_lim_olr)+'_'+str(kmax)+'_'+str(Tlow)+'_'+str(Thig)

# read the 3D data
files_path = dirn + case_dir + '/3D/'
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))
ds = xr.open_mfdataset(nc_files)

# read the OLR data
files_path = dirn + case_dir + '/'
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))
ds1 = xr.open_mfdataset(nc_files)

# average the OLR over 10S-10N
olr = ds1['FLNT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
olravg = olr.mean(dim='lat') # average over 10S-10N

# filter the olr data (k=1-9, f=0.01-0.05)
# olravg[time, lon]
olrflt = mjo.get_MJO_signal(olravg, d=1, kmin=1, kmax=kmax, flow=1.0/Tlow, fhig=1.0/Thig)
# get the location of the miminum OLR
olrmin = olrflt.argmin(dim='lon')
print('olrmin calculated')

# load local MSE budget local_MSE_budget_'+case_dir+'.nc'  

mse_budget = xr.open_dataset(dirn+'analysis/local_MSE_budget/local_MSE_budget_'+case_dir+'.nc').sel(time=olr.time)

# comp = mjo.get_local_MSE_budget_composite(mse_budget, olrmin)

comp = {}

for key in list(mse_budget.data_vars.keys()):
    mse = mse_budget[key]  # [time, lev, lat, lon]
    mse_ano = mse - mse.mean(dim='lon')  # zonal anomaly
    mse_sft = mse_ano.copy()

    for i in range(olrmin.size):
        mse_sft[i,:,:,:] = np.roll(mse_ano[i, :, :, :], shift=90-olrmin[i], axis=-1)
    
    comp[key] = mse_sft.mean(dim='time')  # [lev, lat, lon]
    print(key)

output_path = dirn+'analysis/local_MSE_budget/composite_local_MSE_budget_'+case_dir+flg+'.nc'  

composite = xr.Dataset(comp)
composite.to_netcdf(output_path)

print('Budget saved. Output path:', output_path)
