# The First
7/25/24:
**Part 2 pseudocode**
Use argparse for:
- R1, R2, R3, R4 fastq filenames
- qs_threshold
- matched index.txt filename
Possible useful functions:
- reverse complement
- Append barcodes to record headers
- Average quality score of index read
- Write record to file<br>

**First draft of pseudocode:**

```
#Create set of valid barcodes from text file
barcodes = {set of 24 barcodes}

#Create dictionaries to count number of pairs with matched indices, swapped
#indices, and unknown/low quality indices
matched_dict = {}
hop_dict = {}
unknown_dict = {}

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
				Increment value for "index1-index2" in unknown_dict;
			elif average quality score of either index read < cutoff :
				Write biological R1 record to unknownR1.fq
				Write bological R2 record to unknownR2.fq
				Increment value for "index1-index2" in unknown_dict;
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

Report number of pairs in each dict
```
---
7/27/24:
**Part 1 bash commands for data exploration**
First I got onto a Talapas compute node using `srun -A bgmp -p bgmp -N 1 -c 4 --mem=16G -t 0-3 --pty bash`.
I used `ls -lah` command inside the `/projects/bgmp/shared/2017_sequencing/` directory to check the sizes of the compressed fastq files. R1 and R4 are clearly the biological reads because they're the largest, while R2 and R3 are the index files:
```
-rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp  20G Jul 30  2018 1294_S1_L008_R1_001.fastq.gz
-rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp 2.6G Jul 30  2018 1294_S1_L008_R2_001.fastq.gz
-rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp 2.8G Jul 30  2018 1294_S1_L008_R3_001.fastq.gz
-rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp  21G Jul 30  2018 1294_S1_L008_R4_001.fastq.gz
```
I used the following command to check the lengths of the reads in each file:
`zcat <file.fq> | awk 'NR % 2 == 0 { print length($0) }'`
Here were my results:  
1294_S1_L008_R1_001.fastq.gz: 101  
1294_S1_L008_R2_001.fastq.gz: 8  
1294_S1_L008_R3_001.fastq.gz: 8  
1294_S1_L008_R4_001.fastq.gz: 101

I used `zcat <file.fq> | grep -A 1 --no-group-separator "^+" | grep -v "^+"` to look at the quality score lines in each file to determine the type of Phred encoding. Since there were hyphens and the greatest character seemed to be "J", I figured all of the files were encoded in Phred+33.   
/projects/bgmp/taro/bioinfo/Bi622/Demultiplex/Assignment-the-first  

First job (R1):
```
#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH --time=1-0
#SBATCH --mail-user=taro@uoregon.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=R1-run

/usr/bin/time -v ./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
    -r 101 \
    -o "R1"
```

Results:
```
	Command being timed: "./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r 101 -o R1"
	User time (seconds): 10943.08
	System time (seconds): 2.02
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 3:03:17
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 66288
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 294397
	Voluntary context switches: 2053
	Involuntary context switches: 15093
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```
R2 (Job 7705402):
```
#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 4
#SBATCH --mem=12G
#SBATCH --time=1-0
#SBATCH --mail-user=taro@uoregon.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=R2-run

/usr/bin/time -v ./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
    -r 8 \
    -o "R2"
```
Results:
```
Command being timed: "./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -r 8 -o R2"
User time (seconds): 1307.40
System time (seconds): 0.33
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 21:55.52
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 65708
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 0
Minor (reclaiming a frame) page faults: 47805
Voluntary context switches: 1605
Involuntary context switches: 1845
Swaps: 0
File system inputs: 0
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
```
R3 (Job 7705456):
```
#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 4
#SBATCH --mem=12G
#SBATCH --time=1-0
#SBATCH --mail-user=taro@uoregon.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=R3-run

/usr/bin/time -v ./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
    -r 8 \
    -o "R3"
```
Results:
```
Command being timed: "./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -r 8 -o R3"
User time (seconds): 1312.21
System time (seconds): 0.30
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 21:56.26
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 65836
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 0
Minor (reclaiming a frame) page faults: 47766
Voluntary context switches: 499
Involuntary context switches: 413
Swaps: 0
File system inputs: 0
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
```
R4 (Job 7705802):
```
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
```
Results:
```
Command being timed: "./Part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -r 101 -o R4"
User time (seconds): 10757.02
System time (seconds): 3.58
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 3:00:38
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 63860
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 0
Minor (reclaiming a frame) page faults: 100162
Voluntary context switches: 1781
Involuntary context switches: 3778
Swaps: 0
File system inputs: 0
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
```
![[DemultiplexPart1Jobs.png]]  

