import unittest
import server
import os
import requests
import googlemaps
import math
from model import Posting
from seed import load_posts
from selenium import webdriver

class TestApp(unittest.TestCase):

    def test_get_apartments(self):
        """
        Checks that function returns list of apartment objects.
        """

        example_call = Posting.get_apartments(max_rent=7000, num_rooms=1, origin_lat=37.7914448, origin_lon=-122.3929672, desired_distance=5)
        # origin lat/lon point to an address in San Francisco.

        # Result should always be a list.
        self.assertTrue(type(example_call) is list)

        # Funtion should never return None.
        self.assertIsNotNone(example_call)

        # Example call should always result in at least 75 results.
        # Unless 1 bedrooms in SF start going for more than $7000...
        self.assertTrue(len(example_call) > 75)

        self.assertTrue(type(example_call[0].post_id) is int)
        self.assertTrue(type(example_call[0].latitude) is float)
        self.assertTrue(type(example_call[0].longitude) is float)

        # Check that results are actually from San Francisco.
        self.assertTrue('sfbay' in example_call[0].url)


    def test_check_euclidean_distance(self):
        """
        Verifies that check_distance returns list of apartment objects within Euclidean distance range of origin.
        """

        max_rent=7000
        num_rooms=1
        origin_lat=37.7914448
        origin_lon=-122.3929672
        desired_distance=5

        # Get sample list of 5 apartments.
        apartments = Posting.get_apartments(max_rent, num_rooms, origin_lat, origin_lon, desired_distance)[:5]

        for apt in apartments:
            distance_deg = math.sqrt((apt.latitude - origin_lat)**2 + (apt.longitude - origin_lon)**2)

            # Convert distance to miles
            distance_mi = distance_deg * 69.0

            result = apt.check_euclidean_distance(origin_lat, origin_lon, desired_distance)

            self.assertTrue(distance_mi < desired_distance and result)


    def test_calculate_distance(self):
        """
        Check that Google Maps geocoding and distance matrix API are working.
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


    def test_calculate_outer_bounds(self):
        """Verify that result is within expected area."""

        self.assertTrue(Posting.calculate_outer_bounds(100, 100, 5) == [99.92753623188406, 99.92753623188406, 100.07246376811594, 100.07246376811594])

        self.assertTrue(Posting.calculate_outer_bounds(0, 0, 100) == [-1.4492753623188406, -1.4492753623188406, 1.4492753623188406, 1.4492753623188406])


    def test_database(self):
        """
        Verify that database contains postings from all supported cities.
        """

        # Database should always contain postings from SF, Portland, and Seattle.
        sf_posts = Posting.query.filter(Posting.url.like("%sfbay%")).limit(10).all()
        pdx_posts = Posting.query.filter(Posting.url.like("%portland%")).limit(10).all()
        seattle_posts = Posting.query.filter(Posting.url.like("%seattle%")).limit(10).all()

        city_list = [sf_posts, pdx_posts, seattle_posts]

        for city_posts in city_list:
            self.assertIsNotNone(city_posts)
            self.assertIsInstance(city_posts[0], Posting)


    def test_load_posts(self):
        """
        Test that seed.py is successfully pulling data from Craigslist.
        """

        # Check that Craigslist hasn't changed their data structure.
        city_list = ['http://sfbay.craigslist.org/jsonsearch/apa/', 'http://portland.craigslist.org/jsonsearch/apa/', 'http://seattle.craigslist.org/jsonsearch/apa/']

        for city_link in city_list:
            cl_json = requests.get(city_link)
            parsed_json = cl_json.json()
            list_of_posts = parsed_json[0]
            apartment = list_of_posts[0]

            self.assertTrue(type(parsed_json) is list)
            self.assertTrue(type(list_of_posts) is list)
            self.assertTrue(type(apartment) is dict)

            small_list = list_of_posts[:5]

            # Check that posts contain data needed for plotting on map.
            for post in small_list:
                if post.get("GeoCluster"):
                    continue

                self.assertTrue('PostingTitle' in post)
                self.assertTrue('Latitude' in post)


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def test_form(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Apartment Search')
        a = self.browser.find_element_by_id('address')
        a.send_keys('683 Sutter Street, San Francisco, CA')
        c = self.browser.find_element_by_id('cost')
        c.send_keys('3000')
        btn = self.browser.find_element_by_id('search-btn')
        btn.click()
        self.assertEqual(self.browser.title, 'Apartment Results')
        self.browser.find_element_by_css_selector("div[title='Origin']")


    def test_sign_in(self):
        # Sign in
        self.browser.get('http://localhost:5000/')
        s = self.browser.find_element_by_id('signIn')
        s.click()
        self.assertEqual(self.browser.title, 'Sign In')
        u = self.browser.find_element_by_name('username')
        u.send_keys('admin')
        p = self.browser.find_element_by_name('password')
        p.send_keys('wrongpassword')
        btn = self.browser.find_element_by_class_name('btn')
        btn.click()

        # Make sure error message displays if username or password is incorrect.
        e = self.browser.find_element_by_id('error')
        w = self.browser.find_element_by_xpath("//*[contains(text(), 'Oh no! Your email address or password is incorrect. Please try again')]")

        # If username & password is correct, user should be redirected.
        u.send_keys('admin')
        p.send_keys('admin')
        self.assertEqual(self.browser.title, 'Apartment Results')


if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    connect_to_db(app)
    unittest.main()
