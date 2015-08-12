from flask import Blueprint, session, jsonify
from flask_restful import Api, url_for, marshal_with, reqparse
from heroes.helpers import Api, Resource, make_response
from models import Role

roles_bp = Blueprint('roles', __name__)
roles_api = Api(roles_bp)

@roles_api.resource('/')
class DivisionListView(Resource):

	def get(self):
		roles_dbs = Role.get_dbs()
		return make_response(roles_dbs, Role.FIELDS)

@roles_api.resource('/<int:role_id>/')
class RoleView(Resource):
	
	def get(self, division_id):
		role = Role.get_by_id(role_id)
		return make_response(role, Role.FIELDS)
		