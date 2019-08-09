from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
import logging
import datetime
import pytz

from .models import Match
from heroes.sports.models import Sport
from heroes.venues.models import Venue
from heroes.divisions.models import Division
from heroes.countries.models import Country

match_bp = Blueprint('match', __name__)

# RENDERING #

# A match PAGE.
@match_bp.route('/<key>/')
def match_view(key):
	match_key = ndb.Key(urlsafe=key)
	match = match_key.get()

	#BREADCRUMB
	# event
	event_key = match_key.parent()
	event = event_key.get()
	# sport
	sport = event_key.parent().get()

	breadcrumb_list = [sport, event]
	title = match.title
	#END BREADCRUMB

	venue_entries = Venue.query(ancestor=event_key.parent()).fetch()
	division_entries = Division.query(ancestor=event_key.parent()).fetch()
	country_entries = Country.query(ancestor=event_key.parent()).fetch()

	return render_template('/admin/match.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		match_object=match,
		event_object=event,
		venues=venue_entries,
		divisions=division_entries,
		countries=country_entries,
	)

#NEW match PAGE
@match_bp.route('/new/<key>')
def new_match(key):
	event_key = ndb.Key(urlsafe=key)
	event = event_key.get()

	venue_entries = Venue.query(ancestor=event_key.parent()).fetch()
	division_entries = Division.query(ancestor=event_key.parent()).fetch()
	country_entries = Country.query(ancestor=event_key.parent()).fetch()

	#BREADCRUMB
	# event - done above

	# sport
	sport = event_key.parent().get()

	breadcrumb_list = [sport, event]
	#END BREADCRUMB

	return render_template('/admin/match.html',
		breadcrumb = breadcrumb_list,
		object_title='New match',
		event_object=event,
		venues=venue_entries,
		divisions=division_entries,
		countries=country_entries,
	)



# HANDLERS #

# ADD match
@match_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	event_key = ndb.Key(urlsafe=parent_key)

### MATCH DATE
	datetimestring = request.form['matchdate']+"-"+request.form['matchstarttime']
	matchdate_raw = datetime.datetime.strptime(datetimestring, "%Y-%m-%d-%H:%M")

### MATCH VENUE
	matchvenue_key = ndb.Key(urlsafe=request.form['matchvenue'])
	matchvenue = matchvenue_key.get()

	# add timezone
	timezone = pytz.timezone(matchvenue.timezone)
	matchdate_tz = timezone.localize(matchdate_raw) #date tagged with timezone
	# convert to UTC
	matchdate_utc = matchdate_tz.astimezone(pytz.timezone("UTC"))
	#remove time zone for storage
	matchdate_save = matchdate_utc.replace(tzinfo=None)



### THE REST
	matchdivison = ndb.Key(urlsafe=request.form['matchdivision'])
	matchcountry1 = ndb.Key(urlsafe=request.form['matchcountry1'])
	matchcountry1score = None
	if request.form['c1score']:
		matchcountry1score = int(request.form['c1score'])
		
	
	matchcountry2 = ndb.Key(urlsafe=request.form['matchcountry2'])
	matchcountry2score = None
	if request.form['c2score']:
		matchcountry2score = int(request.form['c2score'])

	match = Match(
		date=matchdate_save, 
		venue=matchvenue_key, 
		division=matchdivison, 
		country1=matchcountry1, 
		country1score=matchcountry1score, 
		country2=matchcountry2, 
		country2score=matchcountry2score, 
		parent=event_key,
		)

	match.put()

	return redirect('/admin/match/{}'.format(match.key.urlsafe()))


# UPDATE match
@match_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
	match_key = ndb.Key(urlsafe=key)
	match = match_key.get()

### MATCH DATE
	datetimestring = request.form['matchdate']+"-"+request.form['matchstarttime']
	matchdate_raw = datetime.datetime.strptime(datetimestring, "%Y-%m-%d-%H:%M")
	match.venue=ndb.Key(urlsafe=request.form['matchvenue'])

	# add timezone Canada/Eastern
	timezone = pytz.timezone(match.venue.get().timezone)
	matchdate_tz = timezone.localize(matchdate_raw) #date tagged with timezone
	# convert to UTC
	matchdate_utc = matchdate_tz.astimezone(pytz.timezone("UTC"))
	#remove time zone for storage
	match.date = matchdate_utc.replace(tzinfo=None)

### THE REST
	match.division=ndb.Key(urlsafe=request.form['matchdivision'])
	match.country1=ndb.Key(urlsafe=request.form['matchcountry1'])
	match.country1score=None
	if request.form['c1score']:
		match.country1score = int(request.form['c1score'])
	match.country2=ndb.Key(urlsafe=request.form['matchcountry2'])
	match.country2score=None
	if request.form['c2score']:
		match.country2score = int(request.form['c2score'])

	match.put()

	return redirect('/admin/match/{}'.format(match.key.urlsafe()))






