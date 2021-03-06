#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:56:24 2019

@author: vilja
"""

import numpy as np
from math import sqrt # You may need this function
import heapq



# Some made-up toy word vectors 

vec = {}

vec['man'] = [1,2,3,4,5] 
vec['woman'] = [6,7,8,9,10] 
vec['king'] = [-5,-4,-3,-2,-1] 
vec['queen'] = [0,1,2,3,4]

vec['dog'] = [-10.2,-3.2,-2.3,-4.3,3.1] 
vec['cat'] = [-8.3,-3.01,-2.0,-1.3,1.1] 
vec['rabbit'] = [-5.2,-2.1,-4.3,1.0,2.0] 
vec['squirrel'] = [2.9,0.1,0.3,2.0,1.5]

for k in vec:
    vec[k] = np.array(vec[k])


def sim(vec1,vec2):
    vecdot = np.dot(vec1,vec2)
    vecnormmultiply = np.sqrt(np.dot(vec1,vec1)) * np.sqrt(np.dot(vec2,vec2))
    result = vecdot / vecnormmultiply
    return result

def find_closest(word,vecarray):
    wordvec = vecarray[word]
    simarray = {}
    for k in vecarray:
        if k != word:
            measure = sim(wordvec,vecarray[k])
            simarray[measure] = k
    bestvalue = max(simarray)
    bestmatch = simarray[bestvalue]
    return bestmatch
    

def find_similar(word,howmany,vecarray):
    wordvec = vecarray[word]
    simarray = {}
    for k in vecarray:
        if k != word:
            measure = sim(wordvec,vecarray[k])
            simarray[measure] = k
    bestvalues = heapq.nlargest(howmany,simarray)
    bestlist = [simarray[b] for b in bestvalues]
    return bestlist



#print(find_similar('cat',5,vec))

#def analogy(pair1a,pair1b,pair2a,vecarray):
#    #sim(x,b-a+c)
#    #a:b :: c:x
#    vec1a = vecarray[pair1a]
#    vec1b = vecarray[pair1b]
#    vec2a = vecarray[pair2a]
#    secondterm = vec1b - vec1a + vec2a
#    simarray = {}
#    for k in vecarray:
#        if k != pair2a:
#            measure = sim(vecarray[k],secondterm)
#            simarray[measure] = k
#    bestvalue = max(simarray.keys())
#    bestmatch = simarray[bestvalue]
#    return bestmatch

def analogy(a, b, c, vecarray):
    #sim(x,b-a+c)
    #a:b :: c:x
    va, vb, vc = vecarray[a], vecarray[b], vecarray[c]
    secondterm = vb - va + vc
    simarray = {word:sim(vecarray[word],secondterm) for word in vecarray if word != c}
    return(max(simarray, key = simarray.get))

    
#this of course does not work because the SVD has messed up the counts.
#def get_context_words(word,howmany,vecarray,reversed_tokendict):
#    contextwordvals = vecarray[word]
#    bestvalues = heapq.nlargest(howmany,contextwordvals)
#    contextcodes = [list(vecarray[word]).index(i) for i in bestvalues]
#    bestlist = [reversed_tokendict[contextcode] for contextcode in contextcodes]
#    return bestlist


# Now implement three functions:
# 1. sim()
# 2. find_closest()
# 3. analogy()
#
# Run the following:
#print(sim(vec['cat'], vec['squirrel'])) #< sanity check, should be -0.7324574388673762
#print(sim(vec['cat'], vec['dog']))
#print "closest to rabbit is:", 
#print(find_closest('rabbit', vec))# < sanity check, should be "cat"
#print "closest to cat is:", 
#print(find_closest('cat', vec))
#print "closest to dog is:", 
#print(find_closest('dog', vec))
#print "closest to king is:", 
#print(find_closest('king', vec))
#
#print "man is to woman as king is to:",
#print(analogy('man','woman','king', vec))# < sanity check, should be "queen"
#print "woman is to man as queen is to:",
#print(analogy('woman','man','queen', vec))
#
#print "rabbit is to dog as squirrel is to:",
#print(analogy('rabbit','dog','squirrel', vec))