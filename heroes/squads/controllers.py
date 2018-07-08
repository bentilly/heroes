from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

import logging

from .models import Squad
from heroes.events.models import Event
from heroes.squadmembers.models import Squadmember
from heroes.matches.models import Match
from heroes.matchteams.models import Matchteam
from heroes.representatives.models import Rep

squad_bp = Blueprint('squad', __name__)

# RENDERING #

# A squad PAGE.
@squad_bp.route('/<key>/')
def squad_view(key):
	squad_key = ndb.Key(urlsafe=key)
	squad = squad_key.get()

	#BREADCRUMB
	#team
	team = squad_key.parent().get()
	# country
	country = squad_key.parent().parent().get()
	# sport
	sport = squad_key.parent().parent().parent().get()

	breadcrumb_list = [sport, country, team]
	title = squad.title

	#-----SQUADMEMBERS
	#All REPS
	rep_entries= Rep.query(ancestor=country.key).order(Rep.firstname).fetch()

	#Some SQUADMEMBERS
	squadmembers_entries = Squadmember.query(ancestor=squad_key).fetch()


	#REP SQUADMEMBERS
	rep_squadmembers = []

	for r in rep_entries:
		rep_squadmember = {}
		rep_squadmember['rep'] = r

		for sm in squadmembers_entries:
			if sm.rep == r.key:
				rep_squadmember['squadmember'] = sm

		rep_squadmembers.append(rep_squadmember)


	#-----MATCHES for this squad
	event_key = squad.event
	team_key = squad_key.parent()
	division_key = team_key.get().division
	country_key = team_key.parent()

	mq = Match.query(ancestor=event_key)
	mq2 = mq.filter(Match.division == division_key)
	mq3 = mq2.filter(ndb.OR(Match.country1 == country_key, Match.country2 == country_key))
	match_entries = mq3.fetch()

	# MATCHTEAMS for this SQUAD
	matchteam_entries = Matchteam.query(Matchteam.squad == squad_key)

	team_matches = []
	for match in match_entries:
		team_match = {}
		team_match['match'] = match

		for team in matchteam_entries:
			if team.match == match.key:
				team_match['team'] = team

		team_matches.append(team_match)


	return render_template('squad.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		squad_object=squad,
		team_object=team,
		squadmembers=squadmembers_entries,
		team_matches=team_matches,
		matchteams=matchteam_entries,
		rep_squadmembers=rep_squadmembers,
	)

#NEW squad PAGE
@squad_bp.route('/new/<key>')
def new_squad(key):
	team_key = ndb.Key(urlsafe=key)
	team = team_key.get()

	#need Sport key as ancestor
	event_entries = Event.query(ancestor=team_key.parent().parent()).fetch()

	#BREADCRUMB
	#team - above
	# country
	country = team_key.parent().get()
	# sport
	sport = team_key.parent().parent().get()

	breadcrumb_list = [sport, country, team]

	return render_template('squad.html',
		breadcrumb = breadcrumb_list,
		object_title='New squad',
		team_object=team,
		events=event_entries,
		)



# HANDLERS #

# ADD squad
@squad_bp.route('/add/<team_key>/<event_key>', methods=['GET'])
def add_entry(team_key, event_key):
	team_key = ndb.Key(urlsafe=team_key)
	event_key = ndb.Key(urlsafe=event_key)

	squad = Squad(parent=team_key, event=event_key)
	squad.put()
	return redirect('/admin/team/{}'.format(team_key.urlsafe()))


# UPDATE squad
#### NO UPDATE SQUAD
# @squad_bp.route('/update/<key>', methods=['POST'])
# def update_entry(key):
#     squad_key = ndb.Key(urlsafe=key)
#     squad = squad_key.get()
#     squad.name = request.form['squadName']
#     squad.put()

#     return redirect('/squad/{}'.format(squad.key.urlsafe()))
