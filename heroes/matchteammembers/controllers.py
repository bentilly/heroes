from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Matchteammember
from heroes.sports.models import Sport
from heroes.roles.models import Role
from heroes.positions.models import Position

matchteammember_bp = Blueprint('matchteammember', __name__)

# RENDERING #

# A matchteammember PAGE.
@matchteammember_bp.route('/<key>/')
def matchteammember_view(key):
	matchteammember_key = ndb.Key(urlsafe=key)
	matchteammember = matchteammember_key.get()

	#BREADCRUMB
	#matchteam
	matchteam = matchteammember_key.parent().get()
	# squad
	squad = matchteam.squad.get()
	#team
	team = squad.key.parent().get()
	# country
	country = squad.key.parent().parent().get()
	# sport
	sport = squad.key.parent().parent().parent().get()

	breadcrumb_list = [sport, country, team, squad, matchteam]
	title = matchteammember.title
	#END BREADCRUMB

	role_entries = Role.query(ancestor=country.key).fetch()
	position_entries = Position.query(ancestor=country.key).fetch()

	return render_template('matchteammember.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		matchteammember_object=matchteammember,
		roles=role_entries,
		positions = position_entries,
	)

#NEW matchteammember PAGE
# @matchteammember_bp.route('/new/<key>')
#---Dont neeed yet
# def new_matchteammember(key):
# 	sport_key = ndb.Key(urlsafe=key)
# 	sport = sport_key.get()


# 	return render_template('matchteammember.html',
# 		object_title='New matchteammember',
# 		sport_object=sport,
# 		)



# HANDLERS #

# ADD matchteammember
@matchteammember_bp.route('/add/<squadmember_key>/<matchteam_key>', methods=['GET']) #Is GET ok here?
def add_entry(squadmember_key, matchteam_key):
	squadmember_key = ndb.Key(urlsafe=squadmember_key)
	matchteam_key = ndb.Key(urlsafe=matchteam_key)
	squadmember = squadmember_key.get()
	rep_key = squadmember.rep
	role_key = squadmember.role #default to squadmember role
	position_key = squadmember.position #default to squadmember role

	matchteammember = Matchteammember(parent=matchteam_key, squadmember=squadmember_key, rep=rep_key, role=role_key, position=position_key)
	matchteammember.put()

	return redirect('/matchteam/{}'.format(matchteam_key.urlsafe()))


# UPDATE matchteammember
@matchteammember_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
	matchteammember_key = ndb.Key(urlsafe=key)
	matchteammember = matchteammember_key.get()

	if request.form['roleinput']:
		role_key = ndb.Key(urlsafe=request.form['roleinput'])
		matchteammember.role = role_key

	if request.form['positioninput']:
		position_key = ndb.Key(urlsafe=request.form['positioninput'])
		matchteammember.position = position_key


	matchteammember.put()

	return redirect('/matchteammember/{}'.format(matchteammember.key.urlsafe()))











