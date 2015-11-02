import logging

from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb


from heroes.positions.models import Position
from heroes.representatives.models import Rep
from heroes.roles.models import Role

from .models import Squadmember

squadmember_bp = Blueprint('squadmember', __name__)


@squadmember_bp.route('/<key>/')
def squadmember_view(key):
    """A squadmember PAGE."""
    squadmember_key = ndb.Key(urlsafe=key)
    squadmember = squadmember_key.get()

    #BREADCRUMB
    squad = squadmember_key.parent().get()
    team = squad.key.parent().get()
    country = squad.key.parent().parent().get()
    sport = squad.key.parent().parent().parent().get()

    breadcrumb_list = [sport, country, team, squad]
    title = squadmember.title
    #END BREADCRUMB

    role_entries = Role.query(ancestor=country.key).fetch()
    position_entries = Position.query(ancestor=country.key).fetch()

    return render_template('squadmember.html',
        breadcrumb = breadcrumb_list,
        object_title=title,
        squadmember_object=squadmember,
        squad_object=squad,
        roles=role_entries,
        positions=position_entries,
    )

#NEW squadmember PAGE
#---- not doing this yet
# @squadmember_bp.route('/new/<key>')
# def new_squadmember(key):
#   squad_key = ndb.Key(urlsafe=key)
#   squad = squad_key.get()

#   # COUNTRY > TEAM > SQUAD = 2 x parent
#   rep_entries = Rep.query(ancestor=squad_key.parent().parent()).fetch()

#   #BREADCRUMB
#   # squad - above
#   #team
#   team = squad.key.parent().get()
#   # country
#   country = squad.key.parent().parent().get()
#   # sport
#   sport = squad.key.parent().parent().parent().get()

#   breadcrumb_list = [sport, country, team, squad]
#   #END BREADCRUMB


#   return render_template('squadmember.html',
#       object_title='Add squad members',
#       squad_object=squad,
#       reps = rep_entries,
#   )



# HANDLERS #

# ADD squadmember
@squadmember_bp.route('/add/<squad_key>/<rep_key>', methods=['GET'])
def add_entry(squad_key, rep_key):
    squad_key = ndb.Key(urlsafe=squad_key)
    rep_key = ndb.Key(urlsafe=rep_key)

    squadmember = Squadmember(rep=rep_key, parent=squad_key)
    squadmember.put()

    return redirect('/admin/squad/{}'.format(squad_key.urlsafe()))


# UPDATE squadmember
@squadmember_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):

    squadmember_key = ndb.Key(urlsafe=key)
    squadmember = squadmember_key.get()

    if request.form['roleinput']:
        role_key = ndb.Key(urlsafe=request.form['roleinput'])
        squadmember.role = role_key

    if request.form['positioninput']:
        position_key = ndb.Key(urlsafe=request.form['positioninput'])
        squadmember.position = position_key


    squadmember.put()
    photo = request.files.get('photo')
    if photo:
        pass

    return redirect('/admin/squadmember/{}'.format(squadmember.key.urlsafe()))
