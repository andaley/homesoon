from flask import Flask, render_template, request, jsonify, session
from model import Posting, db, connect_to_db
from jinja2 import StrictUndefined
import math
import requests
import json
import os

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

    # TODO: convert address to lat/long

    session['max_distance'] = int(request.args.get('distance'))
    session['origin_latitude'] = float(request.args.get('lat')) # sample 37.7914448
    session['origin_longitude'] = float(request.args.get('lon')) # sample -122.3929672
    session['bedrooms'] = request.args.get('bedrooms')
    session['price'] = request.args.get('cost')
    # TODO: add preferred method of transportation
    # session['transit_method'] = request.args.get('transit')

    # can I render a template and return the lat & long to be used by JS? Otherwise I can't render map until getting results

    return render_template("apts.html")


@app.route('/apartments.json')
def display_apartments():
    """
    Query database for posts within the user-specified distance.
    Returns JSON with nested apartment objects.
    """

    search_results = Posting.get_apartments(session['price'], session['bedrooms'], session['origin_latitude'], session['origin_longitude'], session['max_distance'])

    # TODO: if search returns nothing, flash a message.

    if not search_results:
        # return nothing
        pass

    apartments = {'origin_info':
        {"origin_lat": session['origin_latitude'],
        "origin_lon": session['origin_longitude']},
        'listings': {}
        }

    for apt in search_results:
        apartments['listings'][apt.post_id] = {
        "title": apt.title,
        "date_posted": apt.date_posted,
        "url": apt.url,
        "img_url": apt.img_url,
        "price": apt.price,
        "bedrooms": apt.bedrooms,
        "latitude": apt.latitude,
        "longitude": apt.longitude
    }

    return jsonify(apartments)

@app.route('/calculate-distance/<lat>/<lon>')
def calculate_distance(lat, lon):
    """
    Calculate commute time and distance using Google Distance Matrix.
    """

    origin = str(session['origin_latitude']) + ',' + str(session['origin_longitude'])

    # TODO: get method of transportation

    # Grab Google API key
    # note: must source Google API key in the shell before running this function.
    google_key = os.environ['GOOGLE_MAPS_TOKEN']

    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + origin + '&destinations=' + lat + ',' + lon + '&mode=transit&units=imperial&key=' + google_key

    distance_results = requests.get(endpoint).json()

    duration = distance_results['rows'][0]['elements'][0]['duration']['text']
    distance = distance_results['rows'][0]['elements'][0]['distance']['text']

    total_distance = {'duration': duration, 'distance': distance}

    # {u'status': u'OK', u'rows': [{u'elements': [{u'duration': {u'text': u'7 mins', u'value': 431}, u'distance': {u'text': u'0.6 km', u'value': 558}, u'status': u'OK'}]}], u'origin_addresses': [u'121-199 Spear Street, San Francisco, CA 94105, USA'], u'destination_addresses': [u'1-19 Tehama Street, San Francisco, CA 94105, USA']}

    # TODO: link distance to actual Google maps directions

    return jsonify(total_distance)


######### Helper Functions #########

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
