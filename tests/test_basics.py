#! usr/bin/env python

import unittest
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):

    # runs before each method
    # before each method that has test_ prepend to it
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()

        # activates application context
        self.app_context.push()

        # create a database
        db.create_all()

    # runs after each method
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

