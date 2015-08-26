from flask import Blueprint, session, jsonify

from google.appengine.ext import ndb

from heroes.helpers import Api, Resource, make_response, admin_required

from .models import Team

teams_bp = Blueprint('teams', __name__)


@teams_bp.route('/key/')
def team_view():
    pass