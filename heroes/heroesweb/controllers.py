from flask import Blueprint, render_template, redirect, request
from google.appengine.ext import ndb

from heroes.sports.models import Sport
from heroes.countries.models import Country
from heroes.representatives.models import Rep

heroesweb_bp = Blueprint('heroesweb_bp', __name__)

# RENDERING : public website#

@heroesweb_bp.route('/')
def sports_all_view():

	# breadcrumb_list = []
	pagetitle = "Sports Heroes"
	sports = Sport.query().fetch()

	return render_template('public/heroesweb.html',
		# breadcrumb = breadcrumb_list,
		pagetitle=pagetitle,
		itemlist=sports,
	)

@heroesweb_bp.route('/sport/<key>/')
def sport_view(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()

	# breadcrumb_list = []
	pagetitle = sport.title
	countries = Country.query(ancestor=sport_key).order(Country.code).fetch()

	return render_template('public/heroesweb.html',
		# breadcrumb = breadcrumb_list,
		pagetitle=pagetitle,
		itemlist=countries,
	)

@heroesweb_bp.route('/country/<key>/')
def country_view(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()

	sport = country_key.parent().get()

	# breadcrumb_list = []
	pagetitle = country.title+"  "+sport.title
	reps = Rep.query(ancestor=country_key).order(Rep.firstname).fetch()

	return render_template('public/heroesweb.html',
		# breadcrumb = breadcrumb_list,
		pagetitle=pagetitle,
		itemlist=reps,
	)