from flask import Blueprint, session, jsonify
from flask_restful import Api, url_for, marshal_with, reqparse
from heroes.helpers import Api, Resource, make_response
from models import Country

countries_bp = Blueprint('countries', __name__)
countries_api = Api(countries_bp)

@countries_api.resource('/')
class CountryListView(Resource):

    def get(self):
        country_dbs = Country.query().fetch()
        return make_response(country_dbs, Country.FIELDS)

@countries_api.resource('/<int:country_id>/')
class CountryView(Resource):
	
    def get(self, country_id):
        country = Country.get_by_id(country_id)
        return make_response(country, Country.FIELDS)
