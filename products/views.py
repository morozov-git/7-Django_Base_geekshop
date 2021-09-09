from django.shortcuts import render

import json
from products.models import Product, ProductsCategory


# with open("static/products.json", "r", encoding="utf-8") as goods:
# 	products_list = json.load(goods)
products_list = Product.objects.all()
categories_list = ProductsCategory.objects.all()

# Create your views here.
def index(request):
	context = {"title": "geek shop"}
	return render(request, "index.html", context)


def products(request):
	context = {
		"title": "geek shop catalog",
		"products_list": products_list,
		"categories_list": categories_list
	}
	return render(request, "products.html", context)













