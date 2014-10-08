#! usr/bin/env python

import unittest
from app.models import User, ReadOnly
from flask import current_app
from app import db, create_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()

        # activates application context
        self.app_context.push()

        # create a database
        db.create_all()
        u1 = User(email='bamby@gmail.com', username='bamby')
        u2 = User(email='alisa@gmail.com', username='alisa')
        db.session.add_all([u1, u2])
        db.session.commit()

        # add reference to the users in the database
        self.user1 = User.query.filter_by(username='bamby').first()
        self.user2 = User.query.filter_by(username='alisa').first()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        pass

    def test_password_read_only(self):
        with self.assertRaises(AttributeError) as context:
            self.user1.password

    def test_password_verification(self):
        self.user1.password = 'cat'
        self.assertTrue(self.user1.verify_password('cat'))

    def test_password_hashing_differs(self):
        self.user1.password = 'cat'
        self.user2.password = 'cat'

        self.assertNotEqual(self.user1.password_hash, self.user2.password_hash)

    def test_generate_confirmation_token(self):
        'checking that the generated token is not an empty string'
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'confirm': 23})
        self.assertNotEqual('', token)

    @unittest.skip('TODO')
    def test_confirm(self):
        pass
