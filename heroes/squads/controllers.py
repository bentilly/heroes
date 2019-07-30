from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

import logging

# For photos (might not need any more)
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

# CLOUD STORAGE
import os
import cloudstorage
from google.appengine.api import app_identity
import ntpath



squad_bp = Blueprint('squad', __name__)

# CLOUD STORAGE #
def get_bucket_name():
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    return bucket_name

def is_local():
    """ Check if you are currently running on localhost or on GAE. """
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False


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
	# try:
	# 	image_url = images.get_serving_url(squad.photo_key)
	# except:
	# 	image_url = "avatar"

	# form_action = "/admin/squad/uploadPhoto/" +  key
	# upload_url = blobstore.create_upload_url(form_action)


	return render_template('/admin/squad.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		squad_object=squad,
		team_object=team,
		squadmembers=squadmembers_entries,
		team_matches=team_matches,
		matchteams=matchteam_entries,
		rep_squadmembers=rep_squadmembers,
		# photo_url=image_url,
		# upload_url = upload_url,
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


# UPDATE squad
@squad_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):

	squad_key = ndb.Key(urlsafe=key)
	squad = squad_key.get()

	if request.form['squadCode']:
		squad.code = request.form['squadCode']


	#SQUAD PHOTO
	#define file name and path
	#   [bucket] /photos/[sport]/[country]/[division]/[squad(year)]/[first]-[last].jpg
	#   - crap if anything changes name (but not too hard to fix)
	#   - good for bulk upload
	#   - only works for jpgs
	uploaded_file = request.files['uploaded-file']
	file_content = uploaded_file.read()

	if file_content:
		logging.info(" THERE IS A PHOTO!")
		# check for jpg
		file_type = uploaded_file.content_type

		if file_type == "image/jpeg":
			filepath = generate_photo_filename(squad_key)

			# upload the file to Google Cloud Storage
			gcs_file = cloudstorage.open(
				filepath ,
				'w',
				content_type=file_type,
				retry_params=cloudstorage.RetryParams(backoff_factor=1.1)
				)
			gcs_file.write(file_content)
			gcs_file.close()

		else:
			logging.info("Wrong image type")

	else:
		logging.info("No photo uploaded")

	squad.put()

	return redirect('/admin/squad/{}'.format(squad.key.urlsafe()))


# DELETE PHOTO
@squad_bp.route('/deletephoto/<squad_key>/', methods=['GET'])
def delete_photo(squad_key):
    squad_key = ndb.Key(urlsafe=squad_key)
    squad = squad_key.get()
    filepath = generate_photo_filename(squad_key)
    try:
        cloudstorage.delete(filepath)
    except:
        logging.info("NO PHOTO TO DELETE")

    return redirect('/admin/squad/{}'.format(squad.key.urlsafe()))



# ================================================================================
# HELPERS
# ================================================================================

def generate_photo_filename(squad_key):
    bucket_name = get_bucket_name()
    #get parent objects
    squad = squad_key.get()
    team_key = squad_key.parent()
    country_key = team_key.parent()
    sport_key = country_key.parent()
    # file path codes
    sport_code = sport_key.get().code
    country_code = country_key.get().code
    division_code = team_key.get().division.get().code
    squad_code = squad_key.get().code
    #bucket and folder
    bucket_and_folder = '/'+bucket_name+'/photos/'+sport_code+'/'+country_code+'/'+division_code+'/'+squad_code
    logging.info(bucket_and_folder)
    #file name
    file_name = squad_code+'-'+country_code+'-'+division_code
    file_name = file_name+'.jpg'

    return bucket_and_folder + '/' + file_name

















