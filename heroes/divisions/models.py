from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.sports.models import Sport

class Division(Base):
	sport = ndb.KeyProperty(kind=Sport) #This could be replaced by NDP "Parent" entity
	name = ndb.StringProperty(required=True)

	#Display text in admin
	def __repr__(self):
		return u'{} : {}'.format(self.sport.get().name, self.name)

	#Admin CRUD
	class Meta():
		def __init__(self):
			from ndbadmin.admin import fields as admin_fields
			self.fields = {
				admin_fields.KeyField('sport', 'Sport', required=True, query=Sport.query()),
				admin_fields.TextField("name", "Division name", required=True),
			}

	FIELDS = {
		'sport': fields.Key,
		'name': fields.String,
	}
	FIELDS.update(Base.FIELDS)
