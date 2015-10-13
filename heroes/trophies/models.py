"""Trophies-related data model.
"""

from google.appengine.ext import ndb

from heroes.models import Base, BaseExpando

class Trophie(BaseExpando):
    """Trophie, like Worlds Best Football Team. That trophie can change hands at any point
    depending on how the Football administration is set up.
    """
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    owner_changed = ndb.DateProperty(auto_now=True)
    owner = ndb.KeyProperty()
