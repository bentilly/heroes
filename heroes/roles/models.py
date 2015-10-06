from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Role(Base):
	name = ndb.StringProperty(required=True)

	@property
	def link(self):
		return '/role/{}/'.format(self.key.urlsafe())


	FIELDS = {
		'name': fields.String,
	}
	FIELDS.update(Base.FIELDS)
