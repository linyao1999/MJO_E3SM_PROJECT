#!/bin/bash

# salloc --nodes 1 --qos interactive --time 02:00:00 --constraint cpu --account=dasrepo


for case_dir in "control" "FIX_QRT" "GBL_QRT" # "olr" "tcwv" "q200" "q500" "q850" "T200" "T500" "T850" "Z200" "Z500" "Z850" "v200" "v500" "v850" "u200" "u500" "u850" "prep" "sst" # 
do 
    export case_dir
    python3 get_hovmoller.py 
    echo "run ${case_dir}"
done
