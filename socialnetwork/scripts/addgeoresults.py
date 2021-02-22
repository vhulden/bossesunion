#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 10:56:03 2021

@author: vilja

Combine geocoding results with BSTL master file.

Also, since couldn't think of a better place to do it, add a "label" column that
contains Lastname, Firstname, Middle, Birthyear so that can be used as a label
in the networks. 

Also, since can't think of a better place to do it, convert the "role" column to a "NAM" column.
"""
import codecs

masterfile = "../tabular/BookOfStLouisansInfo_OpenRefined_edited.tsv"
georesultsfile = "../tabular/GeocodeResults.tsv"
writemasterfile = "../tabular/BookOfStLouisansInfo_Complete.tsv"


with codecs.open(masterfile,'r',encoding='utf-8') as f:
    masterlines = [[l.strip() for l in line.split('\t')] for line in f.read().splitlines()]

with codecs.open(georesultsfile,'r',encoding='utf-8') as f:
    geolines = [[l.strip() for l in line.split('\t')] for line in f.read().splitlines()]

geodict = {}
for gline in geolines[1:]:
    geodict[gline[0]] = gline[1:]
    
firstmline = masterlines[0][:10] + ['match','matchtype','matchedaddress','lon','lat','label'] + masterlines[0][10:15] + ['NAM'] + masterlines[0][16:]
newmlines = [firstmline]
for mline in masterlines[1:]:
    #label
    lname = mline[1]
    fname = mline[2]
    middle = mline[3]
    byear = mline[8]
    label = lname + ", " + fname 
    if middle.strip() != "": label += " " + middle
    if byear.strip() != "": label += " (" + byear + ")"
    #nam
    nam = mline[15]
    if nam.strip() == "1": nam = "NAM" 
    else: nam = ""
    
    #geodata
    masterid = mline[0]
    geoline = geodict[masterid]
    match = geoline[1]
    matchtype = geoline[2]
    matchedaddress = geoline[3]
    lon = geoline[4]
    lat = geoline[5]
    newmline = mline[:10] + [match,matchtype,matchedaddress,lon,lat,label] + mline[10:15] + [nam] + mline[16:]
    newmlines.append(newmline)
    
newmastertext = '\n'.join(['\t'.join(l) for l in newmlines])

with codecs.open(writemasterfile,'w',encoding='utf-8') as f:
    f.write(newmastertext)
    