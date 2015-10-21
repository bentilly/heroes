from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Sport
from heroes.countries.models import Country
from heroes.divisions.models import Division
from heroes.roles.models import Role
from heroes.events.models import Event
from heroes.venues.models import Venue
from heroes.trophies.models import Trophy




sports_bp = Blueprint('sports', __name__)


# RENDERING #

# HOME PAGE. A list of sports
@sports_bp.route('/all')
def sports_list():
    sports_entries = Sport.query().fetch()
    return render_template('home.html',
            object_title='Heroes',
            sports=sports_entries,
        )

# A SPORT PAGE.
@sports_bp.route('/<key>/')
def sport_view(key):
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()

    country_entries = Country.query(ancestor=sport_key).fetch()
    division_entries = Division.query(ancestor=sport_key).fetch()
    role_entries = Role.query(ancestor=sport_key).fetch() #TODO - move to child of COUNTRY
    event_entries = Event.query(ancestor=sport_key).fetch()
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
    sport = Sport(name=request.form['sportName'])
    sport.put()

    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))


# UPDATE SPORT
@sports_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()
    sport.name = request.form['sportName']
    sport.put()

    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))
