#!/bin/bash

# salloc --nodes 1 --qos interactive --time 04:00:00 --constraint cpu --account=dasrepo
# Define your mapping file
MAP_FILE="map_ne30pg2_to_gaussian90x180_20240724.nc"

# Directory containing the .nc files to be regridded
INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.GBL_QRT.04/run"
# Directory to store the regridded .nc files
OUTPUT_DIR="/global/cfs/cdirs/m4736/E3SM_data_gaussian/GBL_QRT"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Function to perform regridding
regrid() {
    local file=$1
    local output_file="${OUTPUT_DIR}/$(basename -- "$file")_regridded.nc"
    ncremap -i "$file" -o "$output_file" -m "$MAP_FILE"
}

export -f regrid

# Find all .nc files and regrid them in parallel
find ${INPUT_DIR} -name "*.h2.00*.nc" -o -name "*.h1.00*.nc" | parallel regrid {}






# #!/bin/bash

# # module load e4s
# # spack env activate gcc
# # spack load nco

# # Define your mapping file
# MAP_FILE="map_ne30pg2_to_gaussian90x180_20240724.nc"

# # Directory containing the .nc files to be regridded
# # directory with interactive radiation; control simulations
# INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.RADNX_1.04/run"
# # Directory to store the regridded .nc files
# OUTPUT_DIR="/global/cfs/cdirs/m4736/E3SM_data_gaussian/control"

# # # directory with prescribed radiative profiles
# # INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.FIX_QRT.04/run"
# # Directory to store the regridded .nc files
# # OUTPUT_DIR="/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/FIX_QRT"

# # # directory with globally homogenized radiative profiles
# # INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.GBL_QRT.04/run"
# # Directory to store the regridded .nc files
# # OUTPUT_DIR="/pscratch/sd/l/linyaoly/MJO_E3SM/regridded_data/GBL_QRT"

# # Create output directory if it doesn't exist
# mkdir -p $OUTPUT_DIR

# # Loop over all .nc files in the directory
# for file in ${INPUT_DIR}/*.h2.00*.nc; do
#     # Extract the filename without the directory
#     filename=$(basename -- "$file")
    
#     # Define the output file name
#     output_file="${OUTPUT_DIR}/${filename}_regridded.nc"

#     # Perform regridding using ncremap
#     ncremap -i $file -o $output_file -m $MAP_FILE
# done

# # Loop over all .nc files in the directory
# for file in ${INPUT_DIR}/*.h1.00*.nc; do
#     # Extract the filename without the directory
#     filename=$(basename -- "$file")
    
#     # Define the output file name
#     output_file="${OUTPUT_DIR}/${filename}_regridded.nc"

#     # Perform regridding using ncremap
#     ncremap -i $file -o $output_file -m $MAP_FILE
# done

# # ncremap -i /global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.RADNX_1.04/run/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.RADNX_1.04.eam.h1.0001-02-04-00000.nc -o test.nc -m map_ne30pg2_to_gaussian90x180_20240724.nc