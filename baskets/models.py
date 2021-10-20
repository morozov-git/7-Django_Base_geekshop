from django.db import models

# Create your models here.
from users.models import User
from products.models import Product
from django.utils.functional import cached_property

# class BasketQuerySet(models.QuerySet):
#
# 	def delete(self, *args, **kwargs):
# 		for item in self:
# 			item.product.quantity += item.quantity
# 			item.product.save()
# 		super(BasketQuerySet, self).delete(*args, **kwargs)



class Basket(models.Model):
	# objects = BasketQuerySet.as_manager()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)

	created_timestamp = models.DateTimeField(auto_now_add=True)
	update_timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Корзина для {self.user.username} | Продукты {self.product.name}'


	def sum(self):
		return self.quantity * self.product.price

	@cached_property
	def total_sum_quantity(self):
		baskets = Basket.objects.filter(user=self.user).select_related()
		return { 'total_sum': sum(basket.sum() for basket in baskets),
				 'total_quantity' : sum(basket.quantity for basket in baskets)
				 }

	# def total_sum(self):
	# 	baskets = Basket.objects.filter(user=self.user)
	# 	return sum(basket.sum() for basket in baskets)
	#
	# def total_quantity(self):
	# 	baskets = Basket.objects.filter(user=self.user)
	# 	return sum(basket.quantity for basket in baskets)

	@staticmethod
	def get_item(pk):
		return Basket.objects.get(pk=pk).quantity

	@cached_property
	def get_item_cached(self):
		return self.user.basket.select_related()


	# def delete(self, *args, **kwargs):
	# 	self.product.quantity += self.quantity
	# 	self.product.save()
	# 	super(Basket, self).delete(*args, **kwargs)
	#
	# def save(self, *args, **kwargs):
	# 	if self.pk:
	# 		a = self.get_item(int(self.pk))
	# 		b = self.product.quantity
	# 		c = self.quantity
	# 		self.product.quantity -= self.quantity - self.get_item(int(self.pk))
	# 		d = self.product.quantity
	# 	else:
	# 		self.product.quantity -= self.quantity
	# 	self.product.save()
	# 	super(Basket, self).save(*args, **kwargs)
	# #	Если оставить включенным вместе с сигналами в orders/view, то будет вычитаться(в базе/на складе)
	# # по два товара при каждом добовлении одного товара в карзину.