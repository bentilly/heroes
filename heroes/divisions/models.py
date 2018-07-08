from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.sports.models import Sport

class Division(Base):
	name = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.name

	@property
	def link(self):
		return '/admin/division/{}/'.format(self.key.urlsafe())

