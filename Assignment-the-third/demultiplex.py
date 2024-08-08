#!/usr/bin/env python
import gzip
import argparse
import bioinfo

def get_args():
    parser = argparse.ArgumentParser(description="Demultiplex dual-matched barcodes in compressed FASTQ files")
    parser.add_argument("-R1", "--Read1", help="R1 file path")
    parser.add_argument("-R2", "--Read2", help="R2 file path")
    parser.add_argument("-R3", "--Read3", help="R3 file path")
    parser.add_argument("-R4", "--Read4", help="R4 file path")
    parser.add_argument("-c", "--cutoff", help="Index read cutoff score (per base)")
    parser.add_argument("-t", "--txt", help="Matched indexes.txt filename")
    return parser.parse_args()

def reverseComp(index: str) -> str:
    '''Takes index sequence as string input. Returns reverse complement of barcode as string.'''
    rev: str=index[::-1] #reverses string
    rc: str=""
    for base in rev:
        if base=="A":
            rc+="T"
        elif base=="T":
            rc+="A"
        elif base=="C":
            rc+="G"
        elif base=="G":
            rc+="C"
        else:
            rc+="N"
    return rc

def format_header(header: str, index1: str, index2: str) -> str:
    '''Takes fastq header line and both indices in a pair as separate strings.
    Appends pair to the end of the header and returns as string.'''
    new_header: str=f"{header} {index1}-{index2}"
    return new_header

def meetsCutoff(qscore: str, cutoff: int) -> bool:
    '''Takes quality score line for barcode as str input and cutoff value as int.
    Converts each string character to Phred+33 score and checks if it meets cutoff.
    If all base scores are >= cutoff, returns True, otherwise returns False.'''
    for char in qscore:
        if bioinfo.convert_phred(char) < cutoff:
            return False
    return True

def writeRecords(r1List: list, r4List: list, key: str) -> None:
    '''Takes R1 and R4 fastq records as lists (where indices are already appended to headers) and fh_dict key prefix
    as string. This function writes the R1 and R4 records to the R1 and R2 output files
    represented by <key>_R1.fq and <key>_R2.fq, respectively.'''
    for l in r1List:
        fh_dict[f"{key}_R1.fq"].write(f"{l}\n")
    for l in r4List:
        fh_dict[f"{key}_R2.fq"].write(f"{l}\n")

args = get_args()

#Extract set of barcodes from indexes.txt file
barcodes: set=set()
with open(args.txt, "r") as fh:
    firstLine: bool = True
    for line in fh:
        if firstLine: #skips header line
            firstLine = False
            continue
        line = line.strip("\n")
        spl: list=line.split("\t")
        barcodes.add(spl[4]) #add index to set of barcodes

#Create dictionaries to count number of pairs with matched and swapped indices
#Create counter for pairs with low quality/unknown indices
matched_dict: dict[str, int]={}
hop_dict: dict[str, int]={}
unknown: int=0

#Create dict for opening and closing file handles for writing- intended to be a global variable
fh_dict: dict={"hopped_R1.fq":open("hopped_R1.fq", "w"), "hopped_R2.fq":open("hopped_R2.fq", "w"), 
               "unknown_R1.fq":open("unknown_R1.fq", "w"), "unknown_R2.fq":open("unknown_R2.fq", "w")} #keys will be file names and values will initially be open file handles ("open()" objects)
for index in barcodes:
    fh_dict[f'{index}_R1.fq'] = open(f'{index}_R1.fq', "w")
    fh_dict[f'{index}_R2.fq'] = open(f'{index}_R2.fq', "w")

# file1 = "R1-testfile.fq.gz"
# file2 = "R2-testfile.fq.gz"
# file3 = "R3-testfile.fq.gz"
# file4 = "R4-testfile.fq.gz"

with gzip.open(args.Read1, "rt") as fh1, gzip.open(args.Read2, "rt") as fh2, gzip.open(args.Read3, "rt") as fh3, gzip.open(args.Read4, "rt") as fh4:
    i: int=0 #line counter
    r1: list=[] #stores current record from R1
    r2: list=[] #stores current record from R2
    r3: list=[] #stores current record from R3
    r4: list=[] #stores current record from R4
    for line1, line2, line3, line4 in zip(fh1, fh2, fh3, fh4):
        r1.append(line1.strip())
        r2.append(line2.strip())
        r3.append(line3.strip())
        r4.append(line4.strip())
        i+=1
        if i%4 == 0:
            index2 = reverseComp(r3[1]) #reverse complement of index 2
            r1_header: str=format_header(r1[0], r2[1], index2) #append indices to end of biological read1 header
            r2_header: str=format_header(r4[0], r2[1], index2) #append indices to end of biological read2 header
            r1[0] = r1_header #update R1 header in list
            r4[0] = r2_header #update R2 header in list
            if r2[1] not in barcodes or index2 not in barcodes: #if either of the indices is unknown
                # print(r1[0], "*invalid-unknown*", r4[0]) #DEBUGGING
                writeRecords(r1, r4, "unknown")
                unknown += 1
            elif not meetsCutoff(r2[3], int(args.cutoff)) or not meetsCutoff(r3[3], int(args.cutoff)): #if either index read doesn't pass qscore cutoff
                # print(r1[0], "*invalid-poor*", r4[0]) #DEBUGGING
                writeRecords(r1, r4, "unknown")
                unknown += 1
            else:
                if r2[1] == index2: #if index1 matches rc of index2
                    # print(r1[0], "*matched*", r4[0]) #DEBUGGING
                    writeRecords(r1, r4, f"{r2[1]}")
                    key: str=f'{r2[1]}-{index2}'
                    if key in matched_dict:
                        matched_dict[key] += 1
                    else:
                        matched_dict[key] = 1
                else: #if indices don't match
                    # print(r1[0], "*hopped*", r4[0]) #DEBUGGING
                    writeRecords(r1, r4, "hopped")
                    key: str=f'{r2[1]}-{index2}'
                    if key in hop_dict:
                        hop_dict[key] += 1
                    else:
                        hop_dict[key] = 1
            r1 = []
            r2 = []
            r3 = []
            r4 = []

#Close file handles at end of program
for key in fh_dict:
    fh_dict[key].close()

#Write out numbers for user report to output file
total: int=sum(matched_dict.values()) + sum(hop_dict.values()) + unknown #total number of reads outputted to all the files
matched_total: int=sum(matched_dict.values()) #total number of reads with matched barcodes
hop_total: int=sum(hop_dict.values()) #total number of reads with hopped barcodes
with open("user-report.txt", "w") as wf:
    wf.write(f"Overall numbers:\n")
    wf.write(f"|Category|\t|Number of reads|\t|% of total reads|\n")
    wf.write(f"Matched\t{matched_total}\t{matched_total/total}\n")
    wf.write(f"Hopped\t{hop_total}\t{hop_total/total}\n")
    wf.write(f"Unknown\t{unknown}\t{unknown/total}\n")
    wf.write("\n")
    wf.write(f"Matched indices breakdown:\n")
    wf.write(f"|Index Pair|\t|Number of reads|\t|% of matched reads|\n")
    for key in matched_dict:
        wf.write(f"{key}\t{matched_dict[key]}\t{matched_dict[key]/matched_total}\n")
    wf.write("\n")
    wf.write(f"Hopped indices breakdown:\n")
    wf.write(f"|Index Pair|\t|Number of reads|\t|% of hopped reads|\n")
    for key in hop_dict:
        wf.write(f"{key}\t{hop_dict[key]}\t{hop_dict[key]/hop_total}\n")

