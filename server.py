from flask import Flask, render_template, request, jsonify, session, flash, redirect
from model import Posting, User, Favorite, db, connect_to_db
from jinja2 import StrictUndefined
import math
import googlemaps
import json
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_TOKEN']
app.jinja_env.undefined = StrictUndefined

google_key = os.environ['GOOGLE_MAPS_TOKEN']
gmaps = googlemaps.Client(key=google_key)


######### Routes #########

@app.route('/')
def home():
    """Return home page."""

    return render_template('index.html')


#### Log in / out ####

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

    return render_template("apts.html", raw_location=session['raw_location'], price=session['price'], distance=session['max_distance'], bedrooms=session['bedrooms'], transport=session['transit_method'])


@app.route('/apartments.json')
def display_apartments():
    """
    Query database for posts within the user-specified distance.
    Returns JSON with nested apartment objects.
    """

    search_results = Posting.get_apartments(session['price'], session['bedrooms'], session['origin_latitude'], session['origin_longitude'], session['max_distance'])

    session['num_results'] = len(search_results)
    avg_rent = Posting.calculate_avg_rent(search_results)
    session['avg_rent'] = avg_rent

    apartments = {'origin_info':
        {"origin_lat": session['origin_latitude'],
        "origin_lon": session['origin_longitude']},
        'listings': {},
        'avg_rent': avg_rent,
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
    destination = str(lat) + ',' + str(lon)

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


#### Charts ####


@app.route('/charts')
def show_charts():
    """
    Displays graphs related to the users' search as well as general prices from Craigslist.
    """

    # Show number of posts more expensive than search.
    more_expensive = Posting.get_more_expensive(session['price'], session['bedrooms'], session['origin_latitude'], session['origin_longitude'], session['max_distance'])
    num_expensive = more_expensive['total']

    # Show number of posts farther away than desired distance.
    farther = Posting.get_farther_away(session['price'], session['bedrooms'], session['origin_latitude'], session['origin_longitude'], session['max_distance'])

    # Show avg price by bedroom for all 3 cities.
    seattle_data = Posting.get_bedrooms_price('seattle')
    portland_data = Posting.get_bedrooms_price('portland')
    bay_area_data = Posting.get_bedrooms_price('sfbay')

    return render_template('charts.html', raw_location=session['raw_location'], price=session['price'], avg_rent=session['avg_rent'], num_results=session['num_results'], more_expensive=more_expensive, farther=farther, bayarea=bay_area_data, seattle=seattle_data, portland=portland_data, distance=session['max_distance'], bedrooms=session['bedrooms'], transport=session['transit_method'])


#### View / Add Favorites ####

@app.route('/favorites')
def show_favorites():
    """Display favorites page."""

    # return list of apartment objects
    user_favorites = Favorite.query.filter_by(user_id = session['id']).all()

    user_favorites = [favorite for favorite in user_favorites if favorite.post]

    return render_template('favorites.html', favorites=user_favorites)


@app.route('/add-favorite', methods=['GET'])
def add_favorite():
    """Add new Favorite to the database."""

    marker_id = request.args.get('id')
    commute_time = request.args.get('commute_time')

    if not session.get('id'):
        message = 'Sign in to save!'
        return message

    # Only add favorite if user hasn't already saved it.
    if not Favorite.query.filter(Favorite.post_id == marker_id, Favorite.user_id == session['id']).all():

        Favorite.add_favorite(user_id = session['id'], marker_id = marker_id, commute_time = commute_time, raw_location = session['raw_location'])

    message = '<span class="glyphicon glyphicon-star star"></span>'

    return message

@app.route('/remove-favorite', methods=['POST'])
def remove_favorite():
    """Remove a favorite from the database."""

    favorite_id = request.form.get('id')
    favorite = Favorite.query.get(favorite_id)
    favorite.post.is_favorited = False
    db.session.commit()
    db.session.delete(favorite)
    db.session.commit()

    return favorite_id


######### Helper Functions #########

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
