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

    # TODO: convert address to lat/long

    session['max_distance'] = int(request.args.get('distance'))
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

    search_results = Posting.get_apartments(session['price'], session['bedrooms'], session['origin_latitude'], session['origin_longitude'], session['max_distance'])

    # TODO: if search returns nothing, flash a message.

    if not search_results:
        # return nothing
        pass

    apartments = {apt.post_id: {
        "title": apt.title,
        "date_posted": apt.date_posted,
        "url": apt.url,
        "img_url": apt.img_url,
        "price": apt.price,
        "bedrooms": apt.bedrooms,
        "latitude": apt.latitude,
        "longitude": apt.longitude
    } for apt in search_results}

    print len(apartments)

    return jsonify(apartments)

######### Helper Functions #########

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run()
