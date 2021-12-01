#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:38:43 2017

@author: vilja

Take the Goulds Club2Club list (which has edge weights, which represent
number of shared members) and the club membership counts list,
calculate what percentage of membership is shared.

Ex. 
Club A membership = 100
Club B membership = 100
shared members = 50

calc: 
    
     shared
------------------- *100 (just to make it a percent and also scale up a bit)
  A + B - shared


The basic file produced (used for SNA) just shows ClubA, ClubB, sharedpct.

In addition, create two additional files:
    1) that shows the number of shared members, number of ClubA members, 
    number of ClubB members, and the weight% 
    2) that shows what percentage the shared membership is of the SMALLER 
    club's membership; otherwise it looks like the strength of the connection 
    between a club with 20 members and a club with 1,000 is weak even if the 
    smaller club's members all are members of the larger club.

The smaller-club version is used to create an image of particularly closely connected
clubs (in fact, I'm also using it for the larger graph, though in that the edge
weight is set by the simple shared-membership weight.)

"""

import codecs

club2club = "../tabular/GouldsClubLinks.csv"
membercounts = "../tabular/GouldsClubs-counts.csv"

#these are produced by this script
writenewweights = "../tabular/GouldsClubs-shared-weights.csv"
writenewweightsextra = "../intermediate/GouldsClubs-sharedweightsextra.csv"
writenewweightsextrasm = "../intermediate/GouldsClubs-sharedweightsextra-smallc.csv"


with codecs.open(membercounts,'r',encoding='utf-8') as f:
    countlist = [l.split(',') for l in f.read().splitlines()]

with codecs.open(club2club,'r',encoding='utf-8') as f:
    weightededgelist = [l.split(',') for l in f.read().splitlines()]

membercountdict = {}
for c in countlist:
    club = c[0]
    count = int(c[1])
    membercountdict[club] = count

newweights = [['id','from','to','weightpct']]
newweightsextra = [['id','from','to','weight','frommemb','tomemb','weightpct']]
for idn, A, B, w in weightededgelist[1:]:
    clubAm = membercountdict[A]
    clubBm = membercountdict[B]
    pct = float(w) / (clubAm + clubBm - float(w)) * 100
    newweightsextra.append([idn,A,B,w,unicode(clubAm),unicode(clubBm),unicode(pct)])
    newweights.append([idn,A,B,unicode(pct)])

# percentage of smaller club's membership
# so just take the # of shared members and divide by the smaller club's membership 
newweightsextrasm = [['id','from','to','weight','frommemb','tomemb','weightpct']]
for idn, A, B, w in weightededgelist[1:]:
    clubAm = membercountdict[A]
    clubBm = membercountdict[B]
    divisor = min(clubAm,clubBm)
    pct = float(w) / divisor * 100
    newweightsextrasm.append([idn,A,B,w,unicode(clubAm),unicode(clubBm),unicode(pct)])
    
newweightstxt = '\n'.join([','.join(l) for l in newweights])
newweightsextratxt = '\n'.join([','.join(l) for l in newweightsextra])
newweightsextratxtsm = '\n'.join([','.join(l) for l in newweightsextrasm])

with codecs.open(writenewweights,'w',encoding='utf-8') as f:
    f.write(newweightstxt)

with codecs.open(writenewweightsextra,'w',encoding='utf-8') as f:
    f.write(newweightsextratxt)
    
with codecs.open(writenewweightsextrasm,'w',encoding='utf-8') as f:
    f.write(newweightsextratxtsm)