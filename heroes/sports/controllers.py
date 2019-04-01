from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
from google.appengine.api import users

import logging

from heroes.sports.models import Sport
from heroes.countries.models import Country
from heroes.divisions.models import Division
from heroes.roles.models import Role
from heroes.events.models import Event
from heroes.venues.models import Venue
from heroes.trophies.models import Trophy
from heroes.users.models import Editor
from heroes.templates.models import Template

# CLOUD STORAGE
import os
import cloudstorage
from google.appengine.api import app_identity
import ntpath

sports_bp = Blueprint('sports', __name__)


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

# HOME PAGE. A list of sports
@sports_bp.route('/all')
def sports_list():

    logoutlink = users.create_logout_url("/")
    currentuser = users.get_current_user()
    
    if users.is_current_user_admin():
        sports_entries = Sport.query().fetch()
        return render_template('/admin/home.html',
                object_title='Heroes',
                sports=sports_entries,
                logoutlink=logoutlink,
                user=currentuser,
            )
    else:
        #need no admin page. Needs to include log out link
        #self.response.write('You are not an administrator.')
        return render_template('/admin/notAdmin.html',
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


    # CLOUD STORAGE #
    bucket_name = get_bucket_name()
    bucket_and_folder = '/'+bucket_name+'/'+sport.code
    url = 'http://localhost:8080/_ah/gcs' if is_local() else 'https://storage.googleapis.com'
    file_list = []

    files = cloudstorage.listbucket(bucket_and_folder, max_keys=10)
    for f in files:
        filename = f.filename
        basename = ntpath.basename(f.filename)
        filepath = url+f.filename
        file = {'filename':filename, 'basename':basename, 'filepath':filepath}

        file_list.append(file)


    # TEMPLATES #
    templates = {
                    'sport': None,
                    'country': None,
                    'team': None,
                    'rep': None
                }
    templates_entries = Template.query(ancestor=sport_key).fetch()

    for t in templates_entries:
        if t.label == 'sport':
            templates['sport'] = t

        if t.label == 'country':
            templates['country'] = t

        if t.label == 'team':
            templates['team'] = t

        if t.label == 'rep':
            templates['rep'] = t
    

    return render_template('/admin/sport.html',
            objectTitle=sport.name,
            sportObject = sport,
            countries=country_entries,
            divisions=division_entries,
            events=event_entries,
            venues=venue_entries,
            trophies=trophy_entries,
            fileList = file_list,
            templates = templates,
        )

#NEW SPORT PAGE
@sports_bp.route('/new')
def new_sport():
    return render_template('/admin/sport.html',
            object_title='New sport',
        )

# FILES ==========================================================

#UPLOAD A FILE
@sports_bp.route('/uploadfile/<key>', methods=['POST'])
def upload_file(key):

    #get parent
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()

    # work out bucket and folder
    bucket_name = get_bucket_name()
    bucket_and_folder = '/'+bucket_name+'/'+sport.code

    # read file
    uploaded_file = request.files['uploaded-file']
    file_content = uploaded_file.read()

    # file name remove spaces
    file_name = str(uploaded_file.filename).replace(" ", "-")
    file_type = uploaded_file.content_type

    # upload the file to Google Cloud Storage
    gcs_file = cloudstorage.open(
        bucket_and_folder + '/' + file_name,
        'w',
        content_type=file_type,
        retry_params=cloudstorage.RetryParams(backoff_factor=1.1)
        )

    gcs_file.write(file_content)
    gcs_file.close()

    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))

#DELETE A FILE
@sports_bp.route('/deletefile/<key>/<basename>')
def delete_file(key, basename):

    #get parent
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()

    # work out bucket and folder
    bucket_name = get_bucket_name()
    bucket_and_folder = '/'+bucket_name+'/'+sport.code
    filename = bucket_and_folder+'/'+basename

    try:
        cloudstorage.delete(filename)
    except:
        logging.info('Could not delete file')


    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))



# HANDLERS ========================================#

# ADD SPORT
@sports_bp.route('/add', methods=['POST'])
def add_entry():

    # TODO: Form not complete
    sport = Sport(name=request.form['sportName'], code=request.form['sportCode'])
    # TODO sport.code must be unique

    #External URL entrypoint 
    if request.form['externalUrl']:
        if request.form['externalUrl'] != "None":
            sport.external_url = request.form['externalUrl']

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

    #External URL entrypoint
    if request.form['externalUrl']:
        if request.form['externalUrl'] != "None":
            sport.external_url = request.form['externalUrl']

    sport.put()

    return redirect('/admin/sport/{}'.format(sport.key.urlsafe()))
