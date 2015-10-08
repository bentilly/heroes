from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.representatives.models import Rep

class Squadmember(Base):
	#Parent = SQUAD
	rep = ndb.KeyProperty(kind=Rep, required=True)

	@property
	def title(self):
		return self.rep.get().firstname + " " + self.rep.get().lastname

	@property
	def link(self):
		return '/squadmember/{}/'.format(self.key.urlsafe())

