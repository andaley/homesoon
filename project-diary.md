### Project Diary

##### Week 0
7/31
- Drafted this proposal and outline :)
- Researched Google Maps API
- Toyed with Craigslist data
  - Potential blocker: data is formatted terribly and is inconsistent!

8/2
- Drafted, revised, and sent out user research survey
- Received 47 responses

##### Week 1
8/3
- Analysed survey responses
- Data structure confirmed // successfully iterated through 10 sample postings
- Completed Google Maps tutorial
- Drafted user stories
- Drafted sample home page
- Met with mentor to discuss databases and architecture
- Researched Google distance matrix
- Figured out how Craigslist filters their searches
- Library that calculates distance might not be necessary b/c of Google Distance Matrix API
- Challenges:
  - When user enters address, need to query database and find all listings where x<lat<y and x2<lon<y2, which will return all points within a square
  not ideal b/c some apts won’t actually be within proper distance
  - Google distance has API limit which means I might need to only make one API call and save the results as “dummy data"
  to prevent Craigslist shutting me off will need to populate database manually for demo night
  - Maybe show example query on demo day but also show code for how you'd run in production


8/4
- set up database
- set up model and seed file!
- set up flask skeleton
- wrote base.html
- tested server
- challenge:
  - should I use SQLite & euclidean distance or Postgres & earth distance?

8/5
- wrote query for calculating distance from target location
walked through google maps tutorial and added two points to sample map
- use requests library to pull down Craigslist object every time I run seed.py
- add distance query to server
- Tested plotting multiple points on map w/ dummy data
- Challenge:
  - SQL can’t process SQRT or square; need to install extension

8/6
- Tested SQL distance query with hard coded lat/lon -- it works!
- Test SQL distance query w/ user inputted lat/lon
- Successfully connected html form with server
- Displayed results of search as text with post id, latitude, longitude, and distance from origin
- Added map to results page!
- Modify query to check for price and bedrooms
- Moved query to separate route; using AJAX to retrieve results

8/7
- Moved distance and get apartments function into model as class methods
- Wrote two unit tests for model.py
- Challenge: imgs aren't showing up

8/10
- Centered map according to origin latitude and longitude
- Created origin marker with special formatting [https://github.com/Concept211/Google-Maps-Markers#usage-premade]
- Updated event listener to prepare for calculating distance
- Wrote AJAX call and updated infoWindow with sample content
- Tested Google Distance Matrix w/ dummy data
- Calculated distance with real data
- Displayed distance results on marker
- Challenges:
  - adding event listener to each marker that calculates distance; currently piggy backed onto listener for bindinfoWindow but isn't a good long term solution
  - distance is being calculated every time user clicks marker; need to fix

8/11
- added ability to select transportation method
- added geocoding to user inputted address
- Challenge: re-seeded database & img url is still getting cut off
- researched Python Google Maps wrapper
- Added nav bar to allow people to modify search
- updated CSS with navbar and footer
- wrote Google Distance Matrix and Geocoding test
- wrote test for seed.py

8/12
- switch form submission from GET to POST
- added sign in route
- added sign in form (but formatting is messed up)
- fixed bug where distance was being displayed multiple times by replacing setContent with span IDs and jQuery
- linked distance to actual Google Maps directions; however link defaults to driving directions
- improved efficiency of get_lat_lons database query; checks that objects are within square boundary before checking Euclidean distance
- Challenge: is it faster to query for tuples first, check tuples, and then pull object? Or to pull list of objects, then check if object attributes fit Euclidean distance?

8/13
- added users class and table
- improved efficiency of get_apartments db query
- added expired column to Posting table
- added test user to user table
- added sign in route; linked to sign in form
- added sign up form
- added Favorites table
- inserted test favorite data
- new users can now sign up and be added to database
- toggle sign in / sign out based on login status
- added sign out route
- populated favorites page
- Refactored seed file to remove Postings not in Favorites & update db with new posts

8/14
- added button to save to favorites
- created add to favorites route
- created add to favorites event listener and ajax call
- stored favorite in database if user is logged in

8/16
- Successfully added data from other city (Portland)

8/17
- researched Google directions API
- got majorly stuck trying to refactor Javascript; ended up discovering bug where city data was being overwritten
  - fixed this!
- switch google maps directions link to users' preferred transportation method
- fixed seed and get apartments test
- started calculating average price per search

8/18
- added support for Seattle
- added test that verifies data from all cities are in DB
- added post url to favorites table
- fixed bug where favorites weren't being committed to database
- added avg rent to apartment results
- added averge rent to infoWindow
- updated homepage search with placeholder values
- FIXED IMAGES!!!!!!
- added % more / less than average rent

8/19
- added stats route and template to display rent / distance metrics
- wrote sample query and displayed on page as text
- displayed average rent, # posts farther away, and # more expensive posts for search on page
- realized x, x2, y, y2 are way off in get_apartments

8/20
- fixed class methods
 for calculating number of posts more expensive

TODO
- allow user to remove favorites
- write new class method for calculating number of posts that are 5, 10, 20 miles farther
- add submit button for refreshing charts w/ new search
- dynamically set zoom according to number of markers
- change color of marker when user clicks
- compartmentalize map.js for easier legibility
- add selenium tests
- Add charts w/ average rent price, number of results
