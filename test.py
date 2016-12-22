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

