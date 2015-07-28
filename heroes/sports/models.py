from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base


class Sport(Base):
    name = ndb.StringProperty(required=True)

    FIELDS = {
        'name': fields.String,
    }

    FIELDS.update(Base.FIELDS)
