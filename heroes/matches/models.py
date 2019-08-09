from google.appengine.ext import ndb
import datetime
import pytz

from heroes import fields
from heroes.models import Base
from heroes.venues.models import Venue
from heroes.divisions.models import Division
from heroes.countries.models import Country


class Match(Base):
	#PARENT is EVENT
	date = ndb.DateTimeProperty(required=True) #UTC
	venue = ndb.KeyProperty(kind=Venue, required=True)
	division = ndb.KeyProperty(kind=Division, required=True)
	country1 = ndb.KeyProperty(kind=Country, required=True)
	country1score = ndb.IntegerProperty()
	country2 = ndb.KeyProperty(kind=Country, required=True)
	country2score = ndb.IntegerProperty()

	#reference match teams as a shortcut. optional. ??
	# matchteam1 = ndb.KeyProperty(kind=Matchteam)
	# matchteam2 = ndb.KeyProperty(kind=Matchteam)

	#----------------------------
	# UTC date / times not that usefull for UX
	@property
	def datestring(self):
		return self.date.strftime('%d %b %Y')

	@property
	def dateproperty(self):
		return self.date.strftime('%Y-%m-%d')

	@property
	def timeproperty(self):
		return self.date.strftime('%H:%M')
	#----------------------------

	#----------------------------
	# local date / times
	@property
	def datestring_local(self):
		tz_utc = pytz.timezone("UTC")
		matchdate_utc = tz_utc.localize(self.date)
		tz_local = pytz.timezone(self.venue.get().timezone)
		matchdate_local = matchdate_utc.astimezone(tz_local)

		return matchdate_local.strftime('%d %b %Y')

	@property
	def dateproperty_local(self):
		tz_utc = pytz.timezone("UTC")
		matchdate_utc = tz_utc.localize(self.date)
		tz_local = pytz.timezone(self.venue.get().timezone)
		matchdate_local = matchdate_utc.astimezone(tz_local)

		return matchdate_local.strftime('%Y-%m-%d')

	@property
	def timeproperty_local(self):
		tz_utc = pytz.timezone("UTC")
		matchdate_utc = tz_utc.localize(self.date)
		tz_local = pytz.timezone(self.venue.get().timezone)
		matchdate_local = matchdate_utc.astimezone(tz_local)

		return matchdate_local.strftime('%H:%M')

	#----------------------------


	@property
	def title(self):
		return self.country1.get().code + ' vs ' + self.country2.get().code

	@property
	def link(self):
		return '/admin/match/{}/'.format(self.key.urlsafe())


	# @property
	# def dateAsQuebec(self):
	# 	tz_utc = pytz.timezone("UTC")
	# 	matchdate_utc = tz_utc.localize(self.date)
	# 	matchdate_quebec = matchdate_utc.astimezone(pytz.timezone("Canada/Eastern"))
	# 	return matchdate_quebec.strftime('%Y-%m-%d')

	# @property
	# def timeAsQuebec(self):
	# 	tz_utc = pytz.timezone("UTC")
	# 	matchdate_utc = tz_utc.localize(self.date)
	# 	matchdate_quebec = matchdate_utc.astimezone(pytz.timezone("Canada/Eastern"))
	# 	return matchdate_quebec.strftime('%H:%M')


	


