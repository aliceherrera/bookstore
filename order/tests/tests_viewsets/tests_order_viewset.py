import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token #addauthentication


from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order

class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = UserFactory() #adduser
        token = Token.objects.create(user=self.user) #addauthentication
        token.save() #addauthentication

        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        token = Token.objects.get(user__username=self.user.username) #addauthentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key) #addauthentication
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(order_data['results'][0]['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['results'][0]['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['results'][0]['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['results'][0]['product'][0]['category'][0]['title'], self.category.title)

    def test_create_order(self):
        token = Token.objects.get(user__username=self.user.username) #addauthentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key) #addauthentication
        category = CategoryFactory()
        product = ProductFactory()
        product.category.set([category])
        user = UserFactory()
        data = json.dumps({
            'products_id': [product.id],
            'user' : user.id
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        print(response.status_code)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
