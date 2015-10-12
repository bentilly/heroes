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

	#BREADCRUMB
	# sport
	sport = role_key.parent().parent().get()
	# Country
	country = role_key.parent().get()

	breadcrumb_list = [sport, country]
	title = role.title
	#END BREADCRUMB

	return render_template('role.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		role_object=role,
	)

#NEW ROLE PAGE
@role_bp.route('/new/<key>')
def new_role(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()

	sport = country_key.parent().get()

	breadcrumb_list = [sport, country]

	return render_template('role.html',
		breadcrumb = breadcrumb_list,
		object_title='New role',
		country_object=country,
	)



# HANDLERS #

# ADD ROLE
@role_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	country_key = ndb.Key(urlsafe=parent_key)

	role = Role(name=request.form['roleName'], parent=country_key)
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











