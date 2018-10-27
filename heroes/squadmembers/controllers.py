import logging

from flask import Blueprint, render_template, redirect, request
from werkzeug import parse_options_header

from google.appengine.ext import ndb

# For photos
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobKey
from heroes.helpers import get_image_url

from heroes.positions.models import Position
from heroes.representatives.models import Rep
from heroes.roles.models import Role

from .models import Squadmember

squadmember_bp = Blueprint('squadmember', __name__)


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

    # photo
    try:
        image_url = images.get_serving_url(squadmember.photo_key)
    except:
        image_url = "avatar"

    form_action = "/admin/squadmember/update/" +  key
    upload_url = blobstore.create_upload_url(form_action)

    return render_template('squadmember.html',
        breadcrumb = breadcrumb_list,
        object_title=title,
        squadmember_object=squadmember,
        squad_object=squad,
        roles=role_entries,
        photo_url=image_url,
        positions=position_entries,
        upload_url=upload_url,
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

    
    # TODO: seems to be deleting photo if no file selected
    # was a photo uploaded
    f = None
    try:
        f = request.files['photo']
    except:
        pass

    # delete old photo
    if f:
        try:
            blob_key = squadmember.photo_key
            blob = blobstore.BlobInfo.get(blob_key)
            blob.delete()
        except:
            logging.info("SQUADMEMBER: no photo to delete")

    # Record new blobkey
    try:
        header = f.headers['Content-Type']
        parsed_header = parse_options_header(header)
        blob_key = parsed_header[1]['blob-key']
        squadmember.photo_key = BlobKey(blob_key)
        logging.info("SQUADMEMBER: saved new blobkey")
    except:
        logging.info("SQUADMEMBER: didnt save new blobkey")

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















