from flask import Blueprint, session, jsonify

from flask_restful import Api, url_for, marshal_with, reqparse

from heroes.helpers import Api, Resource, make_response

from .models import Sport


sports_bp = Blueprint('sports', __name__)
sports_api = Api(sports_bp)


@sports_api.resource('/')
class SportListApi(Resource):

    def get(self):
        sport_dbs = Sport.get_dbs()
        return make_response(sport_dbs, Sport.FIELDS)


    def post(self):
        parser = self._make_parser(('name', {'required': True}),
                                   ('description', {}))
        args = parser.parse_args()
        sport = Sport(name=args.name, description=args.get('description'))
        sport.put()
        return make_response(sport, Sport.FIELDS)
