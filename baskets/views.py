from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponseRedirect
from products.models import Product
from baskets.models import Basket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db import connection
from django.db.models import F

@login_required
def baskets_add(request, id):
	product = Product.objects.get(id=id)
	baskets = Basket.objects.filter(user=request.user, product=product)
	if not baskets.exists():
		Basket.objects.create(user=request.user, product=product, quantity=1)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	else:
		baskets = baskets.first()
		# baskets.quantity += 1
		baskets.quantity = F('quantity') + 1
		baskets.save()
		# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		# baskets = Basket.objects.filter(user=request.user)
		update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
		print(f'basket_add {update_queries}')
		# context = {'baskets': baskets}
		# result_icon = render_to_string('baskets/baskets_icon.html', context)
		result_icon = render_to_string('baskets/baskets_icon.html', update_queries)
		return JsonResponse({
			'result_icon': result_icon
			})



@login_required
def basket_remove(request, id):
	Basket.objects.get(id=id).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def baskets_show(request):
	context = {
		'title': 'GeekShop - Корзина',
		# 'form': form,
		'baskets': Basket.objects.filter(user=request.user),
	}
	return render(request, 'baskets/only_baskets.html', context)


@login_required
def basket_edit(request, id, quantity):
	if request.is_ajax():
		basket = Basket.objects.get(id=id)
		if quantity > 0:
			basket.quantity = quantity
			basket.save()
		else:
			basket.delete()

		baskets = Basket.objects.filter(user=request.user)
		context = {'baskets': baskets}
		result_icon = render_to_string('baskets/baskets_icon.html', context)
		result = render_to_string('baskets/baskets.html', context)
		return JsonResponse({
			'result': result,
			'result_icon': result_icon
		})
