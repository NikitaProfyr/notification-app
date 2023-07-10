
from django.test import TestCase
from django.urls import reverse

from notification.models import ClientModel


# Create your tests here.

class ClientCreateViewTestCase(TestCase):
    """Набор тестов для создания клиента через View"""

    def setUp(self):
        self.numberPhone = '88005553535'
        ClientModel.objects.filter(numberPhone=self.numberPhone).delete()

    def tearDown(self):
        ClientModel.objects.filter(numberPhone=self.numberPhone).delete()

    def testClientCreate(self):
        response = self.client.post(
            reverse('ClientCreate'),
            {
                'numberPhone': self.numberPhone,
                'codeOperator': '111',
                'tag': '111',
                'timeZone': 'test',
            }
        )
        self.assertRedirects(response, reverse('Clients'))
        self.assertTrue(
            ClientModel.objects.filter(numberPhone=self.numberPhone).exists()
        )


class ClientDetailViewTestCase(TestCase):
    """Набор тестов для отображения деталей о клиенте через View"""

    def setUp(self):
        self.Client = ClientModel.objects.create(
            numberPhone=88005553535, codeOperator=111, tag='111', timeZone='test'
        )

    def tearDown(self):
        self.Client.delete()

    def testClientDetail(self):
        response = self.client.get(
            reverse('ClientDetail', kwargs={'pk': self.Client.pk})
        )
        self.assertEqual(response.status_code, 200)

    def testClientDetailContains(self):
        response = self.client.get(
            reverse('ClientDetail', kwargs={'pk': self.Client.pk})
        )
        self.assertContains(response, self.Client.numberPhone)


class ClientListViewTestCase(TestCase):
    """Набор тестов для отображения клиентов через View"""
    def testClientListView(self):
        response = self.client.get(reverse('Clients'))
        for client in ClientModel.objects.all():
            self.assertContains(response, client.numberPhone)


