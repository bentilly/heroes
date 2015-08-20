import unittest

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import testbed

from heroes.helpers import BaseTestCase
from .models import Country


class EventTestCase(BaseTestCase):

    def test_event_view(self):
        self.login(is_admin=True)
        resp = self.testapp.post('/sports/', {'name': 'Sp1', 'description': 'Sp1 desc'})
        resp = self.testapp.post('/events/',
                                 {'sport_name': 'Sp1', 'title': 'Ev1', 'country': 'Country',
                                  'start_year': 'YEAR'})
        self.assertEqual(resp.status_int, 200)

        event_id = resp.json['result']['id']
