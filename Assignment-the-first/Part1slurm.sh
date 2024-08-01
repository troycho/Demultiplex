#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 4
#SBATCH --mem=12G
#SBATCH --time=1-0
#SBATCH --mail-user=taro@uoregon.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=R4-run

/usr/bin/time -v ./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
    -r 101 \
    -o "R4"