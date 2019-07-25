from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
import logging

from heroes.templates.models import Template


template_bp = Blueprint('template', __name__)

# CRUD ========================= #

# CREATE A TEMPLATE.
@template_bp.route('/create/<label>/<parent_key>/')
def template_create(label, parent_key):
	par_key = ndb.Key(urlsafe=parent_key)
	content = "<html><body><p>Add template html</p></body></html>"

	template = Template(label=label, content=content, parent=par_key)
	template.put()

	# ancestors for menu
	p = template.key.parent().get()
	if p.key.kind() == "Sport":
		sport = p
		country = None

	else:
		country = p
		sport = p.key.parent().get()
		# Loose....Should to better

	return render_template('/admin/template.html',
		template = template,
		country=country,
		sport=sport,
	)

# READ A TEMPLATE.
@template_bp.route('/<key>/')
def template_view(key):
	temp_key = ndb.Key(urlsafe=key)
	template = temp_key.get()

	# ancestors
	p = temp_key.parent().get()

	if p.key.kind() == "Sport":
		sport = p
		country = None

	else:
		country = p
		sport = p.key.parent().get()
		# Loose....Should to better

	return render_template('/admin/template.html',
		template=template,
		country=country,
		sport=sport,
	)


# UPDATE A TEMPLATE.
@template_bp.route('/save/<key>', methods=['POST'])
def template_save(key):
	temp_key = ndb.Key(urlsafe=key)
	template = temp_key.get()

	template.content = request.form['code']
	template.put()

	return redirect('/admin/template/{}'.format(temp_key.urlsafe()))


# DELETE A TEMPLATE.
@template_bp.route('/delete/<key>/')
def template_delete(key):
	temp_key = ndb.Key(urlsafe=key)
	temp_key.delete()

	message = 'Template deleted'

	return render_template('/admin/message.html',
		message=message,
	)
