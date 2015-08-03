# Hackbright Final Project


## Overview
___ allows users to search for housing based on proximity to a given location and commute time.

### Feature List
- Allow user to enter a key point of interest & select how far they're willing to commute
- Scrape Craigslist for housing posts
- Calculate distance between Craigslist posts & key point of interest
- Display results:
  - As text with calculated distance
  - As points on a map
- When user clicks on a result, compute commute time:
  - By driving
  - By public transportation


### User Stories

### Research
**Technologies needed:**
- Craigslist data
- Library for calculating distance given latitude and longitude
- Map API
  - Google Maps
  - Mapbox

**Tutorials and documentation:**
- [Python Guide to JSON](http://docs.python-guide.org/en/latest/scenarios/json/)
- [Python Google Distance Matrix](https://github.com/argaen/python-google-distance-matrix)
- [Mapbox API](https://www.mapbox.com/developers/api/directions/)
- [Google Distance Matrix](https://developers.google.com/maps/documentation/distancematrix/intro)
- [Google Maps Javascript API Tutorial](https://developers.google.com/maps/tutorials/fundamentals/adding-a-google-map)

**Possible Challenges:**
- Load time for calculating distance
- Load time for calculating commute time

### Project Diary

##### Week 0
- Drafted this proposal and outline :)
- Researched Google Maps API
- Toyed with Craigslist data
  - Potential blocker: data is formatted terribly and is inconsistent!
