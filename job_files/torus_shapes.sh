#!/bin/bash
# ----------------SLURM Parameters----------------
#SBATCH -J torus_shapes
#SBATCH -p slims
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --mem=100
#SBATCH --mail-user=dramirez@dim.uchile.cl
#SBATCH --mail-type=ALL
#SBATCH --array=1-400%88
#SBATCH -o ../data/Guacolda/out/Torus_shapes_strand_16_32_rand_4_%A_%a.out
#SBATCH -e ../data/Guacolda/err/Torus_shapes_strand_16_32_rand_4_%A_%a.err

#-----------------Toolchain---------------------------
# ----------------Modulos-----------------------------
module purge
ml  Anaconda3/2020.02
# ----------------Comandos--------------------------
python ../src/unstable_shapes.py 32 strand 16 3452 12000

