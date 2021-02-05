#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J ring_transition
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=400
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-100%88
#SBATCH -o ../data/Guacolda/out/Ring_transition_1024_rand_4_181_221%A_%a.out
#SBATCH -e ../data/Guacolda/err/Ring_transition_1024_rand_4_181-221%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02  
# ----------------Comandos--------------------------
python ../src/ring_transition.py 1024 3452 13000
