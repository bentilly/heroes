from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
import logging

from heroes.countries.models import Country
from heroes.sports.models import Sport
from heroes.divisions.models import Division
from heroes.teams.models import Team
from heroes.representatives.models import Rep
from heroes.roles.models import Role
from heroes.positions.models import Position
from heroes.templates.models import Template

# CLOUD STORAGE
import os
import cloudstorage
from google.appengine.api import app_identity
import ntpath

country_bp = Blueprint('country', __name__)


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

# A COUNTRY PAGE.
@country_bp.route('/<key>/')
def country_view(key):
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()

    #BREADCRUMB
    # sport
    sport = country_key.parent().get()

    breadcrumb_list = [sport]
    title = country.title
    #END BREADCRUMB


    team_entries = Team.query(ancestor=country_key).fetch()
    rep_entries = Rep.query(ancestor=country_key).order(Rep.firstname).fetch()
    role_entries = Role.query(ancestor=country_key).fetch()
    role_entries.sort(key=sort_role_by_sort)

    position_entries = Position.query(ancestor=country_key).fetch()


    # CLOUD STORAGE #
    bucket_name = get_bucket_name()
    bucket_and_folder = '/'+bucket_name+'/files/'+sport.code+'/'+country.code+'/'
    url = 'http://localhost:8080/_ah/gcs' if is_local() else 'https://storage.googleapis.com'
    file_list = []

    files = cloudstorage.listbucket(bucket_and_folder, delimiter='/')
    for f in files:
        filename = f.filename
        basename = ntpath.basename(f.filename)
        if basename:
            filepath = url+f.filename
            file = {'filename':filename, 'basename':basename, 'filepath':filepath}

            file_list.append(file)
        else:
            logging.info("Its a folder - dont show")


    # TEMPLATES #
    templates = {
                    'country': None,
                    'team': None,
                    'rep': None
                }
    templates_entries = Template.query(ancestor=country_key).fetch()

    for t in templates_entries:
        if t.label == 'country':
            templates['country'] = t

        if t.label == 'team':
            templates['team'] = t

        if t.label == 'rep':
            templates['rep'] = t


    return render_template('/admin/country.html',
            breadcrumb = breadcrumb_list,
            object_title=title,
            country_object=country,
            teams=team_entries,
            reps=rep_entries,
            roles=role_entries,
            positions=position_entries,
            bucketName = bucket_name,
            fileList = file_list,
            templates=templates,
        )

#UPLOAD A FILE
@country_bp.route('/uploadfile/<key>', methods=['POST'])
def upload_file(key):

    #get parent objects
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()
    sport = country_key.parent().get()

    # work out bucket and folder
    bucket_name = get_bucket_name()
    bucket_and_folder = '/'+bucket_name+'/files/'+sport.code+'/'+country.code

    # read file
    uploaded_file = request.files['uploaded-file']
    file_content = uploaded_file.read()
    # file name remove spaces
    file_name = str(uploaded_file.filename).replace(" ", "-")
    
    if file_name:
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
    else:
        logging.info('No file so dont save anything')

    return redirect('/admin/country/{}'.format(country.key.urlsafe()))

#DELETE A FILE ==============================================
@country_bp.route('/deletefile/<key>/<basename>')
def delete_file(key, basename):

    # get parent objects
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()
    sport = country_key.parent().get()

    # work out bucket and folder
    bucket_name = get_bucket_name()
    bucket_and_folder = '/'+bucket_name+'/files/'+sport.code+'/'+country.code
    filename = bucket_and_folder+'/'+basename

    logging.info('=========================')
    logging.info(filename)

    try:
        cloudstorage.delete(filename)
    except:
        logging.info('Could not delete file')


    return redirect('/admin/country/{}'.format(country.key.urlsafe()))





#NEW country PAGE
@country_bp.route('/new/<key>')
def new_country(key):
    sport_key = ndb.Key(urlsafe=key)
    sport = sport_key.get()

    breadcrumb_list = [sport]

    return render_template('/admin/country.html',
        breadcrumb = breadcrumb_list,
        object_title='New country',
        sport_object=sport,
    )



# HANDLERS #

# ADD country
@country_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
    sport_key = ndb.Key(urlsafe=parent_key)
    sport = sport_key.get()

    country = Country(name=request.form['countryName'], code=request.form['countryCode'], flagemoji=request.form['flagEmoji'], parent=sport_key)
    country.put()

    #Update TEAMS
    divisions = Division.query(ancestor=sport_key).fetch()
    for division in divisions:
        team = Team(parent=country.key, division=division.key)
        team.put()

    #External URL entrypoint
    if request.form['externalUrl']:
        if request.form['externalUrl'] != "None":
            country.external_url = request.form['externalUrl']

    return redirect('/admin/country/{}'.format(country.key.urlsafe()))


# UPDATE country
@country_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()
    country.name = request.form['countryName']
    country.code = request.form['countryCode']
    country.flagemoji = request.form['flagEmoji']

     #Check box
    published = False
    try:
        if request.form['publishCountry']:
            published = True
        pass
    except:
        pass

    country.published = published

    #External URL entrypoint
    if request.form['externalUrl']:
        if request.form['externalUrl'] != "None":
            country.external_url = request.form['externalUrl']
    
    country.put()

    return redirect('/admin/country/{}'.format(country.key.urlsafe()))


# ================================================================================
# HELPERS
# ================================================================================


def sort_role_by_sort(role):
    try:
        sort = role.sort
    except:
        sort = 0

    return sort





