#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Original created on Tue Jun 20 2017 [new version Feb 2021]

@author: vilja

Extract info from Goulds Blue Book of Clubs, cleaned text file 

Create a dictionary (dumped as json dump) of the form
{clubname:
    [
    member,
    member,
    member]}
    
Note that clubname, which is ALL CAPS to start, is converted into Title Case.

Also save a list of all clubs.

Finally, also get a membership count for each club and save that separately.

"""
import codecs,re,json

readfile = "../texts/GouldBlue_CleanedOpenRefine_initials-OpenRefine.txt"
writefileclubs = "../intermediate/GouldsClubs.txt"
writefileclubcounts = "../intermediate/GouldsClubs-counts.txt" 
dictfile = "../intermediate/GouldsDict.json"


with codecs.open(readfile,'r',encoding='utf-8') as f:
    lines = [l.strip() for l in f.read().splitlines()]

clubdict = {}
notfound = [] #a list to save lines that simply don't match
for l in lines:
    # mclub identifies lines that say what the club is
    mclub = re.match("CLUB:\s*([A-Z .']+)",l,flags=0)
    # mname just takes the whole line if begins with capital plus lower case (Sm)
    mmember = re.match('[A-Z][a-z].*',l,flags=0)
    if mclub: 
        club = re.sub('CLUB:\s*','',mclub.group(1))#the rest of the line is the club name
        club = club.title()
        if club not in clubdict.keys():
            clubdict[club] = []
    elif mmember:
        member = mmember.group(0)
        clubdict[club].append(member)
# 
clubs = clubdict.keys()
clubtxt = '\n'.join(clubs)

membercounts = [cl+','+unicode(len(clubdict[cl])) for cl in clubdict.keys()]
membercountstxt = '\n'.join(membercounts)

with codecs.open(dictfile,'w',encoding='utf-8') as f:
    json.dump(clubdict,f,sort_keys=True, indent=None,separators=(',', ': '))     

with codecs.open(writefileclubs,'w',encoding='utf-8') as f:
    f.write(clubtxt)
    
with codecs.open(writefileclubcounts,'w',encoding='utf-8') as f:
    f.write(membercountstxt)