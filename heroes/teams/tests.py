import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from heroes.helpers import BaseTestCase


class TeamTestCase(BaseTestCase):

    def test_team_view(self):
        data = self.testapp.get('/teams/').json
        self.assertEqual(data['count'], 0)

        # create team anonymous
        resp = self.testapp.post('/teams/',
                                 {'name': 'Tm1', 'country_name': 'Tm1 country',
                                  'division_name': 'Tm1 division'},
                                 expect_errors=True)
        self.assertEqual(resp.status_int, 405)

        self.login(is_admin=True)
        resp = self.testapp.post('/teams/', 
                                 {'name': 'Tm1', 'country_name': 'Tm1 country',
                                  'division_name': 'Tm1 division'})
        self.assertEqual(resp.status_int, 200)

        team_id = resp.json['result']['id']
        # get certain team
        data = self.testapp.get('/teams/{}/'.format(team_id)).json
        self.assertEqual(data['result']['name'], 'Tm1')

        data = self.testapp.put('/teams/{}/'.format(team_id), {'name': 'Team updated',
                                                               'division_name': 'Division',
                                                               'country_name': 'Country'}).json
        self.assertEqual(data['result']['name'], 'Team updated')

        # delete Team entry
        resp = self.testapp.delete('/teams/{}/'.format(team_id))
        self.assertEqual(resp.status_int, 200)
