"""Model and database functions for Craigslist searcher."""

from flask_sqlalchemy import SQLAlchemy
import math

db = SQLAlchemy()

######### Model definitions #########

class Posting(db.Model):
    """Each object represents a Craigslist apartment post."""

    __tablename__ = "postings"

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.Integer)
    url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Post: %s price: %s bedrooms: %s>" % (self.post_id, self.price, self.bedrooms)

    # TODO: Wrap class methods into one 'get apartments' function.

    @classmethod
    def get_lat_lons(cls, max_rent, num_rooms):
        """
        Given price and # of bedrooms, return list of ids, latitudes and longitudes.
        """

        # First, retrieve list of ids, latitudes, and longitudes of apts
        # with desired number of bedrooms and within budget.
        query = db.session.query(cls.post_id, cls.latitude, cls.longitude).filter(cls.price < max_rent, cls.bedrooms == num_rooms)

        all_lat_lons = query.all()

        return all_lat_lons

    @classmethod
    def calculate_distance(cls, all_lat_lons, origin_lat, origin_lon, desired_distance):
        """
        Given list of tuples with (id, latitude, longitude), origin lat/lon, and desired distance, calculate distance from origin.
        If distance is within desired range, retrieve that apartment object and add to list.

        Returns list of apartment objects.
        """

        matching_apts = []
        for post_id, lat, lon in all_lat_lons:

            # Calculate Euclidean distance
            distance_deg = math.sqrt((lat - origin_lat)**2 + (lon - origin_lon)**2)

            # Convert distance to miles
            distance_mi = distance_deg * 69.0

            if distance_mi < desired_distance:
                matching_apts.append(cls.query.get(post_id))

        return matching_apts

    @classmethod
    def get_apartments(cls, max_rent, num_rooms, origin_lat, origin_lon, desired_distance):
        """
        Find apartments meeting the user's preferences. Returns a list of apartment objects.
        """

        l = cls.get_lat_lons(max_rent, num_rooms)
        r = cls.calculate_distance(l, origin_lat, origin_lon, desired_distance)

        return r

######### Helper Functions #########

def connect_to_db(app):
    """Connect database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cl.db'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    """Allow us to interact with database when run in interactive mode."""

    from server import app
    connect_to_db(app)
    print "Connected to db."
