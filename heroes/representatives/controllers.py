from flask import Blueprint, session, jsonify, render_template

from google.appengine.ext.ndb import Key

from heroes.helpers import Api, Resource, make_response, admin_required

from heroes.events.models import Event

from .models import Representative, ReprSquadState, Squad

representatives_bp = Blueprint('representatives', __name__)


@representatives_bp.route('/<event>/<team>/')
def represenatives_list(event, team):
    # get Event's Squad
    event = Key(urlsafe=event)
    team = Key(urlsafe=team)
    squad = Squad.query(Squad.event==event).fetch()

    # filter ReprSquadState by team
    repr_squad_states = ReprSquadState.query(ReprSquadState.team==team).fetch()

    return render_template('table.html',
        root_item=team.get(),
        items=repr_squad_states,
        table_headers=['Start year', 'Title', 'Venue country'],
        fields=['start_year', 'title', 'country_name'])
