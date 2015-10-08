from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Venue
from heroes.sports.models import Sport

venue_bp = Blueprint('venue', __name__)

# RENDERING #

# A venue PAGE.
@venue_bp.route('/<key>/')
def venue_view(key):
	venue_key = ndb.Key(urlsafe=key)
	venue = venue_key.get()

	#BREADCRUMB
	# sport
	sport = venue_key.parent().get()

	breadcrumb_list = [sport]
	title = venue.title
	#END BREADCRUMB

	return render_template('venue.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		venue_object=venue,
	)

#NEW venue PAGE
@venue_bp.route('/new/<key>')
def new_venue(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()

	breadcrumb_list = [sport]


	return render_template('venue.html',
		breadcrumb = breadcrumb_list,
		object_title='New venue',
		sport_object=sport,
	)



# HANDLERS #

# ADD venue
@venue_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	sport_key = ndb.Key(urlsafe=parent_key)
	sport = sport_key.get()

	venue = Venue(name=request.form['venueName'], parent=sport_key)
	venue.put()

	return redirect('/venue/{}'.format(venue.key.urlsafe()))


# UPDATE venue
@venue_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    venue_key = ndb.Key(urlsafe=key)
    venue = venue_key.get()
    venue.name = request.form['venueName']
    venue.put()

    return redirect('/venue/{}'.format(venue.key.urlsafe()))











