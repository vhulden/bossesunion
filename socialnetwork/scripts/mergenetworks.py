#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vilja


Create a merged network of BSTL businessmen manually: take clubconnectioncounts file, 
slice out 3 or more connections, merge with geoconnection distance <0.1 list. 

If there are both types of connection, mark that as its own category.

Am doing this manually because I don't understand how Cytoscape's merge deals with 
situations where there are both connections; it never has two so it prefers one clearly,
I think just the one that got added to the merge list first.

First we read in each list of links (id, id, snclubcount  OR id,id,distance); 
then ensure there are no duplicates in either list;
then concatenate;

"""


import codecs

readfile_social = "/../tabular/BSTL-businessmen_clubconnectioncounts.txt"
readfile_distance = "../tabular/BSTL-businessmen_geoconnections.txt"
#writefile = "/Users/vilja/work/research/manuscript/digitalcomponents/biographical/BSTL-NamInCentralClubs.tsv"
writefile = "../tabular/BSTL-businessmen_geo_and_socialconnections.txt"


with codecs.open(readfile_social,'r',encoding='utf8') as f:
    lines = [[el.strip() for el in line.split('\t')] for line in f.read().splitlines()]
    #remove lines where clubcount is <3
    soclinestemp = [l for l in lines if int(l[2])>=3]


with codecs.open(readfile_distance,'r',encoding='utf8') as f:
    #don't need to cull because these are already <0.1
    distlinestemp = [[el.strip() for el in line.split('\t')] for line in f.read().splitlines()]


#both soclinestemp and distlinestemp have the form:
    # id, id, number
    # number is clubcount or distance

#make dictionaries; that ensures there are no duplicates (in the event that two 
# IDs are really linked by a different distance or by a different club count, just 
# overwrite, it's pretty unlikely and there's no 'good' resolution of it if it does 
# happen)

#sort first to make sure there aren't links that are the same ids in different 
#directions - 100,101 vs 101,100

social_dict = {}
templist_s = [sorted(el for el in l[:2]) + [l[2]] for l in soclinestemp]
for l in templist_s:
    key = l[0] + "_" + l[1]
    social_dict[key] = l[2]

distance_dict = {}
templist_d = [sorted(el for el in l[:2]) + [l[2]] for l in distlinestemp]
for l in templist_d:
    key = l[0] + "_" + l[1]
    distance_dict[key] = l[2]
    
all_lines_temp = templist_s + templist_d

combinedlist = [['key1','key2','measure','connection type']]

seenkeys = []
for l in all_lines_temp:
    key = l[0] + "_" + l[1]
    if key not in seenkeys: #so we don't add duplicates in the combinedlist, since there are duplicates in the all_lines_temp as it's a concatenation
        seenkeys.append(key)    
        if key in social_dict and key in distance_dict:
            combinedlist.append([l[0],l[1],l[2],'social_and_residence'])
            continue
        elif key in social_dict:
            combinedlist.append([l[0],l[1],l[2],'socialclub'])
            continue
        elif key in distance_dict:
            combinedlist.append([l[0],l[1],l[2],'residence'])
        

writetxt = '\n'.join(['\t'.join(infol) for infol in combinedlist])

with codecs.open(writefile,'w',encoding='utf-8') as f:
    f.write(writetxt)

    