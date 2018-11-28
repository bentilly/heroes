from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
from google.appengine.api import users

import logging

from .models import Sport
from heroes.countries.models import Country
from heroes.divisions.models import Division
from heroes.roles.models import Role
from heroes.events.models import Event
from heroes.venues.models import Venue
from heroes.trophies.models import Trophy
from heroes.users.models import Editor



sports_bp = Blueprint('sports', __name__)


# RENDERING #

# HOME PAGE. A list of sports
@sports_bp.route('/all')
def sports_list():

    logoutlink = users.create_logout_url("/")
    currentuser = users.get_current_user()
    
    if users.is_current_user_admin():
        sports_entries = Sport.query().fetch()
        return render_template('home.html',
                object_title='Heroes',
                sports=sports_entries,
                logoutlink=logoutlink,
                user=currentuser,
            )
    else:
        #need no admin page. Needs to include log out link
        #self.response.write('You are not an administrator.')
        return render_template('notAdmin.html',
                logoutlink=logoutlink,
                user=currentuser,
            )





# A SPORT PAGE.
@sports_bp.route('/<key>/')
def sport_view(key):
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()

    country_entries = Country.query(ancestor=sport_key).order(Country.name).fetch()
    division_entries = Division.query(ancestor=sport_key).order(Division.name).fetch()
    role_entries = Role.query(ancestor=sport_key).fetch() #TODO - move to child of COUNTRY
    event_entries = Event.query(ancestor=sport_key).order(Event.startdate).fetch()
    venue_entries = Venue.query(ancestor=sport_key).fetch()
    trophy_entries = Trophy.get_latest_revisions(ancestor=sport_key)
    

    return render_template('sport.html',
            object_title=sport.name,
            sport_object = sport,
            countries=country_entries,
            divisions=division_entries,
            #roles=role_entries,  #TODO - move to child of COUNTRY
            events=event_entries,
            venues=venue_entries,
            trophies=trophy_entries,
        )

#NEW SPORT PAGE
@sports_bp.route('/new')
def new_sport():
    return render_template('sport.html',
            object_title='New sport',
        )



# HANDLERS #

# ADD SPORT
@sports_bp.route('/add', methods=['POST'])
def add_entry():

    # TODO: Form not complete
    sport = Sport(name=request.form['sportName'], code=request.form['sportCode'])
    #TODO sport.code must be unique

    sport.put()

    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))


# UPDATE SPORT
@sports_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    # TODO: Form not complete
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()
    sport.name = request.form['sportName']
    sport.code = request.form['sportCode'] #TODO must be unique
    #Check box
    published = False
    try:
        if request.form['publishSport']:
            published = True
        pass
    except:
        pass

    sport.published = published

    sport.put()

    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))




#REGISTER EDITOR 
# dont do this anymore. Might in the future

# @sports_bp.route('/register', methods=['POST'])
# def register_editor():
#     currentuser = users.get_current_user()
#     editor = Editor(
#         userid=currentuser.user_id(),
#         firstname=request.form['firstName'],
#         lastname=request.form['lastName'],
#         phone=request.form['phone'],
#         country=request.form['country'],
#         sport=request.form['sport'],

#         )

#     editor.put()
#     # return redirect('/admin/sport/all')  Happens to fast. put() has not completed
#     logoutlink = users.create_logout_url("/")
#     sports_entries = Sport.query().fetch()
#     return render_template('home.html',
#             object_title='Heroes',
#             sports=sports_entries,
#             logoutlink=logoutlink,
#             user=currentuser,
#         )