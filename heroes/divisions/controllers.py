from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Division
from heroes.sports.models import Sport
from heroes.countries.models import Country
from heroes.teams.models import Team

division_bp = Blueprint('division', __name__)

# RENDERING #

# A division PAGE.
@division_bp.route('/<key>/')
def division_view(key):
    division_key = ndb.Key(urlsafe=key)
    division = division_key.get()

    #BREADCRUMB
    # sport
    sport = division_key.parent().get()

    breadcrumb_list = [sport]
    title = division.title
    #END BREADCRUMB

    return render_template('/admin/division.html',
            breadcrumb = breadcrumb_list,
            object_title=title,
            division_object=division,
        )

#NEW division PAGE
@division_bp.route('/new/<key>')
def new_division(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()

	breadcrumb_list = [sport]

	return render_template('/admin/division.html',
		breadcrumb = breadcrumb_list,
		object_title='New division',
		sport_object=sport,
		)



# HANDLERS #

# ADD division
@division_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	sport_key = ndb.Key(urlsafe=parent_key)
	sport = sport_key.get()

	division = Division(name=request.form['divisionName'], code=request.form['divisionCode'], parent=sport_key)
	division.put()

	#Update TEAMS
	countries = Country.query(ancestor=sport_key).fetch()
	for country in countries:
		team = Team(parent=country.key, division=division.key)
		team.put()

	return redirect('/admin/division/{}'.format(division.key.urlsafe()))


# UPDATE division
@division_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    division_key = ndb.Key(urlsafe=key)
    division = division_key.get()
    division.name = request.form['divisionName']
    division.code = request.form['divisionCode']
    division.put()

    return redirect('/admin/division/{}'.format(division.key.urlsafe()))











