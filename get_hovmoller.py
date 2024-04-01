import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 
import pickle
import os 

dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# specify which case we use
case_dir = os.environ['case_dir']

import glob
files_path = dirn + case_dir + '/'
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))
ds1 = xr.open_mfdataset(nc_files)

lat_lim = 10    

# precipitation
prep = ds1['PRECT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load() # m/s
prepavg = prep.mean(dim='lat') * 86400 * 1000 # convert to mm/day
prepavg['time'] = np.arange(prepavg.time.size)

olrde = mjo.get_MJO_signal(prepavg, d=1, kmin=1, kmax=9, flow=0.01, fhig=0.05)

olr_re = xr.DataArray(
    data=olrde.real,
    coords=prepavg.coords,
    dims=prepavg.dims,
)

# store prepavg and olr_re to nc files
ds = xr.Dataset(
    {
        'prep_raw': prepavg,
        'prep_flt': olr_re,
    }
)
ds.to_netcdf(dirn+'analysis/hovmoller_prep_'+case_dir+'.nc', mode='w')
del ds
del prepavg
del olr_re
del prep
del olrde

print('prep done')

# PW
pw = ds1['TMQ'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()  # kg m-2
pwavg = pw.mean(dim='lat')
pwavg['time'] = np.arange(pwavg.time.size)

ude = mjo.get_MJO_signal(pwavg, d=1, kmin=1, kmax=9, flow=0.01, fhig=0.05)

u850_re = xr.DataArray(
    data=ude.real,
    coords=pwavg.coords,
    dims=pwavg.dims,
)

# store pwavg and u850_re to nc files
ds = xr.Dataset(
    {
        'pw_raw': pwavg,
        'pw_flt': u850_re,
    }
)
ds.to_netcdf(dirn+'analysis/hovmoller_pw_'+case_dir+'.nc', mode='w')

del ds
del pwavg
del u850_re
del pw
del ude

print('pw done')

# OLR
olr = ds1['FLNT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
olravg = olr.mean(dim='lat') # average over 10S-10N
olravg['time'] = np.arange(olravg['time'].size)

olrde = mjo.get_MJO_signal(olravg, d=1, kmin=1, kmax=9, flow=0.01, fhig=0.05)

olr_re = xr.DataArray(
    data=olrde.real,
    coords=olravg.coords,
    dims=olravg.dims,
)

# store olravg and olr_re to nc files
ds = xr.Dataset(
    {
        'olr_raw': olravg,
        'olr_flt': olr_re,
    }
)
ds.to_netcdf(dirn+'analysis/hovmoller_olr_'+case_dir+'.nc', mode='w')

del ds 
del olravg
del olr_re
del olr
del olrde

print('olr done')

# U850
u850 = ds1['U850'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
u850avg = u850.mean(dim='lat') # average over 10S-10N
u850avg['time']= np.arange(u850avg['time'].size)

ude = mjo.get_MJO_signal(u850avg, d=1, kmin=1, kmax=9, flow=0.01, fhig=0.05)

u850_re = xr.DataArray(
    data=ude.real,
    coords=u850avg.coords,
    dims=u850avg.dims,
)

# store u850avg and u850_re to nc files
ds = xr.Dataset(
    {
        'u850_raw': u850avg,
        'u850_flt': u850_re,
    }
)

ds.to_netcdf(dirn+'analysis/hovmoller_u850_'+case_dir+'.nc', mode='w')

print('u850 done')