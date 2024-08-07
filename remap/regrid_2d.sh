#!/bin/bash


# salloc --nodes 1 --qos interactive --time 04:00:00 --constraint cpu --account=m4736


# module load e4s
# spack env activate gcc
# spack load nco
# # module load parallel

# Define your mapping file
MAP_FILE="map_ne30pg2_to_gaussian90x180_20240724.nc"

# Directory containing the .nc files to be regridded
# directory with interactive radiation; control simulations
INPUT_DIR="/global/cfs/cdirs/m3312/whannah/2022-RCEROT/E3SM.GNUGPU.ne30pg2.F-MMFXX-RCEROT.BVT.FIX_QRT.04/run"
# Directory to store the regridded .nc files
OUTPUT_DIR="/global/cfs/cdirs/m4736/E3SM_data_gaussian/FIX_QRT"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# # Loop over all .nc files in the directory
# for file in ${INPUT_DIR}/*.h2.00*.nc; do
#     # Extract the filename without the directory
#     filename=$(basename -- "$file")
    
#     # Define the output file name
#     output_file="${OUTPUT_DIR}/${filename}_regridded.nc"

#     # Perform regridding using ncremap
#     ncremap -i $file -o $output_file -m $MAP_FILE
# done

# Loop over all .nc files in the directory
for file in ${INPUT_DIR}/*.h1.00*.nc; do
    # Extract the filename without the directory
    filename=$(basename -- "$file")
    
    # Define the output file name
    output_file="${OUTPUT_DIR}/${filename}_regridded.nc"

    # # Perform regridding using ncremap
    # ncremap -i $file -o $output_file -m $MAP_FILE

    # Check if the output file already exists
    if [ ! -f "$output_file" ]; then
        # Perform regridding using ncremap
        ncremap -i $file -o $output_file -m $MAP_FILE
    else
        echo "File $output_file already exists. Skipping regridding for $file."
    fi
    
done
