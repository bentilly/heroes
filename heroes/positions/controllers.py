from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb

from .models import Position
from heroes.sports.models import Sport

position_bp = Blueprint('position', __name__)

# RENDERING #

# A position PAGE.
@position_bp.route('/<key>/')
def position_view(key):
	position_key = ndb.Key(urlsafe=key)
	position = position_key.get()

	#BREADCRUMB
	# sport
	sport = position_key.parent().parent().get()
	# Country
	country = position_key.parent().get()

	breadcrumb_list = [sport, country]
	title = position.title
	#END BREADCRUMB

	return render_template('position.html',
		breadcrumb = breadcrumb_list,
		object_title=title,
		position_object=position,
	)

#NEW position PAGE
@position_bp.route('/new/<key>')
def new_position(key):
	country_key = ndb.Key(urlsafe=key)
	country = country_key.get()

	sport = country_key.parent().get()

	breadcrumb_list = [sport, country]

	return render_template('position.html',
		breadcrumb = breadcrumb_list,
		object_title='New position',
		country_object=country,
	)



# HANDLERS #

# ADD position
@position_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
	country_key = ndb.Key(urlsafe=parent_key)

	position = Position(name=request.form['positionName'], parent=country_key)
	position.put()

	return redirect('/admin/position/{}'.format(position.key.urlsafe()))


# UPDATE position
@position_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    position_key = ndb.Key(urlsafe=key)
    position = position_key.get()
    position.name = request.form['positionName']
    position.put()

    return redirect('/admin/position/{}'.format(position.key.urlsafe()))











