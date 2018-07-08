from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

import logging

class Event(Base):
	name = ndb.StringProperty(required=True)
	startdate = ndb.DateProperty(required=True)
	# hostCity should be replaced by VENUE
	hostCity = ndb.StringProperty(required=False)

	@property
	def startdatestring(self):
		return str(self.startdate)

	@property
	def title(self):
		return str(self.startdate.year) + " " + self.name

	@property
	def link(self):
		return '/admin/event/{}/'.format(self.key.urlsafe())

