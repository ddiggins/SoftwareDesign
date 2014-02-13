# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Devynn Diggins
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons

import random
from random import shuffle

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """ 

    acids = "" #String designation for amino acid sequence
    dna = list(dna)
    for nucleotide in range(0,len(dna),3): #Establishes codon range
        codon = dna[nucleotide:nucleotide+3]
        codon = collapse(codon) #Collapses codon list into codon sets
        for el in range(len(codons)): #Traverses main list within codons
            for element in range(len(codons[el])): #Traverses sublists in codons
                if codon == codons[el][element]:
                    acid = aa[el] #Returns amino acid of same value of main list if true
                    acids = acids + acid
    return acids #Creates a sequence of all acids


#coding_strand_to_AA('TTTTGTCATTGA')


def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
    
    result = coding_strand_to_AA('TTTTGTCATTGA')    
    print "INPUT: TTTTGTCATTGA, EXPECTED OUTPUT: FCH|, OUTPUT: " + result #prints input, expected output, and actual output provided by function 

    result2 = coding_strand_to_AA('TACGCGTATATCGACATAGATATTACA') #Another input test
    
    print "INPUT: TACGCGTATATCGACATAGATATTACA, EXPECTED OUTPUT: YAYIDIDIT, OUTPUT: " + result2

#coding_strand_to_AA_unit_tests()

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    
    dna = list(dna) #converts string into a list to be reversed
    dna = dna[::-1] #reverses list of dna

    for letter in range(len(dna)): #Takes each letter replaces with opposite nucleotide
        if dna[letter] == 'A': #A <=> T and C <=> G in all cases
            dna[letter] = 'T'
        elif dna[letter] == 'T':
            dna[letter] = 'A'
        elif dna[letter] == 'G':
            dna[letter] = 'C'
        elif dna[letter] == 'C':
            dna[letter] = 'G'
    
    return collapse(dna) #returns the collapsed reversed compliment DNA strand

    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
        
    result = get_reverse_complement('GATTACA') #This was a pretty good movie
    print "Input: GATTACA, Expected Output: TGTAATC, Output: " + result
    
    result2 = get_reverse_complement('TAGACAT')
    print "Input: TAGACAT, Expected Output: ATGTCTA, Output: " + result2
    
#get_reverse_complement_unit_tests()

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    codonlist = "" #Creates empty string for codon addition
    dna = list(dna) #Converts string to list
    for nucleotide in range(0,len(dna),3): #Establishes codon range   
        codon = dna[nucleotide:nucleotide+3]
        codon = collapse(codon)
        if codon == 'TAG': #Looks for end codon and returns codonlist if found
            return codonlist
        else: #Otherwise adds codon to current codon list
            codonlist = codonlist + codon 
    return codonlist #codonlist returned if no end codon is ever found


def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
        
    result = rest_of_ORF('ATGGTCCATTAGATA') #Test while using end codon
    print "Input: ATGGTCCATTAGATA, Expected Output: ATGGTCCAT, Output: " + result
    
    result2 = rest_of_ORF('ATGGATCATTAT') #Test without using end codon
    print "Input: ATGGATCATTAT, Expected Output: ATGGATCATTAT, Output: " + result2

#rest_of_ORF_unit_tests()

        
def find_all_ORFs_oneframe(dna, startstep):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        startstep: 
        returns: a list of non-nested ORFs
    """
    codonlist = [] #Creates empty string for codon addition
    dna = list(dna) #Converts string to list
    for nucleotide in range(startstep,len(dna),3): #Establishes codon range
        codon = dna[nucleotide:nucleotide+3]
        codon = collapse(codon)
        if codon == 'ATG':
            add = rest_of_ORF(dna[nucleotide:len(dna)])
            codonlist.append(add) #Uses rest_of_ORF to find... the rest of the ORF
            dna = dna[(nucleotide+len(add)):len(dna)] #Moves past range of previous amino sequence to avoid double registering ATG start codons
    return codonlist 

