from flask import Blueprint, session, jsonify

from flask_restful import Api, Resource, url_for

from heroes.helpers import Api, make_response

from .models import Sport


sports_bp = Blueprint('sports', __name__)
sports_api = Api(sports_bp)


@sports_api.resource('/')
class SportListApi(Resource):
    def get(self):
        sport_dbs = Sport.get_dbs()
        return make_response(sport_dbs, Sport.FIELDS)
