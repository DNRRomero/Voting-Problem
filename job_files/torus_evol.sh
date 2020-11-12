#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J torus_evol
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=10000
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-400%88
#SBATCH -o ../data/Guacolda/out/Torus_evol_32_rand_2_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Torus_evol_32_rand_2_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02
# ----------------Comandos--------------------------
python ../src/torus_evol.py 32 123456 12000

