#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:32:17 2019

@author: vilja

Read files from directory, create two-vocabulary embeddings matrix

        cat     mouse     dog
     
cat

mouse

dog

cat*

mouse*

dog*


The idea is to compare the contexts of words from two different corpora (written
for labor newspapers and other newspapers.)

The vocabulary is made up of the (5000?) most frequent words in the "target" 
corpus (in this case labor papers) - excluding words that do not appear in the 
other corpus at all. (Considering the target corpus makes sense for two reasons:
    first, it's of interest, and second, it's likely to be smaller than the 
    comparison corpus, so words super-prominent in it but not in the comparison
    corpus would never make it.)

Punctuation and stopwords are removed, all words are lowercased.

The resulting SVD is saved to a file, along with three vector arrays: the one
with all the vocabulary (target-marked and comparison), the one with target 
only, and the one with comparison only. (It's handy to have separate ones
so can check "most-similar" across vocabularies or within one.)

"""

import numpy as np
import sys, os, re
import codecs, pickle
import quizscript as qs
import time
from tqdm import tqdm

start = time.time()

snmetadatafile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/sninfo-selected.tsv"
readdir = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/ocrtxts/"



stopwordsf = '/Users/vilja/work/research/digital/classification/english-stopwords.txt'

with open(stopwordsf) as f:
    stopwords = f.read().splitlines()
    addstops = ['tbe','nnd','aud']
    stopwords += addstops
    
#stopwords = [] #if want to remove use of stopwordsm otherwise comment out

trunc = 20000 #max size of vocabulary - center words double this
context = 7 #size of context window
targetc = 'LABOR' #what we're looking for in the file name to indicate target corpus

corpusmark = 'L_' #what to mark target corpus words with
snregex = re.compile('^\d+_(.*?)_') #to get sn (paper id) from filename


#make dictionary sn:affliation,
#e.g. sn78000395: LABOR
#can be used to look up affiliation of files from different corpora
snclasses = {}

with codecs.open(snmetadatafile,'r',encoding='utf-8') as f:
    for line in f: 
        l = line.strip().split('\t')
        sn = l[0].strip()
        affiliation = l[1].strip()
        snclasses[sn] = affiliation
        
#remove all punctuation from tokens
punct = re.compile('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]')

                     
""" Above is preliminaries, actual processing starts below """
                     
#create tokencounts for culling
#separate counts dictionaries for the two corpora        
tokencounts_T = {}
tokencounts = {}

print "Reading files for tokendict..."
sys.stdout.flush()

for item in tqdm(os.listdir(readdir)):
#    print ".",
    match = snregex.search(item)
    if match:
        sn = match.group(1)
    else: continue
    with codecs.open(readdir+item,'r',encoding='utf-8') as f:
        texttokens = [punct.sub('',t.lower()) for t in f.read().split()]
        if snclasses[sn] == targetc:
            #mark tokens and put them in the target corpus counts
            for t in texttokens:
                if t not in stopwords and len(t.strip()) > 1:
                    mt = corpusmark+t
                    tokencounts_T[mt] = tokencounts_T.get(mt,1) + 1
        else:
            #don't mark tokens and put them in the main corpus counts
            for t in texttokens:
                if t not in stopwords and len(t.strip()) > 1:
                    tokencounts[t] = tokencounts.get(t,1) + 1
                
        


#take most frequent from target corpus - how many? trunc, above in preliminaries
#but only keep the ones that are in the main corpus as well
#duplicate marked and unmarked
                
tokens_T = sorted(tokencounts_T,key=tokencounts_T.get,reverse=True)[:trunc] 
tokensmarked = [t for t in tokens_T if t[len(corpusmark):] in tokencounts]
tokensunmarked = [t[len(corpusmark):] for t in tokensmarked]
alltokens = sorted(tokensunmarked) + sorted(tokensmarked)

#make a token dictionary only with most frequent words
#note that it's important above to have unmarked first and marked after since
#otherwise the index for x axis of matrix will be exceeded
tokendict = {t:idx for idx,t in enumerate(alltokens)} #real




print "\nTokendict done." 
sys.stdout.flush()


#make a matrix

size = len(tokensmarked)
doublesize = size * 2
matrix = np.zeros((doublesize,size))

#add a row of 1s and a col of 1s so that rowsum and colsum can never be zero,
#so won't get errors with dividing by zero
dummyrow = [1 for i in range(size)]
dummycol = [[1] for i in range(doublesize+1)] # +1 because there is a dummyrow
#matrix = np.insert(matrix,size,dummyrow,axis=0) #also have to have halfway because there have to be two separate colsums
matrix = np.append(matrix,[dummyrow],axis=0)
matrix = np.append(matrix,dummycol,axis=1)



#then need to loop over files again to get the context counts for the matrix

print "Reading files for context counts..."
sys.stdout.flush()

for item in tqdm(os.listdir(readdir)):
#    print ".",
    match = snregex.search(item)
    if match:
        sn = match.group(1)
    else: continue
    with codecs.open(readdir+item,'r',encoding='utf-8') as f:
        #tokens is all words, minus punctuation, from a single file
        #loop through it so w1 is center word and w2 is context word
        tokens = [punct.sub('',t.lower()) for t in f.read().split()]
        for idx in range(len(tokens)):
            w1 = tokens[idx]  
            if w1 not in tokendict: continue #because not all will be when it's truncated
            if snclasses[sn] == targetc:
                w1code = tokendict[corpusmark+w1]
            else:
                w1code = tokendict[w1]
            for j in range(idx-context,idx+context+1):
                if j < 0 or j == idx or j > len(tokens) - 1: continue
                w2 = tokens[j]
                if w2 not in tokendict: continue
                w2code = tokendict[w2]
                matrix[w1code,w2code] += 1




#get the total word count of each corpus   
#and use them to create a factor by which to scale the counts
#in the matrix of raw counts
#because there are two separate corpora, the larger one dominates otherwise 
totalwords_comp = float(sum(tokencounts.values())) 
totalwords_target = float(sum(tokencounts_T.values())) 
factor_comp = (totalwords_comp + totalwords_target) / totalwords_comp
factor_target = (totalwords_comp + totalwords_target) / totalwords_target





#make a weighted matrix out of the raw counts matrix
#so as to compensate for different sizes of corpora

weighted_matrix = np.zeros((doublesize+1,size+1)) #because the dummyrow/cols are there
for i in range(doublesize+1):
    for j in range(size+1):
        if i < size:
            weighted_matrix[i,j] = matrix[i,j] * factor_comp
        else:
            weighted_matrix[i,j] = matrix[i,j] * factor_target


print "\nCounts matrix done and weighted." 
sys.stdout.flush()


#matrixsum = np.sum(matrix)
#    
#pmatrix = matrix/np.sum(matrix)
#
#rowsums = [np.sum(pmatrix[i,:]) for i in range(doublesize)]
#colsums = [np.sum(pmatrix[:,i]) for i in range(size)] #only single set of vocab in columns
#colsums_c = [np.sum(pmatrix[:size,i]) for i in range(size)]
#colsums_t = [np.sum(pmatrix[size:,i]) for i in range(size)]
#
#
#ppmimatrix = np.zeros((doublesize,size)) 
#
#for i in range(doublesize):
#    rowsum = rowsums[i]
#    for j in range(size): #the other half should be empty
#        if i < doublesize: colsum = colsums_c[j] 
#        else: colsum = colsums_t[j] +1
#        ppmimatrix[i,j] = max(0, np.log2((pmatrix[i,j] / (rowsum * colsum))))


#matrixsum = np.sum(weighted_matrix)
#    
#pmatrix = weighted_matrix/np.sum(weighted_matrix)
#
#rowsums = [np.sum(pmatrix[i,:]) for i in range(doublesize)]
#colsums = [np.sum(pmatrix[:,i]) for i in range(size)] #only single set of vocab in columns
#colsums_c = [np.sum(pmatrix[:size,i]) for i in range(size)]
#colsums_t = [np.sum(pmatrix[size:,i]) for i in range(size)]
#
#
#ppmimatrix = np.zeros((doublesize,size)) 
#
#for i in range(doublesize):
#    rowsum = rowsums[i]
#    for j in range(size): #the other half should be empty
#        colsum = colsums[j] 
#        ppmimatrix[i,j] = max(0, np.log2((pmatrix[i,j] / (rowsum * colsum))))

matrixsum = np.sum(weighted_matrix)
rowsums = weighted_matrix.sum(axis = 1)
colsums = weighted_matrix.sum(axis = 0)

pij = weighted_matrix/matrixsum
pistar = rowsums/matrixsum
pstarj = colsums/matrixsum

ppmimatrix = np.log2(np.maximum(pij/np.outer(pistar, pstarj), np.ones(np.shape(pij))))

print "PPMI matrix done." 
sys.stdout.flush()


U, s, VT = np.linalg.svd(ppmimatrix, full_matrices=False)
SVD = np.dot(U, np.diag(s))
#SVD = U

SVDT = SVD[:,:100]

print "SVD created." 
sys.stdout.flush()

vecarrayall = {}
vecarray_target = {}
vecarray_comp = {}
for token in tokendict:
    vecarrayall[token] = SVDT[tokendict[token]] 
    if token.startswith(corpusmark):
        vecarray_target[token] = SVDT[tokendict[token]]
    else:
        vecarray_comp[token] = SVDT[tokendict[token]]
    
print "Vector array created." 
sys.stdout.flush()
    
#print(qs.find_similar('and',10,vecarray))


end = time.time()

print "Save stuff: countsmatrix, SVD, vecarrayall,vecarray_target,vecarray_comp, tokencounts, tokencounts_T, tokendict"
sys.stdout.flush()

np.save('../countsmatrix_20K_2',matrix)

np.save('../SVD_20K_2',SVD)

with codecs.open('../vecarrayall_20K.pkl_2','wb') as f:
    pickle.dump(vecarrayall,f)

with codecs.open('../vecarray_target_20K_2.pkl','wb') as f:
    pickle.dump(vecarray_target,f)
    
with codecs.open('../vecarray_comp_20K_2.pkl','wb') as f:
    pickle.dump(vecarray_comp,f)

with codecs.open('../tokencounts_20K_2.pkl','wb') as f:
    pickle.dump(tokencounts,f)
    
with codecs.open('../tokencounts_T_20K_2.pkl','wb') as f:
    pickle.dump(tokencounts_T,f)

with codecs.open('../tokendict_20K_2.pkl','wb') as f:
    pickle.dump(tokendict,f)

print(end-start)
#print(qs.analogy('man','woman','business',vecarray)

   






