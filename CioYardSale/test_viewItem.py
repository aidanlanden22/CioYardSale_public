from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from commodity.models import Commodity

class GetItemDetails(TestCase):
	def setUp(self):
		pass

	def success_response(self):

		response = self.client.get(reverse('readAll', kwargs={'pk': 1}))
		self.assertContains(response, 'read')

	def fails_invalid(self):

		response = self.client.get(reverse('readAll'))
		self.assertEquals(response.status_code, 404)

	def tearDown(self):
		pass
