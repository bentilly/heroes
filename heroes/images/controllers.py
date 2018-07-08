from google.appengine.api import images

import logging

from flask import Blueprint, render_template, redirect, request, Response

from heroes.helpers import get_entity_by_key

image_bp = Blueprint('image', __name__)


@image_bp.route('/<key>/<attr>/')
@image_bp.route('/<key>/<attr>/<width>/<height>/')
def get_image(key, attr, width=100, height=100):
    image_data = images.resize(getattr(get_entity_by_key(key), attr), width, height)
    resp = Response(image_data)
    resp.headers['Content-Type'] = 'image/jpeg'
    return resp
