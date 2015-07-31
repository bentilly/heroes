from datetime import datetime
from functools import wraps
import unittest
import logging

from flask import jsonify

from flask.ext import restful
from flask_restful import Api, Resource, url_for, marshal_with, reqparse

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from werkzeug import exceptions
import webtest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

        from . import create_app
        self.app = create_app()
        self.testapp = webtest.TestApp(self.app)


    def login(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(user_email=email, user_id=id,
            user_is_admin='1' if is_admin else '0', overwrite=True)


    def logout(self):
        self.testbed.setup_env(user_email='', user_id='', user_is_admin='', overwrite=True)


    def tearDown(self):
        self.testbed.deactivate()


class Api(restful.Api):
    """Base class for heros api.
    """


class Resource(Resource):
    def _make_parser(self, *fields):
        parser = reqparse.RequestParser()
        for field in fields:
            name, params = field
            parser.add_argument(name, **params)
        return parser


def is_iterable(value):
    return isinstance(value, (tuple, list))


def make_response(data, marshal_table, cursors=None):
    if is_iterable(data):
        response = {
            'status': 'success',
            'count': len(data),
            'now': datetime.utcnow().isoformat(),
            'result': map(lambda l: restful.marshal(l, marshal_table), data),
        }
        return jsonify(response)
    return jsonify({
        'status': 'success',
        'now': datetime.utcnow().isoformat(),
        'result': restful.marshal(data, marshal_table),
    })


def admin_required(func):
    """Requires App Engine admin credentials.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.is_current_user_admin():
            raise exceptions.MethodNotAllowed('Admin credentials required.')
        return func(*args, **kwargs)
    return decorated_view
