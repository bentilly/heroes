"""Trophies-related data model.
"""

from google.appengine.ext import ndb

from heroes.models import Base, BaseExpando


class Trophy(BaseExpando):
    """Trophy, like Worlds Best Football Team. That trophie can change hands at any point
    depending on how the Football administration is set up.
    """

    """
    BT: a team can also be 2nd or 3rd. The 'owner' would be the last team (country) to place 1st
    """
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    owner = ndb.KeyProperty()


    @property
    def link(self):
        return '/trophy/update/{}/'.format(self.uid)
