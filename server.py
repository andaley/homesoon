from flask import Flask, render_template, request, jsonify, session
from model import Posting, db, connect_to_db
from jinja2 import StrictUndefined
import math

app = Flask(__name__)
app.secret_key = "oakzebraland"
app.jinja_env.undefined = StrictUndefined


######### Routes #########

@app.route('/')
def home():
    """Return home page."""

    return render_template('index.html')


@app.route('/apartments')
def find_apartments():
    """
    Add users' search preferences to their session and display apartment results page.
    """

    MILES_TO_DEGREES = 69.0
    max_distance = int(request.args.get('distance'))
    origin_dist_degrees = max_distance / MILES_TO_DEGREES

    # TODO: convert address to lat/long

    origin_lat = float(request.args.get('lat')) # sample 37.7914448
    origin_lon = float(request.args.get('lon')) # sample -122.3929672

    session['origin_latitude'] = origin_lat
    session['origin_longitude'] = origin_lon
    session['max_distance'] = origin_dist_degrees

    return render_template("apts.html")


@app.route('/apartments.json')
def display_apartments():
    """
    Query database for posts within the user-specified distance.
    Returns JSON with nested apartment objects.
    """

    # Retrieve all lat/lon/ids from database as tuples
    all_lat_lons = db.session.query(Posting.post_id, Posting.latitude, Posting.longitude).all()

    # If lat & lon are within desired distance, retrieve the corresponding Posting object
    matching_apts = []

    for post_id, lat, lon in all_lat_lons:
        # calculate distance
        distance_deg = math.sqrt((lat - session['origin_latitude'])**2 + (lon - session['origin_longitude'])**2)
        distance_mi = distance_deg * 69
        if distance_deg < session['max_distance']:
            matching_apts.append(Posting.query.get(post_id))

    apartments = {apt.post_id: {
        "title": apt.title,
        "date_posted": apt.date_posted,
        "url": apt.url,
        "img_url": apt.img_url,
        "price": apt.price,
        "bedrooms": apt.bedrooms,
        "latitude": apt.latitude,
        "longitude": apt.longitude
    } for apt in matching_apts}

    return jsonify(apartments)

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
