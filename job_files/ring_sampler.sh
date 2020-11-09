#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J ring_sampler
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=100
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-400%88
#SBATCH -o ../data/Guacolda/out/Ring_sampler_256_var_rand_2_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Ring_sampler_256_var_rand_2_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02  
# ----------------Comandos--------------------------
python ../src/ring_sampler.py 256 var
 
