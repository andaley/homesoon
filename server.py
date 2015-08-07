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

    session['max_distance'] = origin_dist_degrees
    session['origin_latitude'] = float(request.args.get('lat')) # sample 37.7914448
    session['origin_longitude'] = float(request.args.get('lon')) # sample -122.3929672
    session['bedrooms'] = request.args.get('bedrooms')
    session['price'] = request.args.get('cost')

    return render_template("apts.html")


@app.route('/apartments.json')
def display_apartments():
    """
    Query database for posts within the user-specified distance.
    Returns JSON with nested apartment objects.
    """

    # TODO: move into model.py
    # Retrieve all ids/lat/lons from database as tuples
    Posting.get_lat_lons(session['price'], session['bedrooms'])


    # If lat & lon are within desired distance, retrieve the corresponding Posting object
    # TODO: move into separate function


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

######### Helper Functions #########

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
