from django.shortcuts import render

import json
from products.models import Product, ProductsCategory

# with open("static/products.json", "r", encoding="utf-8") as goods:
# 	products_list = json.load(goods)
# products_list = Product.objects.all()
categories_list = ProductsCategory.objects.all()


# Create your views here.
def index(request):
	context = {"title": "geekshop"}
	return render(request, "index.html", context)


def products(request, cat_id=0):
	if cat_id == 0:
		# print(cat_id)
		products_list = Product.objects.all()
	else:
		# print(cat_id)
		products_list = Product.objects.filter(category_id=cat_id)


	context = {
		"title": "geekshop - Каталог",
		"products_list": products_list,
		"categories_list": categories_list
	}

	return render(request, "products.html", context)

# Предварительная настройка - добавить эти параметры в функцию, чтобы избежать ошибок при
# обработке адресов с категориями
# def products(request, pk=None):
#     print(pk)