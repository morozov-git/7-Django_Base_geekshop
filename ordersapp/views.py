from django.db import transaction
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.forms import inlineformset_factory

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem
from products.models import Product

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class OrderList(ListView):
	model = Order

	# fields = []
	# success_url = reverse_lazy('orders:list')
	def get_queryset(self):
		return Order.objects.filter(user=self.request.user, is_active=True)

	@method_decorator(login_required())
	def dispatch(self, *args, **kwargs):
		return super(ListView, self).dispatch(*args, **kwargs)

class OrderCreate(CreateView):
	model = Order
	fields = []
	success_url = reverse_lazy('orders:list')
	#####
	basket_items_1 = 0
	#####
	def get_context_data(self, **kwargs):
		context = super(OrderCreate, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop|Создать заказ'
		OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
		if self.request.POST:
			formset = OrderFormSet(self.request.POST)
		else:
			basket_items = Basket.objects.filter(user=self.request.user).select_related()
			if basket_items:
				OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_items.count())
				formset = OrderFormSet(instance=self.object)

				for num, form in enumerate(formset.forms):
					form.initial['product'] = basket_items[num].product
					form.initial['quantity'] = basket_items[num].quantity
					form.initial['price'] = basket_items[num].product.price
					form.initial['product_total_price'] = basket_items[num].product.price * basket_items[num].quantity

				# basket_items.delete()  # переделать (корзина должна удаляться только после сохранения заказа)
			else:
				formset = OrderFormSet()
		context['orderitems'] = formset
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		orderitems = context['orderitems']

		with transaction.atomic():
			#####
			# Для удаления корзины только во время сохранения заказа
			basket_items_del = Basket.objects.filter(user=self.request.user)
			basket_items_del.delete()
			#####
			form.instance.user = self.request.user
			self.object = form.save()
			if orderitems.is_valid():
				orderitems.instance = self.object
				orderitems.save()

			if self.object.get_total_cost() == 0:
				self.object.delete()

		return super().form_valid(form)


class OrderUpdate(UpdateView):
	model = Order
	fields = []

	# success_url = reverse_lazy('orders:list')
	def get_context_data(self, **kwargs):
		context = super(OrderUpdate, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop|Создать заказ'
		OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
		queryset = self.object.orderitems.select_related()
		if self.request.POST:
			# queryset = self.object.orderitems.select_related()
			formset = OrderFormSet(self.request.POST, instance=self.object, queryset=queryset)
		else:
			# queryset = self.object.orderitems.select_related()
			formset = OrderFormSet(instance=self.object, queryset=queryset)
			for form in formset:
				if form.instance.pk:
					form.initial['price'] = form.instance.product.price
					form.initial['product_total_price'] = form.instance.product.price * form.instance.quantity
		context['orderitems'] = formset
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		orderitems = context['orderitems']

		with transaction.atomic():
			self.object = form.save()
			if orderitems.is_valid():
				orderitems.instance = self.object
				orderitems.save()
			if self.object.get_total_cost() == 0:
				self.object.delete()

		return super().form_valid(form)

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')


class OrderDelete(DeleteView):
	model = Order
	success_url = reverse_lazy('orders:list')


class OrderRead(DetailView):
	model = Order

	def get_context_data(self, **kwargs):
		context = super(OrderRead, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop|OrderShow'
		return context


def order_forming_complete(request, pk):
	order = get_object_or_404(Order, pk=pk)
	order.status = order.SEND_TO_PROCEED
	order.save()
	return HttpResponseRedirect(reverse('orders:list'))


@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
	if instance.pk:
		instance.product.quantity -= instance.quantity - instance.get_item(int(instance.pk))
	else:
		instance.product.quantity -= instance.quantity
	instance.product.save()


@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
	instance.product.quantity += instance.quantity
	instance.product.save()



def get_product_price(request, pk):
	if request.is_ajax():
		product = Product.objects.filter(pk=pk).first()
		if product:
			return JsonResponse({'price': product.price})
		return JsonResponse({'price': 0})


# Пример подключения Intercassa
def payment_result(request):
	# ik_co_id = 51237daa8f2a2d8413000000
	# ik_inv_id = 339800573
	# ik_inv_st = success
	# ik_pm_no = 1
	status = request.GET.get('ik_inv_st')
	if status == 'success':  # добавить в обработку два еще два статуса (в ожидании и платеж откланен)(из документации Intercassa)
		order_pk = request.GET.get('ik_pm_no')
		order_item = Order.objects.get(pk=order_pk)
		order_item.status = Order.PAID
		order_item.save()
	return HttpResponseRedirect(reverse('orders:list'))

	pass

#
# @receiver(post_save, sender=OrderItem)
# def save_order(**kwargs):
# 	# if kwargs:
# 		return True
