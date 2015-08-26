from flask import Blueprint, session, jsonify, render_template

from google.appengine.ext import ndb

from heroes.helpers import Api, Resource, make_response, admin_required
from heroes.teams.models import Team

from .models import Sport


sports_bp = Blueprint('sports', __name__)

@sports_bp.route('/')
def sports_list():
    sports_entries = Sport.get_dbs()
    return render_template('table.html',
        items=sports_entries,
        table_headers=['Sport title', 'Sport description'],
        fields=['name', 'description'])


@sports_bp.route('/<key>/')
def sport_view(key):
    sport_key = ndb.Key(urlsafe=key)
    # TODO: refactor to "Ancestor Queries" when
    # https://github.com/bentilly/heroes/issues/34 will be fixed.
    teams_entries = Team.query(Team.sport==sport_key).fetch()
    return render_template('table.html',
        root_item=sport_key.get(),
        items=teams_entries,
        table_headers=['Country', 'Division', 'Team name'],
        fields=['country_name', 'division_name', 'name'])