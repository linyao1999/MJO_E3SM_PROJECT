#!/bin/bash

# module load nco

# Define your mapping file
MAP_FILE="/global/homes/l/linyaoly/MJO_E3SM/remap/map_ne30pg2_to_latlon90x180_20230914.nc"

# Directory with prescribed radiative profiles
INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.FIX_QRT.04/run"

# Directory to store the regridded .nc files
OUTPUT_DIR="/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/FIX_QRT/3D"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Define a function to handle the ncremap task
ncremap_task() {
    file=$1
    MAP_FILE=$2
    OUTPUT_DIR=$3
    
    # Extract the filename without the directory
    filename=$(basename -- "$file")
    
    # Define the output file name
    output_file="${OUTPUT_DIR}/${filename}_regridded.nc"

    # Perform regridding using ncremap
    ncremap -i $file -o $output_file -m $MAP_FILE
}

export -f ncremap_task

# Use parallel to process the ncremap tasks concurrently
find ${INPUT_DIR} -name "*.h2.00*.nc" | parallel ncremap_task {} $MAP_FILE $OUTPUT_DIR
