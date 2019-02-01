from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Event
from heroes.sports.models import Sport
from heroes.matches.models import Match

import datetime

event_bp = Blueprint('event', __name__)

# RENDERING #

# An event PAGE.
@event_bp.route('/<key>/')
def event_view(key):
    event_key = ndb.Key(urlsafe=key)
    event = event_key.get()

    match_entries = Match.query(ancestor=event_key).fetch()

    #BREADCRUMB
    # sport
    sport = event_key.parent().get()

    breadcrumb_list = [sport]
    title = event.title
    #END BREADCRUMB


    return render_template('/admin/event.html',
            breadcrumb = breadcrumb_list,
            object_title=title,
            event_object=event,
            matches=match_entries,
        )

#NEW event PAGE
@event_bp.route('/new/<key>')
def new_event(key):
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()

    breadcrumb_list = [sport]

    return render_template('/admin/event.html',
        breadcrumb = breadcrumb_list,
        object_title='New event',
        sport_object=sport,
    )



# HANDLERS #

# ADD event
@event_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	sport_key = ndb.Key(urlsafe=parent_key)
	sport = sport_key.get()

	mydate = datetime.datetime.strptime(request.form['startDate'], "%Y-%m-%d").date()

	event = Event(name=request.form['eventName'], startdate=mydate, hostCity=request.form['hostCity'], parent=sport_key)
	event.put()

	return redirect('/admin/event/{}'.format(event.key.urlsafe()))


# UPDATE event
@event_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    event_key = ndb.Key(urlsafe=key)
    event = event_key.get()
    event.name = request.form['eventName']
    event.startdate = datetime.datetime.strptime(request.form['startDate'], "%Y-%m-%d").date()
    event.hostCity = request.form['hostCity']
    event.put()

    return redirect('/admin/event/{}'.format(event.key.urlsafe()))











