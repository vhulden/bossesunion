# Computational analysis of labor vs. "mainstream" papers

These are fairly extensively explained in the book so I'm not going to duplicate that here. However, you can download the data (that's `newspapers.zip`), the scripts for the word embeddings analysis, the scripts that took the topic modeling results and clumped them together by newspaper, and the (very messy!) Excel file where I've done various calculations on that aggregated topic modeling results file to create the visualizations in the book.

The file `sninfo-selected.tsv` has basic metadata about the newspapers in the data.

The scripts for the word embeddings analysis include:
```
embeddings.py
embeddings_analyze.py
embeddings_analyzecontext.py
embeddingtools.py
```

The script `topiccomp-averages-by-sn.py` aggregates the topic modeling results from the file `laboretal_150_composition-1.tsv`. That file was created with the following commands:

First, to create the mallet:

```
mallet import-dir --input newspapers/ --output laboretal.mallet --keep-sequence --remove-stopwords --extra-stopwords extrastops.txt
```

Then, to train the topic model:

```
mallet train-topics  --input laboretal.mallet  --num-topics 150 --num-iterations 1000 --optimize-interval 10 --random-seed 1 --output-state laboretal_150_topic-state-1.gz  --output-topic-keys laboretal_150_keys-1.txt --output-doc-topics laboretal_150_composition-1.txt
```

(I've also uploaded the `extrastops.txt` and the `laboretal.mallet` files.)
