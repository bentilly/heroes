from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.sports.models import Sport

class Division(Base):
	name = ndb.StringProperty(required=True)

	@property
	def link(self):
		return '/division/{}/'.format(self.key.urlsafe())


	FIELDS = {
		'name': fields.String,
	}
	FIELDS.update(Base.FIELDS)
