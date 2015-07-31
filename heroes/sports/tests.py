import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from heroes.helpers import BaseTestCase


class SportTestCase(BaseTestCase):

    def test_sport_view(self):
        data = self.testapp.get('/sports/').json
        self.assertEqual(data['count'], 0)

        # create sport anonymous
        resp = self.testapp.post('/sports/',
                                 {'name': 'Sp1', 'description': 'Sp1 desc'},
                                 expect_errors=True)
        self.assertEqual(resp.status_int, 405)

        self.login(is_admin=True)
        resp = self.testapp.post('/sports/', {'name': 'Sp1', 'description': 'Sp1 desc'})
        self.assertEqual(resp.status_int, 200)

        sport_id = resp.json['result']['id']
        # get certain sport
        data = self.testapp.get('/sports/{}/'.format(sport_id)).json
        self.assertEqual(data['result']['name'], 'Sp1')

        data = self.testapp.put('/sports/{}/'.format(sport_id), {'name': 'Sport updated'}).json
        self.assertEqual(data['result']['name'], 'Sport updated')

        # delete Sport entry
        resp = self.testapp.delete('/sports/{}/'.format(sport_id))
        self.assertEqual(resp.status_int, 200)
