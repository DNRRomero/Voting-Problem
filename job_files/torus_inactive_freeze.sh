#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J torus_freeze
# SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=100
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-250%88
#SBATCH -o ../data/Guacolda/out/Torus_inactive_freeze_stab-uns_b_32_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Torus_inactive_freeze_stab-uns_b_32_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02
# ----------------Comandos--------------------------
python ../src/inactive_with_freezing.py 32 12000

