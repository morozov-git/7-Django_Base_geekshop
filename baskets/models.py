from django.db import models

# Create your models here.
from users.models import User
from products.models import Product

# class BasketQuerySet(models.QuerySet):
#
# 	def delete(self, *args, **kwargs):
# 		for item in self:
# 			item.product.quantity += item.quantity
# 			item.product.save()
# 		super(BasketQuerySet, self).delete(*args, **kwargs)



class Basket(models.Model):
	# objects = BasketQuerySet.as_manager()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)

	created_timestamp = models.DateTimeField(auto_now_add=True)
	update_timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Корзина для {self.user.username} | Продукты {self.product.name}'

	def sum(self):
		return self.quantity * self.product.price

	def total_sum(self):
		baskets = Basket.objects.filter(user=self.user)
		return sum(basket.sum() for basket in baskets)

	def total_quantity(self):
		baskets = Basket.objects.filter(user=self.user)
		return sum(basket.quantity for basket in baskets)

	@staticmethod
	def get_item(pk):
		return Basket.objects.get(pk=pk).quantity

