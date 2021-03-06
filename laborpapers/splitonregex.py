#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created March 2019

@author: vilja

Read in text files, split on regex.
"""

import os, re, codecs

rootdirname = "/Users/vilja/work/research/digital/NLPproject/"

indirname = rootdirname + "prideandprejudice/"

writedir = rootdirname + "prideandprejudice/"
if not os.path.isdir(writedir):
    os.mkdir(writedir)



howmany = 1
newlist = []

newlinesub = re.compile('(\S)[ \t\r\f\v]*\n(\S)')

splitregex = re.compile('^\s*(Chapter\s+\d+)(.*?)$')

#re.compile('^\s*(\d+\.)(.*?)$')

for fn in os.listdir(indirname):
    count = 0 
    templist = []
    print "processing file number %d" %howmany
    howmany += 1
    with codecs.open(indirname+fn,'r',encoding='utf-8') as f:
        chunkf = f.read()
    
    newchunkf = newlinesub.sub(r'\1 \2',chunkf)
    newchunkl = newchunkf.split('\n')
    
    for line in newchunkl:
        print line
        if splitregex.match(line): #need to get first ch or whatever
            chunk = '\n'.join(newlist)
            number = str(count)
            if count > 0:
                if len(number) < 2:
                    number = "0"+number
                chunkname = fn[:-4] + '_' + number + '.txt'
                with codecs.open(writedir+chunkname,'w',encoding='utf8') as f:
                    f.write(chunk)
            newlist = [line]
            count += 1
        else:
            newlist.append(line) 
        
    #write last one
    chunk = '\n'.join(newlist)
    number = str(count)
    if count > 0:
        if len(number) < 2:
            number = "0"+number
        chunkname = fn[:-4] + '_' + number + '.txt'
    with codecs.open(writedir+chunkname,'w',encoding='utf8') as f:
            f.write(chunk)
           
#for index, line in enumerate(newlist):
#    with codecs.open(writedir+str(chunknames[index]),'w',encoding='utf-8') as f:
#        f.write(line)
    

