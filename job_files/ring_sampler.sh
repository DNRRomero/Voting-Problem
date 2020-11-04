#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J ring_sampler
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=40
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-400%70
#SBATCH -o ../data/Guacolda/out/ring_sampler_256_var_rand_%A_%a.out
#SBATCH -e ../data/Guacolda/err/ring_sampler_256_var_rand_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02  
# ----------------Comandos--------------------------
python ../script/ring_sampler_var.py
 
