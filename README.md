# morning.thechels.uk

Good Morning.

Morning, is a home page built daily at 5:00 UTC using github-actions, utilising python scripts to get the latest news, weather, sports fixtures, stocks, quotes, and other useful information.

## Prerequisites

In order for this solution to work you need to enter some secrets

1. An open weather API key - you can register for a free account on their website.
2. Latitude and Longitude for the weather API.
3. Your city code e.g Bristol to work with the coronovirus API
4. Update websites.json with your list of website rss feeds you care about.
5. Update stocks.json with the ticker ids for the stocks.
6. Update tournaments.json with the list of competition slugs used by the BBC in order to get the relevant fixtures (its only football at this stage, as that is all I care about).
7. Update quotes.json with your favourite quotes.

## Contributing

We welcome pull requests if you want to add more information to the homepage, then we might need to think about having some config to feature switch off certain elements depending on individual user needs.
