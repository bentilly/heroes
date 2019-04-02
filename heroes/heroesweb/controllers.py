from flask import Blueprint, render_template, redirect, request, render_template_string
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
from heroes.templates.models import Template



heroesweb_bp = Blueprint('heroesweb_bp', __name__)


# ================================================================================
# EVALUATE URL's (get KEY to render and pass on)
# ================================================================================

@heroesweb_bp.route('/')
	# 1. Evaluate base URL
	# 2. Hand off to renderers
def eval_base_url():
	#SPORT home page?
	home = Sport.query(Sport.external_url == request.url).fetch(1)
	if home:
		return render_sport_home(home[0])
	else:
		home = Country.query(Country.external_url == request.url).fetch(1)
		if home:
			return render_country_home(home[0])

	return render_sh_home()


@heroesweb_bp.route('sport/<key>/')
	# 1. Retrieve SPORT
	# 2. Hand off to SPORT HOME PAGE renderer
def eval_sport(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()
	return render_sport_home(sport)

@heroesweb_bp.route('country/<key>/')
	# 1. Retrieve COUNTRY
	# 2. Hand off to COUNTRY HOME PAGE renderer
def eval_country(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()
	return render_country_home(country)


@heroesweb_bp.route('squad/<key>/')
	# 1. Retrieve SQUAD
	# 2. Hand off to SQUAD PAGE renderer (Team template)
def eval_squad(key):
	squad_key = ndb.Key(urlsafe=key)
	squad = squad_key.get()
	return render_squad(squad)


@heroesweb_bp.route('rep/<key>/')
	# 1. Retrieve REP
	# 2. Hand off to REP PAGE renderer
def eval_rep(key):
	# check if key is a rep uid
	reps = Rep.query(Rep.uid == key).fetch(1)
	if reps:
		rep = reps[0]
	else: #it better be a NDB key object
		rep_key = ndb.Key(urlsafe=key)
		rep = rep_key.get()

	return render_rep(rep)





# ================================================================================
# RENDERERS
#	t = '<html><body>hello world!</body></html>'  # How to pull a template from database
#	return render_template_string(t)
# ================================================================================

# NOTE: Gradually converting 
#	SPORT => LEAGUE
#	COUNTRY => CLUB


def render_sh_home():
	all_leagues = []

	leagues = Sport.query(Sport.published == True).order(Sport.name).fetch()
	for l in leagues:
		l_franchises = Country.query(Country.published == True, ancestor=l.key).order(Country.name).fetch()
		league = {"name":l.name, "franchises":l_franchises}
		all_leagues.append(league)

	template_path = "public/sh-home.html"

	return render_template(template_path,
			leagues = all_leagues,
		)


def render_sport_home(sport):
	countries = Country.query(Country.published == True, ancestor=sport.key).order(Country.name).fetch()
	templates_entries = Template.query(Template.label == 'sport', ancestor=sport.key).fetch()

	if len(templates_entries) > 0:
		t=templates_entries[0].content
	else:
		t="no template found"

	return render_template_string(t,
			sport = sport,
			countries=countries,
		)



def render_country_home(country):
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
	menu_squads = get_menu_squads(country.key)


	# RENDER TEMPLATE ===========================
	sport = country.key.parent().get()

	try:
		templates = Template.query(Template.label == 'country', ancestor=country.key).fetch()
		t = templates[0].content
	except:
		try:
			templates = Template.query(Template.label == 'd_country', ancestor=sport.key).fetch()
			t = templates[0].content
		except:	
			t="no template found"

	return render_template_string(t,
			heroSquads = hero_squads,
			squads = menu_squads,
			country = country,
			sport = sport,
		)


# PROFILE of SQUAD (and team history) --------- 

def render_squad(squad):
	# trace parents - if not used, delete
	team = squad.key.parent().get()
	country = team.key.parent().get()

	# get all the sqad members
	squadMembers = Squadmember.query(ancestor=squad.key).fetch()
	# sort squadMembers. 1. Captain, 2. Vice Captain, 3. Players, 4 Coach, 5, Manager
	squadMembers.sort(key=sortSquadMembersOnName)
	squadMembers.sort(key=sortSquadMembersOnRole)


	# get all the other squads of this team
	teamSquads = Squad.query(ancestor=team.key).fetch()
	teamSquads.sort(key=sortSquadOnDate, reverse=True)

	# TODO: sort them by event date

	# MENU ======== Get latest squad for every team that has a squad.
	menu_squads = get_menu_squads(country.key)

	# RENDER TEMPLATE =========
	sport = country.key.parent().get()

	try:
		templates = Template.query(Template.label == 'team', ancestor=country.key).fetch()
		t = templates[0].content
	except:
		try:
			templates = Template.query(Template.label == 'd_team', ancestor=sport.key).fetch()
			t = templates[0].content
		except:	
			t="no template found"

	return render_template_string(t,
			squad = squad,
			squadmembers = squadMembers,
			teamsquads = teamSquads, #for history
			menusquads = menu_squads, #for menu
		)	





# PROFILE of SQUADMEMBER ---------

def render_rep(rep):
	#SORT stats
	if rep.stats:
		rep.stats.sort(key=sortRepStats)

	squadmembers = Squadmember.query(Squadmember.rep==rep.key).fetch() #Y

	# sort squadmembers on year
	squadmembers.sort(key=sortSquadMembersByDate, reverse=True)
	squadmember = squadmembers[0]

	# MENU ======== Get latest squad for every team that has a squad.
	country_key = rep.key.parent()
	menu_squads = get_menu_squads(country_key)

	# RENDER TEMPLATE =========
	country = country_key.get()
	sport = country_key.parent().get()

	try:
		templates = Template.query(Template.label == 'rep', ancestor=country.key).fetch()
		t = templates[0].content
	except:
		try:
			templates = Template.query(Template.label == 'd_rep', ancestor=sport.key).fetch()
			t = templates[0].content
		except:	
			t="no template found"

	return render_template_string(t,
			squadmember = squadmember,
			rep = rep,
			squadmembers = squadmembers,
			squads = menu_squads,
		)


# ================================================================================
# HELPERS
# ================================================================================

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



# FORMAT a time delta
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

# SORTING 

def sortRepStats(stat):
    sortid = stat["sort"]
    return sortid

def sortSquadMembersByDate(sm):
	sortvalue = sm.key.parent().get().eventdate.year
	return sortvalue

def sortSquadMembersOnName(sm):
	return sm.title

def sortSquadMembersOnRole(sm):
	# SquadMember may not have a role set
	try:
		sort = sm.role.get().sort
	except:
		sort = 0
	return sort

def getSquadTitle(elem):
	s = elem['squad']
	return s.teamName

def sortSquadOnDivision(s):
	return s.divisionName

def sortSquadOnDate(s):
	return s.eventdate




