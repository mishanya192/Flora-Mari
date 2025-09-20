from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Тестовый товар",
            price=1000.00,
            description="Тестовое описание"
        )
        self.assertEqual(str(product), "Тестовый товар - Букеты")