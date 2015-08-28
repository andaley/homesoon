# HomeSoon
### Hackbright Academy Final Project, Summer 2015
HomeSoon helps renters find housing within a reasonable commute distance. By seeding data from Craigslist, HomeSoon lets users search for a new apartment according to their budget, method of transportation, and desired distance from work. HomeSoon uses the Google Maps API to display a user's search results, where they can view further details such as an image, how the price compares to the average rent of their search, and most importantly, how long it would take to get to work from that location. Additionally, HomeSoon provides interactive charts helping users analyze their search.

### Built With:
- Python
- Flask
- Javascript / jQuery
- SQLite / SQLAlchemy
- Google Maps API
- Google Distance Matrix
- HTML / CSS
- Bootstrap

### Installation

After cloning this repo, set up your virtual environment & activate it.
```
pip install virtualenv
virtualenv env/
source env/bin/activate
```
Install the requirements
```
pip install -r requirements.txt
```
NOTE: You will need a Google Maps API key to access the Google Distance Matrix. If you don't already have one, there are instructions from Google here. https://developers.google.com/maps/documentation/javascript/tutorial

Once you have your API key, store it in a shell file called `secrets.sh` as follows:
```
export GOOGLE_MAPS_TOKEN="YOUR_KEY_HERE"
```

Then, go back to your terminal and source it.
```
source secrets.sh
```
