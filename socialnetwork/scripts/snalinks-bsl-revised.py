#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:24:54 2017

Revised Feb 2021

@author: vilja

Create links for SNA from Book of St Louisans

First part calculates distances between coordinates and creates a link 
if  the distance is less than maxdist (current 0.1 miles is sort of a city 
block width, depending somewhat on city and source) and if the match type is Exact 
(from the geolocation file created by census) or Added (manually added by me, for some hotels).
Double links (223, 10, d / 10, 223, d) are removed using frozenset.

The second part creates links based on shared club membership; produces two lists,
first of which lists id-id-club and second id-id-#ofconnections.

### This seems to no longer be true; I assume it was for network manageabilty but seemed
not so useful in the end?
***NOTE*** that for the # of connections, only links with 3 or more connections (weight
of edge 3 or more, i.e., shared membership in 3 clubs) are saved. 


"""
import codecs,operator
from geopy.distance import vincenty


maxdist = 0.1

"""These are the basic versions for the full table; below have variants for 
.... various slices"""
readfile = "../tabular/BookOfStLouisansInfo_complete.tsv"
#these are the files that are created:
geolinksfile = "../snfiles/BookOfStLouisans_geoconnections.txt"
assnlinksfile = "../snfiles/BookOfStLouisans_assnconnections.txt"
clublinksfile = "../snfiles/BookOfStLouisans_clubconnections.txt"
clubcountsfile = "../snfiles/BookOfStLouisans_clubconnectioncounts.txt"

#readfile = "../tabular/BSTL-businessmen.tsv"
##these are the files that are created:
#geolinksfile = "../snfiles/BSTL-businessmen_geoconnections.txt"
#assnlinksfile = "../snfiles/BSTL-businessmen_assnconnections.txt"
#clublinksfile = "../snfiles/BSTL-businessmen_clubconnections.txt"
#clubcountsfile = "../snfiles/BSTL-businessmen_clubconnectioncounts.txt"

with codecs.open(readfile,'r',encoding='utf8') as f:
     lines = [[l.strip() for l in line.split('\t')] for line in f.read().splitlines()]

    
#This is how it works:
#newport_ri = (41.49008, -71.312796)
#cleveland_oh = (41.499498, -81.695391)
#print(vincenty(newport_ri, cleveland_oh).miles)

geolinks = []
for line in lines[1:]:
    thisid = line[0]
    thismatchtype = line[11].strip()
    if thismatchtype == 'Exact' or thismatchtype=='Added': #only compare exact matches or added ones, others seem too unreliable
       # if line[2] != "": #empty strings can't be converted to floats, and shouldn't be compared anyway
        lon = float(line[13])
        lat = float(line[14])
        thispoint = (lat,lon)
        for otherline in lines[1:]:
            othermatchtype = otherline[11].strip()
            if othermatchtype == 'Exact' or othermatchtype == 'Added':
                otherid = otherline[0]
                if not thisid == otherid:
                    otherlon = float(otherline[13])
                    otherlat = float(otherline[14])
                    otherpoint = (otherlat,otherlon)
                    d = vincenty(thispoint,otherpoint).miles
                    if d <= maxdist:
                        geolinks.append([thisid,otherid,'%.3f'%d])

print "Geolinks done."
#above the distance figure is truncated since 
#for some reason there are sometimes differences, perhaps depending on which
#direction the vincenty was done


#Remove duplicate links, i.e., 2, 4, d  / 4, 2, d
#and then reconvert back to list
geoset = {(frozenset({x[0],x[1]}), x[2]) for x in geolinks}

ugeolinks = [list(gset[0])+[gset[1]] for gset in geoset]


# Create a list of links through clubs: id1, id2, club
clublinks = []
for line in lines[1:]:
    thisid = line[0]
    clubl = line[25].strip('"').strip("[").strip("]").strip('"') #there are some extra characters 
    theseclubs = [c.strip('"') for c in clubl.split(',')]
    for otherline in lines[1:]:
        otherid = otherline[0]
        oclubl = otherline[25].strip('"').strip("[").strip("]").strip('"')
        otherclubs = [c.strip('"') for c in oclubl.split(',')]
        if thisid != otherid:
            for club in theseclubs:
                 if len(club) > 1 and club in otherclubs:
                    clublink = [thisid,otherid,club]
                    clublinks.append(clublink)
                    
print "Clublinks done."

#
##Remove duplicate links, i.e., 2, 4, Noonday  / 4, 2, Noonday
##and then reconvert back to list
##and finally convert so that the first id always is lower, so can order
#...in a sensible way for next step
clubset = {(frozenset({x[0],x[1]}), x[2]) for x in clublinks}

uclublinks = [list(cset[0])+[cset[1]] for cset in clubset]

uclublinksord = []
for link in uclublinks:
    if int(link[0]) > int(link[1]):
        newlink = [link[1],link[0],link[2]]
    else:
        newlink = link
    uclublinksord.append(newlink)

uclublinksord.sort(key = operator.itemgetter(0, 1, 2))

print "Duplicates removed."
# go through clublinks and create dict to calculate how many links two ids share
uclubdict = {}

for link in uclublinksord:
    thiskey = link[0]+'_'+link[1]
    if thiskey in uclubdict:
        uclubdict[thiskey] += 1
    else:
        uclubdict[thiskey] = 1
    
# put that in a list
clubcountslist = []
for key in uclubdict.keys():
#    if uclubdict[key] > 2: #oh -commented out, so maybe I took all and adjusted in Cytoscape?
    line = key.split('_')
    line.append(str(uclubdict[key]))
    clubcountslist.append(line)
    
print "Clubcounts created."


# Create a list of links through shared membership in 
# Business Men's League, CIA, Manufacturers' Association, or Civic League
assnlinks = []
for line in lines[1:]:
    thisid = line[0]
    bml = line[17]
    mfa = line[18]
    civic = line[21]
    if line[19].strip() != "": cia = 'CIA' 
    else: cia = '' #bc some entries say CA instead for CIA and want to match
    theseassns = set([bml,mfa,civic,cia])
    for otherline in lines[1:]:
        otherid = otherline[0]
        obml = otherline[17]
        omfa = otherline[18]
        ocivic = otherline[21]
        if otherline[19].strip() != "": ocia = 'CIA' 
        else: ocia = ''
        otherassns = set([obml,omfa,ocivic,ocia])
        if thisid != otherid:
            for assn in theseassns:
                 if len(assn) > 1 and assn in otherassns:
                    assnlink = [thisid,otherid,assn]
                    assnlinks.append(assnlink)
            
assnset = {(frozenset({x[0],x[1]}), x[2]) for x in assnlinks}

uassnlinks = [list(cset[0])+[cset[1]] for cset in assnset]
                    

print "Writing."
# convert to text and write


assnlinkst = '\n'.join(['\t'.join(l) for l in uassnlinks])
#assnlinkst = '\n'.join(l for l in assnlinkstl)
with codecs.open(assnlinksfile,'w',encoding = 'utf-8') as f:
    f.write(assnlinkst)
    
    
geolinkst = '\n'.join(['\t'.join(l) for l in ugeolinks])
#geolinkst = '\n'.join(l for l in geolinkstl)
with codecs.open(geolinksfile,'w',encoding = 'utf-8') as f:
    f.write(geolinkst)

     
clublinkst = '\n'.join(['\t'.join(l) for l in uclublinksord])
#clublinkst = '\n'.join(l for l in clublinkstl)
with codecs.open(clublinksfile,'w',encoding = 'utf-8') as f:
    f.write(clublinkst)
    
clubcountst = '\n'.join(['\t'.join(l) for l in clubcountslist])
#clubcountst = '\n'.join(l for l in clubcountstl)    
with codecs.open(clubcountsfile,'w',encoding = 'utf-8') as f:
    f.write(clubcountst)
    

    