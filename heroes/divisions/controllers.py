from flask import Blueprint, session, jsonify
from flask_restful import Api, url_for, marshal_with, reqparse
from heroes.helpers import Api, Resource, make_response
from models import Division

divisions_bp = Blueprint('divisions', __name__)
divisions_api = Api(divisions_bp)

@divisions_api.resource('/')
class DivisionListView(Resource):

	def get(self):
		divisions_dbs = Division.get_dbs()
		return make_response(divisions_dbs, Division.FIELDS)

@divisions_api.resource('/<int:division_id>/')
class DivisionView(Resource):
	
	def get(self, division_id):
		division = Division.get_by_id(division_id)
		return make_response(division, Division.FIELDS)
		