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

	#reference match teams as a shortcut. optional. ??
	# matchteam1 = ndb.KeyProperty(kind=Matchteam)
	# matchteam2 = ndb.KeyProperty(kind=Matchteam)

	@property
	def datestring(self):
		return self.date.strftime('%d %b %Y')

	@property
	def dateproperty(self):
		return self.date.strftime('%Y-%m-%d')

	@property
	def timeproperty(self):
		return self.date.strftime('%H:%M')

	@property
	def title(self):
		return self.country1.get().code + ' vs ' + self.country2.get().code

	@property
	def link(self):
		return '/match/{}/'.format(self.key.urlsafe())


