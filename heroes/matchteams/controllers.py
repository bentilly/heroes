from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Matchteam
from heroes.sports.models import Sport
from heroes.matches.models import Match
from heroes.squadmembers.models import Squadmember
from heroes.matchteammembers.models import Matchteammember

matchteam_bp = Blueprint('matchteam', __name__)

# RENDERING #

# A matchteam PAGE.
@matchteam_bp.route('/<key>/')
def matchteam_view(key):
    matchteam_key = ndb.Key(urlsafe=key)
    matchteam = matchteam_key.get()

    #BREADCRUMB
    # squad
    squad = matchteam.squad.get()
    #team
    team = squad.key.parent().get()
    # country
    country = squad.key.parent().parent().get()
    # sport
    sport = squad.key.parent().parent().parent().get()

    breadcrumb_list = [sport, country, team, squad]
    title = matchteam.match.get().title
    #END BREADCRUMB

    #SQUADMEMBERS
    squadmembers_entries = Squadmember.query(ancestor=squad.key).fetch()

    #MATCHTEAMMEMBERS
    matchteammembers_entries = Matchteammember.query(ancestor=matchteam_key).fetch()


    #Squad_Match_members
    squad_matchteam_members = []

    for sm in squadmembers_entries:
        squad_matchteam_member = {}
        squad_matchteam_member['squadmember'] = sm

        for mtm in matchteammembers_entries:
            if mtm.rep == sm.rep:
                squad_matchteam_member['matchteammember'] = mtm

        squad_matchteam_members.append(squad_matchteam_member)

    return render_template('/admin/matchteam.html',
            breadcrumb = breadcrumb_list,
            object_title=title,
            matchteam_object=matchteam,
            squad_matchteam=squad_matchteam_members
            
        )

#NEW matchteam PAGE - create from SQUAD page
# @matchteam_bp.route('/new/<matchkey>/<squadkey>')
# def new_matchteam(key):
# 	match_key = ndb.Key(urlsafe=matchkey)
# 	match = match_key.get()
# 	squad_key = ndb.Key(urlsafe=squadkey)
# 	squad = squad_key.get()

# 	return render_template('matchteam.html',
# 		object_title='New Match Team',
# 		parent_object=squad,
# 		matches=match_entries,
# 		)



# HANDLERS #

# ADD matchteam
@matchteam_bp.route('/add/<match_key>/<squad_key>', methods=['GET']) #IS THIS OK (GET)??
def add_entry(match_key, squad_key):
	match_key = ndb.Key(urlsafe=match_key)
	squad_key = ndb.Key(urlsafe=squad_key)

	matchteam = Matchteam(squad=squad_key, match=match_key)
	matchteam.put()

	return redirect('/admin/matchteam/{}'.format(matchteam.key.urlsafe()))


# UPDATE matchteam
# not doing this either (yet)
# @matchteam_bp.route('/update/<key>', methods=['POST'])
# def update_entry(key):
#     matchteam_key = ndb.Key(urlsafe=key)
#     matchteam = Matchteam_key.get()
#     matchteam.name = request.form['matchteamName']
#     matchteam.put()

#     return redirect('/matchteam/{}'.format(matchteam.key.urlsafe()))











