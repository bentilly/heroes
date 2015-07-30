from datetime import datetime
from functools import wraps

import logging

from flask import jsonify

from flask.ext import restful
from flask_restful import Api, Resource, url_for, marshal_with, reqparse

from google.appengine.api import users

from werkzeug import exceptions


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
