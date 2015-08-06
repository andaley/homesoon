from model import Posting, connect_to_db, db
import json
import requests


def load_posts():
    """Load Craigslist posts from JSON into database."""

    # Retrieve JSON from Craigslist
    endpoint = 'http://sfbay.craigslist.org/jsonsearch/apa/'
    cl_json = requests.get(endpoint)

    parsed_json = cl_json.json() # returns list

    list_of_posts = parsed_json[0] # returns list of 4000 dicts

    # Testing the Craigslist data by iterating through list of dictionaries up to the 10th index.

    i = 0
    while i < len(list_of_posts)-1:
        posting = list_of_posts[i]

        # If this object has a GeoCluster key, skip it, since it's not an actual post.
        if posting.get("GeoCluster"):
            i+= 1
        else:

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

            post_id = posting.get('PostingID')
            title = posting.get('PostingTitle')
            date_posted = posting.get('PostedDate')
            url = posting.get('PostingURL')
            img_url = posting.get('ImageThumb')
            price = posting.get('Ask')
            bedrooms = posting.get('Bedrooms')
            latitude = posting.get('Latitude')
            longitude = posting.get('Longitude')

            new_post = Posting(post_id=post_id, title=title, date_posted=date_posted, url=url, img_url=img_url, price=price, bedrooms=bedrooms, latitude=latitude, longitude=longitude)
            db.session.add(new_post)

        i += 1
    db.session.commit()

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
    load_posts()
    # db.session.commit()
    print "Database updated."
    # If creating database from scratch, run db.create_all()
