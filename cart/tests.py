from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Product
from .models import CartItem

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name="Тест", price=100)
    
    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 1)