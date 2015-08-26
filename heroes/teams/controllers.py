from flask import Blueprint, session, jsonify, render_template

from google.appengine.ext import ndb

from heroes.helpers import Api, Resource, make_response, admin_required

from heroes.events.models import Event

from .models import Team

teams_bp = Blueprint('teams', __name__)


@teams_bp.route('/<key>/')
def team_view(key):
    team_key = ndb.Key(urlsafe=key)
    events_entries = Event.query(Event.teams==team_key).fetch()
    return render_template('table.html',
        root_item=team_key.get(),
        items=events_entries,
        table_headers=['Start year', 'Title', 'Venue country'],
        fields=['start_year', 'title', 'country_name'])