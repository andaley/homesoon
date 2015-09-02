# HomeSoon

HomeSoon helps renters find housing within a reasonable commute distance. By seeding data from Craigslist, HomeSoon lets users search for a new apartment according to their budget, method of transportation, and desired distance from work. HomeSoon uses the Google Maps API to display a user's search results, where they can view further details such as an image, how the price compares to the average rent of their search, and most importantly, how long it would take to get to work from that location. Additionally, HomeSoon uses Chart.js to provide interactive charts helping users analyze their search.

HomeSoon was built by Noelle Daley over the course of 3 and half weeks as part of the [Hackbright Academy](http://www.hackbrightacademy.com/) Summer 2015 fellowship.

![Homepage](/screenshots/home.png)

### Contents
- [Technology Stack](#technology-stack)
- [Feature List](#feature-list)
- [Accessing Craigslist data](#accessing-craigslist-data)
- [Calculating Distance](#calculating-distance)
- [Installation](#installation)
- [Additional Screenshots](#additional-screenshots)


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

- [x] Scrape data from Craigslist, parse, and store in database (Python, SQLite)
    - [x] Store data from SF Bay Area
    - [x] Add support for Portland
    - [x] Add support for Seattle
    - [x] Automate `seed.py` to add any city, given the Craigslist prefix
- [x] Set up HTML form for querying database by price, number of bedrooms, and proximity to work/point of interest (Google Geocoding Service, Google Places API)
- [x] Query database for posts within users' desired distance (Euclidean distance formula, Python)
- [x] Display search results as markers on a map (Google Maps API, Javascript / jQuery)
- [x] Allow user to modify search (HTML, jQuery, AJAX)
- [x] When user clicks on a result, calculate the commute time and distance from that location to their work/point of interest (Google Distance Matrix, AJAX)
    - [x] Calculate commute time according to preferred method of transportation (driving, public transportation, bicycling, or walking), and link to directions in separate tab
- [x] Calculate average price of search results (Python, AJAX)
    - [x] Compare each post with average price
- [x] Allow users to sign in or sign up for an account (Python)
- [x] Allow users to save a post and commute time for later viewing (SQLite, AJAX, Javascript)
   - [x] Allow users to remove a post from their list of favorites
- [x] Display charts with information about users' search (Chart.js, Javascript)
    - [x] Show number of posts and average rent
    - [x] Show number of posts if user were willing to pay more or commute farther
- [x] Display charts about Craigslist data in general (Chart.js, SQLite)
    - [x] Number of 1, 2, or 3 bedroom places
    - [x] Average price of 1, 2, or 3 bedrooms places per city


### Accessing Craigslist Data

One of the most interesting challenges I encountered while working on this project was accessing Craigslist data, parsing it, and storing it in my database. Craigslist does not have an official API nor do they offer (or allow) a formal way of interacting with their data. However, through a combination of inspecting network calls and testing, I was able to get the data I needed and format it accordingly. To see exactly how I accomplished this, you can check out `seed.py`.


### Calculating Distance



### Installation

1. After cloning this repo, set up your virtual environment & activate it.

  ```
  pip install virtualenv
  virtualenv env/
  source env/bin/activate
  ```
2. Install the requirements:
  ```
  pip install -r requirements.txt
  ```
  NOTE: You will need a Google Maps API key to access the Google Distance Matrix. If you don't already have one, follow [these](https://developers.google.com/maps/documentation/javascript/tutorial) instructions from Google.

3. Once you have your API key, store it in a shell file called `secrets.sh` as follows:
  ```
  export GOOGLE_MAPS_TOKEN="YOUR_KEY_HERE"
  ```

4. Then, go back to your terminal and source it.
  ```
  source secrets.sh
  ```

5. Back in your terminal, gather data from Craigslist with the command `python seed.py`.

6. Run `python tests.py` to verify the data structure from Craigslist hasn't changed.

7. Lastly, run `python server.py` and visit `localhost:5000/` in your web browser of choice to use the app.

### Additional Screenshots

#### Example search results
![Search results](/screenshots/search-results.png)

#### Analyze your search
![Charts 1](/screenshots/charts-1.png)

#### Compare prices per city
![Charts 2](/screenshots/charts-2.png)
