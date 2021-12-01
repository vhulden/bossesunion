#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 16:59:18 2017

@author: vilja

Combining St. Louis biographies from 1906 and 1912.


"""

import codecs, operator

firstfile = "../tabular/BookOfStLouisansInfo_1906.tsv"
secondfile = "../tabular/BookOfStLouisansInfo_1912.tsv"
writefile = "../tabular/BookOfStLouisansInfo_BothEds.tsv"


with codecs.open(firstfile,'r',encoding='utf-8') as f:
    firstlines = [[l.strip() for l in line.split('\t')] for line in f.read().splitlines()]

with codecs.open(secondfile,'r',encoding='utf-8') as f:
    secondlines = [[l.strip() for l in line.split('\t')] for line in f.read().splitlines()]
    
allines = firstlines[1:] + secondlines[1:] #first line is headers


culledlines = []


uniqdict = {}
for ll in allines[1:]: 
    #use last, first, birthyear as key; birthyear is more reliable than e.g. middle name,
    # ... esp. since father and son often have the same name
    mykey = ll[0]+ll[1]+ll[7]
    if mykey in uniqdict.keys():
        if len(''.join(uniqdict[mykey])) > ''.join(ll):
            uniqdict[mykey] = ll
    else:
        uniqdict[mykey] = ll

for key in uniqdict:
    culledlines.append(uniqdict[key])

culledlines.sort(key = operator.itemgetter(0, 1, 2))

# add id number for each line
idnumber = 0
for c in culledlines:
    idnumber += 1   
    c.insert(0,unicode(idnumber))

    
    

#headers from firstfile
headerline = firstlines[0]
headerline.insert(0,u'idnumber')
culledlines.insert(0,headerline)


culledtextlines = ['\t'.join(l) for l in culledlines]
culledtext = '\n'.join(l for l in culledtextlines)




with codecs.open(writefile,'w',encoding='utf-8') as f:
    f.write(culledtext)


#for idx,bl in enumerate(allines[1:]):
#    if bl[0] == allines[idx-1][0] and bl[1] == allines[idx-1][1]:
#        blline = ''.join(bl)
#        prevline = ''.join(allines[idx-1])
#        if len(blline) > len(prevline):
#            culledlines.append(bl)
#        else:
#            culledlines.append(allines[idx-1])
#        idx += 1
#    else:
#        culledlines.append(bl)