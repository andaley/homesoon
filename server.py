from flask import Flask, render_template, request
from model import Posting
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "hello"
app.jinja_env.undefined = StrictUndefined


######### Routes #########

@app.route('/')
def home():
    """Return home page."""

    return render_template('index.html')


@app.route('/find-apartments')
def find_apartments():
    """
    Query database for posts within the user-specified distance.

    Returns list of apartment objects.
    """

    MILES_TO_DEGREES = 69
    # max_distance = request.args.get('distance')
    # dist_degrees = max_distance / MILES_TO_DEGREES


    # TODO: convert address to lat/long
    origin_lat = request.args.get('lat')
    origin_long = request.args.get('lon')
    # hard code lat/long
    # change form to take in lat/long
    # once that works, switch to address

    # Gather list of tuples w/ ids, lat & longs
    _QUERY = "SELECT post_id, latitude, longitude FROM postings WHERE SQRT(SQUARE(latitude - ?)) + (SQUARE(longitude - ?)) ) < ?"

    db.session.execute(_QUERY(origin_lat, origin_long, dist_degrees))

    # all_apts = db.session.query(Posting.post_id, Posting.latitude, Posting.longitude).all()

    # Iterate through tuples, checking if any fit the latitude & longitude criteria.
    # If they do post id to list.
    # apt_ids = []
    # for post_id, lat, lon in all_apts:
    #     if x < lat y and x2 < lon < y2:
    #         apt_ids.append(post_id)
    #
    # # Grab all objects in user_apts from database.
    #     # Eventually, all items on this list will be plotted on the map.
    # matching_apts = Posting.query.filter(Posting.id.in_([apt_ids]))
    #
    return render_template(matching_apts=matching_apts)


@app.route
if __name__ == '__main__':
    app.debug = True
    app.run()
