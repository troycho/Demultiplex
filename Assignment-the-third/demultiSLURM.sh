#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --mem=16G
#SBATCH --time=1-0
#SBATCH --mail-user=taro@uoregon.edu
#SBATCH --mail-type=ALL

/usr/bin/time -v ./demultiplex.py \
    -t /projects/bgmp/shared/2017_sequencing/indexes.txt \
    -c 30 \
    -R1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
    -R2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
    -R3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
    -R4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz