from flask import Flask, render_template, request
from model import Posting, db, connect_to_db
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

    MILES_TO_DEGREES = 69.0
    max_distance = int(request.args.get('distance'))

    dist_degrees = max_distance / MILES_TO_DEGREES

    # TODO: convert address to lat/long

    origin_lat = float(request.args.get('lat'))
    # sample 37.7914448
    origin_lon = float(request.args.get('lon'))
    # sample -122.3929672

    print '\n\n\n\n\n', origin_lat, origin_lon, max_distance, '\n\n\n'

    # # Gather list of tuples w/ ids, lat & longs
    #  _QUERY = "SELECT post_id, latitude, longitude FROM postings WHERE SQRT(SQUARE(latitude - ?)) + (SQUARE(longitude - ?)) ) < ?"

    # Retrieve all lat/lon/ids from database
    all_lat_lons = db.session.query(Posting.post_id, Posting.latitude, Posting.longitude).all()

    print '\n\n\n\n\n', len(all_lat_lons), '\n\n\n'

    # If lat & lon are within desired distance, retrieve the corresponding Posting object
    matching_apts = []

    print '\n\n\n\n\n', matching_apts, '\n\n\n'

    for post_id, lat, lon in all_lat_lons:
        if math.sqrt((lat - origin_lat)**2 + (lon - origin_lon)**2) < dist_degrees:
            matching_apts.append(Posting.query.get(post_id))

    print 'There are %s apts within %s miles' % (len(matching_apts), max_distance)

    # db.session.execute(_QUERY(origin_lat, origin_long, dist_degrees))

    return render_template("apts.html", matching_apts=matching_apts)


@app.route('/display-apartments')
def display_apartments():
    """Display apartment search results on a map. When a user clicks on a particular point, they will be re-routed."""
    pass

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
