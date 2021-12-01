#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 10:53:19 2017 [revised Feb 2021]

@author: vilja

Ingest dictionary created by cleangoulds and transform into 
bipartite network 
name, club
name, club

write out for conversion into unimodal network with R
as explained in Posner's Cytoscape tutorial

"""

import codecs,json

dictfile = "../intermediate/GouldsDict.json"
csvfile = "../intermediate/GouldsBipartite.csv"

with codecs.open(dictfile,'r',encoding='utf-8') as f:
    clubsdict = json.loads(f.read())

persontoperson = []
memberclublinks = [[u'member',u'club']]
for club in clubsdict:
    for member in clubsdict[club]:
        memberclublinks.append([member,club])
        
linkstxtl = [','.join(link) for link in memberclublinks]

linkstxt = '\n'.join(linkstxtl)
        
with codecs.open(csvfile,'w',encoding='utf-8') as f:
    f.write(linkstxt)
   