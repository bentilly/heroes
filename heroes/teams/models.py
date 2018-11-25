from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.divisions.models import Division
# from heroes.countries.models import Country

class Team(Base):
    name = ndb.StringProperty(required=False)
    # COUNTRY IS PARENT
    division = ndb.KeyProperty(kind=Division, required=True)
    showOnHomePage = ndb.BooleanProperty(default=False)

    @property
    def title(self):
        return self.key.parent().get().code + " " + self.division.get().name


    @property
    def link(self):
        return '/admin/team/{}/'.format(self.key.urlsafe())

    @property
    def publiclink(self):
        return '/team/{}/'.format(self.key.urlsafe())

