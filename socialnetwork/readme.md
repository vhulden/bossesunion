# Documentation of the creation of the social networks

## Book of St. Louisans

There are two editions of the Book of St. Louisans, [1906](https://hdl.handle.net/2027/loc.ark:/13960/t6rx9kb8c) and [1912](https://hdl.handle.net/2027/yale.39002028025832) (the links take you to the book in HathiTrust). I have combined both and tried to eliminate duplicates (though I'm aware some duplicates do remain).


*The Book of St. Louisans* (BSTL) creates the networks of individuals, because the book has biographical snippets like this:

![BSTL entry](https://github.com/vhulden/governmentbythebosses/blob/main/socialnetwork/images/bstl-entry.png)

I tried to clean the texts as best I could to get one person per row, mainly using [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) in a texteditor (TextMate). The rest of the procedure was as follows:

The information is extracted using the `extractbios.py script`. That script is run for each edition (1906 and 1912). Then the two lists are combined using `combinebios.py`. The script attempts to remove duplicates (by eliminating matching lastname, firstname, and birthyear) and succeeds to some extent: the list of 1906 entries has 3465 rows, the 1912 edition has 3764 rows (original had 4717, but removed rows that were simply “See vol 1906” before even processing the text), and the combined has 5056 rows, so 2173 duplicates have been removed.

The list produced by the combining script (`BookOfStLouisansInfo_BothEds.tsv`) is then opened in [OpenRefine](https://openrefine.org/). Created a new column using lastname, firstname, and birthyear (birthyear is more reliable than e.g. middle name, esp. as fathers and sons often have the same name). Note that need to first set birthyear to empty string, it can’t be null, see [here](https://guides.library.illinois.edu/openrefine/combining). Cluster on that with the available methods (mainly levenshtein max 2). Star the incorrect versions and then facet by star and delete. This duplicate removal results in a total of 4910 rows. The file is `BookOfStLouisansInfo_OpenRefined_edited.tsv`.

Open that file in Excel and grab just the ID and address (residence) field for geocoder. Separate number from street and clean; mostly manually, with regex replaces. Put into format suitable for the [U.S. Census Geocoder](https://geocoding.geo.census.gov/geocoder/) and code. Matching rate: 54.16% of total addresses found an exact match, a further 10.04% a non-exact match, and by adding a few hotels manually we get another 1.73%. (Will only use the exact and added [hotel] matches in the SN).

![Percentages of different types of geolocation matches](https://github.com/vhulden/governmentbythebosses/blob/main/socialnetwork/images/geomatches.png)


### Hotels:

*Buckingham Hotel* (listed as residence for 47 people) has coordinates on Wikipedia, I’m adding those and counting that as exact.
*Washington Hotel* (listed as residence for 31 people) - can’t locate.
*Beers Hotel* (listed as residence for 9 people) is identified at the [University of Missouri at St. Louis digital collection]((https://dl.mospace.umsystem.edu/umsl/islandora/object/umsl%3A36554) as being on the site of what is now the Krantzberg Arts Center, located on Google Maps and coordinates taken from there.
*Buckingham Club* (12 people) noted [here](https://atthefair.homestead.com/Misc/Accom.html) as having been at Kingshighway and Pine, coordinates from Google Maps
*Jefferson Hotel* (12 people) noted in *St. Louis: 1875-1930* by Joan M. Thomas as having become the Jefferson Arms on Tucker, coordinates from Google Maps

There are a few more but the payoff seems too low to bother.

Run addgeoresults.py to add the geolocation data to the masterfile. The main file is now BookOfStLouisansInfo_Complete.tsv.

Note that there was originally a column ‘role’ that marks if a person was member of NAM, mainly - this is restored from an old file, but basically it’s created from looking up individuals in NAM membership lists and correspondence. There are a couple of other role codes that I earlier thought might be useful but that don’t really seem to be (have deleted those roles from current files, and converted the column to NAM column along the lines of BLM/CIA etc. columns. (Role codes: NAM =1;MO  fed legislator = 2; MO state legislator = 3; Other legislator = 4).

The next step is to create the actual social network files. This is done with `snalinks-bsl-revised.py`, which a) calculates distance between residences and creates a link if the distance is smaller than 0.1 miles; b) creates links based on shared club membership; c) creates links based on shared association membership (for a separate network).

That is made into a network in [Cytoscape](https://cytoscape.org/), a free network-creation software that is used in biology but also works nicely for non-biology networks. (I used to use [Gephi](https://gephi.org/) but gave up on it quite a while ago because things were just too complicated and it kept crashing. People do still use it; I haven't checked where it's at for a while.)

The Cytoscape SN file is `BSTL-network.cys`. There, *Book of St Louisans Everyone* has the clubconnectionscount and geoconnections, created by the `snalinks-bsl-revised.py` script. Those are merged into the *BSTL Everyone - GeoPlusClubs* network, and the `BookOfStLouisansInfo_Complete.tsv` is imported as a network table so the nodes are associated with the right individuals. This is the complete set with no cuts.  

In addition, since we’re mainly interested in the businessmen, the .cys network contains a representation of the network of members of business associations. The slicing is done with `slice-bstl.py` — get only those who list membership in BMA/BML, CIA/CA, MFA or who are identified as NAM members. There are 472 such individuals. Saved in `BSTL-businessmen.tsv`.

That is then fed into the `snalinks-bsl-revised.py` script for making geolinks and clublinks between just this group. That produces  `BSTL-businessmen_clubconnectioncounts.txt` and `BSTL-businessmen_geoconnections.txt` which are fed to another script, `mergenetworks.py`, combines both types of links (while also restricting to only 3-or-more-clubs links; the geolinks are already <0.1 miles). That network file, `BSTL-businessmen_geo_and_socialconnections.txt` is then fed into Cytoscape; it's the one that contains the network shown in the book is constructed. It uses the Allegro Fruchterman Reingold algorithm, mostly with default settings, with some scaling added to make it a bit more legible.

(Note: in the Cytoscape file this is the last network in the list; the others are various intermediate products, either not restricted to businessmen or constructed from the separate social-club-link and geolink files; originally I merged and restricted those using Cytoscape, but then realized that I wasn't entirely sure how that worked and why it made the display choices it did. Merging them manually with a script also allowed me to identify individuals who are linked _both_ by geography _and_ by social clubs and to show those links in a different color/line.)

## Gould's Blue Book

Gould’s Blue Book (also [available in HathiTrust](https://hdl.handle.net/2027/mdp.39015073276126)) is used to create a network of the clubs themselves. It is a list of club membership lists, essentially, like this:

![Gould's Blue Book Club entry](https://github.com/vhulden/governmentbythebosses/blob/main/socialnetwork/images/goulds.png)

The text file (`Gould_s_Blue_Book_for_the_City_of_St_Louis_1912_ClubsOnly2.txt`) is processed with OpenRefine to try to consolidate the name + address lines so they’ll match. Did OpenRefine first, then did manual cleaning in TextMate with regexes and just scrolling and fixing, and then one more pass in OpenRefine. Note: replaced first names with initials if there was a middle initial, so *Ballard John O.* became *Ballard J.O.* but *Bailey Warren* would remain *Bailey Warren*.  In consolidating, tried to be a bit careful so as not to confound people who are father and son, or brothers, or something. Still, even if there are a few of those, that’s a kind of a connection in itself, so it’s not too terrible.

The script `infogoulds.py` extracts the info about what members a club has into a json dict file. Note that member info contains the address; seemed more reliable that way. The script `gouldslinks.py` then creates a bipartite network (so the links are member-to-club, not member-to-member or club-to-club). That is converted into a unimodal network of club-to-club connections with the R package *ProjectoR*, as described in [Miriam Posner's tutorial for this](https://github.com/miriamposner/cytoscape_tutorials/blob/master/get-a-unimodal-network.md). The result is `GouldsClubLinks.csv` (well, almost, have to get rid of the quotes with a find and replace).

That is then further processed with `gouldsmemberpercent.py` to calculate more useful weights than sheer shared number of members. That produces two important numbers: the shared member percentage and the percentage of shared members of the smaller club’s total membership.  The latter is more useful in showing the tightness of the connection between two clubs; the former is used to weight edges in the large graph showing all clubs.

So this is the basic shared member percentage calculation:

````
      shared
------------------- *100 
  A + B - shared
  ````

The calculation based on the smaller club is:

````

        shared
------------------------------    *100
membership of smaller club

````

The network is drawn in `Goulds-network.cys`. The network used in the book is the one based on shared membership as percentage of the membership of the smaller club; that way the centrality of the tiny clubs like Log Cabin and Cuivre is visible. The larger network could of course fairly easily be shown as the basic shared membership version, but then the central-clubs network would have a different look, whereas with doing both from the smaller-clubs version allows one to just extract the central ones from the main network and keep their look and position the same as in that network. However, in the larger network the weight of edges is determined by the basic shared member percentage calculation.

