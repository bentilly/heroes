from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

import logging

class Event(Base):
	name = ndb.StringProperty(required=True)
	startdate = ndb.DateProperty(required=True)

	@property
	def startdatestring(self):
		return str(self.startdate)

	@property
	def title(self):
		return str(self.startdate.year) + " " + self.name

	@property
	def link(self):
		return '/event/{}/'.format(self.key.urlsafe())

