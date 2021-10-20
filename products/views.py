from django.shortcuts import render, get_object_or_404
from baskets.models import Basket

import json
from products.models import Product, ProductsCategory
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
import os
from django.conf import settings

MODULE_DIR = os.path.dirname(__file__)

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

def get_links_category():
	if settings.LOW_CACHE:
		key = 'links_category'
		links_category = cache.get(key)

		if links_category is None:
			links_category = ProductsCategory.objects.filter(is_active=True)
			cache.set(key, links_category)
		return links_category
	else:
		return ProductsCategory.objects.filter(is_active=True)

# def get_links_product(cat_id=0):
# 	if settings.LOW_CACHE:
# 		key = 'links_product' + str(cat_id)
# 		links_product = cache.get(key)
#
# 		if links_product is None and cat_id != 0:
# 			links_product = Product.objects.filter(is_active=True).filter(category_id=cat_id).select_related()
# 			# links_product = Product.objects.filter(is_active=True).select_related()
# 			cache.set(key, links_product)
# 		else:
# 			links_product = Product.objects.filter(is_active=True).select_related()
# 			# links_product = Product.objects.filter(is_active=True).select_related()
# 			cache.set(key, links_product)
# 		return links_product
# 	else:
# 		if cat_id != 0:
# 			# return Product.objects.filter(is_active=True).select_related()
# 			return Product.objects.filter(is_active=True).filter(category_id=cat_id).select_related()
# 		else:
# 			return Product.objects.filter(is_active=True).select_related()

def get_links_product():
	if settings.LOW_CACHE:
		key = 'links_product'
		links_product = cache.get(key)

		if links_product is None:
			links_product = Product.objects.filter(is_active=True).select_related()
			# links_product = Product.objects.filter(is_active=True).select_related()
			cache.set(key, links_product)
		return links_product
	else:
			# return Product.objects.filter(is_active=True).select_related()
			return Product.objects.filter(is_active=True).select_related()


def index(request):
	# baskets = basket_icon(request) # после подключения контекстного процессора можно отключить
	context = {
		"title": "geekshop",
		# 'baskets': baskets, # после подключения контекстного процессора можно отключить
	}
	return render(request, "index.html", context)


def products(request, cat_id=0, page=1):
	# categories_list = ProductsCategory.objects.all()
	# baskets = basket_icon(request) # после подключения контекстного процессора можно отключить
	if cat_id == 0:
		# print(cat_id)
		# products_list = Product.objects.all().select_related('category')
		# products_list = get_links_product()  # для кэширования списка продуктов вызываем дополнительный метод
		products_list = get_links_product() # для кэширования списка продуктов вызываем дополнительный метод
	else:
		# print(cat_id)
		# products_list = Product.objects.filter(category_id=cat_id)
		products_list = Product.objects.filter(category_id=cat_id).select_related('category')
		# products_list = get_links_product(cat_id)  # для кэширования списка продуктов вызываем дополнительный метод
		# print(products_list.query)

	paginator = Paginator(products_list, per_page=3) # количество товаров на странице
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
		# "categories_list": categories_list,
		"categories_list": get_links_category(),  # для кэширования категорий вызываем дополнительный метод
		# 'baskets': baskets, # после подключения контекстного процессора можно отключить
	}

	return render(request, "products.html", context)

# Предварительная настройка - добавить эти параметры в функцию, чтобы избежать ошибок при
# обработке адресов с категориями
# def products(request, pk=None):
#     print(pk)
