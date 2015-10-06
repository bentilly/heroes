from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Country
from heroes.sports.models import Sport
from heroes.divisions.models import Division
from heroes.teams.models import Team
from heroes.representatives.models import Rep

country_bp = Blueprint('country', __name__)

# RENDERING #

# A COUNTRY PAGE.
@country_bp.route('/<key>/')
def country_view(key):
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()

    team_entries = Team.query(ancestor=country_key).fetch()
    rep_entries = Rep.query(ancestor=country_key).fetch()

    return render_template('country.html',
            object_title=country.name,
            country_object=country,
            teams=team_entries,
            reps=rep_entries,
        )

#NEW country PAGE
@country_bp.route('/new/<key>')
def new_country(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()


	return render_template('country.html',
		object_title='New country',
		sport_object=sport,
		)



# HANDLERS #

# ADD country
@country_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
    sport_key = ndb.Key(urlsafe=parent_key)
    sport = sport_key.get()

    country = Country(name=request.form['countryName'], code=request.form['countryCode'], parent=sport_key)
    country.put()

    #Update TEAMS
    divisions = Division.query(ancestor=sport_key).fetch()
    for division in divisions:
        team = Team(parent=country.key, division=division.key)
        team.put()

    return redirect('/country/{}'.format(country.key.urlsafe()))


# UPDATE country
@country_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()
    country.name = request.form['countryName']
    country.code = request.form['countryCode']
    country.put()

    return redirect('/country/{}'.format(country.key.urlsafe()))











