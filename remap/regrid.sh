#!/bin/bash

# module load nco

# Define your mapping file
MAP_FILE="/global/homes/l/linyaoly/MJO_E3SM/remap/map_ne30pg2_to_latlon90x180_20230914.nc"

# Directory containing the .nc files to be regridded
# directory with interactive radiation; control simulations
INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.RADNX_1.04/run"
# Directory to store the regridded .nc files
OUTPUT_DIR="/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/control/3D"

# # directory with prescribed radiative profiles
# INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.FIX_QRT.04/run"
# Directory to store the regridded .nc files
# OUTPUT_DIR="/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/FIX_QRT"

# # directory with globally homogenized radiative profiles
# INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.GBL_QRT.04/run"
# Directory to store the regridded .nc files
# OUTPUT_DIR="/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/GBL_QRT"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Loop over all .nc files in the directory
for file in ${INPUT_DIR}/*.h2.00*.nc; do
    # Extract the filename without the directory
    filename=$(basename -- "$file")
    
    # Define the output file name
    output_file="${OUTPUT_DIR}/${filename}_regridded.nc"

    # Perform regridding using ncremap
    ncremap -i $file -o $output_file -m $MAP_FILE
done

# ncremap -i /global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.RADNX_1.04/run/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.RADNX_1.04.eam.h1.0001-02-04-00000.nc -o /pscratch/sd/l/linyaoly/MJO_E3SM/test.nc -m /global/homes/l/linyaoly/MJO_E3SM/remap/map_ne30pg2_to_latlon90x180_20230914.nc