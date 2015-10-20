"""Trophies-related data model.
"""

from google.appengine.ext import ndb

from heroes.models import Base

class Trophie(Base):
    """Trophie, like Worlds Best Football Team. That trophie can change hands at any point
    depending on how the Football administration is set up.
    """

    """
    BT: a team can also be 2nd or 3rd. The 'owner' would be the last team (country) to place 1st
    """
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    owner_changed = ndb.DateProperty(auto_now=True)
    owner = ndb.KeyProperty()
