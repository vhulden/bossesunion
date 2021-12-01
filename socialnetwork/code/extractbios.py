#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 16:51:44 2017

@author: vilja

For processing Book of St. Louisans, possibly of use in other similar compendia as well.

Updated in late June 2017 to identify membership in Businessmen's League 
and to save clubs in a list (Cytoscape likes that).
Original script and original combined lists are saved in biographical/savedversions.

UPDATED JAN 2021 for use with pre-cleaned files and for clarity

"""
import re,codecs


#switch here between 1906 and 1912
#readfile = "../texts/The_Book_of_St_Louisans_2ed_1912-noSee1906.txt"
#writefile = "../tabular/BookOfStLouisansInfo_1912.tsv"
readfile = "../texts/The_Book_of_St_Louisans_1906-cleaned.txt"
writefile = "../tabular/BookOfStLouisansInfo_1906.tsv"
statesfile = "../helpfiles/states.tsv"

with codecs.open(statesfile,'r',encoding='utf-8') as f:
    statenamelist = f.read().splitlines()
    statenames = [[l.strip() for l in line.split('\t')] for line in statenamelist]
        
#statenames includes canadian provices but abbr listed below for nationality check
canadianprovinces = ['AB','BC','MB','NB','NL','NS','NT','NU','ON','PE','QC','SK','YT']


with codecs.open(readfile,'r',encoding='utf-8') as f:
    allentries = f.read().splitlines()

#make a header line for the table and add it to the list to which we'll add the entries
firstline = ['lname','fname','mnames','occupation','company','birthcity','birthstate','birthyear','residence','office','nationality','BMA','MFA','CIA','civic','party','partyqual','clubs','memberships','fullentry']
infoentries = [firstline]

for lline in allentries:
    #regex searches to identify bits and pieces.
    #note that names that had a space, like VAN CLEAVE have been replaced with 
    # the form VAN_CLEAVE
    name = re.match("([A-Za-z0-9_\-']+)[,.](.*?),(.*?)[,;:]",lline)
    lname = name.group(1).strip() #lname
    lname = re.sub("[;(.)#!^*']","",lname) #remove any junk characters
    lname = lname.upper()
    othernames = name.group(2).split()
    fname = othernames[0].strip() #fname
    fname =  re.sub("[;(.)#!^*']","",fname) #remove any junk characters
    fname = fname.capitalize()
    if len(othernames) > 1:
        mnames = ' '.join(othernames[1:]).strip() #mnames: middle names
    else:
        mnames = ''
    occupbase = name.group(3).strip() #occupatoin
    companybase = re.search('(.*?)([A-Z].*)',occupbase) # because co begins with capital
    if companybase: 
        company = companybase.group(2).strip()
        occupation = companybase.group(1).strip()
    else:
        occupation = occupbase.strip()
        company = ""
    
    birthplace = re.search('[Bb]orn(?:\s*in)*\s*(.*?),\s*(.*?)[;,]',lline)
    if birthplace:
        birthcity = birthplace.group(1).strip()
        birthstate = birthplace.group(2).strip()
        if birthstate.endswith("Co.") or birthstate.endswith("County"):
            birthstsearch = re.search(birthstate+'[,](.*?)[,;]',lline)
            if birthstsearch: birthstate = birthstsearch.group(1).strip()
    try:
        birthyear = re.search('[Bb]orn.*?(\d{4})',lline).group(1).strip()
    except:
        birthyear = ""
    try:
        # manipulate clubs a bit to unify club memberships
        clubs = []
        clubsdraft = re.search('Clubs*:(.*?)[;.]',lline).group(1).split(',')
        #clubs = ['"'+club.strip()+'"' for club in clubs]
        for club in clubsdraft:
            club = re.sub(',','',club) 
            club = re.sub('\.','',club) 
            club = re.sub('\'','',club) 
            club = re.sub('\s*^[0-9;7$#2!*.,/\|()]+\s*$','',club) #empty ones that only have numbers and symbols
            club = re.sub('-','',club) #all these just clean up to make easier to group
            club = re.sub('\(.*\)','',club)
            club = re.sub('\(.*$','',club)
            club = re.sub('^\s*and\s*','',club)#sometimes didn't get split so it says "and Glen Echo"
            club = re.sub('^\s*also\s*','',club)
            club = re.sub('of St Louis','',club)#to unify, it's the same club, some just mark
            club = re.sub('\s*Club\s*$','',club)
            club = club.strip()
            #because some have entered e.g. St Louis Country and others Country but it's the same
            if club != 'St Louis': club = re.sub('^St Louis\s*','',club)
            #lots of specification variants, trying to unify
            if club.startswith('Glen Echo'): club = 'Glen Echo'
            if club.startswith('Sunset Hill'): club = 'Sunset Hill'
            if club.startswith('Bellerive'): club = 'Bellerive'
            if club.startswith('Florissant Valley'): club = 'Florissant Valley'
            if club.startswith('Normandie'): club = 'Normandie'
            if club.startswith('Algonquin'): club = 'Algonquin'
            if club.startswith('Oasis'): club = 'Oasis'
            if club.startswith('Westwood'): club = 'Westwood'
            if club.startswith('Midland Valley'): club = 'Midland Valley'
            if club.startswith('Log Cabin'): club = 'Log Cabin'
            if club.startswith('Kings Lake'): club = 'Kings Lake'
            if club.startswith('Traffic') or club.startswith('The Traffic'): club = 'Traffic'
            if club == 'Union League': club = 'Union'
            if club == 'Maine Hunting and Fishing': club = 'Maine Fishing and Hunting'
            if club == 'Amateur Athletic' or club == 'Amateur Athletic Assn' or club == 'Athletic': club = 'Amateur Athletic Association'
            if len(club) < 3: club = ""
            if club == "etc": club =""
            clubs.append(club)
    except:
        clubs = []
    try:
        residence = re.search('(?:[R]esidence|[A]ddress)\s*[:;.]\s*(.*)',lline).group(1).strip().strip()
    except:
        residence = ""
    try:
        if residence:
            office = re.search('[oO]ffice[s]*\s*[:;.]\s*(.*?)(?:[rR]esidence|[aA]ddress)',lline).group(1).strip().strip()
        else:
            office = re.search('[oO]ffice\s*[:;.]\s*(.*)',lline).group(1).strip()
    except:
        office = ""
    offres = re.search('[oO]ffice[s]*\s*and\s*[rR]esidence[s]*\s*[:;.]\s*(.*)',lline)
    if offres:
        office = offres.group(1).strip()
        residence = offres.group(1).strip()
    ## (added June 2017)
    if re.search("Business\s*[mM]en['s]+\s*(League|Association|Assn)",lline):
        bml = "BML"
    else: bml = ""
    if re.search("Citizen[s']+\s*[I1]nd",lline):
        cia = "CIA"
    elif re.search("Citizen[s']+\s*Al",lline):
        cia = "CA"
    else: cia = ""
    if re.search("Manufacturer['s]+\s*Ass.*",lline):
        mfa = "MFA"
    else: mfa = ""
    if re.search("Civic(.*?)League",lline):
        civic = "CL"
    else: civic = ""
    #the pattern is often "Independent Democrat" or "Republican (with qualifications)" or some such
    #"Independent" has to be searched for separately as otherwise it conflicts with above
    pols = re.search("[.,;]\s*([A-Za-z]*)\s*(Democrat|Republican|Socialist)(.*?)[.,;]",lline)
    polinds = re.search("[.,;]\s*([A-Za-z]*)\s*(Independent)(.*?)[.,;]",lline)
    if pols: 
        party = pols.group(2)
        partyqual = pols.group(1).strip() + " / " + pols.group(3).strip()
    elif polinds:
        party = polinds.group(2)
        partyqual = polinds.group(1).strip() + " / " + polinds.group(3).strip()
    else:
        party = ""
        partyqual = ""
    if partyqual == " / " or partyqual == " / in politics": partyqual = ""
    try:
        # this is just for extra info, impossible to compile into data - or too hard anyway
        memberships = re.search('Member (.*?)[.]',lline).group(1)
        memberships.strip('of ')
        memberships = [member.strip() for member in memberships.split(',')]
    except:
        memberships = []
        
    #### That's the primary stuff, what follows is tweaks to it ###
    if birthcity.startswith("St Louis"):
        birthstate = "MO"
    if birthstate.startswith("St Louis"):
        birthstate = "MO"
        birthcity = "St Louis"
    if birthstate.startswith("Indianapolis"):
        birthstate = "IN"
        birthcity = "Indianapolis"
    if birthcity.startswith("New York"):
        birthstate = "NY"
    if "Germany" in birthcity:
        birthstate = "Germany"
    if "Norway" in birthcity:
        birthstate = "Norway"
    if re.search("111",birthstate):
        birthstate = "IL"
    if birthstate.strip().startswith("la.") or birthstate.strip().startswith("la"): birthstate = "IA"
    if birthstate.startswith('County'): birthstate = 'Ireland'
    if birthstate.strip() == 'Eng.': birthstate = 'England'
    if birthstate.strip() == 'Ger.' or birthstate == 'German': birthstate = 'Germany'
    if birthstate.strip() == 'Can.': birthstate = 'Canada'
    occcheck = re.search('(.*)of\s*(?:the)*\s*$',occupation)
    if occcheck: occupation = occcheck.group(1)
        
    
    ### Clean states
    for stlist in statenames:
        if birthstate.strip() in stlist:
            birthstate = stlist[0]
    
    ### These are additional numbered switches -- based on info above, but numeric ###
    if birthstate == 'Germany' or birthstate == 'Saxony' or birthstate == "Bavaria" or birthstate == 'Hesse-Darmstadt' or birthstate == 'Prussia' or birthstate == 'Rhenish Bavaria' or birthstate == 'Hesse Darmstadt': 
        nationality = '1'
    elif birthstate =='England' or birthstate == 'Wales' or birthstate == 'Scotland' or birthstate == 'Yorkshire' or birthstate == 'Great Britain': nationality = 2
    elif birthstate == 'Norway': nationality = 3
    elif birthstate == 'Canada' or birthstate.strip() in canadianprovinces: nationality = 4
    elif birthstate == 'Ireland': nationality = 5
    elif birthstate == 'Austria': nationality = 6
    elif birthstate == 'France': nationality = 7
    elif birthstate == 'Bohemia': nationality = 8
    elif birthstate == 'Hungary': nationality = 9
    
    else: nationality = '0'
    
    
    ### This makes the line ###
    clubtxt = '["' + '","'.join(clubs) + '"]'
    memberstxt = '["' + '","'.join(memberships) + '"]'
    infoline = [lname,fname,mnames,occupation,company,birthcity,birthstate,birthyear,residence,office,unicode(nationality),bml,mfa,cia,civic,party,partyqual,clubtxt,memberstxt,lline]

    infoentries.append(infoline)
    


infotext = '\n'.join(['\t'.join(infol) for infol in infoentries])

with codecs.open(writefile,'w',encoding='utf-8') as f:
    f.write(infotext)