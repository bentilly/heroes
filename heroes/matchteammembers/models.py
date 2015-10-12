from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.squadmembers.models import Squadmember
from heroes.representatives.models import Rep
from heroes.roles.models import Role
from heroes.positions.models import Position

class Matchteammember(Base):
	# Parent = MATCHTEAM

	# Probably dont need both of these
	squadmember = ndb.KeyProperty(kind=Squadmember, required=True)
	rep = ndb.KeyProperty(kind=Rep, required=True)
	role = ndb.KeyProperty(kind=Role)
	position = ndb.KeyProperty(kind=Position)

	@property
	def title(self):
		return self.rep.get().firstname+" "+self.rep.get().lastname

	@property
	def link(self):
		return '/matchteammember/{}/'.format(self.key.urlsafe())
