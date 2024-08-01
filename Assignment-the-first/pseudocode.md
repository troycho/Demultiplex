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
	Read each file 1 line at a time:
		Store 4 lines of current record from each file in a list;
		Take reverse complement of index 2 in R3.fastq;
		Append both barcodes to end of biological R1 and R2 headers;
		if index 1 or rc of index 2 not in barcodes:
			Write biological R1 record to unknown_R1.fq;
			Write biological R2 record to unknown_R2.fq;
			Increment value of unknown_ct;
		elif per base score of either index read < cutoff :
			Write biological R1 record to unknown_R1.fq
			Write bological R2 record to unknown_R2.fq
			Increment value of unknown_ct;
		else:
				if rc of index 2 matches index 1:
					Write biological R1 record to {index1}_R1.fq;
					Write biological R2 record to {index1}_R2.fq;
					Increment value for "index1-index2" in matched_dict;
				else:
					Write biological R1 record to hopped_R1.fq;
					Write biological R2 record to hopped_R2.fq;
					Increment value for "index1-index2" in hop_dict;


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
def meetsCutoff(qscore:str, cutoff: int) -> bool:
    '''Takes quality score line for barcode as str input and cutoff value as int. Converts each character in string to Phred+33 score and checks if it meets cutoff. If all scores in string are >= cutoff, returns True, otherwise returns False.'''
    if char < cutoff:
		return False
	return True

Input: "')(+**&$"
Expected output: False
```
```
def format_header(header: str, index_pair: str) -> str:
    '''Takes fq header sequence and index1-index2 pair as separate strings. Appends index1-index2 pair to the end of the header line and returns new string.'''
    return header + index_pair

Input: "seq1","AAA-AAA"
Expected output: "seq1 AAA-AAA"
```