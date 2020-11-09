#!/bin/bash
# --------------- dimension ----------------------
# ----------------SLURM Parameters----------------
#SBATCH -J torus_agreement
#SBATCH -p general
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=19200
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-400%88
#SBATCH -o ../data/Guacolda/out/Torus_agreement_20_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Torus_agreement_20_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02  
# ----------------Comandos--------------------------
python ../src/torus_agreement.py
 
