from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
import logging

from .models import Team
from heroes.sports.models import Sport
from heroes.squads.models import Squad
from heroes.events.models import Event

team_bp = Blueprint('team', __name__)

# RENDERING #

# A TEAM PAGE.
@team_bp.route('/<key>/')
def team_view(key):
    team_key = ndb.Key(urlsafe=key)
    team = team_key.get()

    #BREADCRUMB
    # country
    country = team_key.parent().get()
    # sport
    sport = country.key.parent().get()

    breadcrumb_list = [sport, country]
    title = team.title
    #END BREADCRUMB


    #All EVENTS
    event_entries= Event.query(ancestor=sport.key).fetch()
    event_entries.sort(key=sortOnTitle, reverse=True)

    #Some SQUADS
    squad_entries = Squad.query(ancestor=team_key).fetch()
    squad_entries.sort(key=sortOnTitle, reverse=True)

    #EVENT SQUADS
    event_squads = []

    for e in event_entries:
        event_squad = {}
        event_squad['event'] = e

        for s in squad_entries:
            if s.event == e.key:
                event_squad['squad'] = s

        event_squads.append(event_squad)


    return render_template('/admin/team.html',
            breadcrumb = breadcrumb_list,
            object_title=title,
            team_object=team,
            squads=squad_entries,
            event_squads=event_squads
        )

def sortOnTitle(object):
    return object.title


# UPDATE TEAM
#Team = Country + Division. Created automatically. Only edit name
@team_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    team_key = ndb.Key(urlsafe=key)
    team = team_key.get()
    team.name = request.form['teamName']

    #Check box
    homepage = False
    try:
        if request.form['showOnHomeCB']:
            homepage = True
        pass
    except:
        pass

    team.show_on_home_page = homepage
    
    team.put()

    return redirect('/admin/team/{}'.format(team.key.urlsafe()))








