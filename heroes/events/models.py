from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.sports.models import Sport
from heroes.teams.models import Team
from heroes.countries.models import Country


class Event(Base):
    sport = ndb.KeyProperty(kind=Sport)
    title = ndb.StringProperty(required=True)
    country = ndb.KeyProperty(kind=Country, required=False)
    start_year = ndb.StringProperty(required=True)
    teams = ndb.KeyProperty(kind="Team", repeated=True)

    def __init__(self, *args, **kw):
        super(Event, self).__init__(*args, **kw)
        self.__link = ''


    def add_team(self, team):
        self.teams.append(team.key)
        self.put()

    def __repr__(self):
        return u'{}: {}: {}'.format(self.title,
                                    self.country_name,
                                    self.start_year)

    @property
    def country_name(self):
        name = ''
        if self.country:
            name = self.country.get().name
        return name


    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, value):
        self.__link = value

    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("title", "Title", required=False),
                admin_fields.KeyField('sport', 'Sport', required=True, query=Sport.query()),
                admin_fields.KeyField('country', 'Country', required=True, query=Country.query()),
                admin_fields.TextField("start_year", "Start year", required=True),
                admin_fields.CheckboxListField("teams", "Teams", initial=[], query=Team.query())
            ]


class TeamCompetitionState(Base):
    """
    """
    team = ndb.KeyProperty('ReprSquadState')
    competition = ndb.KeyProperty('Competition')


class Competition(Base):
    """Many-to-One Event.
    """
    event = ndb.KeyProperty(Event)


class Squad(Base):
    events = ndb.KeyProperty(kind=Event, repeated=True)
