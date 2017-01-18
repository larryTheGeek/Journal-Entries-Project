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

    # def setUp(self):
      # """Stuff to do before every test."""

      # app.config['TESTING'] = True
      # app.config['SECRET_KEY'] = 'key'
      # self.client = app.test_client()

      # with self.client as c:
      #     with c.session_transaction() as sess:
      #         sess['user_id'] = 1

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_homepage(self):
        """Make sure that the Register button appears on the homepage"""

        result = self.client.get('/')
        print "test_homepage"
        self.assertEqual(result.status_code, 200m
        self.assertIn('Register', result.data)

    def test_login(self):
        """Make sure that the login function works"""

        result = self.client.post("/login",
                            data={"username": "fluffykitty", "password": "password123"},
                            follow_redirects=True)
        self.assertIn("Title", result.data) #Journal Entry Title in entry.html

    def test_registration(self):
        result = self.client.post("/login",
                            data={"username": "furryfriends", "password": "fureverfluffy", "email": "hellofriend@gmail.com"},
                            follow_redirects=True)
        self.assertIn("Title", result.data) #Journal Entry Title in entry.html

    def test_view_entries(self):
        pass


if __name__=="__main__":
    unittest.main()