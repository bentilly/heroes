from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base


class Sport(Base):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    code = ndb.StringProperty(required=True) #short name to use in URLs TODO: work out how to update database
    published = ndb.BooleanProperty(default=False) #whether to show on the website or not

    @property
    def title(self):
        return self.name

    @property
    def link(self):
        return '/admin/sport/{}/'.format(self.key.urlsafe())

    @property
    def publiclink(self):
        return '/sport/{}/'.format(self.key.urlsafe())
