#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:24:33 2019

@author: vilja

This reads in the SVD and vecarrays created in embeddings.py so as to be able to
do some analyses of them.

"""

import numpy as np
#import sys, os, re
import codecs, pickle, heapq, sys,os
import embeddingtools as et
from tqdm import tqdm



corpusmark = 'L_' #what target words are marked with
trunc = 20000

SVDfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/SVD_20K_2.npy"
vecarrayfullfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/vecarrayall_20K_2.pkl"
vecarraytargetfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/vecarray_target_20K_2.pkl"
vecarraycompfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/vecarray_comp_20K_2.pkl"
tokencountsfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/tokencounts_20K_2.pkl"
tokencountsTfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/tokencounts_T_20K_2.pkl"

savedfrequentsanalysis = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/frequents_analyzed_withsimilarity.tsv"

#remove because it's written into by appending
if os.path.exists(savedfrequentsanalysis):
    os.remove(savedfrequentsanalysis)


print "Load files..."
sys.stdout.flush()

SVD = np.load(SVDfile)
SVDT = SVD[:,:100]

with codecs.open(vecarrayfullfile,'rb') as f:
    vecarrayfull = pickle.load(f)
    
with codecs.open(vecarraytargetfile,'rb') as f:
    vecarraytarget = pickle.load(f)
    
with codecs.open(vecarraycompfile,'rb') as f:
    vecarraycomp = pickle.load(f)
    
with codecs.open(tokencountsfile,'rb') as f:
    tokencounts = pickle.load(f)

with codecs.open(tokencountsTfile,'rb') as f:
    tokencounts_T = pickle.load(f)
    



print "Calculate similar vectors..."

sys.stdout.flush()

#calculate similar vectors - which words in target corpus and comparison corpus (L_word,word)
#have vectors that are the most similar and the most different

meaningsims = {}

for wordT in tqdm(vecarraytarget):
    wordC = wordT[len(corpusmark):]
    wordTvec = vecarraytarget[wordT]
    wordCvec = vecarraycomp[wordC]
    similarity = et.sim(wordTvec,wordCvec)
    meaningsims[wordC] = similarity #use the non-marked version 


most_similar = heapq.nlargest(500,meaningsims,key=meaningsims.get)
most_dissimilar = heapq.nsmallest(500,meaningsims,key=meaningsims.get)


most_similar_vals = {w:meaningsims[w] for w in most_similar}
most_dissimilar_vals = {w:meaningsims[w] for w in most_dissimilar}

"Figure out frequent words in each corpus..."
sys.stdout.flush()

#Besides similarity, figure out which words are particuilarly frequent in each
#corpus. 
#Note that there is some messing around with the corpusmark so as to make the lists
#consist of the same words (so that can process stuff more easily later) 
#but nevertheless be able to look up the counts in the dictionary.

#floats so divisions don't result in just zeroes

howmany = 10 #how many most frequent words, just so don't have to change inmlutiple places


totalwords_comp = float(sum(tokencounts.values())) #len(tokencounts)  
totalwords_target = float(sum(tokencounts_T.values())) #len(tokencounts_T) 

tokencounts_weighted = {k:v/totalwords_comp for k,v in tokencounts.items()}
tokencounts_T_weighted = {k:v/totalwords_target for k,v in tokencounts_T.items()}


mostfrequent_comp = heapq.nlargest(howmany,tokencounts_weighted,key=tokencounts_weighted.get)
mostfrequent_target = [w[len(corpusmark):] for w in heapq.nlargest(howmany,tokencounts_T_weighted,key=tokencounts_T_weighted.get)]

mostfrequent_comp_vals = {w:tokencounts_weighted[w] for w in mostfrequent_comp}
mostfrequent_target_vals = {w:tokencounts_T_weighted[corpusmark+w] for w in mostfrequent_target}

frequentwordsinboth = list(set(mostfrequent_comp) & set(mostfrequent_target))

frequentincomponly = list(set(mostfrequent_comp) - set(mostfrequent_target))
frequentintargetonly = list(set(mostfrequent_target) - set(mostfrequent_comp))



print "\nCreate dictionary with similar calculations and examples..."
sys.stdout.flush()

frequents_ofinterest = frequentwordsinboth + frequentintargetonly
numberfreqs = 10
frequentsanalysis = {}
joiner = '\t' #what to join the lists with
for item in tqdm(frequents_ofinterest):
    try:
        itemfreq_comp = tokencounts_weighted.get(item,0)
        itemfreq_target = tokencounts_T_weighted.get(corpusmark+item,0)
        freq_diff = itemfreq_target - itemfreq_comp
        similarity = meaningsims[item]
        similars_comp = et.find_similar(item,numberfreqs,vecarraycomp)
        similars_target = et.find_similar(corpusmark+item,numberfreqs,vecarraytarget)
        similars_full_c = et.find_similar(item,numberfreqs,vecarrayfull)
        similars_full_t = et.find_similar(corpusmark+item,numberfreqs,vecarrayfull)
        frequentsanalysis[item] = [item, str(itemfreq_comp),str(itemfreq_target),str(freq_diff),str(similarity),joiner.join(similars_comp),joiner.join(similars_target),joiner.join(similars_full_c),joiner.join(similars_full_t)]   
    except:
        continue


print "\nSave the similar calcs and examples dictionary into csv..."

empty = ['']*9
firstline = ['word','itemfreq_comp','itemfreq_target','freq_diff','similarity','similars_comp'] + empty + ['similars_targets'] + empty+ ['similars_full_c'] + empty + ['similars_full_t'] + empty
firstline = joiner.join(firstline) + '\n'
with codecs.open(savedfrequentsanalysis,'a',encoding='utf-8') as f:
    f.write(firstline)
for key in tqdm(frequentsanalysis):
    line = joiner.join(frequentsanalysis[key]) + '\n'
    with codecs.open(savedfrequentsanalysis,'a',encoding='utf-8') as f:
        f.write(line)
        
        

