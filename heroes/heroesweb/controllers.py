from flask import Blueprint, render_template, redirect, request
from google.appengine.ext import ndb

import logging
import operator
from operator import itemgetter

from heroes.sports.models import Sport
from heroes.countries.models import Country
from heroes.representatives.models import Rep
from heroes.squadmembers.models import Squadmember
from heroes.teams.models import Team
from heroes.squads.models import Squad

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

@heroesweb_bp.route('sport/<key>/')
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

@heroesweb_bp.route('country/<key>/')
def country_view(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()

	sport = country_key.parent().get()

	pagetitle = country.title+"  "+sport.title
	reps = Rep.query(ancestor=country_key).order(Rep.firstname).fetch()
	teams = Team.query(ancestor=country_key).fetch()



	return render_template('public/countryHome.html',
		pagetitle=pagetitle,
		itemlist=reps,
		teamlist=teams,
	)

@heroesweb_bp.route('team/<key>/')
def team_view(key):
	team_key = ndb.Key(urlsafe=key)
	team = team_key.get()

	squads = Squad.query(ancestor=team_key).fetch()
	latestSquad = squads[0]
	for squad in squads:
		if squad.eventdate > latestSquad.eventdate:
			latestSquad = squad

	squadmembers = Squadmember.query(ancestor=latestSquad.key).fetch()
	members = []
	for sm in squadmembers:
		rep = sm.rep.get()
		member = {"publiclink":rep.publiclink, "title":rep.title}

		members.append(member)

	members_sorted = sorted(members, key=itemgetter('title'))

	return render_template('public/team.html',
		pagetitle=team.title,
		subtitle=latestSquad.event.get().title,
		itemlist=members_sorted,
	)


@heroesweb_bp.route('rep/<key>/')
def rep_profile(key):
	rep_key = ndb.Key(urlsafe=key)
	rep_object = rep_key.get()

	squadmember_entries = Squadmember.query(Squadmember.rep==rep_key).fetch()

	rep_squads = []
	for member in squadmember_entries:
		rs_date = member.key.parent().get().event.get().startdate
		rs = {'member':member, 'date':rs_date}
		rep_squads.append(rs)

	rep_squads.sort(key=operator.itemgetter('date'), reverse=True)

	return render_template('public/profile.html',
		rep=rep_object,
		squads=squadmember_entries,
		rep_squads=rep_squads,
	)


