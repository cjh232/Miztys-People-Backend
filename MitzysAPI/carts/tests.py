from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import *
from products.models import *

# Create your tests here.


class CartTests(APITestCase):

    def setUp(self):
        User.objects.create(email="cjh232@rutgers.edu", password="Delete21")
        prod1 = Product.objects.create(title="Sample")
        Item.objects.create(product=prod1, color="Red")


    def test_create_cart_item(self):
        """
        Ensure we can create a new cart item
        """

        user = User.objects.get(email="cjh232@rutgers.edu")
        item = Item.objects.get(color="Red")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        base_url = reverse('add-item-to-cart')
        final_url = f'{base_url}?item_id={item.id}&quantity=1'
        
        response = self.client.post(final_url)
        print(response.data)