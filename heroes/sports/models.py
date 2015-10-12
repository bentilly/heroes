from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base


class Sport(Base):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    @property
    def title(self):
        return self.name

    @property
    def link(self):
        return '/sport/{}/'.format(self.key.urlsafe())

    @property
    def publiclink(self):
        return '/public/sport/{}/'.format(self.key.urlsafe())
