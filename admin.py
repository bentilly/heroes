import os
import urllib

from heroesData import *

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class AdminPage(webapp2.RequestHandler):
	def get(self):
		sports_query = Sport.query()
		sports = sports_query.fetch(100)

		template_values = {
			'sports': sports,
			}

		template = JINJA_ENVIRONMENT.get_template('/templates/admin/admin.html')
		self.response.write(template.render(template_values))


class SportPage(webapp2.RequestHandler):
	def get(self):

		if self.request.get('sport_keystring'):
			sport_key = ndb.Key(urlsafe=self.request.get('sport_keystring'))
			sport = sport_key.get()

			template_values = {
			'sport': sport,
			}

			template = JINJA_ENVIRONMENT.get_template('/templates/admin/sportPage.html')
			self.response.write(template.render(template_values))

		else:
			template = JINJA_ENVIRONMENT.get_template('/templates/admin/sportPage.html')
			self.response.write(template.render())



class UpdateSport(webapp2.RequestHandler):
	def post(self):

		if self.request.get('sport_keystring'):
			sport_key = ndb.Key(urlsafe=self.request.get('sport_keystring'))
			sport = sport_key.get()

		else: 
			sport = Sport()

		sport.title = self.request.get('sport_title')
		sport.description = self.request.get('sport_description')
		sport.put();

		template_values = {
		'title': sport.title,
		'body': sport.description
		}

		template = JINJA_ENVIRONMENT.get_template('/templates/admin/responsePage.html')
		self.response.write(template.render(template_values))
		

class DeleteSport(webapp2.RequestHandler):
	def get(self):
		sport_key = ndb.Key(urlsafe=self.request.get('sport_keystring'))
		sport = sport_key.get()

		template_values = {
		'title': "BOOM!     " + sport.title + "    deleted",
		'body': "I hope you wanted to do that"
		}

		sport.key.delete()

		template = JINJA_ENVIRONMENT.get_template('/templates/admin/responsePage.html')
		self.response.write(template.render(template_values))





app = webapp2.WSGIApplication([
	('/admin', AdminPage),
	('/admin/sportPage', SportPage),
	('/admin/updateSport', UpdateSport),
	('/admin/deleteSport', DeleteSport),

], debug=True)






