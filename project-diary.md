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

TODO

- Test Google Distance Matrix w/ dummy data
- Test adding info windows to map w/ dummy data
- Sort results by distance
- Modify query to check for price and bedrooms
- Add support for East Bay and Portland