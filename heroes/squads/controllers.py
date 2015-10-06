from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

import logging

from .models import Squad
from heroes.events.models import Event
from heroes.squadmembers.models import Squadmember

squad_bp = Blueprint('squad', __name__)

# RENDERING #

# A squad PAGE.
@squad_bp.route('/<key>/')
def squad_view(key):
    squad_key = ndb.Key(urlsafe=key)
    squad = squad_key.get()

    team = squad_key.parent().get()

    squadmembers_entries = Squadmember.query(ancestor=squad_key).fetch()

    #DONT NEED - NO UPDATE
    # event_entries = Event.query(ancestor=squad_key.parent().parent().parent()).fetch()

    return render_template('squad.html',
            object_title=squad.title,
            squad_object=squad,
            team_object=team,
            #events=event_entries,
            squadmembers=squadmembers_entries,
        )

#NEW squad PAGE
@squad_bp.route('/new/<key>')
def new_squad(key):
	team_key = ndb.Key(urlsafe=key)
	team = team_key.get()

	#need Sport key as ancestor
	event_entries = Event.query(ancestor=team_key.parent().parent()).fetch()

	return render_template('squad.html',
		object_title='New squad',
		team_object=team,
		events=event_entries,
		)



# HANDLERS #

# ADD squad
@squad_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	team_key = ndb.Key(urlsafe=parent_key)
	event_key = ndb.Key(urlsafe=request.form['squadEvent'])
	squad = Squad(parent=team_key, event=event_key)
	squad.put()
	return redirect('/squad/{}'.format(squad.key.urlsafe()))


# UPDATE squad
#### NO UPDATE SQUAD
# @squad_bp.route('/update/<key>', methods=['POST'])
# def update_entry(key):
#     squad_key = ndb.Key(urlsafe=key)
#     squad = squad_key.get()
#     squad.name = request.form['squadName']
#     squad.put()

#     return redirect('/squad/{}'.format(squad.key.urlsafe()))











