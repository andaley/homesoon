import unittest
from model import Posting

class TestApp(unittest.TestCase):

    def test_get_lat_lons(self):
        example_call = Posting.get_lat_lons(5000, 2)

        # Result should always be a list.
        self.assertTrue(type(example_call) is list)

        # Funtion should never return None.
        self.assertIsNotNone(example_call)

        # All items in the list should be tuples.
        if len(example_call) > 0:
            self.assertTrue(type(example_call[0]) is tuple)

    def test_calculate_distance(self):
        example_call = Posting.calculate_distance()

        # Function hould never return None.
        self.assertIsNotNone(example_call)

        # All items in list should be apartment objects.
        if len(example_call) > 0:
            self.assertTrue(type(example_call[0]) is Posting)

if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    connect_to_db(app)
    unittest.main()
