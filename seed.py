from model import Posting, connect_to_db, db
from server import app

def load_posts():
    """Load Craigslist posts from JSON into database."""

    fin = open('cl-data.json').read()
    parsed_json = json.loads(fin)  # returns list

    list_of_posts = parsed_json[0] # returns list of 4000 dicts

    # Testing the Craigslist data by iterating through list of dictionaries up to the 10th index.
    i = 0
    while i < 25:
        posting = list_of_posts[i]

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

        post_id = posting[9]
        title = posting[3]
        date_posted = posting[4]
        url = posting[6]
        img_url = posting[1]
        price = posting[0]
        bedrooms = posting[7]
        latitude = posting[2]
        longitude = posting[5]

        new_post = Posting(post_id=post_id, title=title, date_posted=date_posted, url=url, img_url=img_url, price=price, bedrooms=bedrooms, latitude=latitude, longitude=longitude)
        db.session.add(new_post)

        i += 1
    db.session.commit()

    # TODO: ignore all objects without a posting URL

if __name__ == '__main__':
    connect_to_db(app)
    # If creating database from scratch, run db.create_all()
