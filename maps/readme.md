# Mapping people

## Map of NAM members in St. Louis

The data for this and its geocoding explanation are in the [socialnetwork](https://github.com/vhulden/governmentbythebosses/tree/main/socialnetwork) folder, because the residence information is also used in linking people into a network.

From that geocoded data, I simply took the NAM members and made [a map](https://api.mapbox.com/styles/v1/vhulden/ckkqo3fzq1mgw17mm6f74ha9s.html?fresh=true&title=copy&access_token=pk.eyJ1Ijoidmh1bGRlbiIsImEiOiJjaXhkYzFmc3UwMGtnMm9sZnZob2psbmJlIn0.cdxpQbloljQQ7KtgZHkKJQ) with MapBox Studio. 


## Heatmap of active NAM members

As explained in the membersinfo folder, I have a list of "active" NAM members. For the map, I took everyone with a score of 2 or more.  From that list, I took just their ID and the city and state in which they lived. Then I fed that a into the [GPS Visualizer](https://www.gpsvisualizer.com/geocoder/), which returns a geocoded file (where the city&state info gets a latitude and longitude). The file with all that info is `nam-activemembers-states.csv`.

I then took that and made [a map](https://api.mapbox.com/styles/v1/vhulden/cklewcktt0fe917sbgh75hjqa.html?fresh=true&title=copy&access_token=pk.eyJ1Ijoidmh1bGRlbiIsImEiOiJjaXhkYzFmc3UwMGtnMm9sZnZob2psbmJlIn0.cdxpQbloljQQ7KtgZHkKJQ) with MapBox Studio. Ideally, I would have wanted to use dots and to make it interactive so you could hover over the dots and see who they represent, but because the address data is just city & state, every dot for a particular city is on the exact same spot, so that won't work. The heatmap seemed a better way of showing where there were a lot of members.

The same data can of course make other maps too. Here's a [per-state choropleth map](https://docs.google.com/spreadsheets/d/e/2PACX-1vSsJcuJ9JFb4MYF0TZbrA4jwEdf8hzyBKJJC0queCudGMduzqQ5iOFj1iWN1EOooWEINR5DK9w8fA0r/pubchart?oid=1273408223&format=interactive) created with Google Sheets (incidentally, creating these could not be easier; see e.g. the [instructions at GeoAwesomeness](https://geoawesomeness.com/make-awesome-interactive-map-using-google-sheets-1-minute/). (Below, you have the map as an image; if you click on the link above you can get the interactive version that shows you howm many members each state has).

![Active NAM members per state](https://github.com/vhulden/governmentbythebosses/blob/main/maps/activemembers.png)

That was made from the same data; I just made a pivot table of the state column in Excel and then uploaded that data into Google Sheets (the file is `nam-activemembers-states.csv`).
