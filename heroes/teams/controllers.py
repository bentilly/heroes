from flask import Blueprint, session, jsonify, render_template

from google.appengine.ext import ndb

from heroes.helpers import Api, Resource, make_response, admin_required
from heroes.helpers import get_enitity_by_key

from heroes.events.models import Event

from .models import Team

teams_bp = Blueprint('teams', __name__)


@teams_bp.route('/<key>/')
def team_view(key):
    team_key = ndb.Key(urlsafe=key)
    events_entries = Event.query(Event.teams==team_key).fetch()
    for event in events_entries:
        event.link = '/representatives/{}/{}'.format(event.key.urlsafe(), team_key.urlsafe())

    return render_template('table.html',
        root_item=team_key.get(),
        items=events_entries,
        table_headers=['Start year', 'Title', 'Venue country'],
        fields=['start_year', 'title', 'country_name'])
