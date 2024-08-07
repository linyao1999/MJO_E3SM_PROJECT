#!/bin/bash
#SBATCH -A dasrepo
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=32
#SBATCH -t 10:00:00
#SBATCH --output=outlog/%j.out

echo "run ${case_dir}"
python3 MJO_E3SM_local_MSE_composite.py

wait
