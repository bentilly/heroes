from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Country(Base):
	name = ndb.StringProperty(required=True)
	#three letter country code
	code = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.code

	@property
	def link(self):
	    return '/country/{}/'.format(self.key.urlsafe())
	    

	FIELDS = {
		'name': fields.String,
		'code': fields.String,
	}
	FIELDS.update(Base.FIELDS)