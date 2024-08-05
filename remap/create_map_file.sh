#!/bin/bash

# sometimes errors can be solved by using older versions of nco
# Define your destination grid file
# DST_GRID_FILE="grid_latlon90x180_20230914.nc"
DST_GRID_FILE="gaussian_grid_90x180.nc"
# DST_GRID_FILE="90x180_SCRIP.20150901.nc"

# Define your source grid and mapping file variables
SRC_GRID_FILE="ne30pg2.nc"
MAP_FILE="map_ne30pg2_to_gaussian90x180_20240724.nc"

# Generate the mapping file between the two grids
ncremap --grd_src=$SRC_GRID_FILE --grd_dst=$DST_GRID_FILE --map_fl=$MAP_FILE
# ncremap -a conserve -s ne30pg2.nc -g grid_latlon90x180_20230914.nc -m map_ne30pg2_to_latlon90x180_20230914.nc --vrb=3
# ncremap --alg_typ=aave --grd_src=ne30pg2.nc --grd_dst=grid_latlon90x180_20230914.nc --map_fl=map_ne30pg2_to_latlon90x180_20230914.nc
