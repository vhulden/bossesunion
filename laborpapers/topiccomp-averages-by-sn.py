#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Apr 28, 2019

@author: vilja

This is another version of addsnstopics-revised; this one does not have 
clusters or chunks and simply deals with the different affiliations (labor, dem, gop, etc.)

The filenames identify which is which - type, sn, etc. There are in this version
no cases where same sn can have two types, as would be the case with reprint/non.

The idea is to enable seeing e.g. if particular topics are prominent in 
particular SNs, and whether there is a difference by paper type (affiliation).
"""

import re, codecs,sys,os

topiccompfile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/topicmodeled/laboretal_70_composition-2.tsv"
snmetadatafile = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/sninfo-selected.tsv"
writefilecombinesnavgs = "/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/topicssummedbysn-laboretal-70-2.tsv"

#   because writing with 'a' flag below 
if os.path.exists(writefilecombinesnavgs):
    os.remove(writefilecombinesnavgs)
    

print "Read the SN metadata file into a dictionary"
sys.stdout.flush()

snmetadata = {}

with codecs.open(snmetadatafile,'r',encoding='utf-8') as f:
    for line in f: 
        l = line.strip().split('\t')
        sn = l[0].strip()
        snmetadata[sn] = snmetadata.get(sn, []) + l

#it's date_sn_rest:  19091020_sn84759937
snregex = re.compile('([0-9]+)_([A-Za-z0-9]+)_')

#the composition file has the full path, that just makes things complicated. removed below.
fnbegjunk = 'file:/Users/vilja/work/research/digital/newspapers-reprints/labor-compare-lawcha/ocrchunks/'

#newtopiccomplines = []

counts = 0
#sntopicdict's role is to create a representation where all topic weights are 
# added to the dictionary entry of a particular sn
# like so:
# {sn: 
#    [topweight1, topweight2, ...],
#    [topweight1, topweight2, ...], ...}
sntopicsdict = {}
print "Starting to add sns to topics and write to file"
sys.stdout.flush()

with codecs.open(topiccompfile,'r',encoding='utf-8') as f1:
    for line in f1:
        li = line.strip().split('\t')
        if counts%10 == 0: print "Processing topic line {0}".format(counts),
        counts +=1
        sys.stdout.flush()
        filename = re.sub(fnbegjunk,'',li[1])
        snmatch = snregex.search(filename)
        if snmatch:
            sn = snmatch.group(2)
            #could get date too, group(1)
        else:
            sn = 'WRONG'
        papertype = snmetadata[sn][1]
        sntopicsdict[sn] = sntopicsdict.get(sn,[]) + [[float(it) for it in li[2:]]]


# then loop through sndict to average the topics

print "\nCreating average topic files with SN and metadata"
sys.stdout.flush()

f2 = codecs.open(writefilecombinesnavgs,'a',encoding='utf-8')
firstline = '\t'.join(['papertype','sn','title','language','publisher','pubfreq','city','state','placeofpub','lat','lon','affdetail'])+'\n'
f2.write(firstline)
for sn in sntopicsdict:
    weightslists = sntopicsdict[sn] #it's a list of lists
    if len(weightslists) > 1:
        #average all weights for a topic in this sn
        averagedweights = [unicode(sum(x)/len(x)) for x in zip(*weightslists)]
    else:
        #I suppose the else is if there's only been one document with this sn, or what??
        averagedweights = [unicode(it) for it in weightslists[0]]
#    snandtypem = re.search('([A-Za-z0-9]+)_([A-Z]+)',snkey)
#    sn = snandtypem.group(1)
#    papertype = snandtypem.group(2)
    
    snmeta = snmetadata[sn]
    addline = '\t'.join(snmeta) + '\t' + '\t'.join(averagedweights) +'\n'
    f2.write(addline)

    

f2.close()

print "Done."
sys.stdout.flush()

 
    
    
    