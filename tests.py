import unittest
import server
import os
import requests
import googlemaps
from model import Posting
from seed import load_posts

class TestApp(unittest.TestCase):

    def test_get_lat_lons(self):
        """
        Checks that function returns list of tuples.
        """

        example_call = Posting.get_lat_lons(max_rent=7000, num_rooms=1, desired_distance=5)

        # Result should always be a list.
        self.assertTrue(type(example_call) is list)

        # Funtion should never return None.
        self.assertIsNotNone(example_call)

        # Example call should always result in at least 50 results.
        # Unless 1 bedrooms in SF start going for more than $7000...
        self.assertTrue(len(example_call) > 100)

        # Function should always return list of tuples
        # (post_id, latitude, longitude) <-- all integers
        self.assertTrue(type(example_call[0].post_id) is int)
        self.assertTrue(type(example_call[0].latitude) is float)
        self.assertTrue(type(example_call[0].longitude) is float)


    def test_get_apartments(self):
        """
        Checks that database query returns correct data.
        """

        example_call = Posting.get_apartments(max_rent=7000, num_rooms=1, origin_lat=37.7914448, origin_lon=-122.3929672, desired_distance=10)

        # Result should always be a list.
        self.assertTrue(type(example_call) is list)

        # Function hould never return None.
        self.assertIsNotNone(example_call)

        # Example call should always result in at least 50 results.
        self.assertTrue(len(example_call) > 100)

        # All items in list should be apartment objects.
        if len(example_call) > 0:
            self.assertTrue(type(example_call[0]) is Posting)

    def test_calculate_distance(self):
        """
        Checks that geocoding and distance matrix API are working.
        """

        # Check that Google Maps API key has been sourced.
        self.assertTrue('GOOGLE_MAPS_TOKEN' in os.environ)

        origin = '188 Spear Street, San Francisco, CA'
        destination = '37.7857435,-122.4112531'

        matrix = server.gmaps.distance_matrix(origin, destination)

        duration = matrix['rows'][0]['elements'][0]['duration']['text']
        distance = matrix['rows'][0]['elements'][0]['distance']['text']

        self.assertTrue(type(duration) is unicode)
        self.assertTrue(type(distance) is unicode)

    def test_load_posts(self):
        """
        Tests that seed.py is successfully pulling data from Craigslist.
        """

        endpoint = 'http://sfbay.craigslist.org/jsonsearch/apa/'
        cl_json = requests.get(endpoint)
        parsed_json = cl_json.json()
        list_of_posts = parsed_json[0]

        self.assertTrue(type(parsed_json) is list)
        self.assertTrue(type(parsed_json[0]) is list)
        self.assertTrue(type(parsed_json[0][0]) is dict)

if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    connect_to_db(app)
    unittest.main()