7/29/24:  
**Counting number of barcodes with "N" base calls in R2 and R3 files:**
```
zcat 1294_S1_L008_R2_001.fastq.gz | grep -A 1 --no-group-separator "^@" | grep -v "^@" | grep -c "N"
```
R2 Output: 3976613  
```
zcat 1294_S1_L008_R3_001.fastq.gz | grep -A 1 --no-group-separator "^@" | grep -v "^@" | grep -c "N"
```
R3 output: 3328051<br>

7/30/24:
**Part 2 unit test files**  
File names: `<R1,R2,R3,R4>-testfile.fq`
Index reads (denoted by header lines) that cover the following cases:
- Matched index pairs: (@seq2-2, @seq2-3), (@seq5-2, @seq5-3)
- Hopped index pairs: (@seq3-2, @seq3-3)
- Unknown index pairs: (@seq1-2, @seq1-3)
- Low quality index pairs (but valid):  (@seq4-2, @seq4-3)  

**Final draft of pseudocode**
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
# The Third
8/3/24
Just for convenience, here are some file paths I use a lot: <br>
`/projects/bgmp/shared/2017_sequencing/indexes.txt`<br>
`/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz`<br>
`/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz`<br>
`/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz`<br>
`/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz`<br>
`/projects/bgmp/taro/bioinfo/Bi622/Demultiplex/`<br>
Ideas for writing to 52 files while only opening them once:
- For files that need to be opened for writing, first make a list of file names based on the barcodes in the indexes.txt file. Create a dictionary where keys will be the string filenames, and the values will be the file handles (i.e. `open(<filename>)` objects). Iterate over your list and open each file, then store the file handle in the dictionary with the key as the filename. After you're done writing to all the files, you can have another for loop at the end of your code that will close all the file handles in the dictionary.
- Maybe you could implement the above with a "try-finally" block as described here: https://stackoverflow.com/questions/8990387/close-all-open-files-in-ipython

For the useful output, I just had the idea that it might be helpful to show the frequency of pairs that were matched but didn't meet the cutoff (placed into the "unknown" files) compared to the number of matched and high quality pairs. 

**First issue with `demultiplex.py`**:
I just realized that I created the test files incorrectly according to my algorithm- it turns out that most of the index reads I selected did not meet the per base quality score cutoff of 30, so the reads I'd designated as hopped and matched were actually outputted to the "unknown" files. Now, I'm concerned I may have set the per base cutoff too high. That's why I got the idea to compare the number of "matched but low quality"  vs "matched and high quality" pairs to determine if I might be filtering too much data.<br>

==I corrected the quality scores in my R2 and R3 test files, and now I'm seeing the expected output from my `demultiplex.py` script. Whether I want to adjust my quality score cutoff remains to be seen.==
<br>
Output from command `./demultiplex.py -t /projects/bgmp/shared/2017_sequencing/indexes.txt -c 30 -R1 R1-testfile.fq.gz -R2 R2-testfile.fq.gz -R3 R3-testfile.fq.gz -R4 R4-testfile.fq.gz`:
```
Matched pairs: {'AACAGCGA-AACAGCGA': 1, 'TCTTCGAC-TCTTCGAC': 1}
Hopped pairs: {'CGGTAATC-AACAGCGA': 1}
Unknown ct: 2
```
The above shows the expected results from my test files. I still need to create an end report for the user through figures and stats. 

8/7/24:
I ran the demultiplexing Python script with the actual input files using my `demultiSLURM.sh` script. Here were my /usr/bin/time -v results:
```
Command being timed: "./demultiplex.py -t /projects/bgmp/shared/2017_sequencing/indexes.txt -c 30 -R1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -R2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -R3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -R4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
User time (seconds): 3728.83
System time (seconds): 38.09
Percent of CPU this job got: 89%
Elapsed (wall clock) time (h:mm:ss or m:ss): 1:10:09
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 248856
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 0
Minor (reclaiming a frame) page faults: 38597
Voluntary context switches: 48587
Involuntary context switches: 9102
Swaps: 0
File system inputs: 0
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
```

The run finished successfully and my output statistics in `user-report.txt` seem to align with the expected results. 