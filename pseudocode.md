### Pseudocode
```
#Create set of valid barcodes from text file
barcodes = {set of 24 barcodes}

#Create dictionaries to count number of pairs with matched indices and swapped indices
#Create counter to count pairs with low quality/unknown indices
matched_dict = {}
hop_dict = {}
unknown_ct: int

#Read fq files concurrently and separate records into appropriate
#output files based on matched index pairs 
Open all 4 fastq files in read mode:
	while True:
		if not end of any file:
			Store 4 lines of current record from every file in a list;
			Append both barcodes to end of biological R1 and R2 headers;
			Take reverse complement of index 2 in R3.fastq;
			if index 1 or rc of index 2 not in barcodes:
				Write biological R1 record to unknownR1.fq;
				Write biological R2 record to unknownR2.fq;
				Increment value of unknown_ct;
			elif average quality score of either index read < cutoff :
				Write biological R1 record to unknownR1.fq
				Write bological R2 record to unknownR2.fq
				Increment value of unknown_ct;
			else:
				 if rc of index 2 matches index 1:
					 Write biological R1 record to {index1}_R1.fq;
					 Write biological R2 record to {index2}_R2.fq;
					 Increment value for "index1-index2" in matched_dict;
				else:
					Write biological R1 record to unmatchedR1.fq;
					Write biological R2 record to unmatchedR2.fq;
					Increment value for "index1-index2" in hop_dict;
		else:
			break

Report number and names of pairs in each dict
```

### High level functions
```
def rv_complement(index: str) -> str:
    '''Takes string for barcode as input. Returns reverse complement of that barcode as str.'''
    return rc_index

Input: "ACCGTA"
Expected output: "TACGGT"
```
```
def mean_qs(index:str) -> float:
    '''Takes quality score for barcode as str input. Calculates average quality score of sequence and returns as float. Assumes Phred+33 encoding.'''
    return qs_sum/len(index)

Input: "GHI"
Expected output: 39.0
```
```
def format_header(header: str, index_pair: str) -> str:
    '''Takes fq header sequence and index1-index2 pair as separate strings. Appends index1-index2 pair to the end of the header line and returns new string.'''
    return header + index_pair

Input: "seq1","AAA-AAA"
Expected output: "seq1AAA-AAA"
```
### Answers
1. **Define the problem.**  
The problem is that there are data associated with different barcodes in each of the 4 fastq files since the 24 samples were multiplexed during sequencing, and we need to separate the barcodes into different files to make downstream analysis possible.  
2. **Determine/describe what output would be informative.**  
- It would be useful to quantify and graph the frequency of each index-pair in the output to see if certain samples are over or underrepresented in the data.