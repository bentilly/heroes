"""Trophies-related controllers.
"""
from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Trophy

trophy_bp = Blueprint('trophy', __name__)


@trophy_bp.route('/new/')
@trophy_bp.route('/new/<sport_key>/', methods=['GET', 'POST'])
def new_trophy_page(sport_key=None):
    """Display 'New Trophie' page and create new trophie in db.
    """
    data = {'object_title': 'Trophy'}
    if sport_key is not None:
        sport = ndb.Key(urlsafe=sport_key).get()
        data['breadcrumb'] = [sport]
        data['sport_object'] = sport
        # display page.
    if request.method == 'POST':
        # store data.
        trophy = Trophy.create_new_revision(**request.form.to_dict())
        trophy.put()
    return render_template('trophy.html', **data)


@trophy_bp.route('/<key>')
def read_trophie():
    pass


@trophy_bp.route('/<key>')
def update_trophie():
    pass


@trophy_bp.route('/<key>')
def delete_trophie():
    pass
