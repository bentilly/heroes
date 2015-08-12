import unittest

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import testbed

from heroes.helpers import BaseTestCase
from .models import Country


class TeamTestCase(BaseTestCase):

    def test_team_view(self):
        self.login(is_admin=True)
        resp = self.testapp.post('/sports/', {'name': 'Sp1', 'description': 'Sp1 desc'})
        country = Country(name='Country', code='1234')
        country = country.put()
        urlsafe = country.urlsafe()
        resp = self.testapp.post('/teams/', 
                                 {'name': 'Tm1', 'country_id': urlsafe,
                                  'sport_name': 'Sp1', 'division_name': 'Tm1 division'})
        self.assertEqual(resp.status_int, 200)

        team_id = resp.json['result']['id']

