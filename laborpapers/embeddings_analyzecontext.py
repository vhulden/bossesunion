#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:15:41 2019

@author: vilja

Get context words for a set of words of interest using tokendict and the 
matrix of raw counts, produced and saved by embeddings.py.
"""

import codecs,pickle
import numpy as np
from tqdm import tqdm
import heapq, operator
import embeddingtools as et

tokendictfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/tokendict_20K_2.pkl"
countsmatrixfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/countsmatrix_20K_2.npy"
wordfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/frequentwordslist.txt"
contextwordsfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/contextwords_ignore.tsv"

corpusmark = "L_"
howmany = 25 #how many context words we want

with codecs.open(tokendictfile, 'rb') as f:
    tokendict = pickle.load(f)

countsmatrix = np.load(countsmatrixfile)

print "Counts matrix and token dictionary loaded."

#read words into a list plus create a version that is 
#marked with the corpus mark, so can get both vocabularies, comparison and target
with codecs.open(wordfile,'rb') as f:
    ws = f.read().splitlines()
    markedws = [corpusmark+w for w in ws]

words = ws + markedws

#reversing from http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/
tokendict_reversed = dict([[v,k] for k,v in tokendict.items()])
    

# getting index of largest values in list is taken from here:
#https://stackoverflow.com/questions/13070461/get-index-of-the-top-n-values-of-a-list-in-python
contextdict = {}
for word in tqdm(words):
    try:
        wordcode = tokendict[word]
        wordcontextvector = list(countsmatrix[wordcode]) #use wordcode as row number 
        contextcodes = list(zip(*heapq.nlargest(howmany, enumerate(wordcontextvector), key=operator.itemgetter(1)))[0])
        contextwords = [tokendict_reversed[contextcode] for contextcode in contextcodes]
        contextdict[word] = contextwords
    except:
        continue

contextlines = []
for k in contextdict:
    contextline = k + "\t" + "\t".join(contextdict[k])
    contextlines.append(contextline)

contextwordstext = "\n".join(contextlines)

with codecs.open(contextwordsfile,'w',encoding='utf-8') as f:
    f.write(contextwordstext)
