from google.appengine.ext import ndb

from heroes.models import Base
from heroes.teams.models import Team
from heroes.events.models import Event


REPR_ROLES = ['Player', 'Captain', 'Coach']


class Representative(Base):
    name = ndb.StringProperty(required=True)


    def __repr__(self):
        return u'{}'.format(self.name)


    @property
    def link(self):
        return '/representatives/{}/'.format(self.key.urlsafe())


    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("name", "Name", required=False),
            ]


class ReprSquadState(Base):
    """Represenative role and other data for certain event.
    """
    representative = ndb.KeyProperty(kind=Representative)
    role = ndb.StringProperty(required=True, choices=REPR_ROLES)
    team = ndb.KeyProperty(kind=Team)


    def __repr__(self):
        return u'{}: {} {}'.format(self.representative.get().name, self.role, self.team.get().name)


    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.KeyField('representative', "Representaive", required=True,
                                      query=Representative.query()),
                admin_fields.KeyField('team', 'Team', required=True, query=Team.query()),
                admin_fields.ChoiceField('role', 'Role', initial=REPR_ROLES, query=REPR_ROLES)
            ]


class Squad(Base):
    """Group of team represenatives for certain event.
    """

    representatives = ndb.KeyProperty(kind=ReprSquadState, repeated=True)
    event = ndb.KeyProperty(kind=Event)


    @property
    def link(self):
        return '/squads/{}/'.format(self.key.urlsafe())


    def __repr__(self):
        return u'{}'.format(self.event.get().title)


    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            reprs = ReprSquadState.query()
            self.fields = [
                admin_fields.KeyField('event', 'Event', required=True, query=Event.query()),
                admin_fields.CheckboxListField('representatives', 'Represenatives',
                                         initial=[], query=reprs),
            ]
