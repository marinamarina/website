#! usr/bin/env python

import unittest
from flask import current_app
from app import create_app, db
from app.main.forms import LoginForm, RegistrationForm
from app.models import User, Role
from wtforms import StringField

class BasicTestCase(unittest.TestCase):

    # runs before each method
    # before each method that has test_ prepend to it
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create a database
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    # runs after each method
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()