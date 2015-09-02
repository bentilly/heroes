from google.appengine.ext import ndb

from heroes.models import Base
from heroes.teams.models import Team
from heroes.events.models import Event


REPR_ROLES = ['Player', 'Captain', 'Coach']


class Representative(Base):
    name = ndb.StringProperty(required=True)
    role = ndb.StringProperty(required=True, choices=REPR_ROLES)
    team_event_repr = ndb.KeyProperty(kind='TeamEventRepresentative', repeated=True)


    def __repr__(self):
        return u'{}: {}'.format(self.name, self.role)


    @property
    def link(self):
        return '/representatives/{}/'.format(self.key.urlsafe())


    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("name", "Name", required=False),
                admin_fields.KeyField('teams', "Team", required=True, query=Team.query()),
                admin_fields.KeyField("events", "Event", required=True, query=Event.query()),
                admin_fields.ChoiceField("role", "Role", initial=REPR_ROLES,
                                        query=REPR_ROLES)
            ]


class TeamEventRepresentative(Base):
    """Group of team represenatives for certain event.
    """

    representatives = ndb.KeyProperty(kind=Representative, repeated=True)
    event = ndb.KeyProperty(kind=Event)
    team = ndb.KeyProperty(kind=Team)


    def __repr__(self):
        return u'{}: {}'.format(self.event.get().title, self.team.get().name)


    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            reprs = Representative.query()
            self.fields = [
                admin_fields.KeyField('team', "Team", required=True, query=Team.query()),
                admin_fields.KeyField("event", "Event", required=True, query=Event.query()),
                admin_fields.CheckboxListField('representatives', 'Represenatives',
                                         initial=[], query=reprs),
            ]
