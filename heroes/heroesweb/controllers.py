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
# Sports Heroes HOME ------------------

@heroesweb_bp.route('/') 
def render_sh_home():
	# Lets see if I can detect the url
	logging.info("#############   BASE URL")
	logging.info(request.url)

	all_sports = Sport.query(Sport.published == True).fetch()
	return render_template('public/sh-home.html',
        allSports=all_sports,
    )


# A SPORT home page
@heroesweb_bp.route('sport/<key>/')
def sport_home(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()
	countries = Country.query(Country.published == True, ancestor=sport_key).order(Country.name).fetch()

	return render_template('public/sh-sport.html',
		sport = sport,
		countries=countries,
	)


# A SPORT/COUNTRY home page
# eg: Underwater Hockey, New Zealand

@heroesweb_bp.route('country/<key>/')
def render_country_home(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()

	hero_squads = []
	hero_teams = Team.query(Team.show_on_home_page == True, ancestor=country.key).fetch()

	for team in hero_teams:
		squads = Squad.query(ancestor=team.key).fetch()
		# TODO: this throws an error if no squads - fix
		# TODO: Probably a better way to do this with sorting or something
		latest_squad = squads[0]
		for squad in squads:
			if squad.eventdate > latest_squad.eventdate:
				latest_squad = squad

		squad_members = Squadmember.query(ancestor=latest_squad.key).fetch()
		# sort squadMembers. 1. Captain, 2. Vice Captain, 3. Players, 4 Coach, 5, Manager
		squad_members.sort(key=sortSquadMembersOnName)
		squad_members.sort(key=sortSquadMembersOnRole)

		hero_squad = {"squad":latest_squad, "squad_members":squad_members, "next_match_in":None}
		hero_squads.append(hero_squad)
			
	hero_squads.sort(key=getSquadTitle)  #TODO: Update name case format (get_squad_title)

	#Next next match for each hero_squad in hero_squads
	now = datetime.datetime.now() #now is UTC. match.date is also UTC

	for hero_squad in hero_squads:
		squad = hero_squad["squad"]
		event_key = squad.event
		division = squad.key.parent().get().division
		country_key = squad.key.parent().parent()

		division_matches = Match.query(Match.division == division, ancestor=event_key).order(Match.date).fetch()

		for match in division_matches:
			if match.country1 == country_key or match.country2 == country_key:
				if match.date > now:
					delta = match.date - now
					days = delta.days
					hours = strfdelta(delta, "{hours}")
					minutes = strfdelta(delta, "{minutes}")

					delta_display = {"d":delta.days, "h":hours, "m":minutes}
					hero_squad["nextMatchIn"] = delta_display

					break

	# MENU ======== Get latest squad for every team that has a squad.
	menu_squads = get_menu_squads(country_key)

	# render nzlHome template
	return render_template('public/nzlHome.html',  ##TODO: Update name case format (nzl-home.html)
		heroSquads = hero_squads,
		squads = menu_squads,
	)


# PROFILE of SQUAD (and team history) --------- 
@heroesweb_bp.route('squad/<key>/')
def render_squad_profile(key):
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

	# MENU ======== Get latest squad for every team that has a squad.
	menu_squads = get_menu_squads(country.key)

	# render the page
	return render_template('public/nzlTeam.html',
		squad = squad,
		squadmembers = squadMembers,
		teamsquads = teamSquads, #for history
		menusquads = menu_squads, #for menu
	)




# PROFILE of SQUADMEMBER ---------
@heroesweb_bp.route('rep/<key>/')
def render_rep_profile(key):
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

	# MENU ======== Get latest squad for every team that has a squad.
	country_key = rep_key.parent()
	menu_squads = get_menu_squads(country_key)

	return render_template('public/nzlSquadmember.html',
		squadmember = squadmember,
		rep = rep,
		squadmembers = squadmembers,
		squads = menu_squads,
	)


# HELPERS ================================================================================

def get_menu_squads(country_key):
	teams = Team.query(ancestor=country_key).fetch()
	menu_squads = []
	for t in teams:
		allsquads = Squad.query(ancestor=t.key).fetch()

		if allsquads: #empty list returns False
			latest_squad = allsquads[0]

			for asq in allsquads:
				if asq.eventdate > latest_squad.eventdate:
					latest_squad = asq
					# TODO: Can I sort by date and pick the first?

			menu_squads.append(latest_squad)

	menu_squads.sort(key=sortSquadOnDivision) #TODO: Update name case format (sort_squad_on_division)
	return menu_squads


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




