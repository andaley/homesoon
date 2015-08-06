from flask import Flask, render_template, request
from model import Posting, db
from jinja2 import StrictUndefined
import math

app = Flask(__name__)
app.secret_key = "hello"
app.jinja_env.undefined = StrictUndefined


######### Routes #########

@app.route('/')
def home():
    """Return home page."""

    return render_template('index.html')


@app.route('/search-apartments')
def find_apartments():
    """
    Query database for posts within the user-specified distance.

    Returns list of apartment objects.
    """

    MILES_TO_DEGREES = 69
    max_distance = int(request.args.get('distance'))
    print max_distance, type(max_distance)

    dist_degrees = max_distance / MILES_TO_DEGREES


    # TODO: convert address to lat/long

    origin_lat = request.args.get('lat')
    origin_long = request.args.get('lon')

    # # Gather list of tuples w/ ids, lat & longs
    #  _QUERY = "SELECT post_id, latitude, longitude FROM postings WHERE SQRT(SQUARE(latitude - ?)) + (SQUARE(longitude - ?)) ) < ?"

    # SELECT post_id, latitude, longitude
    # FROM postings
    # WHERE SQRT(SQUARE(latitude - 37.7914448) + SQUARE(longitude - -122.3929672)) < .072463768

    # retrieve all lat/lon/ids from database
    ALL_lat_lons = db.session.query(Posting.post_id, Posting.latitude, Posting.longitude).all()
    # run math

    matching_apts = []
    for id, lat, lon in ALL_lat_lons:
        if math.sqrt((lat - 37.7914448)**2 + (lon - -122.3929672)**2) < .072463768:
            matching_apts.append(Posting.query.get(id))

    # db.session.execute(_QUERY(origin_lat, origin_long, dist_degrees))

    return render_template("apts.html", matching_apts=matching_apts)


@app.route('/display-apartments')
def display_apartments():
    """Display apartment search results on a map. When a user clicks on a particular point, they will be re-routed."""
    pass

if __name__ == '__main__':
    app.debug = True
    app.run()
