#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:28:54 2021

@author: vilja

Slice BSTL full table in various ways for importing into Cytoscape 
(could presumably restrict in Cytoscape but cleaner and easier this way, I think.)

Currently: 
    - Only members of BML, CIA, NAM, MFA
    - Note that NAM is recorded in role (=0) whereas the others have their own columns
"""
import codecs

readfile = "../tabular/BookOfStLouisansInfo_complete.tsv"
writefile = "../tabular/BSTL-businessmen.tsv"

with codecs.open(readfile,'r',encoding='utf8') as f:
     lines = [[l.strip() for l in line.split('\t')] for line in f.read().splitlines()]

businesslines = [lines[0]] #header line

lnames = []
for line in lines[1:]:
    #debugging
    lname = line[1]
    lnames.append(lname)
    #real
    bma = line[18].strip()
    mfa = line[19].strip()
    cia = line[20].strip()
    nam = line[21].strip()
    if bma or mfa or cia or nam:
        businesslines.append(line)
#        print "YES"
        
        

businesstext = '\n'.join(['\t'.join(l) for l in businesslines])

with codecs.open(writefile,'w',encoding='utf-8') as f:
    f.write(businesstext)
        
    

