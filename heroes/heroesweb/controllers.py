from flask import Blueprint, render_template, redirect, request
from google.appengine.ext import ndb
from google.appengine.api import images

from heroes.helpers import get_image_url

import logging
import operator
import datetime
from operator import itemgetter

from heroes.sports.models import Sport
from heroes.countries.models import Country
from heroes.representatives.models import Rep
from heroes.squadmembers.models import Squadmember
from heroes.teams.models import Team
from heroes.squads.models import Squad
from heroes.matches.models import Match

heroesweb_bp = Blueprint('heroesweb_bp', __name__)

# RENDERING : public website#
# HOME ------------------
@heroesweb_bp.route('/')
def heroes_home():
	#find UWH + NZL
	sport = Sport.query(Sport.name == 'Underwater Hockey').fetch(1)
	countries = Country.query(ancestor=sport[0].key).fetch()

	for country in countries:
		if country.code == 'NZL': #replace 'NZL' later with DB branch or URL
			heroSquads = []
			allNZLteams = Team.query(ancestor=country.key).fetch()

			############## LOAD TEAMS BASED ON FLAG IN DB (TEAM)

			for team in allNZLteams:
				# if team.title == 'NZL Elite Men' or team.title == 'NZL Elite Women' or team.title == 'NZL Mens Masters':
				if team.showOnHomePage == True:
					squads = Squad.query(ancestor=team.key).fetch()
					# TODO: this throws an error if no squads - fix
					# TODO: Probably a better way to do this with sorting or something
					latestSquad = squads[0]

					for squad in squads:
						if squad.eventdate > latestSquad.eventdate:
							latestSquad = squad

					
					squadMembers = Squadmember.query(ancestor=latestSquad.key).fetch()
					# sort squadMembers. 1. Captain, 2. Vice Captain, 3. Players, 4 Coach, 5, Manager
					squadMembers.sort(key=sortSquadMembersOnName)
					squadMembers.sort(key=sortSquadMembersOnRole)

					heroSquad = {"squad":latestSquad, "squadMembers":squadMembers, "nextMatchIn":None}
					heroSquads.append(heroSquad)
					
			heroSquads.sort(key=getSquadTitle)

			#Next next match for each heroSquad in heroSquads
			now = datetime.datetime.now() #now is UTC. match.date is also UTC

			for heroSquad in heroSquads:
				squad = heroSquad["squad"]
				event_key = squad.event
				division = squad.key.parent().get().division
				country = squad.key.parent().parent()

				divisionMatches = Match.query(Match.division == division, ancestor=event_key).order(Match.date).fetch()

				for match in divisionMatches:
					if match.country1 == country or match.country2 == country:
						if match.date > now:
							delta = match.date - now
							days = delta.days
							hours = strfdelta(delta, "{hours}")
							minutes = strfdelta(delta, "{minutes}")

							deltaDisplay = {"d":delta.days, "h":hours, "m":minutes}
							heroSquad["nextMatchIn"] = deltaDisplay

							break

			# Get latest squad for every team. Used in MENU
			menuSquads = []
			for t in allNZLteams:
				allsquads = Squad.query(ancestor=t.key).fetch()
				latestSquad = allsquads[0]

				for asq in allsquads:
					if asq.eventdate > latestSquad.eventdate:
						latestSquad = asq
						# TODO: Can I sort by date and pick the first?

				menuSquads.append(latestSquad)
				menuSquads.sort(key=sortSquadOnDivision)

			# render nzlHome template
			return render_template('public/nzlHome.html',
				heroSquads = heroSquads,
				squads = menuSquads,
			)


# PROFILE of SQUAD (and team history) --------- 
@heroesweb_bp.route('squad/<key>/')
def squad_profile(key):
	squad_key = ndb.Key(urlsafe=key)
	squad = squad_key.get()
	# trace parents - if not used, delete
	team = squad_key.parent().get()
	country = team.key.parent().get()


	# get all the sqad members
	squadMembers = Squadmember.query(ancestor=squad_key).fetch()
	# sort squadMembers. 1. Captain, 2. Vice Captain, 3. Players, 4 Coach, 5, Manager
	squadMembers.sort(key=sortSquadMembersOnName)
	squadMembers.sort(key=sortSquadMembersOnRole)


	# get all the other squads of this team
	teamSquads = Squad.query(ancestor=team.key).fetch()
	teamSquads.sort(key=sortSquadOnDate, reverse=True)

	# TODO: sort them by event date


	# get the latest squad for all teams for this sport/country - to build the menu
	menuTeams = Team.query(ancestor=country.key).fetch()
	menuSquads = []
	for t in menuTeams:
		allsquads = Squad.query(ancestor=t.key).fetch()
		latestSquad = allsquads[0]

		for asq in allsquads:
			if asq.eventdate > latestSquad.eventdate:
				latestSquad = asq

		menuSquads.append(latestSquad)
		menuSquads.sort(key=sortSquadOnDivision)

	# render the page
	return render_template('public/nzlTeam.html',
		squad = squad,
		squadmembers = squadMembers,
		teamsquads = teamSquads, #for history
		menusquads = menuSquads, #for menu
	)




# PROFILE of SQUADMEMBER ---------
@heroesweb_bp.route('rep/<key>/')
def rep_profile(key):
	# check if key is a rep uid
	reps = Rep.query(Rep.uid == key).fetch(1)
	if reps:
		rep = reps[0]
		rep_key = rep.key
	else: #it better be a NDB key object
		rep_key = ndb.Key(urlsafe=key)
		# squadmember = sm_key.get()
		# rep_key = squadmember.rep
		rep = rep_key.get()


	#SORT stats
	if rep.stats:
		rep.stats.sort(key=sortRepStats)

	squadmembers = Squadmember.query(Squadmember.rep==rep_key).fetch()
	# sort squadmembers on year
	squadmembers.sort(key=sortSquadMembersByDate, reverse=True)
	squadmember = squadmembers[0]

	# MENU Get latest squad for every team.
	country = rep_key.parent().get()
	allNZLteams = Team.query(ancestor=country.key).fetch()

	# Get latest squad for every team. Used in MENU
	menuSquads = []
	for t in allNZLteams:
		allsquads = Squad.query(ancestor=t.key).fetch()
		latestSquad = allsquads[0]

		for asq in allsquads:
			if asq.eventdate > latestSquad.eventdate:
				latestSquad = asq
				# TODO: Can I sort by date and pick the first?
				# TODO: this is used on every page. Should be abstracted

		menuSquads.append(latestSquad)
		menuSquads.sort(key=sortSquadOnDivision)

	return render_template('public/nzlSquadmember.html',
		squadmember = squadmember,
		rep = rep,
		squadmembers = squadmembers,
		squads = menuSquads,
	)


# HELPERS -----------------------------------------------

def sortRepStats(stat):
    sortid = stat["sort"]
    return sortid

def sortSquadMembersByDate(sm):
	sortvalue = sm.key.parent().get().eventdate.year
	return sortvalue

#format a time delta
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def sortSquadMembersOnName(sm):
	name = sm.title
	return name

def sortSquadMembersOnRole(sm):
	roleKey = 3
	try:
		role = sm.roleName

		if role == "Captain":
			roleKey = 1
		if role == "Vice Captain":
			roleKey = 2
		if role == "Coach":
			roleKey = 4
		if role == "Manager":
			roleKey = 5
	except:
		roleKey = 3

	return roleKey

def getSquadTitle(elem):
	s = elem['squad']
	return s.teamName

def sortSquadOnDivision(s):
	return s.divisionName

def sortSquadOnDate(s):
	return s.eventdate




