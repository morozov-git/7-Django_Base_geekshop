from django.shortcuts import render, get_object_or_404
from baskets.models import Basket

import json
from products.models import Product, ProductsCategory
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# with open("static/products.json", "r", encoding="utf-8") as goods:
# 	products_list = json.load(goods)
# products_list = Product.objects.all()
# categories_list = ProductsCategory.objects.all()
# baskets = Basket.objects.filter(user=request.user),


# Create your views here.

def basket_icon(request):
	if not request.user.is_active:
		return False
	else:
		return Basket.objects.filter(user=request.user)




def index(request):
	baskets = basket_icon(request)
	context = {
		"title": "geekshop",
		'baskets': baskets,
	}
	return render(request, "index.html", context)


def products(request, cat_id=0, page=1):
	categories_list = ProductsCategory.objects.all()
	baskets = basket_icon(request)

	if cat_id == 0:
		# print(cat_id)
		products_list = Product.objects.all()
	else:
		# print(cat_id)
		products_list = Product.objects.filter(category_id=cat_id)

	paginator = Paginator(products_list, per_page=1)
	try:
		products_paginator = paginator.page(page)
	except PageNotAnInteger:
		products_paginator = paginator.page(1)
	except EmptyPage:
		products_paginator = paginator.page(paginator.num_pages)


	context = {
		"title": "geekshop - Каталог",
		"products_list": products_paginator,
		# "products_list": products_list,
		'cat_id': cat_id,
		"categories_list": categories_list,
		'baskets': baskets,
	}

	return render(request, "products.html", context)

# Предварительная настройка - добавить эти параметры в функцию, чтобы избежать ошибок при
# обработке адресов с категориями
# def products(request, pk=None):
#     print(pk)
