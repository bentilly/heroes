from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Matchteammember
from heroes.sports.models import Sport

matchteammember_bp = Blueprint('matchteammember', __name__)

# RENDERING #

# A matchteammember PAGE.
#---Dont neeed yet
# @matchteammember_bp.route('/<key>/')
# def matchteammember_view(key):
#     matchteammember_key = ndb.Key(urlsafe=key)
#     matchteammember = matchteammember_key.get()
#     return render_template('matchteammember.html',
#             object_title=matchteammember.name,
#             matchteammember_object=matchteammember,
#         )

#NEW matchteammember PAGE
# @matchteammember_bp.route('/new/<key>')
#---Dont neeed yet
# def new_matchteammember(key):
# 	sport_key = ndb.Key(urlsafe=key)
# 	sport = sport_key.get()


# 	return render_template('matchteammember.html',
# 		object_title='New matchteammember',
# 		sport_object=sport,
# 		)



# HANDLERS #

# ADD matchteammember
@matchteammember_bp.route('/add/<squadmember_key>/<matchteam_key>', methods=['GET']) #Is GET ok here?
def add_entry(squadmember_key, matchteam_key):
	squadmember_key = ndb.Key(urlsafe=squadmember_key)
	matchteam_key = ndb.Key(urlsafe=matchteam_key)
	rep_key = squadmember_key.get().rep

	matchteammember = Matchteammember(parent=matchteam_key, squadmember=squadmember_key, rep=rep_key)
	matchteammember.put()

	return redirect('/matchteam/{}'.format(matchteam_key.urlsafe()))


# UPDATE matchteammember
#---Dont neeed yet
# @matchteammember_bp.route('/update/<key>', methods=['POST'])
# def update_entry(key):
#     matchteammember_key = ndb.Key(urlsafe=key)
#     matchteammember = matchteammember_key.get()
#     matchteammember.name = request.form['matchteammemberName']
#     matchteammember.put()

#     return redirect('/matchteammember/{}'.format(matchteammember.key.urlsafe()))











