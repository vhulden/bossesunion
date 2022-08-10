# Computational analysis of labor vs. "mainstream" papers


The book contains an analysis of 4 labor papers and 12 "mainstream" papers; the aim of the analysis is to try to demonstrate how the labor press was different from the mainstream press in both content and use of language, and how this can help us understand what kinds of news Americans in general got about labor (or did not get, as the case may be).

The analysis uses two main techniques: topic modeling and word embeddings. The conclusions I draw from the analyses are in the book, so I'm not going to repeat that here, but below you can find an explanation of each technique, some notes on how I used them, and some results. You can also download all scripts and data here.

I downloaded the newspapers from  [Chronicling America](chroniclingamerica.loc.gov/). You can download the data I used (that's `newspapers.zip`). The file `sninfo-selected.tsv` has basic metadata about the newspapers in the data.

## Topic modeling

Topic modeling was all the rage when it first came out about a decade ago, but it got kind of passé quickly. However, I still find it really useful especially for comparative work: how are the topics in material X different from the topics in material Y? That's how I'm using it here.

Topic modeling is basically an algorithmic technique that automatically identifies "topics" in a body of texts. The topics are based on word cooccurrence: to simplify, words that occur in the same texts repeatedly (say, _ball_ and _pitcher_ and _bat_ and _diamond_) are likely to end up forming a topic. 

In other words, one does not tell the topic modeling program what topics to find; instead, one feeds it the _number_ of topics desired and the texts one is interested in, and the program creates a model that attempts to construct coherent topics based on the cooccurrence of words in the documents. 

The program outputs a list of "topics," represented as lists of words characteristic of the topic, and a calculation of how prominent each topic is in each document. It is worth emphasizing that the program does not label the topics or have any "understanding" of them: it simply reports which words, according to its algorithms, often occur together in documents (a word can occur in multiple topics, and each document may contain multiple topics). It is up to the scholar using the program to label the topic based on the scholar’s interpretation of what the words prominent in it share---what their "common denominator" is, so to speak. Thus, if the list of words defining a topic contained _ball_ and _pitcher_ and _bat_ and _diamond_, one might reasonably label the topic _baseball_. Topics sometimes conflate different types of material, however, so labeling them is generally an iterative process of alternately examining the topic model and the documents one fed to it. 

Having labeled the topics, one can make use of the topic modeler’s report of how prominent each topic is in each document to examine the distribution of topics within different subsets of the material. 

If you want more explanations of topic modeling, check out e.g. Matt Jockers' [The LDA Buffet is Now Open; or, Latent Dirichlet Allocation for English Majors](https://www.matthewjockers.net/2011/09/29/the-lda-buffet-is-now-open-or-latent-dirichlet-allocation-for-english-majors/) or [Getting Started with Topic Modeling and MALLET](https://programminghistorian.org/en/lessons/topic-modeling-and-mallet) by Shawn Graham, Scott Weingart, and Ian Milligan. 

Before topic modeling, I did some preprocessing: I made sure the file names allowed identification of the newspaper title and I chunked the files (which were downloaded newspaper page by newspaper page) into smaller units, since  a newspaper page isn't a very meaningful document for the purposes of topic modeling; after all, all kinds of words cooccur on a newspaper page. The chunking was done with a script along the lines of `splitonregex.py`, so that the "regex" was four or more consecutive capital letters---headlines are often enough in all caps that that tended to work. I discarded overly small chunks.

Then I used [MALLET](mallet.cs.umass.edu/) to create the topic model; I tried various numbers of topics, but found the 150-topic model most useful (or least opaque, depending on how optimistic you want to be).

Commands:

First, to create the mallet:

```
mallet import-dir --input newspaperchunks/ --output laboretal.mallet --keep-sequence --remove-stopwords --extra-stopwords extrastops.txt
```

Then, to train the topic model:

```
mallet train-topics  --input laboretal.mallet  --num-topics 150 --num-iterations 1000 --optimize-interval 10 --random-seed 1 --output-state laboretal_150_topic-state-1.gz  --output-topic-keys laboretal_150_keys-1.txt --output-doc-topics laboretal_150_composition-1.txt
```

(I've also uploaded the `extrastops.txt` and the `laboretal.mallet` files. Note that the `newspaperchunks` in the mallet creation is the newspaper texts chunked into smaller files.)

Then, because I was interested in comparing topics in specific newspaper titles, the script `topiccomp-averages-by-sn.py` aggregates the topic modeling results from the file `laboretal_150_composition-1.tsv` that was produced by Mallet. ("SN" in the script name refers to the newspaper ID.)

You can download the scripts that took the topic modeling results and clumped them together by newspaper, and the (very messy!) Excel file where I've done various calculations on that aggregated topic modeling results file to create the visualizations in the book.


## Word embeddings

Word embeddings construct numerical representations of words as they are used in a corpus. The goal is often to produce a representation of the vocabulary that provides measures of similarity in two different ways. First, words that often occur as neighbors, like _wrote_ and _book_, are judged to be similar; this is called first-order co-occurrence. Second, words that themselves may not be neighbors, but that tend to occur next to the same neighboring words should also be numerically close to each other. This second-order co-occurrence would characterize e.g. such words as _wrote_ and _said_: they might not often occur next to each other, but they would occur in a similar position, i.e., next to many of the same words. The principle for achieving such calculations of similarity is simple: define a context window, and for each word, collect counts of the words occurring within the word’s context window. In other words, the method is based on the old adage that you shall know a word by the company it keeps.

The basic procedure is to first construct a matrix that has the vocabulary on the x axis as well as the y axis, and where each cell contains a count of how often the x axis word has appeared in a context window that also contains the y axis word. For example, in the table below, the word _cat_ has never appeared in a context window that also contains _freedom_, but has appeared six times in a context that also contains _queen_. So, assuming a context window of 3 words on either side, our corpus might contain phrases like "the queen had a cat" or "the cat queen was evil," but not a phrase like "the freedom of the cat to roam."

  _term_    | cat	| queen	| dog |	freedom	| watermelon
------|:---:   | :-----: | :---: | :--------:| :---------:
**cat** 	| 0	  |  6  	| 3   | 	0     | 	0
**queen** |	6   | 0     |	0   | 	8     | 	0
**dog**	  | 3   |	0     |	0   |	  2     | 	1
**freedom**|0	  | 8     |	2   |	  0     |	  0
**watermelon**|	0 |	0   |	1   | 	0     |	0


These counts are then transformed into lists of numbers, with each word being represented by a different number list constructed from its context words; here, the list for queen is ´6 0 0 8 0´. Such lists of numbers are, mathematically, called "vectors," and representing words as vectors allows one to perform various calculations on them. (In actuality, those calculations contain a few extra mathematical steps, but the list-of-numbers is the foundation for the general principle behind many different methods of producing word embeddings.)

One can, then, use these vectors to calculate how similar two words are ("similar," again, meaning how often they appear surrounded by the same words). This works remarkably well. The most-similar words for, say, _apple_ are likely to include words like _pear_, _banana_, _orange_, and so on. On the other hand, it is important to keep in mind that the model constructs the vectors not out of some objective view of the real world, but out of the material given to it: if the material consists of pie recipes, _apple_ might well have _pecan_ among its most-similar words, whereas _pecan_ might be rather less likely to appear on that list if the material consists of cider-brewing manuals (let alone if it consists of computer magazines). This, of course, allows one to explore the different meanings of a word in different sets of material. 

The table below shows examples of the similarity calculations for selected words in the labor and mainstream news materials and illustrates the meaning and range of the similarity score. It functions as a basic sanity check: that is, it shows that the scores and context words and similarities are what one would expect for these simple standard words. The sim column indicates the measure of similarity (a score of 1 would signify that the words appear in exactly the same contexts in both materials). 

_word_	 | material	 | sim	 | similar to	 | context word examples
---		 | :--------:|:-----:|:-------------|:-------------
**coats**	 | main	 | 0.96	 | suits, skirts, overcoats, jackets, tailored, dresses, worsted, capes, wool	 | suits, worth, long, price, ladies, mens, fur, rain, childrens, values, sweater
**coats** | labor	 | 	 | suits, jackets, skirts, 1250, dresses, priced, plush, 1950, worsted, overcoats	 | suits, ladies, price, sale, long, childrens, sweater, mens, new, fur, dresses
**bodies**	 | main	 | 0.68	 | victims, ruins, burned, supposed, missing, lives, body, burning, believed, unknown	 | dead, found, recovered, desired, charge, commercial, director, victims, mine, ruins, burned
**bodies**	 | labor	 | 	 | body, organizations, central, various, representatives, affiliated, formed, civic, unions, clubs	 | central, labor, federation, state, american, officials, unions, embracing, local, minds, city
**scab**	 | main	 | 0.39	 | parasites, germ, worms, eradicate, parasitic, germs, insect, preventive, scalp	 | apple, seed, treatment, solid, potatoes, disease, diseases, blight
**scab**	 | labor	 | 	 | scabs, quit, hire, jobs, employ, hired, refuse, job, insist	 | union, labor, coal, clothes, fields, tobacco, cigars, nonunion, company


Having established that the results make sense, we can move on to checking some words of interest. The way I arrived at this set of words wasn't exactly superbly scientific, but it wasn't entirely random either: as a starting point, I sorted a list according to which words were the least similar in the sets of material, and then skimmed that list. So I picked the words manually, on the basis of the kinds of topics I am investigating, but in the process I paid attention to the sim score. Some were dramatically different (like _capitalist_, below) while others were sort of moderate (_courts_ below) and some where pretty subtly different (_strikers_ below).


word	 | material	 | sim	 | similar to	 | context word examples
:--------:|:----------:|:-----:|:-------------|:------------
**bosses**	 | main	 | 0.83	 | politicians, dictate, faction, tammany, officeholders, congressmen	 | mine, foremen, fire, party, political, democratic, republican, state, machine, examinations
**bosses**	 | labor	 | 	 | operators, refuse, tactics, officials, threatened, strikers, contractors	 | political, strike, union, workers, foremen, mine, strikers, labor, party, public, fire
**capitalist**	 | main	 | 0.47	 | financier, magnate, philanthropist, millionaire, banker, dobbs, rockefellers, onetime, wealthy	 | banker, york, city, new, prominent, business, chicago, dead, man, died, estate, george, home, known, real, son, john, late
**capitalist**	 | labor	 | 	 | capitalists, capitalism, class, capitalistic, trusts, nation, masses, masters, slave, greed	 | class, system, working, rule, power, present, struggle, capitalist, press, workers, society, profits, oppression,
**courts** | main	 | 0.88	 | decision, ruling, federal, supreme, jurisdiction,  injunction, proceedings, legal	 | federal, state, practice, law, decision, case, supreme, court, county, lawyer, states, washington, circuit
**courts** | labor	 | 	 | judges, injunction, legal, supreme, justice, injunctions, federal, rights, decisions, contempt	 | labor, law, state, justice, federal, power, legislatures, states, people, judges, corrupt, supreme, injunction
**socialism**	 | main	 | 0.82	 | doctrines, doctrine, viewpoint, socialistic, morality, propaganda, believer, theories, ethical, aims	 | socialist, church, means, people, men, socialists, labor, party, capitalism, system, unionism, principles, vote, great
**socialism**	 | labor	 | 	 | economic, unionism, common, nation, socialists, democracy, masses, true, labors, capitalist	 | state, socialist, lecture, people, principles, antitrust, forms, human, party, public, church, city, country
**socialist**	 | main	 | 0.79	 | socialists, dahlman, tammany, nominee, democrat, polls, reelection, hearst, bryans, nominated	 | party, candidate, mayor, vote, city, ticket, elected, member, milwaukee, berger
**socialist**	 | labor	 | 	 | party, socialists, political, campaign, issue, vote, press, democratic, socialism, republicans, votes	 | party, socialist, ticket, labor, vote, national, movement, press, city, milwaukee
**strikers**	 | main	 | 0.91	 | strikebreakers, nonunion, walkout, sympathizers, riot, rioting, foreigners	 | men, union, company, police, victory, committee, demands, city, meeting, aid
**strikers**	 | labor	 | 	 | strikebreakers, miners, scabs, refused, threatened, officials, bosses	 | men, company, today, meeting, car, police, return, , union, street, ranks, city, committee


The scripts for the word embeddings analysis include:
```
embeddings.py
embeddings_analyze.py
embeddings_analyzecontext.py
embeddingtools.py
```

