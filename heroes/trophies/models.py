"""Trophies-related data model.
"""

from google.appengine.ext import ndb

from heroes.models import Base, BaseExpando


class Trophy(BaseExpando):
    """Trophy, like Worlds Best Football Team. That trophie can change hands at any point
    depending on how the Football administration is set up.
    """
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    owner = ndb.KeyProperty()
