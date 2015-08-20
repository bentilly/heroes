from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.sports.models import Sport
from heroes.countries.models import Country

class Team(Base):
    sport = ndb.KeyProperty(kind=Sport)
    name = ndb.StringProperty(required=False)
    country = ndb.KeyProperty(kind=Country, required=True)
    division_name = ndb.StringProperty(required=True)
    @property
    def event(self):
        return Event.query().filter(Event.teams == self.key)

    def __repr__(self):
        return u'{}: {}: {}'.format(self.name,
                                    self.country.get().code if self.country else 'None',
                                    self.division_name)

    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("name", "Name", required=False),
                admin_fields.KeyField('sport', 'Sport', required=True, query=Sport.query()),
                admin_fields.KeyField('country', 'Country', required=True, query=Country.query()),
                admin_fields.TextField("division_name", "Division", required=True),
            ]

    FIELDS = {
        'name': fields.String,
        'sport': fields.Key,
        'country': fields.Key,
        'division_name': fields.String,
    }
    FIELDS.update(Base.FIELDS)
