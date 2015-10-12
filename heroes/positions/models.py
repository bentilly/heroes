from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Position(Base):
	#PARENT = COUNTRY
	name = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.name

	@property
	def link(self):
		return '/position/{}/'.format(self.key.urlsafe())

