from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.squads.models import Squad
from heroes.matches.models import Match


class Matchteam(Base):
	#has no parent. Needs to link MATCH to SQUAD
	match = ndb.KeyProperty(kind=Match, required=True)
	squad = ndb.KeyProperty(kind=Squad, required=True)

	@property
	def title(self):
		return self.match.get().country1.get().code + 'vs' + self.match.get().country2.get().code

	@property
	def link(self):
		return '/matchteam/{}/'.format(self.key.urlsafe())

