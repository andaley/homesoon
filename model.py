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
    img_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_favorited = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Post: %s, price: %s, bedrooms: %s>" % (self.post_id, self.price, self.bedrooms)


    @classmethod
    def get_apartments(cls, max_rent, num_rooms, origin_lat, origin_lon, desired_distance):
        """
        Given price, # of bedrooms, max price, and origin, return list of apartment objects within desired distance.
        """

        # X and Y correspond to latitudes and longitudes that form a square boundary from the origin. Use these values inititally to query database, then check Euclidean distance after to ensure they fall within the circular boundary.
        MILES_TO_DEGREES = 69.0
        distance_degrees = desired_distance * MILES_TO_DEGREES

        x = origin_lat - distance_degrees
        x2 = origin_lon + distance_degrees
        y = origin_lat - distance_degrees
        y2 = origin_lon + distance_degrees

        # Retrieve list of apts with desired number of bedrooms, within budget, and that are within desired distance range.
        apartment_list = cls.query.filter(cls.price < max_rent, cls.bedrooms == num_rooms, cls.latitude > x, cls.latitude < x2, cls.longitude > y, cls.longitude < y2).all()

        # Check Euclidean distance of each apartment in list.
        # If apartment is within range, add to matching_apts list.
        matching_apts = [apt for apt in apartment_list if apt.check_euclidean_distance(origin_lat, origin_lon, desired_distance)]

        return matching_apts


    def check_euclidean_distance(self, origin_lat, origin_lon, desired_distance):
        """
        Given an apartment object, origin latitude/longitude, and desired radius, calculate Euclidean distance.
        If distance is within desired range, return True.
        """

        MILES_TO_DEGREES = 69.0

        # Calculate Euclidean distance
        distance_deg = math.sqrt((self.latitude - origin_lat)**2 + (self.longitude - origin_lon)**2)

        # Convert distance to miles
        distance_mi = distance_deg * MILES_TO_DEGREES

        # If apt is farther than desired distance, return False.
        if distance_mi > desired_distance:
            return False

        return True

    @classmethod
    def calculate_avg_rent(cls, apartments):
        """Calculates average rent for a given list of apartment objects."""

        rents = [cls.price for post in apartments]
        avg_rent = float(sum(rents)/len(rents))

        return avg_rent


class User(db.Model):
    """Represents a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<user_id: %s, username: %s>" % (self.user_id, self.username)


class Favorite(db.Model):
    """Stores all apartments that users have favorited."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.ForeignKey("postings.post_id"))
    user_id = db.Column(db.ForeignKey("users.user_id"))
    origin = db.Column(db.String(50))
    commute_time = db.Column(db.String(10))

    post = db.relationship("Posting", backref=db.backref("favorites", order_by=post_id))
    user = db.relationship("User", backref=db.backref("users", order_by=user_id))

    def __repr__(self):
        return "<favorite_id: %s, post_id: %s, user_id: %s>" % (self.favorite_id, self.post_id, self.user_id)

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
