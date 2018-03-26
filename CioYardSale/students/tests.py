from django.test import TestCase, Client
from django.urls import reverse
import json

# Create your tests here.
class Tests(TestCase):
    fixtures = ['database.json']

    #User wants to get a list of commodities
    def testGetAllCommodities(self):
        cli = Client()
        resp = cli.get('/api/v1/commodity/readAll/')
        commodities = resp.json()
        self.assertEqual(len(commodities), 2)