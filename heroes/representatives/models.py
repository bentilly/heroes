from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Rep(Base):
	firstname = ndb.StringProperty(required=True)
	lastname = ndb.StringProperty(required=True)

	@property
	def title(self):
		return self.firstname + " " + self.lastname

	@property
	def link(self):
		return '/rep/{}/'.format(self.key.urlsafe())


	FIELDS = {
		'name': fields.String,
	}
	FIELDS.update(Base.FIELDS)
