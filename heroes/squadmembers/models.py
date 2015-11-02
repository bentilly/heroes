from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.representatives.models import Rep
from heroes.roles.models import Role
from heroes.positions.models import Position

class Squadmember(Base):
    #Parent = SQUAD
    rep = ndb.KeyProperty(kind=Rep, required=True)
    role = ndb.KeyProperty(kind=Role)
    position = ndb.KeyProperty(kind=Position)

    photo = ndb.BlobProperty()

    @property
    def title(self):
        return self.rep.get().firstname + " " + self.rep.get().lastname


    @property
    def link(self):
        return '/admin/squadmember/{}/'.format(self.key.urlsafe())
