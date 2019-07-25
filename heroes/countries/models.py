from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.templates.models import Template

class Country(Base):
	#Parent = Sport
	name = ndb.StringProperty(required=True)
	code = ndb.StringProperty(required=True)	#three letter country code
	flagemoji = ndb.StringProperty(required=False)
	published = ndb.BooleanProperty(default=False)	#whether to show on the website or not
	external_url = ndb.StringProperty()	#If this sport+country has an external home page url, eg: uwhhereos.co.nz (UWH in New Zealand home page)

	@property
	def title(self):
		return self.code

	@property
	def link(self):
		return '/admin/country/{}/'.format(self.key.urlsafe())

	@property
	def publiclink(self):
		return '/country/{}/'.format(self.key.urlsafe())
