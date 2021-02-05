#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J torus_transition
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=500
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-100%88
#SBATCH -o ../data/Guacolda/out/Torus_transition_32_rand_4_180end_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Torus_transition_32_rand_4_180end_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02  
# ----------------Comandos--------------------------
python ../src/torus_transition.py 32 3452 12000
