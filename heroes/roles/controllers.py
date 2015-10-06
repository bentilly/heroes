from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Role
from heroes.sports.models import Sport

role_bp = Blueprint('role', __name__)

# RENDERING #

# A ROLE PAGE.
@role_bp.route('/<key>/')
def role_view(key):
    role_key = ndb.Key(urlsafe=key)
    role = role_key.get()
    return render_template('role.html',
            object_title=role.name,
            role_object=role,
        )

#NEW ROLE PAGE
@role_bp.route('/new/<key>')
def new_role(key):
	sport_key = ndb.Key(urlsafe=key)
	sport = sport_key.get()


	return render_template('role.html',
		object_title='New role',
		sport_object=sport,
		)



# HANDLERS #

# ADD ROLE
@role_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	sport_key = ndb.Key(urlsafe=parent_key)
	sport = sport_key.get()

	role = Role(name=request.form['roleName'], parent=sport_key)
	role.put()

	return redirect('/role/{}'.format(role.key.urlsafe()))


# UPDATE ROLE
@role_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    role_key = ndb.Key(urlsafe=key)
    role = role_key.get()
    role.name = request.form['roleName']
    role.put()

    return redirect('/role/{}'.format(role.key.urlsafe()))











