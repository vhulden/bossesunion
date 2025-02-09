# Tracking open shop, closed shop, union shop, industrial democracy as ngrams 

## What's an ngram?

Google Books has for years now provided a service called [Google Ngram](https://books.google.com/ngrams), which gives anyone access to easily drawing graphs of the frequency of specific phrases over time. The phrases are called ngrams - sequences of strings (words) of length "n", so a two-word sequence is a bigram (2-gram), a three-word sequence a trigram (3-gram), and so on.

The service allows one to select a corpus (set of texts) in which to search for a phrase, so one can (sort of) limit it to "American English" versus "British English" for example. Whether something is "American" or "British" depends on the place of publication. With a corpus selected, one can choose the span of years of interest, and then enter one's phrase of interest, after which the system draws a graph representing the frequency of that phrase as a proportion of all phrases of that length in that year. 

Note that searches are case sensitive! For more documentation and possibilities, see [Google's own documentation of its Ngram Viewer](https://books.google.com/ngrams/info).

## Caveats

None of this is error-free: there are problems with the accuracy of OCR (text recognition, so some texts may have severe problems with spelling or misrecognized words) as well as with the accuracy of the metadata (such as year and place of publication). Moreover, this is not necessarily a measure of what people were talking about: it does not weight books that everyone read more heavily than books that nobody opened. Even less is it a measure of what existed out there in the world &mdash; an obvious point, but one that is all too easy to forget. To remind yourself of it, it is good to consider this graph every now and then. Spoiler alert: it does not mean that we have, since the last years of the 20th century, been facing an ever-increasing zombie apocalypse accompanied by an even more terrifying proliferation of vampires.

![Google Ngram: vampires vs. zombies](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/vampirezombie.png)

(See the [original at Google Ngrams](https://books.google.com/ngrams/graph?content=zombie%2Cvampire&year_start=1900&year_end=2019&corpus=26&smoothing=3]). This search was inspired by Andrew Gelman & George A. Romero, "['How many zombies do you know?' Using indirect survey methods to measure alien attacks and outbreaks of the undead](https://arxiv.org/abs/1003.6087)," 2010.)

Language is not reality. It's also good to keep in mind that language change may or may not reflect change in ideas and sentiments &mdash; and that the graphs the service draws may change over time as more books are ingested! For example, back in the day there was  quite a bit of debate about the meaning of this ngram graph:

![Google Ngram: The United States are/The United States is](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/us-are-vs-us-is1.png)

(It seems the exact query is too long for the current restrictions of the Ngram viewer, but you can see a [live version of a simpler one](https://books.google.com/ngrams/graph?content=The+United+States+are%2CThe+United+States+is&year_start=1770&year_end=2000&corpus=28&smoothing=3&direct_url=t1%3B%2CThe%20United%20States%20are%3B%2Cc0%3B.t1%3B%2CThe%20United%20States%20is%3B%2Cc0).)

Does it say something about how people conceptualized the United States, or is it just language change? (The graph is from a 2012 [article in the Atlantic](https://www.theatlantic.com/technology/archive/2012/10/bigger-better-google-ngrams-brace-yourself-for-the-power-of-grammar/263487/) by Ben Zimmer, and while that article seems to have lost its images, you can still find it in a [later blog post](https://languagelog.ldc.upenn.edu/nll/?p=8472) by Zimmer.)

Finally, the *kinds* of books in Google Books tend to skew toward academic-scientific literature, and &mdash; of particular interest to a historian &mdash; published books do not necessarily reflect hot current events topics, at least not immediately. 

For more discussions on caveats, see e.g. [this 2015 article in Wired! magazine](https://www.wired.com/2015/10/pitfalls-of-studying-language-with-google-ngram/) that also contains handy links to some more academic papers on the topic.

So, one shouldn't put too much store by ngrams, and should not jump to conclusions based on them. But then again, it's usually a bad idea to be jumping to conclusions on the basis of anything. I do think ngrams are useful, used responsibly.


## How the ngram on open shop, closed shop, union shop in Figure XXX was created

To get the data, I did a search in Google Ngrams on closed shop, open shop, union shop, using the American English corpus and the years 1875-2019. I set the smoothing at 0. That looks like this:

![Ngram closed shop, open shop, union shop](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/closedopenunion-google.png)

Or view it in [the ngram creator](https://books.google.com/ngrams/graph?content=closed+shop%2Copen+shop%2Cunion+shop&year_start=1875&year_end=2019&corpus=28&smoothing=0).

We need a few extra years at either end since we'll be smoothing the data --- that is, taking an average of several years --- so that doesn't work for the values at the edges.

I found some instructions [here](https://johannesfilter.com/how-to-export-data-from-google-ngram-viewer/), and playing around with them, figured out that now the variable is now called **ngram.data** so I found that, copied its contents, and pasted it into a text file.

![Chrome inspector screenshot](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/chromedata.png)

It looks like below. Could of course read that into Python or R, but simple enough to just copy-paste into Excel: Copy the values, separate by using text to data in the Data tab (if necessary, sometimes it gets it right just with copy-paste), copy the row, paste special with transpose to get into a column instead. Label the columns. Add another column with year values (start from the start year, i.e., 1875, and in next cell do that cell + 1, and copy-paste that into the rest of the cells in the column). Do this for each phrase in the ngram.

![data screenshot](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/data.png)

Save as csv. 

Open in RStudio for smoothing (I’m using smoothing of 7 - I tried using 3 to reproduce Google ngram’s standard smoothing of 3, but it looks different, even though I think what should be happening should be what they say they do).

```
> library(data.table)
> newdata <- data.table(ngramdata)
> newdata[, `:=`(rollNopen = frollmean(open.shop, n = 7, align = "center"))]
> newdata[, `:=`(rollNclosed = frollmean(closed.shop, n = 7, align = "center"))]
> newdata[, `:=`(rollNunion = frollmean(union.shop, n = 7, align = "center"))]
```

Next, got rid of the old columns and renamed the new, rolling mean columns. Also cut out the earliest and the latest years, so it’s now 1880-2010.

Then we need to "stack" the data or convert it from "wide" to "long" – here's an [explanation and instructions](https://towardsdatascience.com/reshape-r-dataframes-wide-to-long-with-melt-tutorial-and-visualization-ddf130cd9299). The command is the following:

```
> data_long <- melt(data = newdata, id.vars = "year", variable.name = "term", value.name = "percentage")
```


So now it looks like this:

<img src="https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/datarows.png" width=150 height=218 alt="data in rows">

You can download the data file if you like, it's `openclosed_ngram.csv`. 

Then we can get a plot, nicely formatted, by:

```
> library(ggplot2)
> ggplot(smoothedngramdata_stacked_1880.2010,aes(x=year,y=percentage,group=term)) + geom_line(aes(linetype=term)) +  scale_linetype_manual(values=c("solid", "longdash","dotted")) + theme(panel.background = element_rect(fill = 'white'), legend.position = "bottom", panel.grid.major = element_line(colour = "grey90"),  panel.grid.minor.y = element_blank(), panel.grid.major.x = element_blank(), axis.text.x.bottom = element_text(size=14), axis.text.y.left = element_text(size=14), legend.title = element_blank(), legend.text = element_text(size=14)) + scale_x_continuous(breaks=seq(1880, 2010, 10)) + scale_y_continuous(labels = scales::percent_format(accuracy = 0.0001)) +  labs(x = "", y = "")
```

And that produced the image in the book. The numbers don't quite match Google ngram &mdash; there the peak of closed shop is 0.0006 and the peak of open shop is 0.000355. On the other hand, the graph on Ngrams on google doesn’t show them right; the open shop peak goes over 0.0004 despite the #.  However, the shape is the same, and the minor differences don't change the argument.

Same procedure, of course, worked for the industrial democracy ngram.

## Some variants

Back when I first started playing with ngrams, there was an ngram viewer called Bookworm (which I think was mostly a creation of [Ben Schmidt](http://benschmidt.org/), now at NYU) that allowed one to make ngram graphs from the newspapers in [Chronicling America](chroniclingamerica.loc.gov/), the National Archives newspaper digitization project. That would of course be of quite a bit of interest to a historian, since with newspapers we know what we are looking at (that is, we don't have to wonder about what genres of books are under- or overrepresented) and since the timeline is cleaner (if "closed shop" is used a lot in newspapers in 1904, it's probably because it's an important topic that year, and not ten years earlier). The bookworm is now broken, but I saved an image (about 2014).

![Ngram of union shop, closed shop, open shop in Chronicling America newspapers](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/unionshop_bookworm.png)

Also, *The New York Times* had a wonderful service called Chronicle Labs where you could draw ngrams from NYT articles. Same deal, it's defunct now, but I have an old saved an image created ca. 2014.

![Ngram of union shop, closed shop, open shop in New York Times](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/nyt_ngram_percentage.png)

I don't recall what the specifics of these ngrams were (for example, they're a percentage of something, but of what exactly? of all bigrams that year?). However, it's nice and comforting that they more or less match up with the Google Ngram; gives me a bit more confidence that my argument about that image isn't entirely off base.

Although the closed shop language has persisted to some extent, and the *idea* that unions are "coercive" because they require people to join if the workplace is unionized has certainly persisted, the modern-day terminology isn't quite the same. To an extent, the phrase "right to work" has taken the place of "open shop", but not as clearly or dominantly. 

![Google ngram with closed shop, union shop, right to work](https://github.com/vhulden/governmentbythebosses/blob/main/ngram/images/ngram-with-rtw.png)

(The image above says `[right to work]+right to work` because often the phrase is "right-to-work" which Google represents as "[right to work]".)

You can see the original [here](https://books.google.com/ngrams/graph?content=union+shop%2Cclosed+shop%2C%5Bright+to+work%5D%2Bright+to+work&year_start=1880&year_end=2019&corpus=28&smoothing=3&direct_url=t1%3B%2Cunion%20shop%3B%2Cc0%3B.t1%3B%2Cclosed%20shop%3B%2Cc0%3B.t1%3B%2C%28%5Bright%20to%20work%5D%20%2B%20right%20to%20work%29%3B%2Cc0). It's also fun to play with some other phrases: for example, "American Plan", an alternative term for the open shop in the 1920s, "compulsory unionism" which has periodically been somewhat popular in the postwar decades, and so on. (In playing with the Ngram viewer, note that the y-axis changes as you do searches, so don't take the height of the graph too seriously! It can be helpful to contextualize your search by including a really common phrase for contrast.)
