from model import Posting, User, Favorite, connect_to_db, db
import json
import requests
import sqlite3

# List of craigslist URLs. Can add any city to this list as long as we have the city prefix.
city_list = ['http://sfbay.craigslist.org/jsonsearch/apa/', 'http://portland.craigslist.org/jsonsearch/apa/', 'http://seattle.craigslist.org/jsonsearch/apa/']

def load_posts(city_list):
    """Load Craigslist posts from JSON into database.

    Upon first seed, this will create all tables and gather Craigslist data.
    When re-seeding, will remove all posts that have not been favorited by a user, then
    update database with fresh Craigslist data.

    Recommended: re-seed database once per day or every other day to maintain up-to-date data.
    """

    # Delete any post that hasn't been favorited.
    query = "DELETE FROM postings WHERE is_favorited = 0"
    db.session.execute(query)
    db.session.commit()

    for link in city_list:

        # Retrieve JSON from Craigslist
        cl_json = requests.get(link)

        parsed_json = cl_json.json() # returns list

        list_of_posts = parsed_json[0] # returns list of 4000 dicts

        for posting in list_of_posts:

            # If this object has a GeoCluster key, skip it, since it's not an actual post.
            if posting.get("GeoCluster"):
                continue


            if not Posting.query.get(posting.get('PostingID')):

                # Example key value pairs:
                    # 0 Ask: 2400
                    # 1 ImageThumb: 'http:\/\/images.craigslist.org...jpg'
                    # 2 Latitude: 38.927686
                    # 3 PostingTitle: 'title'
                    # 4 PostedDate: '1438725510'
                    # 5 Longitude: -122.3888
                    # 6 PostingURL: '\/\/sfbay.craigslist.org...html'
                    # 7 Bedrooms: '2'
                    # 8 CategoryID: '1'
                    # 9 PostingID: '5156767694'

                # Reformat img url to display as HTML in infoWindow
                raw_img_url = posting.get('ImageThumb')
                if raw_img_url:
                    new_url = raw_img_url.split(',')
                    img_url = new_url[0] + '_300x300.jpg'

                post_id = posting.get('PostingID')
                title = posting.get('PostingTitle')
                date_posted = posting.get('PostedDate')
                url = posting.get('PostingURL')
                price = posting.get('Ask')
                bedrooms = posting.get('Bedrooms')
                latitude = posting.get('Latitude')
                longitude = posting.get('Longitude')
                new_post = Posting(post_id=post_id, title=title, date_posted=date_posted, url=url, img_url=img_url, price=price, bedrooms=bedrooms, latitude=latitude, longitude=longitude)
                db.session.add(new_post)

    db.session.commit()

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
    load_posts(city_list)
    print "Database updated."
