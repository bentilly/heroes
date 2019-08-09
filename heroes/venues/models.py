from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Venue(Base):
	name = ndb.StringProperty(required=True)
	timezone = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.name

	@property
	def link(self):
		return '/admin/venue/{}/'.format(self.key.urlsafe())

