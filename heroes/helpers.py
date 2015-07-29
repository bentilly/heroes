from datetime import datetime
import logging

from werkzeug import exceptions

from flask_restful import Api, Resource, url_for, marshal_with, reqparse

import flask
from flask import jsonify

from flask.ext import restful


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
