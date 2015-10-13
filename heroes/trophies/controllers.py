"""Trophies-related controllers.
"""
from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Trophie

trophie_bp = Blueprint('trophie', __name__)


@trophie_bp.route('/new/')
@trophie_bp.route('/new/<sport_key>/', methods=['GET', 'POST'])
def new_trophie_page(sport_key=None):
    """Display 'New Trophie' page and create new trophie in db.
    """
    if sport_key is not None:
        sport_key = ndb.Key(urlsafe=sport_key)
    if request.method == 'GET':
        # display page.
        pass
    elif request.method == 'POST':
        # store data.
        pass
    return render_template('trophie.html')


@trophie_bp.route('/<key>')
def read_trophie():
    pass


@trophie_bp.route('/<key>')
def update_trophie():
    pass


@trophie_bp.route('/<key>')
def delete_trophie():
    pass
