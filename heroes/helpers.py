from datetime import datetime
import logging

from werkzeug import exceptions

import flask
from flask import jsonify

from flask.ext import restful


class Api(restful.Api):
    """Base class for heros api.
    """


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
    return jsonpify({
        'status': 'success',
        'now': datetime.utcnow().isoformat(),
        'result': restful.marshal(data, marshal_table),
    })
