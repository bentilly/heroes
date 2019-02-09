from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

import logging

# For photos
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobKey
from heroes.helpers import get_image_url
from werkzeug import parse_options_header

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

	#-----PHOTO for this squad
	try:
		image_url = images.get_serving_url(squad.photo_key)
	except:
		image_url = "avatar"

	form_action = "/admin/squad/uploadPhoto/" +  key
	upload_url = blobstore.create_upload_url(form_action)


	return render_template('/admin/squad.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		squad_object=squad,
		team_object=team,
		squadmembers=squadmembers_entries,
		team_matches=team_matches,
		matchteams=matchteam_entries,
		rep_squadmembers=rep_squadmembers,
		photo_url=image_url,
		upload_url = upload_url,
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

	return render_template('/admin/squad.html',
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

# REMOVE Squad
@squad_bp.route('/remove/<squad_key>', methods=['GET'])
def remove_entry(squad_key):
	squad_key = ndb.Key(urlsafe=squad_key)
	team_key = squad_key.parent()

	# Dont delete if there are Squadmambers
	squadmembers = Squadmember.query(ancestor=squad_key).fetch()

	if len(squadmembers) == 0:
		squad_key.delete()

	return redirect('/admin/team/{}'.format(team_key.urlsafe()))

# UPLOAD squad photo
@squad_bp.route('/uploadPhoto/<key>', methods=['POST'])
def upload_squad_photo(key):

	squad_key = ndb.Key(urlsafe=key)
	squad = squad_key.get()


	# TODO: may be deleting photo if no file selected
	# was a photo uploaded
	f = None
	try:
		f = request.files['photo']
	except:
		pass

	# delete old photo
	if f:
		try:
			blob_key = squad.photo_key
			blob = blobstore.BlobInfo.get(blob_key)
			blob.delete()
			logging.info("SQUAD: deleted old photo")
		except:
			logging.info("SQUAD: no photo to delete")

	# Record new blobkey
	try:
		header = f.headers['Content-Type']
		parsed_header = parse_options_header(header)
		blob_key = parsed_header[1]['blob-key']
		squad.photo_key = BlobKey(blob_key)
		logging.info("SQUAD: saved new blobkey for TEAM PHOTO")
		squad.put()

	except:
		logging.info("SQUAD: didnt save new TEAM PHOTO")


	return redirect('/admin/squad/{}'.format(squad_key.urlsafe()))






















