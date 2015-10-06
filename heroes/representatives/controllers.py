from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Rep
from heroes.sports.models import Sport

rep_bp = Blueprint('rep', __name__)

# RENDERING #

# A REP PAGE.
@rep_bp.route('/<key>/')
def rep_view(key):
    rep_key = ndb.Key(urlsafe=key)
    rep = rep_key.get()

    country = rep_key.parent().get()

    return render_template('rep.html',
            object_title=rep.title,
            rep_object=rep,
            country_object=country,
        )

#NEW rep PAGE
@rep_bp.route('/new/<key>')
def new_rep(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()


	return render_template('rep.html',
		object_title='New rep',
		country_object=country,
		)



# HANDLERS #

# ADD rep
@rep_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	country_key = ndb.Key(urlsafe=parent_key)
	country = country_key.get()

	rep = Rep(firstname=request.form['firstname'], lastname=request.form['lastname'], parent=country_key)
	rep.put()

	return redirect('/rep/{}'.format(rep.key.urlsafe()))


# UPDATE rep
@rep_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    rep_key = ndb.Key(urlsafe=key)
    rep = rep_key.get()
    rep.firstname = request.form['firstname']
    rep.lastname = request.form['lastname']
    rep.put()

    return redirect('/rep/{}'.format(rep.key.urlsafe()))











