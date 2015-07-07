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
 		

class MainPage(webapp2.RequestHandler):
	def get(self):
		sports_query = Sport.query()
		sports = sports_query.fetch(100)

		template_values = {
			'sports': sports,
			}

		template = JINJA_ENVIRONMENT.get_template('/templates/allSports.html')
		self.response.write(template.render(template_values))

		
		
app = webapp2.WSGIApplication([
	('/', MainPage),

], debug=True)





