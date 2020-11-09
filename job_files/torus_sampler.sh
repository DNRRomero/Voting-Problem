#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J torus_sampler
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=100
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-400%80
#SBATCH -o ../data/Guacolda/out/Torus_sampler_16_var_rand_2_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Torus_sampler_16_var_rand_2_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02  
# ----------------Comandos--------------------------
python ../src/torus_sampler.py
 
