from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.events.models import Event

class Squad(Base):
    # TEAM IS PARENT
    event = ndb.KeyProperty(kind=Event, required=True)

    @property
    def publictitle(self):
        return 'a squad title'

    # EVENT stuff
    @property
    def title(self):
        return self.event.get().title

    @property
    def eventHost(self):
        return self.event.get().hostCity
    

    @property
    def link(self):
        return '/admin/squad/{}/'.format(self.key.urlsafe())

    @property
    def eventdate(self):
        return self.event.get().startdate

    @property
    def teamName(self):
        return self.key.parent().get().title
    

