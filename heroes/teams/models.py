from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.sports.models import Sport

class Team(Base):
    sport = ndb.KeyProperty(kind=Sport)
    name = ndb.StringProperty(required=False)
    country_name = ndb.StringProperty(required=True)
    division_name = ndb.StringProperty(required=True)


    def __repr__(self):
        return u'{}: {}: {}'.format(self.name, self.country_name, self.division_name)

    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("name", "Name", required=False),
                admin_fields.KeyField('sport', 'Sport', required=True, query=Sport.query()),
                admin_fields.TextField("country_name", "Country", required=True),
                admin_fields.TextField("division_name", "Division", required=True),
            ]

    FIELDS = {
        'name': fields.String,
        'country_name': fields.String,
        'division_name': fields.String,
    }
    FIELDS.update(Base.FIELDS)
