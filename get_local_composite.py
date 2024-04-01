import numpy as np
import xarray as xr
import MJO_E3SM_util as mjo
import pandas as pd 
import matplotlib.pyplot as plt 

# --constraint cpu
# salloc --nodes 1 --qos interactive --time 04:00:00 --constraint cpu --account=dasrepo


# def get_local_MSE_budget_parallel(ds, lat_lim=50, plim=100, latmean=False, iceflg=False):
#     mse_budget = {}

#     # get local MSE
#     mse_sel = mjo.get_local_MSE(ds, lat_lim=lat_lim, latmean=latmean).load()  # [time, lev, lat, lon]
#     raw_mse = mse_sel.sel(lev=slice(plim,None)) 
#     mse_budget['mse'] = raw_mse
#     print('mse done')
#     dtmse_sel = mjo.get_local_MSE_tendency(ds, lat_lim=lat_lim, latmean=latmean).load() # [lev, lat, lon]
#     raw_dtmse = dtmse_sel.sel(lev=slice(plim,None))
#     mse_budget['tendency'] = raw_dtmse * 86400
#     print('tendency done')
#     # # get local MSE source: CRM
#     # dtmse_sel = (mjo.get_local_MSE_source(ds,'DDSE_CRM',lat_lim=lat_lim, latmean=latmean).load()
#     #         + mjo.get_local_MSE_source(ds,'DQLV_CRM',lat_lim=lat_lim, latmean=latmean).load())
#     # raw_dtmse = dtmse_sel.sel(lev=slice(plim,None))
#     # mse_budget['crm'] = raw_dtmse * 86400
#     # print('crm done')
#     # get local MSE source: CRM_ALT
#     dtmse_sel = (mjo.get_local_MSE_source(ds,'DDSE_CRM_ALT',lat_lim=lat_lim, latmean=latmean).load()
#             + mjo.get_local_MSE_source(ds,'DQLV_CRM_ALT',lat_lim=lat_lim, latmean=latmean).load()
#             - mjo.get_local_MSE_source(ds,'DDSE_QRS',lat_lim=lat_lim, latmean=latmean).load()
#             - mjo.get_local_MSE_source(ds,'DDSE_QRL',lat_lim=lat_lim, latmean=latmean).load())
#     raw_dtmse = dtmse_sel.sel(lev=slice(plim,None))
#     mse_budget['crmalt'] = raw_dtmse * 86400
#     print('crmalt done')
#     # get local MSE source: PBL
#     dtmse_sel = (mjo.get_local_MSE_source(ds,'DDSE_PBL',lat_lim=lat_lim, latmean=latmean).load()
#             + mjo.get_local_MSE_source(ds,'DQLV_PBL',lat_lim=lat_lim, latmean=latmean).load())
#     raw_dtmse = dtmse_sel.sel(lev=slice(plim,None))
#     mse_budget['pbl'] = raw_dtmse * 86400
#     print('pbl done')

#     dtmse_sel = (mjo.get_local_MSE_source(ds,'DDSE_QRS',lat_lim=lat_lim, latmean=latmean).load()
#                  + mjo.get_local_MSE_source(ds,'DDSE_QRL',lat_lim=lat_lim, latmean=latmean).load())
#     raw_dtmse = dtmse_sel.sel(lev=slice(plim,None))
#     mse_budget['qr'] = raw_dtmse * 86400
#     print('qr done')
#     dtmse_sel = (mjo.get_local_MSE_source(ds,'DDSE_DYN',lat_lim=lat_lim, latmean=latmean).load() 
#                  + mjo.get_local_MSE_source(ds,'DQLV_DYN',lat_lim=lat_lim, latmean=latmean).load())
#     raw_dtmse = dtmse_sel.sel(lev=slice(plim,None))
#     mse_budget['dyn'] = raw_dtmse * 86400
#     print('dyn done')
#     return mse_budget

# from concurrent.futures import ProcessPoolExecutor

# def process_key(key, mse_data, olrmin):
#     """Function to process mse data for a given key."""
#     mse_ano = mse_data - mse_data.mean(dim='lon')
#     mse_sft = np.empty_like(mse_ano)

#     for i in range(olrmin.size):
#         mse_sft[i, :, :] = np.roll(mse_ano[i, :, :], shift=90 - olrmin[i], axis=-1)

#     return key, mse_sft.mean(dim='time')

# def get_local_MSE_budget_composite_parallel(mse_budget, olrmin):
#     comp = {}

#     # Prepare arguments for each process
#     args = [(key, mse_budget[key], olrmin) for key in mse_budget.keys()]

#     # Using ProcessPoolExecutor to parallelize the computation for each key
#     with ProcessPoolExecutor() as executor:
#         for key, result in executor.map(lambda p: process_key(*p), args):
#             comp[key] = result

#     return comp

# calculate the MSE budget 
# The composites are based on Ma's paper

# directory that stores all case data
dirn = '/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/'
# specify which case we use
case_dir = 'control'

lat_lim = 10

# read all files in the case directory
import glob
# files_path = dirn + case_dir + '/3D/'

# # Find all .nc files in the directory
# nc_files = sorted(glob.glob(f"{files_path}/*.nc"))

# ds = xr.open_mfdataset(nc_files)

files_path = dirn + case_dir + '/'

# Find all .nc files in the directory
nc_files = sorted(glob.glob(f"{files_path}/*.nc"))

ds1 = xr.open_mfdataset(nc_files)

# average the OLR over 10S-10N
olr = ds1['FLNT'].sel(lat=slice(-lat_lim,lat_lim)).resample(time='1D').mean().load()
olravg = olr.mean(dim='lat') # average over 10S-10N

# filter the olr data (k=1-9, f=0.01-0.05)
# olravg[time, lon]

olrflt = mjo.get_MJO_signal(olravg, d=1, kmin=1, kmax=9, flow=0.01, fhig=0.05)
# get the location of the miminum OLR
olrmin = olrflt.argmin(dim='lon')

# mse_budget = get_local_MSE_budget_parallel(ds, lat_lim=lat_lim, plim=100, latmean=True)

import pickle

# # Write to a JSON file MJO_E3SM/regridded_data/analysis/local_MSE_budget
# with open(dirn+'analysis/local_MSE_budget/local_MSE_budget_control_latavg_backup.json', 'wb') as file:
#     pickle.dump(mse_budget, file)

# print('budget saved')

mse_budget = pickle.load(open(dirn+'analysis/local_MSE_budget/local_MSE_budget_control_latavg_backup.json', 'rb'))

comp = mjo.get_local_MSE_budget_composite(mse_budget, olrmin)


# Write to a JSON file MJO_E3SM/regridded_data/analysis/local_MSE_budget
with open(dirn+'analysis/local_MSE_budget/local_MSE_budget_composite_control_latavg_backup.json', 'wb') as file:
    pickle.dump(comp, file)

# comp is a list of 4
# store the composite

