from flask import Blueprint, session, jsonify, render_template

from google.appengine.ext import ndb

from heroes.helpers import Api, Resource, make_response, admin_required

from heroes.events.models import Event

from .models import Representative

representatives_bp = Blueprint('representatives', __name__)


@representatives_bp.route('/<key>/')
def represenatives_list(key):
    '''
    return render_template('table.html',
        root_item=team_key.get(),
        items=events_entries,
        table_headers=['Start year', 'Title', 'Venue country'],
        fields=['start_year', 'title', 'country_name'])
    '''
    return 'Hello'
