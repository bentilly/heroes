from flask import Blueprint, session, jsonify

from flask_restful import Api, url_for, marshal_with, reqparse

from heroes.helpers import Api, Resource, make_response, admin_required

from .models import Team
from .models import Sport

teams_bp = Blueprint('teams', __name__)
teams_api = Api(teams_bp)



@teams_api.resource('/')
class TeamListView(Resource):

    def get(self):
        team_dbs = Team.get_dbs()
        return make_response(team_dbs, Team.FIELDS)


    @admin_required
    def post(self):
        parser = self._make_parser(('sport_name', {'required': True}),
                                   ('name', {'required': False}),
                                   ('country_id', {'required': True}),
                                   ('division_name', {'required': True}))
        args = parser.parse_args()
        team = Team(parent=Sport.sport_key(args.sport_name),
                    name=args.name, country=args.country_id,
                    division_name=args.division_name)
        team.put()
        return make_response(team, Team.FIELDS)


@teams_api.resource('/<int:team_id>/')
class TeamView(Resource):

    def get(self, team_id):
        team = Team.get_by_id(team_id)
        return make_response(team, Team.FIELDS)


    @admin_required
    def put(self, team_id):
        parser = self._make_parser(('name', {'required': False}),
                                   ('country_id', {'required': True}),
                                   ('division_name', {'required': True}))
                                   
        args = parser.parse_args()

        team = Team.get_by_id(team_id)
        team.name = args.name
        team.country = args.country_id
        team.division_name = args.division_name
        team.put()
        return make_response(team, Team.FIELDS)


    @admin_required
    def delete(self, team_id):
        team = Team.get_by_id(team_id)
        team.key.delete()
