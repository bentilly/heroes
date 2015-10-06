from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.venues.models import Venue
from heroes.divisions.models import Division
from heroes.countries.models import Country


class Match(Base):
	#PARENT is EVENT
	date = ndb.DateTimeProperty(required=True)
	venue = ndb.KeyProperty(kind=Venue, required=True)
	division = ndb.KeyProperty(kind=Division, required=True)
	country1 = ndb.KeyProperty(kind=Country, required=True)
	country1score = ndb.IntegerProperty()
	country2 = ndb.KeyProperty(kind=Country, required=True)
	country2score = ndb.IntegerProperty()

	@property
	def link(self):
		return '/match/{}/'.format(self.key.urlsafe())


	# FIELDS = {
	# 	'name': fields.String,
	# }
	# FIELDS.update(Base.FIELDS)
