import unittest
from server import app
import doctest
from selenium import webdriver
from model import connect_to_db, db, User, Entry, Tag, EntryTag, example_data

class TestRoutes(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True 

        connect_to_db(app, "postgresql://test")
        print "setUp"

        db.create_all()
        example_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_homepage(self):
        """Make sure that the Register button appears on the homepage"""

        result = self.client.get('/')
        print "test_homepage"
        self.assertEqual(result.status_code, 200)
        self.assertIn('Register', result.data)

    def test_login(self):
        pass

    def test_registration(self):
        pass

    def test_view_entries(self):
        pass


if __name__=="__main__":
    unittest.main()