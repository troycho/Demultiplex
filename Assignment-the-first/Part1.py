#!/usr/bin/env python
import argparse
import gzip
import matplotlib.pyplot as plt
import bioinfo
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description="Generate mean distributions for each nucleotide position")
    parser.add_argument("-f", "--file", help="Enter filename absolute path")
    parser.add_argument("-r", "--read_length", help="Specify read length")
    parser.add_argument("-o", "--outFile", help="Output filename prefix")
    return parser.parse_args()

args = get_args()
mean_qs = np.zeros(int(args.read_length), dtype=float) #Creates 1D array to hold qscore mean for each position
i: int=0 #line counter for file
#Populates array with sum of qscores at each position
with gzip.open(f'{args.file}', 'rt') as fh:
    for line in fh:
        line = line.strip('\n')
        if i%4 == 3: #if quality score line
            for index, letter in enumerate(line):
                mean_qs[index] += bioinfo.convert_phred(letter)
        i+=1

x: list = [] #will contain nucleotide positions
y: list = [] #will contain qscore averages for corresponding positions
#Calculates mean at each nucleotide position
#Simultaneously, appends values to x and y lists for plotting later
with open(f'{args.outFile}_dist.txt', 'w') as wf:
    wf.write(f'Pos\tMean\n')
    for index, sum in enumerate(mean_qs):
        mean_qs[index] = mean_qs[index]/(i/4)
        wf.write(f'{index}\t{mean_qs[index]}\n')
        x.append(index)
        y.append(mean_qs[index])

#Generates histogram plot
plt.title(f'{args.outFile} mean quality score at each position')
plt.scatter(x, y)
plt.xlabel("Nucleotide Position")
plt.ylabel("Mean Phred Score")
plt.savefig(f'{args.outFile}_hist.png')




