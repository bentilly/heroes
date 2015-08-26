from flask import Blueprint, session, jsonify

from google.appengine.ext import ndb

from flask_restful import Api, url_for, marshal_with, reqparse

from heroes.helpers import Api, Resource, make_response, admin_required

from heroes.teams.models import Team
from .models import Event
from .models import Sport

events_bp = Blueprint('events', __name__)
events_api = Api(events_bp)



@events_api.resource('/')
class EventListView(Resource):

    def get(self):
        event_dbs = Event.get_dbs()
        return make_response(event_dbs, Event.FIELDS)


    @admin_required
    def post(self):
        parser = self._make_parser(('sport_name', {'required': True}),
                                   ('title', {'required': True}),
                                   ('country', {'required': True}),
                                   ('start_year', {'required': True}))


        args = parser.parse_args()
        event = Event(parent=Sport.sport_key(args.sport_name),
                     title=args.title, country=args.get('country'),
                     start_year=args.get('start_year'))
        event.put()
        return make_response(event, Event.FIELDS)


@events_api.resource('/<int:event_id>/')
class EventView(Resource):

    def get(self, event_id):
        event = Event.get_by_id(event_id)
        return make_response(event, Event.FIELDS)


    @admin_required
    def put(self, event_id):
        parser = self._make_parser(('title', {'required': True}),
                                   ('country', {'required': True}),
                                   ('start_year', {'required': True}))
                                   
        args = parser.parse_args()

        event = Event.get_by_id(event_id)
        event.title = args.title
        event.country = args.country
        event.start_year = args.start_year
        event.put()
        return make_response(event, Event.FIELDS)


    @admin_required
    def delete(self, event_id):
        event = Event.get_by_id(event_id)
        event.key.delete()
