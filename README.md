# HomeSoon
### Hackbright Academy Final Project, Summer 2015
HomeSoon helps renters find housing within a reasonable commute distance. By seeding data from Craigslist, HomeSoon lets users search for a new apartment according to their budget, method of transportation, and desired distance from work. HomeSoon uses the Google Maps API to display a user's search results, where they can view further details such as an image, how the price compares to the average rent of their search, and most importantly, how long it would take to get to work from that location. Additionally, HomeSoon uses Chart.js to provide interactive charts helping users analyze their search.


### Contents
Technology Stack
Feature List
Accessing Craigslist data
Calculating Distance
Installation


### Technology Stack:
- Python
- Flask
- Javascript / jQuery
- SQLite / SQLAlchemy
- Craigslist
- Google Maps API
- Google Distance Matrix
- Google Geocoding Service
- Google Places
- Chart.js
- HTML / CSS
- Bootstrap

### Feature List

- [x] Scrape data from Craigslist and store in database (Python, SQLite)
- [x] Set up HTML form for querying database by price, number of bedrooms, and proximity to work/point of interest (Google Geocoding Service, Google Places API)
- [x] Display search results as markers on a map (Google Maps API, Javascript / jQuery)
- [x] When user clicks on a result, calculate the commute time and distance from that location to their work/point of interest (Google Distance Matrix, AJAX)
- [x] Calculate commute time according to their preferred method of transportation (driving, public transportation, bicycling, or walking), and link to directions in separate tab (Google Distance Matrix, AJAX)
- [x] 

### Installation

After cloning this repo, set up your virtual environment & activate it.
```
pip install virtualenv
virtualenv env/
source env/bin/activate
```
Install the requirements:
```
pip install -r requirements.txt
```
NOTE: You will need a Google Maps API key to access the Google Distance Matrix. If you don't already have one, follow [these](https://developers.google.com/maps/documentation/javascript/tutorial) instructions from Google.

Once you have your API key, store it in a shell file called `secrets.sh` as follows:
```
export GOOGLE_MAPS_TOKEN="YOUR_KEY_HERE"
```

Then, go back to your terminal and source it.
```
source secrets.sh
```

Back in your terminal, gather data from Craigslist with the command `python seed.py`.

Run `python tests.py` to verify the data structure from Craigslist hasn't changed.

Lastly, run `python server.py` and visit `localhost:5000/` in your web browser of choice to use the app.
