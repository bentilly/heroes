from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.divisions.models import Division
# from heroes.countries.models import Country

class Team(Base):
    name = ndb.StringProperty(required=False)
    # country = ndb.KeyProperty(kind=Country, required=True)
    # COUNTRY IS PARENT
    division = ndb.KeyProperty(kind=Division, required=True)

    @property
    def title(self):
        return self.key.parent().get().code + " " + self.division.get().name


    @property
    def link(self):
        return '/admin/team/{}/'.format(self.key.urlsafe())

