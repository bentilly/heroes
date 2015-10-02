from flask import Blueprint, session, jsonify, render_template, redirect

from google.appengine.ext import ndb

from heroes.helpers import admin_required
from heroes.teams.models import Team

from .models import Sport


sports_bp = Blueprint('sports', __name__)


# HOME PAGE. A list of sports
@sports_bp.route('/')
def sports_list():
    sports_entries = Sport.query().fetch()
    return render_template('home.html',
            object_title='Heroes',
        )

# ADD A SPORT
@sports_bp.route('/add', methods=['POST'])
def add_entry():
    return redirect('/')


#BLANK SPORT PAGE
@sports_bp.route('/new')
def new_sport():
    return render_template('sport.html',
            object_title='New sport',
        )



# A SPORT PAGE.
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
