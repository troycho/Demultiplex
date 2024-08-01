#!/usr/bin/env python

# Author: <Tayana Roychowdhury> <taro@uoregon.edu>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.4"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = "ACTGN"
RNA_bases = "ACUGN"

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    """Takes phred_score string as parameter. Returns average quality score of the whole phred string."""
    score_sum: int = 0
    for letter in phred_score:
        score_sum += convert_phred(letter)
    return score_sum/len(phred_score)

def validate_base_seq(seq: str, RNAflag: bool=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    return set(seq).issubset(RNA_bases) if RNAflag else set(seq).issubset(DNA_bases)


def gc_content(seq: str, RNAflag: bool=False) -> float:
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(seq, RNAflag), "String contains invalid characters- are you sure you used a nucleotide sequence?"
    seq = seq.upper()
    gc_sum = seq.count("G") + seq.count("C")
    return gc_sum/len(seq)

def calc_median(lst: list) -> float:
    '''Given a sorted list, returns the median value of the list.'''
    if len(lst) % 2 == 1: #length of list is odd
        median = lst[int(len(lst)/2)]
    else:
        first = lst[int((len(lst)-1)/2)]
        second = lst[int(((len(lst)-1)/2)+1)]
        median = (first+second)/2
    return median

def oneline_fasta(file: str, out_file: str) -> None:
    '''Takes path to FASTA file and output file name as arguments. Converts each record in file to single-line FASTA record and writes to out_file. 
    Returns None.'''
    with open(file, "r") as fh, open(out_file, "w") as wf:
        first_time: bool=True
        for line in fh:
            if first_time:
                wf.write(line)
                first_time = False
            elif ">" in line:
                wf.write(f'\n{line}')
            else:
                wf.write(line.strip("\n"))

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("Hi there!") == False, "Validate base seq fails to recognize nonDNA"
    assert validate_base_seq("Hi there!", True) == False, "Validate base seq fails to recognize nonDNA"
    print("Passed DNA and RNA tests")
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
