import logging

from flask import Blueprint, render_template, redirect, request
from werkzeug import parse_options_header

from google.appengine.ext import ndb

# For photos
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobKey
from heroes.helpers import get_image_url #not used

# CLOUD STORAGE
import os
import cloudstorage
from google.appengine.api import app_identity
import ntpath

from heroes.positions.models import Position
from heroes.representatives.models import Rep
from heroes.roles.models import Role

from .models import Squadmember

squadmember_bp = Blueprint('squadmember', __name__)

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


@squadmember_bp.route('/<key>/')
def squadmember_view(key):
    """A squadmember PAGE."""
    squadmember_key = ndb.Key(urlsafe=key)
    squadmember = squadmember_key.get()

    #BREADCRUMB
    squad = squadmember_key.parent().get()
    team = squad.key.parent().get()
    country = squad.key.parent().parent().get()
    sport = squad.key.parent().parent().parent().get()

    breadcrumb_list = [sport, country, team, squad]
    title = squadmember.title
    #END BREADCRUMB

    role_entries = Role.query(ancestor=country.key).fetch()
    position_entries = Position.query(ancestor=country.key).fetch()


    form_action = "/admin/squadmember/update/" +  key
    upload_url = blobstore.create_upload_url(form_action)

    return render_template('/admin/squadmember.html',
        breadcrumb = breadcrumb_list,
        object_title=title,
        squadmember_object=squadmember,
        squad_object=squad,
        roles=role_entries,
        # photo_url=image_url,
        positions=position_entries,
        # upload_url=upload_url,
    )


# HANDLERS #

# ADD squadmember
@squadmember_bp.route('/add/<squad_key>/<rep_key>', methods=['GET'])
def add_entry(squad_key, rep_key):
    squad_key = ndb.Key(urlsafe=squad_key)
    rep_key = ndb.Key(urlsafe=rep_key)

    squadmember = Squadmember(rep=rep_key, parent=squad_key)
    squadmember.put()

    return redirect('/admin/squad/{}'.format(squad_key.urlsafe()))


# UPDATE squadmember
@squadmember_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):

    squadmember_key = ndb.Key(urlsafe=key)
    squadmember = squadmember_key.get()

    if request.form['roleinput']:
        role_key = ndb.Key(urlsafe=request.form['roleinput'])
        squadmember.role = role_key

    if request.form['positioninput']:
        position_key = ndb.Key(urlsafe=request.form['positioninput'])
        squadmember.position = position_key

    #SQUADMEMBER PHOTO
    #define file name and path
    #   [bucket] /photos/[sport]/[country]/[division]/[squad(year)]/[first]-[last].jpg
    #   - crap if anything changes name (but not too hard to fix)
    #   - good for bulk upload
    #   - only works for jpgs
    uploaded_file = request.files['uploaded-file']
    file_content = uploaded_file.read()

    if file_content:
        logging.info(" THERE IS A PHOTO!")
        # check for jpg
        file_type = uploaded_file.content_type

        if file_type == "image/jpeg":
            filepath = generate_photo_filename(squadmember_key)

            # upload the file to Google Cloud Storage
            gcs_file = cloudstorage.open(
                filepath ,
                'w',
                content_type=file_type,
                retry_params=cloudstorage.RetryParams(backoff_factor=1.1)
                )
            gcs_file.write(file_content)
            gcs_file.close()

        else:
            logging.info("Wrong image type")

    else:
        logging.info("No photo uploaded")

    squadmember.put()

    return redirect('/admin/squadmember/{}'.format(squadmember.key.urlsafe()))




# REMOVE squadmember
@squadmember_bp.route('/remove/<squadmember_key>/', methods=['GET'])
def remove_entry(squadmember_key):
    squadmember_key = ndb.Key(urlsafe=squadmember_key)
    squad_key = squadmember_key.parent().get().key
    squadmember_key.delete()

    # TODO delete any photos 

    return redirect('/admin/squad/{}'.format(squad_key.urlsafe()))



# DELETE PHOTO
@squadmember_bp.route('/deletephoto/<squadmember_key>/', methods=['GET'])
def delete_photo(squadmember_key):
    squadmember_key = ndb.Key(urlsafe=squadmember_key)
    squadmember = squadmember_key.get()
    filepath = generate_photo_filename(squadmember_key)
    try:
        cloudstorage.delete(filepath)
    except:
        logging.info("NO PHOTO TO DELETE")

    return redirect('/admin/squadmember/{}'.format(squadmember.key.urlsafe()))



# ================================================================================
# HELPERS
# ================================================================================



def generate_photo_filename(squadmember_key):
    bucket_name = get_bucket_name()
    #get parent objects
    squadmember = squadmember_key.get()
    squad_key = squadmember_key.parent()
    team_key = squad_key.parent()
    country_key = team_key.parent()
    sport_key = country_key.parent()
    # file path codes
    sport_code = sport_key.get().code
    country_code = country_key.get().code
    division_code = team_key.get().division.get().code
    squad_code = squad_key.get().code
    #bucket and folder
    bucket_and_folder = '/'+bucket_name+'/photos/'+sport_code+'/'+country_code+'/'+division_code+'/'+squad_code
    logging.info(bucket_and_folder)
    #file name
    file_name = str(squadmember.title).replace(" ", "-").lower()
    file_name = file_name+'.jpg'

    return bucket_and_folder + '/' + file_name




