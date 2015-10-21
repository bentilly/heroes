from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Role(Base):
	name = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.name

	@property
	def link(self):
		return '/admin/role/{}/'.format(self.key.urlsafe())

