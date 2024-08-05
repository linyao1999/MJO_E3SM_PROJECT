#!/bin/bash


for case_dir in "GBL_QRT"
do 
    export case_dir
    sbatch arun.slurm
    
done

wait 

# for case_dir in "control" "FIX_QRT" "GBL_QRT"
# do 
#     export case_dir
#     sbatch arun.slurm
    
# done

# wait 

# for case_dir in "control" "FIX_QRT" "GBL_QRT" 
# do 
#     export case_dir
#     for lat_lim in 5 10 15 
#     do 
#         for kmax in 7 9 11
#         do 
#             for Tlow in 90 100 110
#             do 
#                 for Thig in 10 20 30
#                 do 
#                     export lat_lim
#                     export kmax
#                     export Tlow
#                     export Thig
                    
#                     echo "run ${case_dir} ${lat_lim} ${kmax} ${Tlow} ${Thig}"
#                     sbatch arun.slurm
#                 done
#             done
#         done
#     done
# done