from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.squadmembers.models import Squadmember
from heroes.representatives.models import Rep

class Matchteammember(Base):
	# Parent = MATCHTEAM

	# Probably dont need both of these
	squadmember = ndb.KeyProperty(kind=Squadmember, required=True)
	rep = ndb.KeyProperty(kind=Rep, required=True)

	@property
	def title(self):
		return self.name

	@property
	def link(self):
		return '/role/{}/'.format(self.key.urlsafe())
