#!/bin/bash

# Define your destination grid variables
DST_GRID_FILE="grid_latlon90x180_20230914.nc"
DST_GRID="90x180"
DST_NY="90"
DST_NX="180"

# Generate the destination grid file
ncremap -g ${DST_GRID_FILE} -G ttl="Equi-Angular grid, dimensions ${DST_GRID}, cell edges on Poles/Equator and Prime Meridian/Date Line"#latlon=${DST_NY},${DST_NX}#lat_typ=uni#lon_typ=grn_wst
