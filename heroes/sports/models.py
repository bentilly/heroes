from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base


class Sport(Base):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()

    FIELDS = {
        'name': fields.String,
        'description': fields.String,
    }
    FIELDS.update(Base.FIELDS)
