from django.test import TestCase
from django.test.client import Client


# Create your tests here.
from products.models import ProductsCategory, Product


class TeatMainSmokeTeas(TestCase):
	status_code_success = 200
	# Предустановленные параметры
	def set_up(self) -> None:
		category = ProductsCategory.objects.create(name='test')
		Product.objects.create(category=category, name='product_test', price=100)
		self.client = Client()

	# Тест
	def test_products_page(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, self.status_code_success) # self.assertEqual(response.status_code, 200)

	def test_products_product(self):
		for product_item in Product.objects.all():
			response = self.client.get(f'/products/detail/{product_item.pk}/')
			self.assertEqual(response.status_code, self.status_code_success)

	def test_products_basket(self):
		response = self.client.get('/users/profile/')
		self.assertEqual(response.status_code, 302)

	# Завершение теста (освобождение памяти от данных)
	def ternDown(self) -> None:
		pass