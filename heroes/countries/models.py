from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base

class Country(Base):
	name = ndb.StringProperty(required=True)
	#three letter country code
	code = ndb.StringProperty(required=True)

	#Display text in admin
	def __repr__(self):
		return u'{} - {}'.format(self.name, self.code)

	#Admin CRUD
	class Meta():
		def __init__(self):
			from ndbadmin.admin import fields as admin_fields
			self.fields = [
				admin_fields.TextField("name", "Name", required=True),
				admin_fields.TextField("code", "Code (3 letters)", required=True),
			]

	FIELDS = {
		'name': fields.String,
		'code': fields.String,
	}
	FIELDS.update(Base.FIELDS)