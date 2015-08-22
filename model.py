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
    def calculate_outer_bounds(cls, origin_lat, origin_lon, desired_distance):
        """Given origin latitude, longitude, and desired distance, calculate the
        """

        # X and Y correspond to latitudes and longitudes that form a square boundary from the origin. Use these values inititally to query database, then check Euclidean distance after to ensure they fall within the circular boundary.
        MILES_TO_DEGREES = 69.0
        distance_degrees = desired_distance / MILES_TO_DEGREES

        x = origin_lat - distance_degrees
        y = origin_lon - distance_degrees
        x2 = origin_lat + distance_degrees
        y2 = origin_lon + distance_degrees

        return [x, y, x2, y2]


    @classmethod
    def get_apartments(cls, max_rent, num_rooms, origin_lat, origin_lon, desired_distance):
        """
        Given price, # of bedrooms, max price, and origin, return list of apartment objects within desired distance.
        """

        x, y, x2, y2 = Posting.calculate_outer_bounds(origin_lat, origin_lon, desired_distance)

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

        rents = [int(post.price) for post in apartments]
        avg_rent = (sum(rents))/len(rents)

        return avg_rent


    @classmethod
    def get_more_expensive(cls, price, bedrooms, origin_lat, origin_lon, desired_distance):
        """
        Given users' search parameters, find number of apartments that are more expensive. Returns dictionary where key 'one_hundred' contains apartments that the user could find if they increased their maximum price by $100.
        """

        # t = Posting.get_more_expensive(3000, 1, 37.7914448,-122.3929672, 5)

        x, y, x2, y2 = cls.calculate_outer_bounds(origin_lat, origin_lon, desired_distance)

        # Gather all pofst_ids and prices that are more expensive than original price.
        total_more = db.session.query(cls.price, cls.post_id).filter(cls.price > price, cls.bedrooms == bedrooms, cls.latitude > x, cls.latitude < x2, cls.longitude > y, cls.longitude < y2).all()

        # These lists will contain apartment ids and prices that are within $100, $200, or $300 of original price.
        one_hundred = []
        two_hundred = []
        three_hundred = []

        price = int(price)
        for apt_price, post_id in total_more:
            if apt_price > (price + 200) and apt_price <= (price + 300):
                three_hundred.append(apt_price)
            elif apt_price > (price + 100) and apt_price <= (price + 200):
                two_hundred.append(apt_price)
            elif apt_price > price and apt_price <= (price + 100):
                one_hundred.append(apt_price)

        more_expensive = {'total': len(total_more),
                            '$100 more': len(one_hundred),
                            '$200 more': len(two_hundred),
                            '$300 more': len(three_hundred)}

        return more_expensive


    @classmethod
    def get_farther_away(cls, price, bedrooms, origin_lat, origin_lon, desired_distance):

        """Calculate # posts within 5, 10, 20 miles of origin.

        Returns a dictionary where the key is the distance in miles from origin, and the value is a list with the # of posts within that distance and the average price.

        e.g.
        {15: [153, 1927], 20: [240, 1844], 10: [105, 1919]}
        """

        # t = Posting.get_farther_away(2500, 1, 37.7914448, -122.3929672, 5)
        increment = [5, 10, 20]
        posts = {}

        for i in increment:
            new_sum = desired_distance + i

            x, y, x2, y2 = cls.calculate_outer_bounds(origin_lat, origin_lon, new_sum)

            farther_listings = db.session.query(cls.price, cls.post_id).filter(cls.bedrooms == bedrooms, cls.price < price, cls.latitude > x, cls.latitude < x2, cls.longitude > y, cls.longitude < y2).all()

            rents = [post_price for post_price, post_id in farther_listings]
            avg_price = (sum(rents))/len(farther_listings)

            posts[i] = [len(farther_listings), avg_price]

        # Remove repeat listings
        posts[20][0] -= posts[10][0]
        posts[10][0] -= posts[5][0]

        return posts

    @classmethod
    def get_bedrooms_price(cls, city_prefix):
        """
        Find the number and average price of 1, 2, and 3 bedroom apartments for a given city. Returns dictionary with # of posts and average price.
        """

        one_bedrooms = db.session.query(cls.price, cls.post_id).filter(cls.url.like("%{}%".format(city_prefix)), cls.bedrooms == 1).all()
        num_one_beds = len(one_bedrooms)
        rents_one_beds = [price for price, post_id in one_bedrooms]
        avg_price_one_beds = (sum(rents_one_beds))/num_one_beds

        two_bedrooms = db.session.query(cls.price, cls.post_id).filter(cls.url.like("%{}%".format(city_prefix)), cls.bedrooms == 2).all()
        num_two_beds = len(two_bedrooms)
        rents_two_beds = [price for price, post_id in two_bedrooms]
        avg_price_two_beds = (sum(rents_two_beds))/num_two_beds

        three_bedrooms = db.session.query(cls.price, cls.post_id).filter(cls.url.like("%{}%".format(city_prefix)), cls.bedrooms == 3).all()
        num_three_beds = len(three_bedrooms)
        rents_three_beds = [price for price, post_id in three_bedrooms]
        avg_price_three_beds = (sum(rents_three_beds))/num_three_beds

        return {'1 bedrooms': [num_one_beds, avg_price_one_beds],
                '2 bedrooms': [num_two_beds, avg_price_two_beds],
                '3 bedrooms': [num_three_beds, avg_price_three_beds]}

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
