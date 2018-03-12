from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from api.cio.models import Cio
from api.students.models import Student
from api.commodity.models import Commodity

class HomePageTests(TestCase):

    fixtures = ["database.json"]

    # Front end tests 1
    def renderHomePageWhenNotLoggedIn(self):
        # Get a response from the root url
        response = self.client.get('/')

        # Check that it has a navbar
        self.assertContains(response, '<nav class="navbar navbar-expand-lg navbar-light bg-light">')

        # Check that it lists items for sale
        self.assertContains(response, '<h3>All items for sale</h3>')

    # Front end tests 2
    def renderHomePageWhenNotLoggedIn(self):
        # Get a response from the root url
        response = self.client.get('/')

        # Check that it has a button to sell an item
        self.assertContains(response, '<button class="btn btn-success px-5">Sell</button>')
