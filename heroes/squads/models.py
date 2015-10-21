from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.events.models import Event

class Squad(Base):
    # TEAM IS PARENT
    event = ndb.KeyProperty(kind=Event, required=True)

    @property
    def title(self):
        return self.event.get().title

    @property
    def link(self):
        return '/admin/squad/{}/'.format(self.key.urlsafe())

