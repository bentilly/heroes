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
        sport_key = ndb.Key(urlsafe=sport_key)
        sport = sport_key.get()
        data['breadcrumb'] = [sport]
        data['sport_object'] = sport
        # display page.
    if request.method == 'POST':
        # store data.
        entry_data = request.form.to_dict()
        if sport_key:
            entry_data['parent'] = sport_key
        trophy = Trophy.create_new_revision(**entry_data)
    return render_template('/admin/trophy.html', **data)


@trophy_bp.route('/<key>')
def read_trophie():
    pass


@trophy_bp.route('/update/<uid>/', methods=['GET', 'POST'])
def update_trophy(uid):
    # get latest revision of trophy.
    trophy = Trophy.get_latest_revision(uid)
    data = {'object_title': 'Trophy',
            'breadcrumb': [trophy.key.parent().get()],
            'trophy_object': trophy}
    if request.method == 'POST':
        entry_data = request.form.to_dict()
        entry_data['uid'] = uid
        entry_data['parent'] = trophy.key.parent()
        trophy = Trophy.create_new_revision(**entry_data)
        data['trophy_object'] = trophy
    return render_template('/admin/trophy.html', **data)


@trophy_bp.route('/<key>')
def delete_trophie():
    pass
