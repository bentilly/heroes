from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

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

    #Some SQUADS
    squad_entries = Squad.query(ancestor=team_key).fetch()


    #EVENT SQUADS
    event_squads = []

    for e in event_entries:
        event_squad = {}
        event_squad['event'] = e

        for s in squad_entries:
            if s.event == e.key:
                event_squad['squad'] = s

        event_squads.append(event_squad)


    return render_template('team.html',
            breadcrumb = breadcrumb_list,
            object_title=title,
            team_object=team,
            squads=squad_entries,
            event_squads=event_squads
        )

#NEW TEAM PAGE
#Team = Country + Division. Create automatically on COUNTRY or DIVISION creation
# @team_bp.route('/new/<key>')
# def new_team(key):
# 	country_key = ndb.Key(urlsafe=key)
# 	country = country_key.get()

# 	division_entries = Division.query(ancestor=country_key.parent()).fetch()

# 	return render_template('team.html',
# 		object_title='New team',
# 		country_object=country,
# 		divisions=division_entries,
# 		)



# HANDLERS #

#Team = Country + Division. Create automatically on COUNTRY or DIVISION creation
# @team_bp.route('/add/<parent_key>', methods=['POST'])
# def add_entry(parent_key):
# 	country_key = ndb.Key(urlsafe=parent_key)
# 	country = country_key.get()

# 	division_key = ndb.Key(urlsafe=request.form['division'])

# 	team = Team(name=request.form['teamName'], division=division_key, parent=country_key)
# 	team.put()

# 	return redirect('/team/{}'.format(team.key.urlsafe()))


# UPDATE TEAM
#Team = Country + Division. Created automatically. Only edit name
@team_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    team_key = ndb.Key(urlsafe=key)
    team = team_key.get()
    team.name = request.form['teamName']
    team.put()

    return redirect('/admin/team/{}'.format(team.key.urlsafe()))








