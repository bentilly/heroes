from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base


class Sport(Base):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    # @classmethod
    # def sport_key(self, sport_name):
    #     return ndb.Key('Sport', sport_name)


    @property
    def link(self):
        return '/sport/{}/'.format(self.key.urlsafe())


    FIELDS = {
        'name': fields.String,
        'description': fields.String,
    }
    FIELDS.update(Base.FIELDS)