def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """

    result = find_all_ORFs_oneframe('CGCATGCGTATCCGGTAGAGGATGCAGGATTAGAGA', 0) #Multiple ORFs with unused letters between end/start codons
    print "Input: CGCATGCGTATCCGGTAGAGGATGCAGGATTAGAGA, Expected Output: ['ATGCGTATCCGG','ATGCAGGAT'], Output: " + str(result)

    result2 = find_all_ORFs_oneframe('ATGTAGGATTAGATGATGTAG', 0) #Testing ATGs one after another in sequence will not be interpreted as multiple codons
    print "Input: ATGTAGGATTAGATGATGTAG, Expected Output: ['ATG', 'ATGATG'], Output: " + str(result2)


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    mastercodonlist = [] #Starts w/ empty list
    for i in range(0,3):
        mastercodonlist = mastercodonlist + find_all_ORFs_oneframe(dna,i) #Loops ORF_oneframe function for offset steps of 0, 1, and 2 
    return mastercodonlist

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
        
    result = find_all_ORFs('ATGGATGATTAGCCAGTAGAA') #Input with ATGs and TAGs with offsets of 0, and 1
    print "Input: 'ATGGATGATTAGCCAGTAGAAATGTAGAA', Expected Output: ['ATGGATGAT', 'ATGATTAGCCAG'], Output: " + str(result)
    
    
    result2 = find_all_ORFs('TATGAATGATACATG') #Input with ATGs in all offsets but no TAGs
    print "Input: 'TATGAATGATACATG', Expected Output: ['ATG', 'ATGAATGATACATG', 'ATGATACATG'], Output: " + str(result2)


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    masterlist = find_all_ORFs(dna) #Creates a list of the ORFs of dna
    reverse = get_reverse_complement(dna) #Computes the reverse of DNA
    masterlist += find_all_ORFs(reverse) #Concatenates the original matrix with the ORFs of the reverse
    return masterlist

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    result = find_all_ORFs_both_strands('ATGTAGCTACAT') #Inputs a ATGTAG and its converse to get the same result forwards and backwards
    print "Input: 'ATGTAGCTACAT', Expected Output: ['ATG', 'ATG'], Output: " + str(result)
    
    result2 = find_all_ORFs_both_strands('CTACATATGTAG') #Inputs a ATGTAG and its converse to get the same result forwards and backwards
    print "Input: 'CTACATATGTAG', Expected Output: ['ATG', 'ATG'], Output: " + str(result2)

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""

    masterlist =  find_all_ORFs_both_strands(dna)#Finds all ORFs and sorts into a list'
    if len(masterlist)>0:
        return collapse(max(masterlist,key = len))#Finds the ORF with the maximum length and returns it!
    else:
        return ""

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """

    result = longest_ORF('ATGTCGAGCAGGTAGCTACAT') #Input with forward codon being the largest
    print "Input: 'ATGTCGAGCAGGTAGCTACAT', Expected Output: ATGTCAGAGCAGG, Output: " + result


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    
    maxORFs = []    #Establishes a blank list to hold the ORFs calculated in the function
    
    for i in range(0,num_trials): #range set to loop number of trials
        dna = list(dna) 
        shuffle(dna) #Shuffles the listed DNA
        dna = collapse(dna)
        maxORFs.append(longest_ORF(dna)) #Adds the longest ORFs of the shuffled DNA to the maxORFs list
    
    return len(max(maxORFs, key = len))
        
    
#print longest_ORF_noncoding('ATGAGCTGACGGTAGCTAGCTTGGATGGTATGTAAGTTTGAGTGTATGTCATCGATCGAGTCTAGCTTCGATCGTACGTATCGATCTGGGGCGCTATCTGCTACGATCGTSGCTAGTCTGGG', 1500)

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    totalaminoacids = [] #Empty list for amino acids generated later

    longvectors = find_all_ORFs_both_strands(dna) #sets elements i to be the ORFs calculated by the previous function
    for i in longvectors:
        if len(i) > threshold: #if the length of ORF is greater than the threshold, lets pass
            aminos = coding_strand_to_AA(i)
            totalaminoacids = totalaminoacids + [aminos] #converts codon sequence to amino acid and dumps it into totalaminoacids
    return totalaminoacids


#print gene_finder('ATGAGCTGACGGTAGCTAGCTTGGATGGTATGTAAGTTTGAGTGTATGTCATCGATCGAGTCTAGCTTCGATCGTACGTATCGATCTGGGGCGCTATCTGCTACGATCGTSGCTAGTCTGGG', 2)