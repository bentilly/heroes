from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base


class Sport(Base):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    @classmethod
    def sport_key(self, sport_name):
        return ndb.Key('Sport', sport_name)

    def __repr__(self):
        return u'{}: {}'.format(self.name, self.description)

    @property
    def link(self):
        return '/sports/{}/'.format(self.key.urlsafe())

    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("name", "Name", required=True),
                admin_fields.BigTextField("description", "Description"),
            ]

    FIELDS = {
        'name': fields.String,
        'description': fields.String,
    }
    FIELDS.update(Base.FIELDS)
