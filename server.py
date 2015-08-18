from flask import Flask, render_template, request, jsonify, session, flash, redirect
from model import Posting, User, Favorite, db, connect_to_db
from jinja2 import StrictUndefined
import math
import googlemaps
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


### Log in / out ###

@app.route('/sign-in')
def show_sign_in():
    """Show sign-in and sign-up page."""

    return render_template('sign-in.html')


@app.route('/process-login', methods=['POST'])
def sign_in():
    """Check user's credentials and login."""

    username = request.form.get('username')
    user = User.query.filter_by(username = username).first()
    password = request.form.get('password')

    if not user or user.password != password:
        flash('Oh no! Your email address or password is incorrect. Please try again.')
        return redirect('/sign-in')

    session['username'] = user.username
    session['id'] = user.user_id

    return redirect ('/')


@app.route('/add-user', methods=['POST'])
def add_user():
    """Adds new user to database."""

    username = request.form.get('new-username')
    email = request.form.get('new-email')
    password = request.form.get('new-password')

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    session['username'] = new_user.username
    session['id'] = new_user.user_id

    return redirect ('/')


@app.route('/sign-out')
def sign_out():
    """Logs user out."""

    for key in session.keys():
        del session[key]

    return redirect('/')


#### View / Add Favorites ####

@app.route('/favorites')
def show_favorites():
    """Display favorites page."""

    # return list of apartment objects
    user_favorites = Favorite.query.filter_by(user_id = session['id']).all()

    return render_template('favorites.html', favorites=user_favorites)


@app.route('/add-favorite', methods=['GET'])
def add_favorite():
    """Add new Favorite to the database."""

    marker_id = request.args.get('id')
    commute_time = request.args.get('commute_time')

    if not session.get('id'):
        message = 'Sign in to save!'
        return message

    new_favorite = Favorite(user_id = session['id'], post_id = marker_id, commute_time = commute_time, origin = session['raw_location'])
    db.session.add(new_favorite)
    db.session.commit()

    message = 'Saved.'

    return message

#### Search for apartments ####

@app.route('/apartments', methods=['POST'])
def find_apartments():
    """
    Add users' search preferences to their session and display apartment results page.

    Uses Google Maps Geocoding to determine origin latitude and longitude.
    """

    session['raw_location'] = request.form.get('address')
    location = gmaps.geocode(session['raw_location']) # returns list

    session['max_distance'] = int(request.form.get('distance'))

    # Test values:
    # session['origin_latitude'] = 37.7914448
    # session['origin_longitude'] = -122.3929672

    session['origin_latitude'] = float(location[0]['geometry']['location']['lat'])
    session['origin_longitude'] = float(location[0]['geometry']['location']['lng'])
    session['bedrooms'] = request.form.get('bedrooms')
    session['price'] = request.form.get('cost')
    session['transit_method'] = request.form.get('transportation')

    return render_template("apts.html", raw_location=session['raw_location'], price=session['price'], )


@app.route('/apartments.json')
def display_apartments():
    """
    Query database for posts within the user-specified distance.
    Returns JSON with nested apartment objects.
    """

    search_results = Posting.get_apartments(session['price'], session['bedrooms'], session['origin_latitude'], session['origin_longitude'], session['max_distance'])

    # avg_rent = Posting.calculate_avg_rent(search_results)

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
    Calculate commute time and distance using Google Distance Matrix. Returns JSON object.
    """

    # Convert origin and destination to format recognized by Google Maps Python wrapper.
    origin = str(session['origin_latitude']) + ',' + str(session['origin_longitude'])
    # '37.7914448,-122.3929672'
    destination = str(lat) + ',' + str(lon)
    # '37.7857435,-122.4112531'

    distance_results = gmaps.distance_matrix(origin, destination, mode=session['transit_method'], units='imperial') # returns dictionary


    if session['transit_method'] == 'transit':
        method = 'data=!3m1!4b1!4m2!4m1!3e3'
    elif session['transit_method'] == 'bicycling':
        method = 'data=!3m1!4b1!4m2!4m1!3e1'
    elif session['transit_method'] == 'walking':
        method = 'data=!3m1!4b1!4m2!4m1!3e2'
    else:
        method = ""

    duration = distance_results['rows'][0]['elements'][0]['duration']['text']
    distance = distance_results['rows'][0]['elements'][0]['distance']['text']
    directions = 'https://www.google.com/maps/dir/' + destination + '/' + origin + '/' + method

    total_distance = {'duration': duration, 'distance': distance, 'directions': directions}

    return jsonify(total_distance)


######### Helper Functions #########

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
