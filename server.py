from flask import Flask, render_template, request, jsonify, session
from model import Posting, db, connect_to_db
from jinja2 import StrictUndefined
import math
import googlemaps
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "oakzebraland"
app.jinja_env.undefined = StrictUndefined

google_key = os.environ['GOOGLE_MAPS_TOKEN']
gmaps = googlemaps.Client(key=google_key)

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

    location = gmaps.geocode(request.args.get('address')) # returns list

    session['max_distance'] = int(request.args.get('distance'))
    session['origin_latitude'] = float(location[0]['geometry']['location']['lat']) # sample 37.7914448
    session['origin_longitude'] = float(location[0]['geometry']['location']['lng']) # sample -122.3929672
    session['bedrooms'] = request.args.get('bedrooms')
    session['price'] = request.args.get('cost')
    # TODO: add preferred method of transportation
    session['transit_method'] = request.args.get('transportation')

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

    # Convert origin and destination to format recognized by Google Maps Python wrapper.
    origin = str(session['origin_latitude']) + ',' + str(session['origin_longitude'])
    # '37.7914448,-122.3929672'
    destination = str(lat) + ',' + str(lon)
    # '37.7857435,-122.4112531'

    distance_results = gmaps.distance_matrix(origin, destination, mode=session['transit_method'], units='imperial') # returns dictionary

    if distance_results != 'OK':
        # TODO: figure out what to do if no results
        pass

    duration = distance_results['rows'][0]['elements'][0]['duration']['text']
    distance = distance_results['rows'][0]['elements'][0]['distance']['text']

    total_distance = {'duration': duration, 'distance': distance}

    # TODO: link distance to actual Google maps directions

    return jsonify(total_distance)


######### Helper Functions #########

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
