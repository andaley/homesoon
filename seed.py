from model import Posting, connect_to_db, db
from server import app

def load_posts():
    """Load Craigslist posts from JSON into database."""

    fin = open('cl-data.json').read()
    parsed_json = json.loads(fin)  # returns list

    list_of_dicts = parsed_json[0] # returns list of 4000 dicts

    # Testing the Craigslist data by iterating through list of dictionaries up to the 10th index.
    i = 0
    while i < 25:
        posting = list_of_dicts[i]


        for key, value in posting.items():
            print 'Key: %s, Value: %s'% (key, value)
        i += 1

    # TODO: ignore all objects without a posting URL

if __name__ == '__main__':
    connect_to_db(app)
    # If creating database from scratch, run db.create_all()
