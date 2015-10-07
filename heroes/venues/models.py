from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Venue(Base):
	name = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.name

	@property
	def link(self):
		return '/venue/{}/'.format(self.key.urlsafe())


	FIELDS = {
		'name': fields.String,
	}
	FIELDS.update(Base.FIELDS)
