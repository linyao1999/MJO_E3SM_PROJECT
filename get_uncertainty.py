import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 
import pickle
import glob
import os 

# calculate the MSE budget 
# The composites are based on Ma's paper

# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# specify which case we use
case_dir = os.environ['case_dir']

# parameters to get uncertainty
lat_lim = int(os.environ['lat_lim'])  # 5, 10, 15
kmax = int(os.environ['kmax'])  # 7, 9, 11
Tlow = int(os.environ['Tlow'])  # 90, 100, 110
Thig = int(os.environ['Thig'])  # 10, 20, 30    

flg = str(lat_lim)+'_'+str(kmax)+'_'+str(Tlow)+'_'+str(Thig)

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

# calculate the MSE budget, sperate T and Q
mse_budget = mjo.get_local_MSE_budget_sep(ds, lat_lim=lat_lim, plim=100, latmean=True)

# Write to a JSON file MJO_E3SM/regridded_data/analysis/local_MSE_budget
with open(dirn+'analysis/local_MSE_budget/local_MSE_budget_'+case_dir+'_latavg_septq'+flg+'.json', 'wb') as file:
    pickle.dump(mse_budget, file)

print('budget saved')

# mse_budget = pickle.load(open(dirn+'analysis/local_MSE_budget/local_MSE_budget_'+case_dir+'_latavg_septq.json', 'rb'))

comp = mjo.get_local_MSE_budget_composite(mse_budget, olrmin)

# Write to a JSON file MJO_E3SM/regridded_data/analysis/local_MSE_budget
with open(dirn+'analysis/local_MSE_budget/local_MSE_budget_composite_'+case_dir+'_latavg_septq'+flg+'.json', 'wb') as file:
    pickle.dump(comp, file)

# comp is a list of 4
# store the composite

